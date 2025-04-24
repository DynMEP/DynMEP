# =============================================================================
# Script Header: Revit Electrical-HVAC Clash Detection
# =============================================================================
# Purpose: Automates clash detection between electrical systems (conduits, cable trays)
#          and HVAC ducts in Autodesk Revit, generating a CSV report to streamline
#          BIM coordination for MEP firms.
# Version: 1.0
# Author: Alfonso Davila - Electrical Engineer, Revit MEP Dynamo BIM Expert
# Contact: davila.alfonso@gmail.com - www.linkedin.com/in/alfonso-davila-3a121087
# Repository: https://github.com/DynMEP
# License: MIT License (see LICENSE file in repository)
# Created: April 24, 2025
# Compatibility: Revit 2025, Dynamo 2.17+, IronPython 2.7 or CPython 3
# Dependencies: RevitAPI, RevitServices
# Notes:
#   - Ensure Revit model contains conduits, cable trays, and HVAC ducts.
#   - Outputs CSV report to Desktop for clash analysis.
#   - See repository for documentation and additional MEP tools.
# =============================================================================

import clr
clr.AddReference('RevitAPI')
clr.AddReference('RevitServices')
from Autodesk.Revit.DB import *
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager
import csv
import os

# Get the current Revit document
doc = DocumentManager.Instance.CurrentDBDocument

# Function to format clash report row
def format_clash_row(clash):
    return "Clash: {} (ID: {}) vs {} (ID: {})".format(
        clash["Element1_Category"], clash["Element1_ID"],
        clash["Element2_Category"], clash["Element2_ID"]
    )

# Collect electrical systems (conduits and cable trays)
conduit_collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Conduit).WhereElementIsNotElementType()
cable_tray_collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_CableTray).WhereElementIsNotElementType()
electrical_elements = list(conduit_collector.ToElements()) + list(cable_tray_collector.ToElements())

# Collect HVAC ducts
duct_collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_DuctCurves).WhereElementIsNotElementType()
flex_duct_collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_FlexDuctCurves).WhereElementIsNotElementType()
hvac_elements = list(duct_collector.ToElements()) + list(flex_duct_collector.ToElements())

# List to store clash data
clash_data = []

# Perform clash detection
for elec in electrical_elements:
    try:
        # Get category name for electrical element
        elec_category = elec.Category.Name if elec.Category else "Unknown"
        elec_id = elec.Id.IntegerValue
        
        # Create intersection filter for this electrical element
        intersect_filter = ElementIntersectsElementFilter(elec)
        
        for hvac in hvac_elements:
            try:
                # Get category name for HVAC element
                hvac_category = hvac.Category.Name if hvac.Category else "Unknown"
                hvac_id = hvac.Id.IntegerValue
                
                # Check for intersection
                if intersect_filter.PassesFilter(hvac):
                    clash_data.append({
                        "Element1_Category": elec_category,
                        "Element1_ID": elec_id,
                        "Element2_Category": hvac_category,
                        "Element2_ID": hvac_id
                    })
            except:
                # Skip HVAC elements with issues
                continue
    except:
        # Skip electrical elements with issues
        continue

# Format clash report for Dynamo output
clash_report = ["Clash Detection Results: {} clashes found".format(len(clash_data))]
if clash_data:
    clash_report.append("----------------------------------------")
    for clash in clash_data:
        clash_report.append(format_clash_row(clash))
else:
    clash_report.append("No clashes detected.")

# Optional: Write to CSV
output_path = os.path.join(os.path.expanduser("~"), "Desktop", "Clash_Detection_Report.csv")
csv_data = [["Element 1 Category", "Element 1 ID", "Element 2 Category", "Element 2 ID"]]

for clash in clash_data:
    csv_data.append([
        clash["Element1_Category"],
        clash["Element1_ID"],
        clash["Element2_Category"],
        clash["Element2_ID"]
    ])

try:
    with open(output_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(csv_data)
    output_message = "CSV file written to: {}".format(output_path)
except Exception as e:
    output_message = "Error writing CSV: {}".format(str(e))

# Output for Dynamo (clash report and CSV message)
OUT = clash_report + [output_message]