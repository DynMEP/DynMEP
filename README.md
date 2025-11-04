# 👷‍♂️ DynMEP

Welcome to **DynMEP**! I'm Alfonso Davila, an Electrical Engineer with 20+ years of experience in power systems, renewable integration, and multidisciplinary project leadership. My mission is to advance U.S. electrical infrastructure and sustainable design by developing automation and AI-powered tools for Revit MEP and BIM workflows. These solutions streamline engineering processes, enhance accuracy, and promote energy efficiency across the construction and power sectors. Projects include NEC-compliant Dynamo/Python scripts, AI-based symbol detection systems, and computational optimization methods supporting reliable and sustainable energy distribution. All repositories are hosted at [github.com/DynMEP](https://github.com/DynMEP) under the MIT License.

---

## 🌟 About Me

With 20+ years in electrical engineering specializing in power distribution, MEP design, and sustainable energy systems, I develop cutting-edge tools across multiple domains:

- **Renewable Energy**: Solar+storage optimization and hybrid system integration
- **Computer Vision**: YOLO-based AI for automated technical drawing analysis
- **Renewable Energy Simulation**: MATLAB simulations for hybrid solar/wind integration
- **Motor Control Systems**: VFD simulation and analysis for industrial applications
- **Reinforcement Learning**: Deep Q-Networks for microgrid energy optimization
- **Revit MEP Automation**: NEC-compliant Dynamo scripts saving 5–15 hours per project
- **Professional Focus**: Power systems, BIM workflows, and green energy solutions

---

## 📂 Public Repositories

