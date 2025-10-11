# 👷‍♂️ DynMEP

Welcome to **DynMEP**! I'm Alfonso Davila, an electrical engineer and automation enthusiast with 20+ years of experience in power systems and multidisciplinary project leadership. My mission is to revolutionize MEP and BIM workflows through innovative automation tools, computational methods, and renewable energy solutions. From Revit MEP scripts to AI-powered symbol detection and advanced mathematical research, these projects save time, enhance accuracy, and drive sustainability. All repositories are hosted at [github.com/DynMEP](https://github.com/DynMEP) under the MIT License.

---

## 🌟 About Me

With 20+ years in electrical engineering specializing in power distribution, MEP design, and sustainable energy systems, I develop cutting-edge tools across multiple domains:

- **Revit MEP Automation**: NEC-compliant Dynamo scripts saving 5–15 hours per project
- **Computer Vision**: YOLO-based AI for automated technical drawing analysis
- **Renewable Energy**: MATLAB simulations for hybrid solar/wind integration
- **Motor Control Systems**: VFD simulation and analysis for industrial applications
- **Computational Mathematics**: Advanced algorithms for additive combinatorics research
- **Professional Focus**: Power systems, BIM workflows, and green energy solutions

---

## 📂 Public Repositories

### 1. **DynMEP** - Revit MEP Automation Suite 🔧
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

