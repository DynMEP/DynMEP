# =============================================================================
# Script Header: Revit Electrical Load Estimator
# =============================================================================
# Purpose: Automates electrical load estimation for equipment, HVAC, and lighting
#          in Autodesk Revit, generating NEC-compliant load reports for MEP firms.
# Version: 1.0
# Author: Alfonso Davila - Electrical Engineer, Revit MEP Dynamo BIM Expert
# Contact: [Your Email or LinkedIn, optional]
# Repository: https://github.com/DynMEP
# License: MIT License (see LICENSE file in repository)
# Created: April 24, 2025
# Compatibility: Revit 2025, Dynamo 2.17+, IronPython 2.7 or CPython 3
# Dependencies: RevitAPI, RevitServices
# Notes:
#   - Ensure relevant categories (Electrical, HVAC, Lighting) are populated.
#   - Outputs formatted table and CSV with total load data.
#   - See repository for usage guide and additional MEP tools.
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

# Function to format table row with fixed-width columns
def format_table_row(columns, widths):
    return "| " + " | ".join(str(col).ljust(width) for col, width in zip(columns, widths)) + " |"

# Define table structure
table_headers = ["Category", "Equipment Name", "Load (VA)", "Voltage (V)", "System Type"]
column_widths = [15, 25, 12, 12, 15]
table_lines = []

# Add header to table
table_lines.append(format_table_row(table_headers, column_widths))
table_lines.append("|" + "-|" * len(table_headers))

# Collect elements from relevant categories
categories = [
    (BuiltInCategory.OST_ElectricalEquipment, "Electrical"),
    (BuiltInCategory.OST_MechanicalEquipment, "HVAC"),
    (BuiltInCategory.OST_LightingFixtures, "Lighting")
]

load_data = []
total_load = 0.0

# Process each category
for category, category_name in categories:
    collector = FilteredElementCollector(doc).OfCategory(category).WhereElementIsNotElementType()
    elements = collector.ToElements()
    
    for element in elements:
        try:
            # Get equipment name
            name = element.Name or "Unknown"
            
            # Get load (Apparent Load in VA)
            load_param = element.LookupParameter("Apparent Load")
            load_va = load_param.AsDouble() if load_param else 0.0
            
            # Get voltage
            voltage_param = element.LookupParameter("Voltage")
            voltage = voltage_param.AsDouble() * 120.0 if voltage_param else 120.0  # Default to 120V
            
            # Get system type (e.g., single-phase or three-phase)
            poles_param = element.LookupParameter("Number of Poles")
            system_type = "Three-Phase" if poles_param and poles_param.AsInteger() == 3 else "Single-Phase"
            
            # Add to total load
            total_load += load_va
            
            # Store data
            load_data.append({
                "Category": category_name,
                "Name": name[:25],  # Truncate for table
                "Load": round(load_va, 2),
                "Voltage": round(voltage, 2),
                "System": system_type
            })
        except:
            # Skip elements with missing data
            continue

# Add data to table
for data in load_data:
    row = [
        data["Category"],
        data["Name"],
        data["Load"],
        data["Voltage"],
        data["System"]
    ]
    table_lines.append(format_table_row(row, column_widths))

# Add total load row
table_lines.append("|" + "-|" * len(table_headers))
table_lines.append(format_table_row(["Total", "", round(total_load, 2), "", ""], column_widths))

# Optional: Write to CSV
output_path = os.path.join(os.path.expanduser("~"), "Desktop", "Electrical_Load_Estimate.csv")
csv_data = [table_headers] + [[data["Category"], data["Name"], data["Load"], data["Voltage"], data["System"]] for data in load_data]
csv_data.append(["Total", "", round(total_load, 2), "", ""])

try:
    with open(output_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(csv_data)
    output_message = "CSV file written to: {}".format(output_path)
except Exception as e:
    output_message = "Error writing CSV: {}".format(str(e))

# Output for Dynamo (table as list of strings)
OUT = table_lines + [output_message]