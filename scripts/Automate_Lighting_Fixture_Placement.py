# =============================================================================
# Script Header: Revit Lighting Fixture Placement
# =============================================================================
# Purpose: Automates NEC 2023-compliant lighting fixture placement in Revit rooms,
#          supporting grid and boundary placement, DIALux CSV integration, and
#          ceiling-hosted fixtures for MEP firms.
# Version: 12.2
# Author: Alfonso Davila - Electrical Engineer, Revit MEP Dynamo BIM Expert
# Contact: davila.alfonso@gmail.com - www.linkedin.com/in/alfonso-davila-3a121087
# Repository: https://github.com/DynMEP
# License: MIT License (see LICENSE file in repository)
# Created: April 24, 2025
# Compatibility: Revit 2025, Dynamo 2.17+, IronPython 2.7 or CPython 3
# Dependencies: RevitAPI, RevitServices
# Notes:
#   - Ensure rooms have closed boundaries and ceilings for accurate placement.
#   - Outputs CSV with fixture coordinates and detailed log for NEC compliance.
#   - See repository for user guide and troubleshooting.
# =============================================================================

import clr
import System
from System import DateTime
from System.IO import Path, File
clr.AddReference('RevitAPI')
clr.AddReference('RevitServices')
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB.Architecture import Room
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager
import math
import csv
import os
import logging
import tempfile

# Initialize document and UI
doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application
active_view = doc.ActiveView

# NEC 2023 Configuration
FIXTURE_WATTAGE = 25  # Default 25W LED downlight
CIRCUIT_LIMIT = 1440  # 15A circuit at 120V, 80% capacity (NEC 210.19(A))
MIN_CLEARANCE = 0.5  # Non-IC-rated clearance (NEC 410.116)
IS_IC_RATED = True  # Assume IC-rated (NEC 410.62(C))
BOUNDARY_BUFFER = 1.0  # Buffer from room boundaries (ft)
WALL_PROXIMITY = 2.5  # Minimum wall distance (ft, v8)
WALL_THICKNESS = 0.5  # Typical wall thickness (ft, added to proximity)
NEC_MIN_WATTS_PER_SQFT = 2.5  # NEC 220.12(B), Retail
IESNA_MIN_WATTS_PER_SQFT = 0.5  # IESNA LED minimum
IESNA_MAX_WATTS_PER_SQFT = 1.0  # IESNA efficient maximum
SQFT_TO_SQM = 10.764  # W/m² conversion
WATTAGE_RANGE = (10.0, 100.0)  # Valid wattage range
SPACING_MIN = 10.0  # Grid spacing minimum (ft, v8)
SPACING_MAX = 12.0  # Grid spacing maximum (ft, v8)
ANTI_CLUSTERING_DISTANCE = 8.0  # Minimum fixture separation (ft, v8)

# Helper function: Generate timestamp
def get_timestamp():
    return DateTime.Now.ToString("yyyyMMdd_HHmmss")

# Helper function: Fallback logging (v8-style)
def log_message_fallback(message, log_file):
    timestamp = DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss")
    try:
        with open(log_file, 'a') as f:
            f.write("[{}] {}\n".format(timestamp, message))
            f.flush()
    except Exception as e:
        print(f"Fallback logging failed: {str(e)}")  # Print to Dynamo console

# Setup logging
timestamp = get_timestamp()
log_paths = [
    os.path.join(os.path.expanduser("~/Desktop"), f"LightingPlacementLog_{timestamp}.txt"),
    os.path.join(os.path.expanduser("~"), f"LightingPlacementLog_{timestamp}.txt"),
    os.path.join(tempfile.gettempdir(), f"LightingPlacementLog_{timestamp}.txt")
]

log_file = None
for path in log_paths:
    try:
        with open(path, 'a') as f:
            f.write("")
        log_file = path
        break
    except (PermissionError, IOError):
        continue

if log_file:
    try:
        logging.basicConfig(filename=log_file, level=logging.DEBUG, format='[%(asctime)s] %(message)s', force=True)
        logging.getLogger().handlers[0].flush()
        logging.debug(f"Logging initialized successfully to {log_file}")
    except Exception as e:
        log_message_fallback(f"Logging setup failed: {str(e)}. Using fallback logging.", log_file)
        logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] %(message)s')
else:
    log_message_fallback("All log paths failed. Logging to console.", log_paths[0])
    logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] %(message)s')