### 1. **SOLARA** - Solar Analytics & Revenue Advisor ☀️
**Repository**: [github.com/DynMEP/solara](https://github.com/DynMEP/solara)

Professional-grade photovoltaic and battery energy storage system optimization platform. Built on NREL's validated PySAM models, SOLARA delivers capabilities comparable to commercial tools like HOMER Pro and PVsyst - completely free and open source.

**Key Features**:
- **NREL-Validated**: Built on PySAM (same engine used by national labs and Fortune 500s)
- **Automated Weather Data**: NREL NSRDB integration with caching and retry logic
- **Advanced Optimization**: Genetic (NSGA-II), Bayesian, ML Surrogate, Differential Evolution
- **Interactive Dashboard**: Real-time Dash/Plotly UI with live optimization tracking
- **NEC 2023 Compliant**: Automated compliance checking for Articles 690, 705, 706
- **Production-Ready**: Comprehensive test suite (11 automated tests)

**Optimization Methods**:
- Parametric grid search for rapid design space exploration
- NSGA-II genetic algorithm for Pareto-optimal solutions
- Gaussian Process Bayesian optimization for sample efficiency
- Gradient Boosting ML surrogate with Latin Hypercube Sampling
- Differential Evolution for global optimization

**Real Value**:
- **Zero Cost**: vs $600-8,000/year for commercial tools
- **Time Savings**: 15-40 hours per project through automation
- **Research-Grade**: NREL-validated accuracy meets practical efficiency

**Perfect For**:
- Energy consultants doing techno-economic analysis
- C&I demand charge optimization projects
- Researchers needing validated solar+storage models
- Utilities planning distributed energy resources
- MEP engineers designing NEC-compliant PV systems

**Technology Stack**:
- Python 3.9+
- PySAM 5.0+ (NREL)
- Plotly, Dash (visualization)
- Multiple optimization libraries (pymoo, scikit-optimize, scikit-learn)

**Quick Start**:
```bash
git clone https://github.com/DynMEP/solara.git
cd solara
pip install -r requirements.txt
python solara.py --config examples/example_config.json
```

**Version**: 3.1.1 

---

### 2. **YOLOplan** - AI-Powered Symbol Detection 🤖
**Repository**: [github.com/DynMEP/YOLOplan](https://github.com/DynMEP/YOLOplan)

YOLOplan revolutionizes technical drawing analysis by automating symbol detection and counting using advanced YOLO object detection. It processes PDF, image, and CAD formats with exceptional accuracy, even in noisy or complex plans.

**Key Features**:
- **Automatic Detection**: Identifies and counts electrical, HVAC, plumbing, and architectural symbols
- **Multi-Format Support**: Works with PDF, images, and CAD files
- **Robust Performance**: Handles background noise, varied symbol sizes, and rotations
- **Custom Training**: Train models for your own symbols
- **Export Options**: CSV, Excel, JSON, or annotated images with bounding boxes

**Applications**:
- Electrical and MEP engineering takeoff
- Construction estimation
- BIM and digital building modeling
- Facility management
- QA/QC for technical plans

**Technology Stack**:
- Python 3.8+
- Ultralytics YOLO
- OpenCV, pdf2image, PyMuPDF

**Project Structure**:
```
YOLOplan/
├── yolo_plan_core/        # Common utilities
├── yolo_plan_electric/    # Electrical symbols models
├── yolo_plan_hvac/        # HVAC models (future)
├── datasets/              # Training datasets
├── notebooks/             # Demo notebooks
└── demo_takeoff_electric.ipynb
```

---

### 3. **GreenPowerHub** - Renewable Energy Integration 🌿⚡
**Repository**: [github.com/DynMEP/GreenPowerHub](https://github.com/DynMEP/GreenPowerHub)

GreenPowerHub serves as a comprehensive hub for renewable energy integration tools, simulations, and resources. Focused on advancing sustainable energy solutions through power systems expertise and advanced simulations.

**Mission**:
- Develop innovative tools for renewable energy integration
- Enhance power system efficiency through data-driven simulations
- Foster global collaboration for sustainable practices
- Drive positive impact with cutting-edge energy solutions

**Current Scripts**:

#### Hybrid Renewable Integration Simulator
**File**: `Hybrid_Renewable_Integration.m`  
**Released**: October 07, 2025

A MATLAB script simulating hybrid solar PV and wind energy systems integrated into power distribution grids.

**Features**:
- Calculates power outputs based on irradiance, temperature, and wind speed
- Applies basic MPPT (Maximum Power Point Tracking) approximation
- Estimates daily energy yield and grid contribution
- Saves results to CSV for MEP integration

**Benefits**:
- **Time Savings**: 5–10 hours per analysis
- **Compliance**: Supports NEC 2023-compliant designs
- **Planning**: Aids renewable project feasibility studies

**Planned Development**:
- **Renewable_Load_Optimizer.py**: Python script for load distribution optimization with Dynamo integration
- NEC 220 demand factor calculations
- Enhanced grid reliability analysis

**Requirements**:
- MATLAB (base version, no toolboxes required)
- Python 3.x (for future scripts)
- Optional: Revit/Dynamo for MEP integration

---

### 4. **VFD Motor Simulation** - Variable Frequency Drive Analysis ⚙️
**Repository**: [github.com/DynMEP/vfd-motor-simulation](https://github.com/DynMEP/vfd-motor-simulation)

A comprehensive Python-based simulation of Variable Frequency Drive (VFD) controlled motor startup for high-power induction motors, with comparative analysis against Direct-On-Line (DOL) starting methods.

**Target Audience**:
- Electrical Engineers (system design and analysis)
- Research Applications (motor control studies)
- Educational Purposes (understanding VFD operation)
- Industrial Planning (equipment specification)

**Key Features**:
- **Accurate Physics Modeling**: Proper torque-slip characteristics with constant V/f control
- **Multiple Load Types**: Constant torque, fan/pump (quadratic), and constant power loads
- **VFD vs DOL Comparison**: Side-by-side performance analysis with 81% peak current reduction
- **Real-time Analysis**: Speed, torque, current, slip, power, and efficiency tracking
- **Data Export**: Timestamped CSV files for further analysis
- **Professional Visualizations**: 6-panel comparison dashboard

**Simulation Capabilities**:
- 800HP (596.6 kW) three-phase induction motor (configurable)
- Multiple load type simulations (conveyors, fans/pumps, machine tools)
- DOL starting comparison with grid impact assessment
- Energy and efficiency analysis during startup
- Comprehensive performance metrics

**Key Results** (800HP motor example):
```
VFD Starting:
- Peak Current: 1104.6 A (1.23 × FLA)
- Final Speed: 1729 RPM
- Final Slip: 3.93%
- Startup Energy: 4.424 kWh

DOL Starting:
- Peak Current: 5821.6 A (6.50 × FLA)
- Starting Time: ~5 seconds
- Startup Energy: 2.724 kWh

VFD Advantages:
- 81% lower peak current
- Significantly reduced mechanical stress
- Minimal voltage sag (<5% vs 30-40%)
```

**Load Type Options**:
1. **Constant Torque**: Conveyors, hoists, positive displacement pumps
2. **Fan/Pump**: Centrifugal fans and pumps (torque ∝ speed²)
3. **Constant Power**: Machine tools, winders (torque ∝ 1/speed)

**Technical Specifications**:
- Python 3.x with NumPy, SciPy, Matplotlib
- First-order induction motor model with torque-slip characteristics
- Constant V/f control with low-frequency voltage boost
- IEEE standards validated
- Execution time: ~0.6 seconds for standard simulation

**Applications**:
- VFD rating determination
- Electrical infrastructure capacity evaluation
- Mechanical system compatibility assessment
- Energy consumption comparison
- Educational demonstrations
- Research baseline for advanced control strategies

**Version**: 3.0.0 (October 10, 2025)

**Future Roadmap**:
- GUI interface with real-time parameter adjustment (Q1 2026)
- Additional motor types and harmonic analysis (Q1-Q2 2026)
- Multi-motor simulation and thermal modeling (Q2 2026)
- Real-time hardware integration and web dashboard (Future)

---

### 5. **Dynamic Microgrid Resilience** - AI-Powered Energy Management 🔋⚡
**Repository**: [github.com/DynMEP/dynamic-microgrid-resilience](https://github.com/DynMEP/dynamic-microgrid-resilience)

An anticipatory Deep Q-Network (DQN) approach that achieves near-perfect microgrid energy management through intelligent battery control. The system learns to prepare for evening peak demand hours in advance, achieving 100% load coverage with zero unmet energy.

**Target Audience**:
- Energy Engineers (microgrid design and optimization)
- Renewable Energy Researchers (AI-based control systems)
- Utility Companies (grid reliability and peak management)
- Educational Institutions (reinforcement learning applications)

**Key Features**:
- **98.8% Average Load Coverage**: Across 100 diverse test scenarios
- **100% Best Policy Performance**: Optimal policy found at episode 100
- **Anticipatory Behavior**: Pre-evening preparation with 87% SOC by hour 15
- **Time-to-Event State Augmentation**: Explicit temporal encoding for peak anticipation
- **Hierarchical Reward Shaping**: Extreme penalties for evening failures, bonuses for preparation
- **Fast Training**: 21 minutes on laptop CPU to achieve optimal performance

**System Configuration**:
- Solar PV Array: 5 kW DC capacity
- Wind Turbine: 3 kW AC capacity
- Battery Storage: 18 kWh capacity, 6 kW power rating
- NEC 2023 Compliant (Articles 690, 694, 706)
- 95% round-trip efficiency

**Performance Highlights**:
```
✅ 98.8% Average Load Coverage (100 test scenarios)
✅ 100% Peak Policy Performance
✅ 99.2% Evening Reliability (vs 71.5% baseline)
✅ 0.13 kWh Average Unmet Energy
✅ 4.3 Year Payback Period
✅ 190% ROI (20-year projection)
✅ $7,088 Annual Savings
```

**Technology Stack**:
- Python 3.8+
- PyTorch 2.0+ (Deep Q-Network)
- NumPy, Pandas, Matplotlib
- Experience Replay with Target Networks
- 3-Layer Neural Network (256-128-64)

**Quick Start**:
```bash
git clone https://github.com/DynMEP/dynamic-microgrid-resilience.git
cd dynamic-microgrid-resilience
pip install -r requirements.txt

# Quick demo (1 minute)
python cli.py demo

# Full training with plots
python cli.py train --full --plot --economics

# Evaluate pre-trained model
python cli.py evaluate --auto-latest --scenarios 100 --plot
```

**Applications**:
- Off-grid residential/commercial microgrids
- Peak demand management and load shifting
- Renewable energy integration optimization
- Battery energy storage system (BESS) control
- Grid resilience and reliability improvement
- Energy cost reduction strategies

**Economic Viability**:
- Total System Cost: $35,808
- Payback Period: 4.3 years (vs 7-10 industry standard)
- 20-Year NPV: $57,886 (5% discount rate)
- Internal Rate of Return: 21.4%

**Research Paper**: "Anticipatory Deep Reinforcement Learning for Microgrid Energy Management: Achieving 100% Evening Peak Coverage Through Pre-Event Preparation" by Alfonso Davila (2025)

---

### 6. **DynMEP** - Revit MEP Automation Suite 🔧
**Repository**: [github.com/DynMEP/DynMEP](https://github.com/DynMEP/DynMEP)

A comprehensive collection of Python/Dynamo scripts designed to turbocharge Revit MEP workflows with NEC 2023 compliance.

**Available Scripts**:

#### Clash Detection (Electrical-HVAC) 🛡️
**File**: `Clash_Detection_Electrical_HVAC_Dynamo.py`  
Automates clash detection between electrical systems (conduits, cable trays) and HVAC ducts in Revit 2025. Generates detailed CSV reports, identifies conflicts early, and reduces costly rework.
- **Time Savings**: 10–15 hours per project
- **Compliance**: NEC-compliant design verification
- **Output**: CSV reports with detailed clash locations

#### Lighting Fixture Placement 💡
**File**: `Automate_Lighting_Fixture_Placement.py`  
Places fixtures in rooms using grid and boundary logic with DIALux CSV integration. Ensures ceiling-hosted installations per NEC 410.36(A).
- **Time Savings**: 6–10 hours per project
- **Features**: Grid-based placement, wall conflict avoidance
- **Output**: CSV logs for compliance verification

#### Receptacle Placement 🔌
**File**: `Receptacle_Placement_Revit.py`  
Automates NEC-compliant receptacle placement on both wall faces with precise spacing calculations.
- **Time Savings**: 6–10 hours per project
- **Compliance**: Meets NEC spacing standards
- **Output**: Detailed logs and CSV documentation

#### Panel Schedule Generator ⚡️
**File**: `Panel_Schedule_Generator_Dynamo.py`  
Generates NEC-compliant panel schedules with automated circuit sorting and voltage correction.
- **Time Savings**: 10–15 hours per project
- **Features**: Load and current data validation
- **Output**: Detailed CSV schedules

#### Electrical Load Estimator 📊
**File**: `Electrical_Load_Estimator_Dynamo.py`  
Automates load estimation for electrical, HVAC, and lighting systems with NEC compliance.
- **Time Savings**: 5–8 hours per project
- **Features**: Comprehensive error handling
- **Output**: Formatted tables and CSV reports

#### Conduit Length Calculator 📏
**File**: `Conduit_Length_Calculator_Dynamo.py`  
Calculates conduit lengths for material takeoffs and cost estimation.
- **Time Savings**: 8–12 hours per project
- **Features**: Type and size summaries
- **Output**: Detailed CSV reports

---

## 🔧 Installation & Usage

### General Prerequisites
- **SOLARA**: Python 3.9+, PySAM 5.0+, Plotly, Dash
- **YOLOplan**: Python 3.8+, Ultralytics YOLO, OpenCV
- **GreenPowerHub**: MATLAB (base version) or Python 3.x
- **vfd-motor-simulation**: Python 3.x, NumPy, SciPy, Matplotlib
- **Revit Scripts**: Autodesk Revit 2025, Dynamo 2.17+, Python (IronPython 2.7 or CPython 3)

### Quick Start - SOLARA:
```bash
git clone https://github.com/DynMEP/solara.git
cd solara
pip install -r requirements.txt
python solara.py --config examples/example_config.json --dashboard
```

### Quick Start - YOLOplan
```bash
git clone https://github.com/DynMEP/YOLOplan.git
cd YOLOplan
pip install -r requirements.txt
```
Run detection on your technical drawings and export results to CSV/Excel.

### Quick Start - GreenPowerHub
```bash
git clone https://github.com/DynMEP/GreenPowerHub.git
```
Open `Hybrid_Renewable_Integration.m` in MATLAB, adjust parameters, and run.

### Quick Start - VFD Motor Simulation
```bash
git clone https://github.com/DynMEP/vfd-motor-simulation.git
cd vfd-motor-simulation
pip install numpy scipy matplotlib
python vfd_simulation_v3.py
```
Customize motor parameters (HP, voltage, poles) and load types in the configuration section.

### Quick Start - DynMEP Scripts:
```bash
git clone https://github.com/DynMEP/DynMEP.git
```
1. Open Revit 2025 and load your MEP project
2. Launch Dynamo and create a new workspace
3. Add a Python Script node and paste the desired script
4. Connect appropriate inputs (see individual script documentation)
5. Run and check Desktop outputs (CSV, logs)

---

## 🎯 Combined Benefits

**Time Savings Across Projects**:
- **SOLARA**: 15-40 hours per solar+storage project
- **YOLOplan**: Automated symbol counting (hours to minutes)
- **GreenPowerHub**: 5–10 hours per renewable energy analysis
- **vfd-motor-simulation**: Instant VFD analysis vs. manual calculations (hours saved)
- **Dynamic Microgrid**: AI-powered energy management with 4.3-year payback
- **Revit MEP Scripts**: 5–15 hours per project

**Professional Value**:
- **NEC Compliance**: All electrical scripts meet NEC 2023 standards
- **Accuracy**: Reduce errors through automation
- **Innovation**: Cutting-edge AI and mathematical methods
- **Sustainability**: Support renewable energy adoption
- **Open Source**: MIT License for maximum collaboration

**Industry Impact**:
- BIM coordination excellence
- Renewable energy integration and optimization
- Motor control and VFD system design
- Microgrid resilience and AI control
- Construction estimation efficiency
- MEP engineering automation
- Academic research advancement

---

## 📜 License

All repositories are licensed under the MIT License. See individual repository LICENSE files for details.

---

## 🤝 Collaboration & Support

**Contribute**: Fork any repository, submit pull requests, or open issues to enhance these tools.

**Custom Development**: Need specialized automation, AI models, renewable energy simulations, or solar optimization? Contact me for consulting and custom solutions.

**Support**: Report issues via GitHub Issues on the respective repositories.

**Community**: Join the growing community of engineers, developers, and researchers using these tools worldwide.

---

## 📞 Contact

**Author**: Alfonso Antonio Dávila Vera  
**Email**: davila.alfonso@gmail.com  
**LinkedIn**: [www.linkedin.com/in/alfonso-davila-3a121087](http://www.linkedin.com/in/alfonso-davila-3a121087)  
**GitHub**: [github.com/DynMEP](https://github.com/DynMEP)  
**YouTube**: [@DynMEP](https://youtube.com/@DynMEP)  
**Website** (Coming Soon): [dynmep.com](http://dynmep.com)

---

## 🌟 Featured Achievements

- **20+ Years**: Electrical engineering expertise
- **7 Major Projects**: From Revit automation to solar optimization
- **Open Source**: All tools freely available under MIT License
- **Innovation**: Combining traditional engineering with cutting-edge technology
- **Impact**: Serving MEP firms, engineers, and researchers globally
- **Validated**: NREL, IEEE standards compliance and field-tested results

---

> _"Let's build smarter MEP workflows, advance renewable energy, and push the boundaries of computational research together! 🚧🌿🔬"_

---

<p><a href="https://www.buymeacoffee.com/h1pot"> <img align="left" src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" height="50" width="210" alt="h1pot" /></a></p><br><br>

---

## 🗺️ Repository Navigation

| Repository | Focus | Status | Key Technology |
|------------|-------|--------|----------------|
| [solara](https://github.com/DynMEP/solara) | Solar+Storage Optimization | ✅ Active | Python/PySAM/Plotly |
| [YOLOplan](https://github.com/DynMEP/YOLOplan) | AI Symbol Detection | ✅ Active | YOLO/Computer Vision |
| [GreenPowerHub](https://github.com/DynMEP/GreenPowerHub) | Renewable Energy | ✅ Active | MATLAB/Python |
| [vfd-motor-simulation](https://github.com/DynMEP/vfd-motor-simulation) | VFD Motor Analysis | ✅ Active | Python/NumPy/SciPy |
| [dynamic-microgrid-resilience](https://github.com/DynMEP/dynamic-microgrid-resilience) | Microgrid AI Control | ✅ Active | PyTorch/Deep RL |
| [DynMEP](https://github.com/DynMEP/DynMEP) | Revit MEP Automation | ✅ Active | Python/Dynamo |

**New scripts and repositories are added regularly - check back often!**
