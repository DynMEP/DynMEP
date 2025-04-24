# 👷‍♂️ DynMEP

Welcome to **DynMEP**! I'm an engineer and automation enthusiast crafting **Dynamo scripts** to turbocharge **Revit MEP** and **BIM** workflows. My mission is to streamline mechanical, electrical, and plumbing design with NEC-compliant tools, saving MEP firms 5–15 hours per project. Built for Revit 2025, these tested scripts, backed by 20+ years of electrical engineering expertise, are hosted at [github.com/DynMEP](https://github.com/DynMEP) under the MIT License. Explore below to automate your BIM projects, reduce errors, and deliver top-notch MEP designs. New scripts are added regularly, so check back often!

---

## 🔧 What I Do

I create Python/Dynamo scripts to accelerate MEP design in Revit, optimizing BIM data handling and ensuring NEC 2023 compliance. From clash detection to lighting placement, my tools boost productivity for engineers, designers, and contractors.

### 🔍 Key Areas of Focus
- 🚀 **Dynamo Automation**: Streamline MEP tasks with custom scripts.
- 🧠 **BIM Data Optimization**: Clean, tag, and manage MEP systems.
- 🛠️ **Revit API**: Precision automation for electrical designs.
- 🧰 **Smart Families**: Automate placement with MEP logic.
- 🏗️ **Parametric Design**: Rules-based modeling for efficiency.

---

## 📁 Scripts

Below is a growing collection of Revit MEP automation scripts. Each includes a description highlighting time savings, NEC compliance, and MEP benefits.