# Helper function: Validate wattage
def validate_wattage(wattage):
    try:
        wattage = float(wattage)
        if WATTAGE_RANGE[0] <= wattage <= WATTAGE_RANGE[1]:
            return wattage
        logging.warning(f"Invalid wattage {wattage}W, outside range {WATTAGE_RANGE}. Using default: {FIXTURE_WATTAGE}W")
        return FIXTURE_WATTAGE
    except (ValueError, TypeError):
        logging.warning(f"Invalid wattage format: {wattage}. Using default: {FIXTURE_WATTAGE}W")
        return FIXTURE_WATTAGE

# Helper function: Check clearance between points
def check_clearance(points, min_clearance):
    violations = []
    for i, pt1 in enumerate(points):
        for j, pt2 in enumerate(points[i+1:]):
            distance = pt1.DistanceTo(pt2)
            if distance < min_clearance:
                violations.append(f"Fixtures too close: ({pt1.X:.2f}, {pt1.Y:.2f}, {pt1.Z:.2f}) and ({pt2.X:.2f}, {pt2.Y:.2f}, {pt2.Z:.2f}), distance={distance:.2f} ft")
    return len(violations) == 0, violations

# Helper function: Get distance to nearest wall (using geometry)
def get_wall_distance(pt, room):
    try:
        collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Walls).WhereElementIsNotElementType()
        min_distance = float('inf')
        options = Options()
        options.ComputeReferences = True
        for wall in collector:
            geometry = wall.get_Geometry(options)
            if geometry:
                for geom in geometry:
                    if isinstance(geom, Solid):
                        for face in geom.Faces:
                            closest_point = face.Project(pt)
                            if closest_point:
                                distance = pt.DistanceTo(closest_point.XYZPoint)
                                min_distance = min(min_distance, distance)
        return min_distance if min_distance != float('inf') else None
    except Exception as e:
        logging.warning(f"Error checking wall distance: {str(e)}")
        return None

# Helper function: Check if point is too close to walls (using geometry and Z-check)
def is_point_near_wall(pt, room, min_distance):
    try:
        collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Walls).WhereElementIsNotElementType()
        options = Options()
        options.ComputeReferences = True
        for wall in collector:
            # Check Z-coordinate against wall height
            bbox = wall.get_BoundingBox(None)
            if bbox and pt.Z > bbox.Max.Z:
                continue  # Point is above wall
            geometry = wall.get_Geometry(options)
            if geometry:
                for geom in geometry:
                    if isinstance(geom, Solid):
                        for face in geom.Faces:
                            closest_point = face.Project(pt)
                            if closest_point:
                                distance = pt.DistanceTo(closest_point.XYZPoint)
                                if distance < min_distance:
                                    return True, f"Point ({pt.X:.2f}, {pt.Y:.2f}, {pt.Z:.2f}) too close to wall (distance={distance:.2f} ft)"
        return False, None
    except Exception as e:
        logging.warning(f"Error checking wall proximity: {str(e)}")
        return False, None

# Helper function: Validate room boundaries
def validate_room_boundaries(room):
    try:
        boundary_options = SpatialElementBoundaryOptions()
        boundary_segments = room.GetBoundarySegments(boundary_options)
        wall_boundaries = []
        for loop in boundary_segments:
            for segment in loop:
                element = segment.Element
                if element and isinstance(element, Wall):
                    wall_boundaries.append(f"Wall ID {element.Id.IntegerValue}")
        if wall_boundaries:
            logging.warning(f"Room boundaries include walls: {', '.join(wall_boundaries)}. Edit boundaries to exclude walls (Architecture > Room > Edit Boundary).")
            return False, wall_boundaries
        return True, None
    except Exception as e:
        logging.warning(f"Error validating room boundaries: {str(e)}")
        return True, None

