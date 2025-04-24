# =============================================================================
# Script Header: Revit Electrical Panel Schedule Generator
# =============================================================================
# Purpose: Automates NEC-compliant electrical panel schedule generation in Autodesk
#          Revit, including voltage correction and natural circuit sorting for MEP
#          firms.
# Version: 4.2
# Author: Alfonso Davila - Electrical Engineer, Revit MEP Dynamo BIM Expert
# Contact: davila.alfonso@gmail.com - www.linkedin.com/in/alfonso-davila-3a121087
# Repository: https://github.com/DynMEP
# License: MIT License (see LICENSE file in repository)
# Created: April 24, 2025
# Compatibility: Revit 2025, Dynamo 2.17+, IronPython 2.7 or CPython 3
# Dependencies: RevitAPI, RevitServices
# Notes:
#   - Ensure electrical panels and systems are defined in the Revit model.
#   - Outputs CSV schedule with load and current data.
#   - See repository for documentation and customization options.
# =============================================================================

import clr
import os
import csv
import re
import traceback

clr.AddReference('RevitServices')
from RevitServices.Persistence import DocumentManager

clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import (
    FilteredElementCollector,
    BuiltInCategory,
    BuiltInParameter,
    FamilyInstance,
)

# ElectricalSystem import varies by version
try:
    from Autodesk.Revit.DB.Electrical import ElectricalSystem
except ImportError:
    from Autodesk.Revit.DB import ElectricalSystem

# Current Revit document
doc = DocumentManager.Instance.CurrentDBDocument

# -------------------------------------------------------------
# Helper functions
# -------------------------------------------------------------

def circuit_sort_key(circ_num):
    """Return sortable tuple; ints first, then alphanumerics."""
    if circ_num is None:
        return (1, "")
    try:
        return (0, int(circ_num))
    except Exception:
        leading = re.split(r"\D+", str(circ_num))[0]
        try:
            return (0, int(leading))
        except Exception:
            return (1, str(circ_num))

def safe_as_string(param):
    return param.AsString() if param and param.HasValue else None

# -------------------------------------------------------------
# Main routine
# -------------------------------------------------------------
try:
    header = [
        "Panel Name",
        "Circuit Number",
        "Load Name",
        "Voltage (V)",
        "kVA (Connected)",
        "Current @100% (A)",
        "Current @125% (A) - NEC Continuous",
        "Warnings",
    ]
    rows = []

    # Collect panels
    panels = (
        FilteredElementCollector(doc)
        .OfClass(FamilyInstance)
        .OfCategory(BuiltInCategory.OST_ElectricalEquipment)
        .WhereElementIsNotElementType()
        .ToElements()
    )

    for pnl in panels:
        if not pnl or not pnl.IsValidObject:
            continue

        panel_name = safe_as_string(pnl.get_Parameter(BuiltInParameter.RBS_ELEC_PANEL_NAME)) or f"Panel_{pnl.Id.IntegerValue}"

        mep = getattr(pnl, "MEPModel", None)
        if not mep or not mep.IsValidObject:
            continue

        for sys in mep.GetAssignedElectricalSystems() or []:
            if not isinstance(sys, ElectricalSystem) or not sys.IsValidObject:
                continue

            warnings = []

            circ_num = sys.CircuitNumber
            load_name = sys.LoadName or "Unknown"

            # Voltage
            voltage_param = sys.get_Parameter(BuiltInParameter.RBS_ELEC_VOLTAGE)
            voltage_raw = voltage_param.AsDouble() if voltage_param else 0.0

            # Some projects store decivolts → convert
            voltage = voltage_raw / 10.0 if voltage_raw >= 600 else voltage_raw

            if voltage > 600:
                warnings.append(f"Unrealistic voltage: {voltage} V")

            # Apparent load
            load_param = sys.get_Parameter(BuiltInParameter.RBS_ELEC_APPARENT_LOAD)
            load_va = load_param.AsDouble() if load_param else 0.0

            kva = load_va / 1000.0 if load_va > 0 else 0.0
            i100 = load_va / voltage if voltage > 0 else 0.0

            is_cont = "Continuous" in (getattr(sys, "LoadClassifications", "") or "")
            i125 = i100 * 1.25 if is_cont else i100

            if kva == 0 and load_name.lower() != "spare":
                warnings.append("Zero kVA load")
            if i100 > 1000:
                warnings.append(f"Unrealistic current: {i100:.2f} A")

            rows.append([
                panel_name,
                circ_num,
                load_name,
                round(voltage, 1),
                round(kva, 3),
                round(i100, 2),
                round(i125, 2),
                "; ".join(warnings),
            ])

    # Natural sort
    rows_sorted = sorted(rows, key=lambda r: (r[0], circuit_sort_key(r[1])))

    schedule = [header] + rows_sorted

    # Export CSV
    out_folder = os.path.expanduser("~/Desktop")
    csv_path = os.path.join(out_folder, "panel_schedule.csv")
    with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
        csv.writer(f).writerows(schedule)

    OUT = schedule  # Dynamo node output

except Exception:
    OUT = "Error:\n" + traceback.format_exc()