### 1. Clash Detection (Electrical-HVAC) 🛡️
**Clash_Detection_Electrical_HVAC_Dynamo.py**  
Streamline BIM coordination with this Python/Dynamo script, automating clash detection between electrical systems (conduits, cable trays) and HVAC ducts in Revit 2025. Saving 10–15 hours per project, it ensures NEC-compliant designs by identifying conflicts early, reducing costly rework. The script generates detailed CSV reports, enhancing MEP collaboration and project accuracy. With robust error handling and logging, it simplifies troubleshooting for MEP firms. Hosted at [github.com/DynMEP/DynMEP/tree/main/scripts](https://github.com/DynMEP/DynMEP/tree/main/scripts), this tool boosts efficiency, ensuring seamless integration into electrical workflows, delivering high-quality, clash-free designs for modern MEP projects.

### 2. Lighting Fixture Placement 💡
**Automate_Lighting_Fixture_Placement.py**  
Automate NEC 2023-compliant lighting placement with this Python/Dynamo script for Revit 2025, saving 6–10 hours per project. It places fixtures in rooms using grid and boundary logic, supports DIALux CSV integration, and ensures ceiling-hosted installations per NEC 410.36(A). MEP firms benefit from precise fixture positioning, avoiding wall conflicts, with detailed CSV outputs and logs for compliance verification. Available at [github.com/DynMEP/DynMEP/tree/main/scripts](https://github.com/DynMEP/DynMEP/tree/main/scripts), this script enhances design accuracy and efficiency, streamlining lighting workflows and delivering code-compliant, high-quality MEP projects with minimal manual effort.

### 3. Receptacle Placement 🔌
**Receptacle_Placement_Revit.py**  
This Python/Dynamo script automates NEC-compliant receptacle placement on both wall faces in Revit 2025, saving 6–10 hours per project. By grouping wall segments and ensuring precise spacing, it meets NEC standards, reducing errors in MEP electrical designs. Detailed logs and task dialogs provide transparency, while CSV outputs support documentation. Hosted at [github.com/DynMEP](https://github.com/DynMEP), this tool enhances MEP firm productivity, delivering accurate, code-compliant layouts with minimal effort. Streamline your electrical workflows and achieve high-quality, efficient designs with this proven automation solution.

### 4. Panel Schedule Generator ⚡️
**Panel_Schedule_Generator_Dynamo.py**  
Generate NEC-compliant panel schedules in Revit 2025 with this Python/Dynamo script, saving 10–15 hours per project. It automates circuit sorting and voltage correction, producing detailed CSV schedules for MEP electrical designs. With robust error handling, it ensures accurate load and current data, enhancing project reliability. Available at [github.com/DynMEP](https://github.com/DynMEP), this script streamlines MEP workflows, reducing manual effort and ensuring compliance with NEC standards. Boost efficiency and deliver high-quality electrical documentation with this essential tool for modern MEP firms.

### 5. Electrical Load Estimator 📊
**Electrical_Load_Estimator_Dynamo.py**  
This Python/Dynamo script automates NEC-compliant load estimation for electrical, HVAC, and lighting systems in Revit 2025, saving 5–8 hours per project. It generates formatted tables and CSV reports, ensuring accurate load calculations for MEP designs. With comprehensive error handling, it minimizes errors, enhancing project accuracy. Hosted at [github.com/DynMEP](https://github.com/DynMEP), this tool streamlines MEP workflows, delivering code-compliant load data with minimal effort. Improve efficiency and ensure high-quality electrical designs with this reliable automation solution for MEP firms.

### 6. Conduit Length Calculator 📏
**Conduit_Length_Calculator_Dynamo.py**  
Automate conduit length calculations in Revit 2025 with this Python/Dynamo script, saving 8–12 hours per project. It generates detailed CSV reports for material takeoffs, supporting NEC-compliant MEP cost estimation. Robust error logging ensures reliability, while type and size summaries enhance project planning. Available at [github.com/DynMEP](https://github.com/DynMEP), this script boosts MEP firm efficiency, reducing manual effort and ensuring accurate conduit data. Streamline your electrical workflows and deliver high-quality, cost-effective designs with this essential automation tool.

---

## 🛠️ Installation

1. **Prerequisites**:
   - Autodesk Revit 2025
   - Dynamo 2.17+
   - Python (IronPython 2.7 or CPython 3)
   - RevitAPI, RevitServices libraries

2. **Setup**:
   - Clone the repo: `git clone https://github.com/DynMEP`
   - Copy scripts to your Dynamo project folder.
   - Load scripts into Dynamo’s Python Script node.
   - Ensure Revit model includes relevant elements (e.g., conduits, rooms, panels).

3. **Dependencies**:
   - Included in Revit/Dynamo (`RevitAPI`, `RevitServices`).
   - No external packages required.

---

## 🚀 Usage

1. Open Revit 2025 and load your MEP project.
2. Launch Dynamo and create a new workspace.
3. Add a Python Script node and paste the desired script.
4. Connect inputs:
   - **Clash Detection**: No inputs; runs on model elements.
   - **Lighting Placement**: Rooms, fixture symbol, optional DIALux CSV.
   - **Receptacle Placement**: Walls, receptacle family, offset/spacing.
   - **Panel Schedule**: No inputs; runs on panels.
   - **Load Estimator**: No inputs; runs on equipment.
   - **Conduit Calculator**: No inputs; runs on conduits.
5. Run the script and check Desktop outputs (CSV, logs, guides).
6. Review script logs for NEC compliance and troubleshooting (e.g., ensure closed room boundaries for Lighting Placement).

See each script’s header or [wiki](https://github.com/DynMEP/wiki) for detailed guides.

---

## 🎯 Benefits

- **Time Savings**: Save 5–15 hours per project, streamlining MEP tasks (aligned with Desapex’s 50% efficiency gains).
- **NEC Compliance**: Meet NEC 2023 standards (e.g., 410.36(A) for lighting, 210.19(A) for circuits).
- **MEP Value**: Enhance BIM coordination, reduce rework, and improve accuracy with CSV outputs and robust logging.

---


📜 License
Licensed under the MIT License. See LICENSE for details.

🤝 Let’s Collaborate
Got a BIM challenge or need custom automation? Explore, fork, or contribute to github.com/DynMEP! Submit pull requests or open issues to enhance these tools. For consulting or custom scripts, reach out via GitHub Issues or direct message.

---

Author: Alfonso Davila  
Email: davila.alfonso@gmail.com  
LinkedIn: www.linkedin.com/in/alfonso-davila-3a121087  
GitHub: github.com/DynMEP  

🌐 Website (Coming Soon): [dynmep.io](http://dynmep.io)  
📺 YouTube: [@DynMEP](https://youtube.com/@DynMEP)

---

> _“Let’s build smarter MEP workflows together! 🚧”_