# Helper function: Calculate grid and boundary points
def calculate_grid_points(room, spacing_min=SPACING_MIN, spacing_max=SPACING_MAX, z_level=None):
    logging.debug(f"Calculating grid points for room {room.get_Parameter(BuiltInParameter.ROOM_NAME).AsString()}")
    try:
        # Validate room boundaries
        is_valid, boundary_errors = validate_room_boundaries(room)
        if not is_valid:
            logging.warning(f"Invalid room boundaries: {boundary_errors}")
        
        # Get room boundary segments
        boundary_options = SpatialElementBoundaryOptions()
        boundary_segments = room.GetBoundarySegments(boundary_options)
        if not boundary_segments:
            logging.warning("No valid boundary segments found for room")
            return None, "No valid boundary segments"
        segment_counts = [len(loop) for loop in boundary_segments]
        segment_lengths = [[seg.GetCurve().Length for seg in loop if seg.GetCurve()] for loop in boundary_segments]
        logging.info(f"Found {len(boundary_segments)} boundary segment loops for room (segments per loop: {segment_counts}, lengths: {segment_lengths})")
        
        # Get room bounding box
        bbox = room.get_BoundingBox(active_view)
        if not bbox:
            logging.warning("No valid bounding box for room")
            return None, "No valid bounding box for room"
        min_pt, max_pt = bbox.Min, bbox.Max
        z_range = (min_pt.Z, max_pt.Z)
        logging.info(f"Room Z-range: Min Z={min_pt.Z:.2f}, Max Z={max_pt.Z:.2f}")
        
        # Get room Upper Limit
        upper_limit_param = room.get_Parameter(BuiltInParameter.ROOM_UPPER_OFFSET)
        level_elevation = room.Level.Elevation if room.Level else 0
        upper_limit = (level_elevation + upper_limit_param.AsDouble()) if upper_limit_param else (level_elevation + 8)
        if upper_limit <= level_elevation:
            logging.warning(f"Invalid UpperLimit ({upper_limit:.2f} ft) for room, falling back to default 8 ft")
            upper_limit = level_elevation + 8
        
        # Validate Z-coordinate
        z_coord = z_level if z_level and z_level <= upper_limit else upper_limit
        if z_coord < z_range[0] or z_coord > z_range[1]:
            logging.warning(f"Z-coordinate ({z_coord:.2f} ft) outside room Z-range ({z_range[0]:.2f} to {z_range[1]:.2f} ft), using BBox ZMax ({max_pt.Z:.2f} ft)")
            z_coord = max_pt.Z
        
        logging.info(f"Using Z-coordinate for room: Z={z_coord:.2f} (UpperLimit={upper_limit:.2f}, BBox ZMax={max_pt.Z:.2f})")
        
        # Calculate grid spacing
        area = room.Area
        target_fixtures = min(
            int(area * IESNA_MIN_WATTS_PER_SQFT / FIXTURE_WATTAGE),
            int(CIRCUIT_LIMIT / FIXTURE_WATTAGE)
        )
        grid_size = min(spacing_max, max(spacing_min, math.sqrt(area / target_fixtures)))
        current_watts_per_sqft = (target_fixtures * FIXTURE_WATTAGE) / area if area > 0 else 0
        current_watts_per_sqm = current_watts_per_sqft / SQFT_TO_SQM
        logging.info(f"Room area: {area:.2f} sq ft, Estimated fixtures: {target_fixtures}, W/sq ft: {current_watts_per_sqft:.2f}, W/m²: {current_watts_per_sqm:.3f} (NEC Min: {NEC_MIN_WATTS_PER_SQFT}, IESNA: {IESNA_MIN_WATTS_PER_SQFT}–{IESNA_MAX_WATTS_PER_SQFT})")
        
        points = []
        failed_points = 0
        point_distances = []
        
        # Step 1: Generate grid points
        x_start = min_pt.X + grid_size / 2 + BOUNDARY_BUFFER
        y_start = min_pt.Y + grid_size / 2 + BOUNDARY_BUFFER
        x_end = max_pt.X - BOUNDARY_BUFFER
        y_end = max_pt.Y - BOUNDARY_BUFFER
        
        x = x_start
        while x < x_end:
            y = y_start
            while y < y_end:
                pt = XYZ(x, y, z_coord)
                if room.IsPointInRoom(pt):
                    is_near_wall, wall_error = is_point_near_wall(pt, room, WALL_PROXIMITY + WALL_THICKNESS)
                    wall_distance = get_wall_distance(pt, room)
                    point_distances.append(f"Grid point ({x:.2f}, {y:.2f}, {z_coord:.2f}): Wall distance={wall_distance:.2f} ft" if wall_distance else f"Grid point ({x:.2f}, {y:.2f}, {z_coord:.2f}): Wall distance=Unknown")
                    if not is_near_wall:
                        too_close = any(pt.DistanceTo(existing_pt) < ANTI_CLUSTERING_DISTANCE for existing_pt in points)
                        if not too_close:
                            points.append(pt)
                        else:
                            failed_points += 1
                            logging.info(f"Grid point rejected at ({x:.2f}, {y:.2f}, {z_coord:.2f}): Too close to existing point")
                    else:
                        failed_points += 1
                        logging.info(f"Grid point rejected at ({x:.2f}, {y:.2f}, {z_coord:.2f}): {wall_error}")
                else:
                    failed_points += 1
                    logging.info(f"Grid point rejected at ({x:.2f}, {y:.2f}, {z_coord:.2f}): Not in room")
                y += grid_size
            x += grid_size
        
        # Step 2: Generate boundary points
        boundary_points = []
        for segment_loop in boundary_segments:
            for segment in segment_loop:
                try:
                    curve = segment.GetCurve()
                    if not curve or curve.Length < spacing_min:
                        continue
                    length = curve.Length
                    num_points = int(math.floor(length / (grid_size * 1.5)))
                    for i in range(num_points + 1):
                        t = i * (grid_size * 1.5) / length
                        pt = curve.Evaluate(t, False)
                        direction = curve.ComputeDerivatives(t, False).BasisX.Normalize()
                        normal = XYZ(-direction.Y, direction.X, 0)
                        offset_pt = XYZ(pt.X + normal.X * (WALL_PROXIMITY + WALL_THICKNESS), 
                                      pt.Y + normal.Y * (WALL_PROXIMITY + WALL_THICKNESS), z_coord)
                        if room.IsPointInRoom(offset_pt):
                            is_near_wall, wall_error = is_point_near_wall(offset_pt, room, WALL_PROXIMITY + WALL_THICKNESS)
                            wall_distance = get_wall_distance(offset_pt, room)
                            point_distances.append(f"Boundary point ({offset_pt.X:.2f}, {offset_pt.Y:.2f}, {offset_pt.Z:.2f}): Wall distance={wall_distance:.2f} ft" if wall_distance else f"Boundary point ({offset_pt.X:.2f}, {offset_pt.Y:.2f}, {offset_pt.Z:.2f}): Wall distance=Unknown")
                            if not is_near_wall:
                                too_close = any(offset_pt.DistanceTo(existing_pt) < ANTI_CLUSTERING_DISTANCE for existing_pt in points + boundary_points)
                                if not too_close:
                                    boundary_points.append(offset_pt)
                                else:
                                    failed_points += 1
                                    logging.info(f"Boundary point rejected at ({offset_pt.X:.2f}, {offset_pt.Y:.2f}, {offset_pt.Z:.2f}): Too close to existing point")
                            else:
                                failed_points += 1
                                logging.info(f"Boundary point rejected at ({offset_pt.X:.2f}, {offset_pt.Y:.2f}, {offset_pt.Z:.2f}): {wall_error}")
                        else:
                            failed_points += 1
                            logging.info(f"Boundary point rejected at ({offset_pt.X:.2f}, {offset_pt.Y:.2f}, {offset_pt.Z:.2f}): Not in room")
                except Exception as e:
                    logging.warning(f"Error processing boundary segment: {str(e)}")
        
        points.extend(boundary_points)
        
        # Log all point distances
        for dist_log in point_distances:
            logging.debug(dist_log)
        
        # Check spacing violations
        is_spaced, spacing_errors = check_clearance(points, 6.0)
        if not is_spaced:
            for error in spacing_errors:
                logging.warning(f"Spacing violation: {error}")
        
        # Check non-IC-rated clearance
        if not IS_IC_RATED:
            is_clear, clearance_errors = check_clearance(points, MIN_CLEARANCE)
            if not is_clear:
                logging.warning(f"Non-IC clearance violation: {'; '.join(clearance_errors)}")
                return None, "; ".join(clearance_errors)
        
        if not points:
            logging.warning(f"No valid points found after boundary and grid calculation ({failed_points} points rejected)")
            return None, f"No valid points found ({failed_points} points rejected)"
        
        logging.info(f"Generated {len(points) - len(boundary_points)} grid points and {len(boundary_points)} boundary points for room (Rejected: {failed_points})")
        logging.getLogger().handlers[0].flush()
        return points, None
    except Exception as e:
        logging.error(f"Grid calculation error: {str(e)}")
        return None, str(e)

