# =============================================================================
# Script Header: Revit Conduit Length Calculator
# =============================================================================
# Purpose: Automates conduit length calculations in Autodesk Revit, generating
#          detailed CSV reports for material takeoffs and cost estimation in MEP
#          projects.
# Version: 2.0
# Author: Alfonso Davila - Electrical Engineer, Revit MEP Dynamo BIM Expert
# Contact: davila.alfonso@gmail.com - www.linkedin.com/in/alfonso-davila-3a121087
# Repository: https://github.com/DynMEP
# License: MIT License (see LICENSE file in repository)
# Created: April 24, 2025
# Compatibility: Revit 2025, Dynamo 2.17+, IronPython 2.7 or CPython 3
# Dependencies: RevitAPI, RevitServices
# Notes:
#   - Ensure conduits are modeled in the Revit project.
#   - Outputs CSV with conduit type, size, and length summaries.
#   - See repository for setup and debugging instructions.
# =============================================================================

import clr
clr.AddReference('RevitAPI')
clr.AddReference('RevitServices')
from Autodesk.Revit.DB import *
from RevitServices.Persistence import DocumentManager
import csv
import os
from datetime import datetime

# Get the current Revit document
doc = DocumentManager.Instance.CurrentDBDocument

# Function to convert Revit internal units to project display units (feet)
def convert_length_to_display_units(length, unit_type=UnitTypeId.Feet):
    try:
        display_length = UnitUtils.ConvertFromInternalUnits(length, unit_type)
        return round(display_length, 2)
    except:
        return "Unknown"

# Collect conduits
def get_conduits():
    collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Conduit).WhereElementIsNotElementType()
    conduits = collector.ToElements()
    return conduits

# Main processing
def process_conduits():
    conduits = get_conduits()
    conduit_data = []
    total_length = 0.0
    error_log = []
    debug_info = [f"Found {len(conduits)} conduits in the model"]

    if not conduits:
        error_log.append("No conduits found in the model. Check category OST_Conduit or model content.")

    # Start a transaction for reading
    t = Transaction(doc, "Read Conduit Data")
    t.Start()

    try:
        for conduit in conduits:
            conduit_id = conduit.Id.IntegerValue
            try:
                # Get conduit type
                type_name = "Unknown"
                try:
                    type_id = conduit.GetTypeId()
                    if type_id and type_id != ElementId.InvalidElementId:
                        conduit_type = doc.GetElement(type_id)
                        if conduit_type:
                            type_param = conduit_type.LookupParameter("Type Name")
                            type_name = type_param.AsString() if type_param and type_param.HasValue else conduit_type.Name if hasattr(conduit_type, "Name") else "No Type"
                        else:
                            error_log.append(f"Conduit ID {conduit_id}: Invalid type ID {type_id.IntegerValue}")
                    else:
                        error_log.append(f"Conduit ID {conduit_id}: No valid type ID")
                except Exception as e:
                    error_log.append(f"Conduit ID {conduit_id}: Failed to get type name: {str(e)}")

                # Get conduit size (diameter)
                size = "Unknown"
                try:
                    diameter_param = conduit.get_Parameter(BuiltInParameter.RBS_CONDUIT_DIAMETER_PARAM)
                    if diameter_param and diameter_param.HasValue:
                        size = convert_length_to_display_units(diameter_param.AsDouble())
                    else:
                        alt_params = ["Nominal Diameter", "Diameter"]
                        for param_name in alt_params:
                            param = conduit.LookupParameter(param_name)
                            if param and param.HasValue:
                                size = convert_length_to_display_units(param.AsDouble())
                                break
                except Exception as e:
                    error_log.append(f"Conduit ID {conduit_id}: Failed to get diameter: {str(e)}")

                # Get conduit length
                length = 0.0
                try:
                    length_param = conduit.get_Parameter(BuiltInParameter.CURVE_ELEM_LENGTH)
                    if length_param and length_param.HasValue:
                        length = convert_length_to_display_units(length_param.AsDouble())
                    else:
                        length_param = conduit.LookupParameter("Length")
                        if length_param and length_param.HasValue:
                            length = convert_length_to_display_units(length_param.AsDouble())
                except Exception as e:
                    error_log.append(f"Conduit ID {conduit_id}: Failed to get length: {str(e)}")

                # Add to total length
                total_length += length if isinstance(length, float) else 0.0

                # Store data
                conduit_data.append({
                    "Type": type_name,
                    "Size": size,
                    "Length": length,
                    "ElementId": conduit_id
                })
            except Exception as e:
                error_log.append(f"Conduit ID {conduit_id}: General processing error: {str(e)}")
                conduit_data.append({
                    "Type": "Error",
                    "Size": "Unknown",
                    "Length": 0.0,
                    "ElementId": conduit_id
                })
    finally:
        t.Commit()

    debug_info.append(f"Processed {len(conduit_data)} conduits, {len(error_log)} errors")
    return conduit_data, total_length, error_log, debug_info

# Summarize by type and size
def summarize_conduit_data(conduit_data):
    summary_data = {}
    for data in conduit_data:
        key = (data["Type"], data["Size"])
        if key not in summary_data:
            summary_data[key] = 0.0
        summary_data[key] += data["Length"] if isinstance(data["Length"], float) else 0.0
    return summary_data

# Write to CSV
def write_to_csv(summary_data, total_length, conduit_data, error_log, debug_info):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    project_name = doc.ProjectInformation.Name if doc.ProjectInformation else "Revit"
    filename = f"{project_name}_Conduit_Length_Summary_{timestamp}.csv"
    output_path = os.path.join(os.path.expanduser("~"), "Desktop", filename)

    # Ensure output directory exists
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Prepare CSV data
    csv_data = [["Conduit Type", "Size (ft)", "Total Length (ft)"]]
    for (type_name, size), length in sorted(summary_data.items()):
        csv_data.append([type_name, str(size), round(length, 2)])
    csv_data.append(["Total", "", round(total_length, 2)])

    # Write CSV
    try:
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(csv_data)
        output_message = f"CSV file written to: {output_path}"
    except Exception as e:
        output_message = f"Error writing CSV: {str(e)}"
        output_path = None

    # Write error and debug log
    if error_log or debug_info:
        log_path = output_path.replace(".csv", "_debug.log") if output_path else os.path.join(os.path.expanduser("~"), "Desktop", "conduit_debug.log")
        try:
            with open(log_path, 'w', encoding='utf-8') as log_file:
                log_file.write("Debug Info:\n" + "\n".join(debug_info) + "\n\nErrors:\n" + "\n".join(error_log))
            output_message += f"\nDebug log written to: {log_path}"
        except:
            output_message += "\nFailed to write debug log."

    return conduit_data, output_message, debug_info

# Execute
try:
    conduit_data, total_length, error_log, debug_info = process_conduits()
    summary_data = summarize_conduit_data(conduit_data)
    result, output_message, debug_info = write_to_csv(summary_data, total_length, conduit_data, error_log, debug_info)
except Exception as e:
    result = []
    output_message = f"Script failed: {str(e)}"
    debug_info = ["Script failed", str(e)]

# Output for Dynamo: return conduit data, message, and debug info
OUT = [result, output_message, debug_info]