# =============================================================================
# Script Header: Revit NEC-Compliant Receptacle Placement
# =============================================================================
# Purpose: Automates NEC-compliant receptacle placement on both faces of grouped
#          wall segments in Autodesk Revit, optimizing MEP electrical design
#          workflows.
# Version: 13.0
# Author: Alfonso Davila - Electrical Engineer, Revit MEP Dynamo BIM Expert
# Contact: davila.alfonso@gmail.com - www.linkedin.com/in/alfonso-davila-3a121087
# Repository: https://github.com/DynMEP
# License: MIT License (see LICENSE file in repository)
# Created: April 24, 2025
# Compatibility: Revit 2025, Dynamo 2.17+, IronPython 2.7 or CPython 3
# Dependencies: RevitAPI, RevitServices
# Notes:
#   - Ensure walls and receptacle family are loaded in the Revit model.
#   - Outputs log file and task dialog for placement results.
#   - See repository for setup instructions and additional tools.
# =============================================================================

import clr
import math
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import TaskDialog
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager
from System.Collections.Generic import List
from datetime import datetime
import os

clr.AddReference('RevitAPI')
clr.AddReference('RevitServices')

doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication

# Inputs
input_walls = IN[0]
walls = input_walls if isinstance(input_walls, list) else [input_walls]
walls = [UnwrapElement(w) for w in walls]

receptacle_family = UnwrapElement(IN[1])

#start_offset = 6.0
#spacing = 12.0
start_offset = IN[2] if IN[2] else 6.0  # in feet
spacing = IN[3] if IN[3] else 12.0  # in feet
end_clearance = 0.167

results = []
errors = []

timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
desktop = os.path.expanduser("~/Desktop")
log_path = os.path.join(desktop, "NECReceptaclesDualSideLog_{}.txt".format(timestamp))
log_file = open(log_path, "w")

def log(msg):
    log_file.write("[{}] {}".format(datetime.now().strftime('%H:%M:%S'), msg))

def get_curve_pts_dir(wall):
    loc = wall.Location
    if isinstance(loc, LocationCurve):
        curve = loc.Curve
        p1 = curve.GetEndPoint(0)
        p2 = curve.GetEndPoint(1)
        direction = p2.Subtract(p1).Normalize()
        return curve, p1, p2, direction
    return None, None, None, None

def are_walls_connected(w1, w2, tol=0.5, angle_tol=10):
    _, p1a, p1b, d1 = get_curve_pts_dir(w1)
    _, p2a, p2b, d2 = get_curve_pts_dir(w2)
    if not all([p1a, p1b, p2a, p2b, d1, d2]): return False
    if p1a.DistanceTo(p2a) < tol or p1a.DistanceTo(p2b) < tol or        p1b.DistanceTo(p2a) < tol or p1b.DistanceTo(p2b) < tol:
        angle = math.degrees(d1.AngleTo(d2))
        return angle < angle_tol
    return False

def group_walls(walls):
    groups = []
    visited = set()
    for i, wall in enumerate(walls):
        if wall.Id.IntegerValue in visited:
            continue
        group = [wall]
        visited.add(wall.Id.IntegerValue)
        to_check = [wall]
        while to_check:
            current = to_check.pop()
            for other in walls:
                if other.Id.IntegerValue not in visited and are_walls_connected(current, other):
                    group.append(other)
                    to_check.append(other)
                    visited.add(other.Id.IntegerValue)
        groups.append(group)
    return groups

def get_wall_face_for_orientation(wall, orientation_vector):
    options = Options()
    options.IncludeNonVisibleObjects = False
    options.DetailLevel = ViewDetailLevel.Fine
    options.ComputeReferences = True

    best_face = None
    best_edge = None
    longest = 0.0

    for geom in wall.get_Geometry(options):
        solid = geom if isinstance(geom, Solid) else None
        if not solid: continue
        for face in solid.Faces:
            normal = face.ComputeNormal(UV(0.5, 0.5))
            dot = normal.DotProduct(orientation_vector)
            if dot > 0.5:
                for loop in face.EdgeLoops:
                    for edge in loop:
                        curve = edge.AsCurve()
                        if isinstance(curve, Line):
                            p1, p2 = curve.GetEndPoint(0), curve.GetEndPoint(1)
                            if abs(p1.Z - p2.Z) < 0.01 and curve.Length > longest:
                                best_face = face
                                best_edge = curve
                                longest = curve.Length
    return best_face, best_edge

def place_on_group(walls_group, orientation_vector, label):
    try:
        total_len = 0.0
        face_refs = []
        curves = []

        for wall in walls_group:
            face, curve = get_wall_face_for_orientation(wall, orientation_vector)
            if face and curve:
                total_len += curve.Length
                face_refs.append((wall, face))
                curves.append((wall, curve))

        usable_length = total_len - 2 * end_clearance
        if usable_length <= start_offset:
            log("Group too short for NEC placement on {}.".format(label))
            return []

        count = int(math.floor((usable_length - start_offset) / spacing))
        dist_list = [start_offset + i * spacing for i in range(count + 1)]

        placed = []
        dist_covered = 0.0

        for wall, curve in sorted(curves, key=lambda x: x[1].GetEndPoint(0).X):
            curve_len = curve.Length
            direction = curve.GetEndPoint(1).Subtract(curve.GetEndPoint(0)).Normalize()
            face = dict(face_refs)[wall]

            while dist_list and dist_list[0] <= dist_covered + curve_len:
                d = dist_list.pop(0) - dist_covered
                point = curve.GetEndPoint(0).Add(direction.Multiply(d))
                point = XYZ(point.X, point.Y, point.Z + 0.15)
                fam = doc.Create.NewFamilyInstance(face.Reference, point, XYZ.BasisZ, receptacle_family)
                placed.append((fam.Id.IntegerValue, point))
            dist_covered += curve_len
        return placed
    except Exception as e:
        log("Error placing on group {}: {}".format(label, str(e)))
        errors.append(str(e))
        return []

if not receptacle_family.IsActive:
    TransactionManager.Instance.EnsureInTransaction(doc)
    receptacle_family.Activate()
    doc.Regenerate()
    TransactionManager.Instance.TransactionTaskDone()

TransactionManager.Instance.EnsureInTransaction(doc)

groups = group_walls(walls)
for g in groups:
    base_orient = g[0].Orientation
    exterior = place_on_group(g, base_orient, "Exterior")
    interior = place_on_group(g, base_orient.Negate(), "Interior")

    if exterior:
        results.append(("Group Exterior", len(exterior)))
    if interior:
        results.append(("Group Interior", len(interior)))

TransactionManager.Instance.TransactionTaskDone()
log_file.close()

TaskDialog.Show("NEC Dual-Side Placement", "Receptacles placed on both wall faces.\nGroups: {}\nLog: {}".format(len(groups), log_path))
OUT = results