# Helper function: Read DIALux CSV
def read_dialux_csv(csv_path):
    logging.debug(f"Reading DIALux CSV: {csv_path}")
    try:
        points = []
        fixture_types = []
        with open(csv_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                x = float(row['x']) / 304.8  # mm to feet
                y = float(row['y']) / 304.8
                z = float(row['z']) / 304.8
                points.append(XYZ(x, y, z))
                fixture_types.append(row['fixture_type'])
        is_spaced, spacing_errors = check_clearance(points, 6.0)
        if not is_spaced:
            logging.warning(f"DIALux spacing violation: {'; '.join(spacing_errors)}")
            return None, None, "; ".join(spacing_errors)
        if not IS_IC_RATED:
            is_clear, clearance_errors = check_clearance(points, MIN_CLEARANCE)
            if not is_clear:
                logging.warning(f"DIALux non-IC clearance violation: {'; '.join(clearance_errors)}")
                return None, None, "; ".join(clearance_errors)
        logging.info(f"Read {len(points)} points from DIALux CSV")
        return points, fixture_types, None
    except Exception as e:
        logging.error(f"DIALux CSV error: {str(e)}")
        return None, None, str(e)

# Main function: Place lighting fixtures
def place_lighting_fixtures(rooms, fixture_symbol, dialux_csv=None):
    logging.debug("Starting place_lighting_fixtures")
    output_csv = os.path.join(os.path.expanduser("~/Desktop"), f"LightingPlacement_{timestamp}.csv")
    guide_file = os.path.join(os.path.expanduser("~/Desktop"), f"LightingPlacement_Guide_{timestamp}.txt")
    
    logging.info(f"Running LightingPlacement.py Version: 20250423_v12.2")
    
    # Initialize outputs
    fixture_ids = []
    csv_rows = []
    total_wattage = 0
    
    # Log active view
    try:
        logging.info(f"Active view: Name={active_view.Name}, Type={active_view.ViewType}")
    except Exception as e:
        logging.warning(f"Failed to retrieve active view details: {str(e)}")
    
    # Validate fixture symbol
    if not isinstance(fixture_symbol, FamilySymbol):
        logging.error(f"Input fixture_symbol is not a valid FamilySymbol. Got type: {type(fixture_symbol)}")
        return None, None, None, "Invalid fixture symbol type"
    
    # Activate FamilySymbol
    try:
        if not fixture_symbol.IsActive:
            TransactionManager.Instance.EnsureInTransaction(doc)
            fixture_symbol.Activate()
            doc.Regenerate()
            TransactionManager.Instance.TransactionTaskDone()
            logging.info(f"Activated FamilySymbol: ElementId={fixture_symbol.Id.IntegerValue}")
    except Exception as e:
        logging.error(f"Error activating FamilySymbol: {str(e)}")
        return None, None, None, "Failed to activate FamilySymbol"
    
    # Validate wattage
    wattage_param = fixture_symbol.LookupParameter("Wattage")
    wattage = validate_wattage(wattage_param.AsDouble() if wattage_param else FIXTURE_WATTAGE)
    logging.info(f"Fixture symbol: ElementId={fixture_symbol.Id.IntegerValue}, Wattage={wattage:.1f}W, IC-Rated={IS_IC_RATED}")
    
    # Validate rooms
    if not rooms:
        logging.error("No rooms provided")
        return None, None, None, "No rooms provided"
    
    if not isinstance(rooms, list):
        rooms = [rooms]
    
    # Start transaction
    try:
        TransactionManager.Instance.EnsureInTransaction(doc)
    except Exception as e:
        logging.error(f"Failed to start transaction: {str(e)}")
        return None, None, None, str(e)
    
    try:
        for room in rooms:
            if not isinstance(room, Room):
                logging.warning(f"Skipping invalid room element: {room}")
                continue
            
            room_name = room.get_Parameter(BuiltInParameter.ROOM_NAME).AsString()
            points = []
            fixture_types = []
            room_wattage = 0
            area = room.Area
            logging.debug(f"Processing room: {room_name}, Area={area:.2f} sq ft")
            
            # Log room details
            try:
                level_name = room.Level.Name if room.Level else "Unknown"
                level_elevation = room.Level.Elevation if room.Level else 0
                room_bbox = room.get_BoundingBox(active_view)
                bbox_info = f"Min=({room_bbox.Min.X:.2f}, {room_bbox.Min.Y:.2f}, {room_bbox.Min.Z:.2f}), Max=({room_bbox.Max.X:.2f}, {room_bbox.Max.Y:.2f}, {room_bbox.Max.Z:.2f})" if room_bbox else "No valid bounding box"
                upper_limit_param = room.get_Parameter(BuiltInParameter.ROOM_UPPER_OFFSET)
                upper_limit = (level_elevation + upper_limit_param.AsDouble()) if upper_limit_param else (level_elevation + 8)
                logging.info(f"Room {room_name}: Level={level_name}, Elevation={level_elevation:.2f}, UpperLimit={upper_limit:.2f}, BoundingBox={bbox_info}")
            except Exception as e:
                logging.warning(f"Failed to retrieve room details for {room_name}: {str(e)}")
            
            # Find ceiling
            collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Ceilings).WhereElementIsNotElementType()
            ceiling = None
            ceiling_height = None
            room_level_name = room.Level.Name if room.Level else None
            fallback_ceiling = None
            min_z_diff = float('inf')
            
            for c in collector:
                try:
                    ceiling_id = c.Id.IntegerValue
                    level_param = c.get_Parameter(BuiltInParameter.LEVEL_PARAM)
                    level = c.Level if hasattr(c, 'Level') else None
                    level_elevation = level.Elevation if level else 0
                    height_param = c.get_Parameter(BuiltInParameter.CEILING_HEIGHTABOVELEVEL_PARAM)
                    height_offset = height_param.AsDouble() if height_param else 0
                    ceiling_z = level_elevation + height_offset
                    phase = c.get_Parameter(BuiltInParameter.PHASE_CREATED).AsValueString() if c.get_Parameter(BuiltInParameter.PHASE_CREATED) else "Unknown"
                    workset = doc.GetWorksetTable().GetWorkset(c.WorksetId).Name if c.WorksetId else "Unknown"
                    level_param_name = level_param.AsValueString() if level_param else "None"
                    
                    logging.info(f"Candidate ceiling for room {room_name}: ElementId={ceiling_id}, Z={ceiling_z:.2f}, LevelParam={level_param_name}, Phase={phase}, Workset={workset}")
                    
                    if room_level_name and level_param_name == room_level_name:
                        ceiling = c
                        ceiling_height = ceiling_z
                        logging.info(f"Selected ceiling by LevelParam match: ElementId={ceiling_id}, Z={ceiling_z:.2f}")
                        break
                    z_diff = abs(ceiling_z - (room.Level.Elevation + 8))
                    if z_diff < min_z_diff:
                        min_z_diff = z_diff
                        fallback_ceiling = (c, ceiling_z)
                except Exception as e:
                    logging.warning(f"Skipping invalid ceiling for room {room_name}: ElementId={ceiling_id}, Error={str(e)}")
            
            if not ceiling and fallback_ceiling:
                ceiling, ceiling_height = fallback_ceiling
                logging.info(f"Selected fallback ceiling by Z-height: ElementId={ceiling.Id.IntegerValue}, Z={ceiling_height:.2f}")
            
            if not ceiling:
                logging.warning(f"No valid ceiling found for room {room_name}. Falling back to default Z=UpperLimit ({upper_limit:.2f} ft)")
                ceiling_height = upper_limit
            
            z_coord = ceiling_height if ceiling_height and ceiling_height <= upper_limit else upper_limit
            logging.info(f"Final Z-coordinate for room: Z={z_coord:.2f} (Ceiling Z={ceiling_height if ceiling_height else -1:.2f}, UpperLimit={upper_limit:.2f})")
            
            # Placement logic
            if dialux_csv:
                points, fixture_types, error = read_dialux_csv(dialux_csv)
                if error:
                    logging.warning(f"DIALux CSV error for room {room_name}: {error}")
                    continue
            else:
                points, error = calculate_grid_points(room, z_level=z_coord)
                if error:
                    logging.warning(f"Grid calculation error for room {room_name}: {error}")
                    continue
                fixture_types = ["25W Square"] * len(points)
            
            # Place fixtures
            for pt, f_type in zip(points, fixture_types):
                try:
                    wall_distance = get_wall_distance(pt, room)
                    wall_distance_log = f"{wall_distance:.2f} ft" if wall_distance is not None else "Unknown"
                    if wall_distance is not None and wall_distance < WALL_PROXIMITY:
                        logging.warning(f"Fixture at ({pt.X:.2f}, {pt.Y:.2f}, {pt.Z:.2f}) too close to wall (distance: {wall_distance_log})")
                    if ceiling:
                        fixture = doc.Create.NewFamilyInstance(pt, fixture_symbol, ceiling, room.Level, Structure.StructuralType.NonStructural)
                    else:
                        fixture = doc.Create.NewFamilyInstance(pt, fixture_symbol, room.Level, Structure.StructuralType.NonStructural)
                    logging.info(f"Placed {'ceiling-hosted' if ceiling else 'non-hosted'} fixture ID {fixture.Id.IntegerValue} at ({pt.X:.2f}, {pt.Y:.2f}, {pt.Z:.2f}) in room {room_name} (wall distance: {wall_distance_log})")
                    fixture_ids.append(fixture.Id.IntegerValue)
                    room_wattage += wattage
                    total_wattage += wattage
                    
                    csv_rows.append({
                        'Fixture_ID': fixture.Id.IntegerValue,
                        'X': pt.X * 304.8,
                        'Y': pt.Y * 304.8,
                        'Z': pt.Z * 304.8,
                        'Room_Name': room_name,
                        'Fixture_Type': f_type
                    })
                except Exception as e:
                    logging.warning(f"Fixture placement error at ({pt.X:.2f}, {pt.Y:.2f}, {pt.Z:.2f}): {str(e)}")
            
            # Log room results
            watts_per_sqft = room_wattage / area if area > 0 else 0
            watts_per_sqm = watts_per_sqft / SQFT_TO_SQM
            logging.info(f"Room {room_name}: Total fixtures={len(points)}, Load={room_wattage:.1f}W, W/sq ft={watts_per_sqft:.2f}, W/m²={watts_per_sqm:.3f} (NEC Min: {NEC_MIN_WATTS_PER_SQFT}, IESNA: {IESNA_MIN_WATTS_PER_SQFT}–{IESNA_MAX_WATTS_PER_SQFT})")
            if watts_per_sqft < IESNA_MIN_WATTS_PER_SQFT:
                logging.warning(f"Room {room_name} W/sq ft ({watts_per_sqft:.2f}) below IESNA minimum ({IESNA_MIN_WATTS_PER_SQFT}). Consider higher-wattage fixtures or DIALux design.")
            elif watts_per_sqft > IESNA_MAX_WATTS_PER_SQFT:
                logging.warning(f"Room {room_name} W/sq ft ({watts_per_sqft:.2f}) above IESNA maximum ({IESNA_MAX_WATTS_PER_SQFT}). Reduce fixture count.")
            if room_wattage > CIRCUIT_LIMIT:
                logging.warning(f"Room {room_name} load ({room_wattage:.1f}W) exceeds circuit limit ({CIRCUIT_LIMIT}W)")
            logging.getLogger().handlers[0].flush()
        
        logging.info(f"Total load across all rooms: {total_wattage:.1f}W")
        if total_wattage > CIRCUIT_LIMIT:
            logging.warning(f"Total load ({total_wattage:.1f}W) exceeds circuit limit ({CIRCUIT_LIMIT}W)")
        
        # Write output CSV
        try:
            with open(output_csv, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=['Fixture_ID', 'X', 'Y', 'Z', 'Room_Name', 'Fixture_Type'])
                writer.writeheader()
                writer.writerows(csv_rows)
            logging.info(f"Wrote output CSV: {output_csv}")
        except Exception as e:
            logging.warning(f"Failed to write CSV {output_csv}: {str(e)}")
        
        # Write user guide
        guide_content = """Lighting Placement Script User Guide
-----------------------------------
Complies with NEC 2023 (NFPA 70) for commercial lighting, including irregular rooms.
Version: 20250423_v12.2

Setup:
1. Ensure Revit 2025 and Dynamo are installed.
2. Load the script in a Dynamo Python node.
3. Load a UL-listed lighting fixture family (e.g., Downlight - Rectangle - LED, 25W Square, IC-rated).
4. Ensure ceilings exist in rooms for ceiling-hosted fixtures (NEC 410.36(A)):
   - Go to Architecture > Ceiling.
   - Select a ceiling type (e.g., Generic Ceiling).
   - Draw the ceiling to match the room's footprint, including irregular shapes.
   - Set Level to match room's Level (e.g., Electrical, L1 - Block 43).
   - Set Height Offset From Level (e.g., 8 ft for Electrical, 5.67 ft for L1 - Block 43).
5. Set room Upper Limit to ceiling height:
   - Select room, set Upper Limit (e.g., Electrical: -3.46 + 8 = 4.54 ft; L1 - Block 43: 0 + 5.67 = 5.67 ft).
   - Fix negative UpperLimit values (e.g., -5.46 ft, -0.50 ft).
6. Ensure room boundaries are closed and exclude walls:
   - Go to Architecture > Room > Edit Boundary.
   - Ensure walls are outside the room footprint. Check in a section view to confirm boundaries align with room interior.
7. (Optional) Prepare a DIALux CSV with columns: x, y, z, fixture_type (coords in mm).

Inputs:
- IN[0]: Single room or list of rooms (Revit Room elements).
- IN[1]: Revit FamilySymbol (Family Types node, select '25W Square').
- IN[2]: (Optional) Path to DIALux CSV file (String node).

Usage:
1. Connect inputs to the Python node in Dynamo.
2. Verify fixture family is loaded and Family Types selects '25W Square'.
3. Check rooms have ceilings and closed boundaries in a 3D or ceiling plan view.
4. Set active view to a 3D view or ceiling plan showing rooms, ceilings, walls.
5. Run the script.
6. Check Desktop outputs:
   - LightingPlacement_[timestamp].csv: Fixture placement data (coords in mm).
   - LightingPlacementLog_[timestamp].txt: Debug log with NEC compliance.
   - LightingPlacement_Guide_[timestamp].txt: This guide.

NEC 2023 Compliance:
- Spacing: 10–12 ft grid, boundary points for irregular rooms (NEC 410.116, IESNA).
- Clearance: 2.5 ft from walls, accounting for wall thickness (NEC 410.116, IESNA).
- Load: Tracks wattage, warns if >1440W (NEC 210.19(A)).
- W/sq ft: Tracks vs. NEC 220.12(B) (2.5 W/sq ft min), IESNA (0.5–1.0 W/sq ft).
- Installation: Ceiling-hosted fixtures (NEC 410.36(A)).
- Fixture: Assumes UL-listed, IC-rated (NEC 410.62(C), 410.44). Verify specs.

Troubleshooting:
- If log file is empty:
  - Check {log_file} or temporary directory for logs.
  - Ensure write permissions on Desktop or home directory.
  - Verify script runs to completion in Dynamo (check CSV/guide outputs).
  - Enable console logging in Dynamo for real-time debug.
- If fixtures are too close to walls or over walls:
  - Check log for 'too close to wall' warnings (distance <2.5 ft) or boundary validation warnings.
  - Verify walls are outside room footprint (Architecture > Room > Edit Boundary).
  - In a section view, ensure room boundaries align with interior faces, not wall centerlines.
  - If boundaries include walls, edit them to exclude walls (log will warn about wall IDs).
- If too many fixtures:
  - Check log for 'Spacing violation' or 'Too close to existing point'.
  - Adjust SPACING_MIN to 12 ft or ANTI_CLUSTERING_DISTANCE to 10 ft.
- If W/sq ft is too low:
  - Check log for 'below IESNA minimum' warning.
  - Use higher-wattage fixtures (e.g., 32W) or DIALux CSV.
- If fixtures are below ceiling:
  - Set UpperLimit to ceiling height (e.g., 4.54 ft for Electrical, 5.67 ft for L1 - Block 43).
  - Check log for 'Z-coordinate' and 'UpperLimit'.
- If 'No valid points found':
  - Check log for 'Grid point rejected' or 'Boundary point rejected'.
  - Ensure boundaries are closed (Architecture > Room > Edit Boundary).
- If irregular areas are missed:
  - Check log for boundary segment loops and lengths.
  - Use DIALux CSV for complex rooms.
- If 'No valid ceiling found':
  - Recreate ceilings with correct Level and Height Offset.
- If 'Load exceeds circuit limit', split fixtures across circuits.
- Ensure active view is 3D or ceiling plan.
"""
        try:
            with open(guide_file, 'w') as f:
                f.write(guide_content)
            logging.info(f"Wrote user guide: {guide_file}")
        except Exception as e:
            logging.warning(f"Failed to write guide {guide_file}: {str(e)}")
        
        TransactionManager.Instance.TransactionTaskDone()
        logging.info("Fixture placement completed")
        logging.getLogger().handlers[0].flush()
        return fixture_ids, output_csv, guide_file, None
    
    except Exception as e:
        TransactionManager.Instance.ForceCloseTransaction()
        logging.error(f"Critical error: {str(e)}")
        logging.getLogger().handlers[0].flush()
        return None, None, None, str(e)