### 5. **ZeroSumFreeSets-Z4** - Computational Mathematics 🔬
**Repository**: [github.com/DynMEP/ZeroSumFreeSets-Z4](https://github.com/DynMEP/ZeroSumFreeSets-Z4)

An advanced computational mathematics project providing explicit constructions of maximal 3-zero-sum-free subsets in (ℤ/4ℤ)ⁿ. This addresses an open problem in additive combinatorics posed by Nathan Kaplan in the 2014 CANT problem session.

**Mathematical Problem**:
Find the largest subset H ⊆ (ℤ/4ℤ)ⁿ such that there are no distinct x, y, z ∈ H with x + y + z ≡ 0 (mod 4) (pointwise vector addition).

**Breakthrough Results**:
- **Proven Optimal Density**: 0.5 for all n
- **Universal Construction**: First coordinate odd (1 or 3 mod 4)
- **Explicit Sizes**: 
  - n=5: 512 vectors (50% of 1024)
  - n=6: 2048 vectors (50% of 4096)
  - n=7: 8192 vectors (50% of 16384)

**Methodology**:
AI-assisted hybrid greedy-genetic algorithm refined with Grok (xAI), inspired by combinatorial searches like FunSearch.

**Algorithm Evolution**:
1. **Baseline** (`baseline_script.py`): Initial greedy approach (176 for n=5)
2. **Refined** (`refined_script.py`): Enhanced with probes (512 for n=5)
3. **Omni-Optimized v5.0.0** (`omni_optimized_hybrid_discovery_v5.py`):
   - Universal optimal construction
   - Stratified sampling and adaptive mutations
   - GPU acceleration with batching (n=8+)
   - Early stopping and profile chaining

**Features**:
- Exhaustive verification of 3-zero-sum-free property
- JSON export of full subsets with metadata
- GPU support for large-scale computation
- Comprehensive documentation and references

**Installation**:
```bash
git clone https://github.com/DynMEP/ZeroSumFreeSets-Z4.git
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
python3 omni_optimized_hybrid_discovery_v5.py --n 6 7 --mod 4 --profile all
```

**Academic References**:
- Y. Caro, A weighted Erdős–Ginzburg–Ziv theorem, J. Combin. Theory Ser. A (1997)
- W.D. Gao and A. Geroldinger, Zero-sum problems survey, Expo. Math. (2006)
- S.J. Miller et al., CANT Problem Sessions (2017)
- MathOverflow discussion thread available

**Release**: v5.0.0 (August 28, 2025) - Universal construction with GPU support

---

## 🔧 Installation & Usage

### General Prerequisites
- **Revit Scripts**: Autodesk Revit 2025, Dynamo 2.17+, Python (IronPython 2.7 or CPython 3)
- **YOLOplan**: Python 3.8+, Ultralytics YOLO, OpenCV
- **GreenPowerHub**: MATLAB (base version) or Python 3.x
- **vfd-motor-simulation**: Python 3.x, NumPy, SciPy, Matplotlib
- **ZeroSumFreeSets**: Python 3.8+, optional PyTorch for GPU

### Quick Start - DynMEP Scripts
```bash
git clone https://github.com/DynMEP/DynMEP.git
```
1. Open Revit 2025 and load your MEP project
2. Launch Dynamo and create a new workspace
3. Add a Python Script node and paste the desired script
4. Connect appropriate inputs (see individual script documentation)
5. Run and check Desktop outputs (CSV, logs)

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

### Quick Start - ZeroSumFreeSets
```bash
git clone https://github.com/DynMEP/ZeroSumFreeSets-Z4.git
python3 omni_optimized_hybrid_discovery_v5.py --n 6 --runs 20
```

---

## 🎯 Combined Benefits

**Time Savings Across Projects**:
- **Revit MEP Scripts**: 5–15 hours per project
- **YOLOplan**: Automated symbol counting (hours to minutes)
- **GreenPowerHub**: 5–10 hours per renewable energy analysis
- **vfd-motor-simulation**: Instant VFD analysis vs. manual calculations (hours saved)
- **ZeroSumFreeSets**: Breakthrough mathematical research results

**Professional Value**:
- **NEC Compliance**: All electrical scripts meet NEC 2023 standards
- **Accuracy**: Reduce errors through automation
- **Innovation**: Cutting-edge AI and mathematical methods
- **Sustainability**: Support renewable energy adoption
- **Open Source**: MIT License for maximum collaboration

**Industry Impact**:
- MEP engineering automation
- BIM coordination excellence
- Renewable energy integration
- Motor control and VFD system design
- Academic research advancement
- Construction estimation efficiency

---

## 📜 License

All repositories are licensed under the MIT License. See individual repository LICENSE files for details.

---

## 🤝 Collaboration & Support

**Contribute**: Fork any repository, submit pull requests, or open issues to enhance these tools.

**Custom Development**: Need specialized automation, AI models, or renewable energy simulations? Contact me for consulting and custom solutions.

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
- **Multiple Domains**: MEP automation, AI/ML, renewable energy, mathematics
- **Open Source**: All tools freely available under MIT License
- **Innovation**: Combining traditional engineering with cutting-edge technology
- **Impact**: Serving MEP firms, engineers, and researchers globally
- **Validated**: IEEE standards compliance and field-tested results

---

> _"Let's build smarter MEP workflows, advance renewable energy, and push the boundaries of computational research together! 🚧🌿🔬"_

---

<p><a href="https://www.buymeacoffee.com/h1pot"> <img align="left" src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" height="50" width="210" alt="h1pot" /></a></p><br><br>

---

## 🗺️ Repository Navigation

| Repository | Focus | Status | Key Technology |
|------------|-------|--------|----------------|
| [DynMEP](https://github.com/DynMEP/DynMEP) | Revit MEP Automation | ✅ Active | Python/Dynamo |
| [YOLOplan](https://github.com/DynMEP/YOLOplan) | AI Symbol Detection | ✅ Active | YOLO/Computer Vision |
| [GreenPowerHub](https://github.com/DynMEP/GreenPowerHub) | Renewable Energy | ✅ Active | MATLAB/Python |
| [vfd-motor-simulation](https://github.com/DynMEP/vfd-motor-simulation) | VFD Motor Analysis | ✅ Active | Python/NumPy/SciPy |
| [ZeroSumFreeSets-Z4](https://github.com/DynMEP/ZeroSumFreeSets-Z4) | Computational Math | ✅ Active | Python/GPU Computing |

**New scripts and repositories are added regularly - check back often!**