# Validate inputs
logging.debug("Validating inputs")
try:
    if len(IN) < 2:
        error_msg = "Error: Insufficient inputs. Provide rooms (IN[0]) and fixture symbol (IN[1]). Optional DIALux CSV (IN[2])."
        logging.error(error_msg)
        logging.getLogger().handlers[0].flush()
        OUT = [error_msg]
    else:
        rooms = UnwrapElement(IN[0])
        fixture_symbol = UnwrapElement(IN[1])
        dialux_csv = IN[2] if len(IN) > 2 else None

        logging.info(f"Input rooms: {rooms}")
        logging.info(f"Input fixture_symbol (before unwrap): {IN[1]}")
        logging.info(f"Input fixture_symbol (after unwrap): {fixture_symbol}")
        logging.info(f"Input dialux_csv: {dialux_csv}")
        logging.getLogger().handlers[0].flush()

        fixture_ids, csv_path, guide_path, error = place_lighting_fixtures(rooms, fixture_symbol, dialux_csv)
        if error:
            logging.error(f"Placement error: {error}")
            OUT = [f"Error: {error}"]
        else:
            logging.info(f"Output: Fixture IDs={fixture_ids}, CSV={csv_path}, Guide={guide_path}")
            OUT = [fixture_ids, csv_path, guide_path]
        logging.getLogger().handlers[0].flush()
except Exception as e:
    error_msg = f"Syntax or runtime error: {str(e)}"
    logging.error(error_msg)
    logging.getLogger().handlers[0].flush()
    OUT = [error_msg]