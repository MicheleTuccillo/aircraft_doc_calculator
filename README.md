# ✈️ doc_calculator

`doc_calculator` is a Python package designed to calculate **Direct Operating Costs (DOC)** and **Indirect Operating Costs (IOC)** for **short-haul** and **medium-haul** aircraft. It supports both **regional** and **large transport** categories, and includes modules for **hybrid-electric aircraft** configurations.

## 🚀 Features

- Compute **Direct Operating Costs (DOC)** and **Indirect Operating Costs (IOC)**
- Supports both **conventional** and **hybrid-electric** propulsion systems
- Cost modules for:
  - **Fuel**, **Electricity** and **Hydrogen** consumption
  - Financial costs anlsysis including **Depreciation**, **Interests** and **Insurance**
  - Charges and Fees:
    - Landing
    - Payload Handling
    - Navigation
    - Noise Emissions
    - CO Emissions
    - NOx Emissions
    - CO2 Emissions (EU ETS)
  - Maintenance costs for:
    - Airframe
    - Turboprop Engines
    - Propulsive Batteries
    - Fuel Cells
    - Electric Machines
    - Power Electronics
  - Crew Handling costs:
    - Pilots costs
    - Cabin Crew costs  

- The package includes a ready-to-use **GEMSEO discipline** to allow integration with multidisciplinary design analysis (MDA) and optimization (MDO) workflows based on the GEMSEO framework.

## 🛠️ Installation

Install the package using `pip`:

```bash
pip install doc_calculator
```
## 📦 Usage

Import the `DirectOperatingCost` class

```python
from from doc_calculator import DirectOperatingCost
```

Prepare Aircraft Input Dictionary

```python
aircraft_data = {
    "adp": 22.0, # aircraft delivery price (M. USD)
    "mtow": 23.0, # aircraft MTOM in kg
    "bt": 1.5,  # mission block time (including taxi) in hours
    "co2_value": 500,  # CO2 emissions per flight in kg
    "prico2": 0.03,  # CO2 cost per kg in USD
    "ioc_fact": 0.15,  # IOC factor (fraction)
    # ... add all other required aircraft parameters
    }
```
> ⚠️ **Note:** See the source code or documentation for the full list of required aircraft parameters.

Create DOC Object and Run Calculations

```python
doc_calculator = DOC(aircraft=aircraft_data)

# Calculate DOC
doc_result = doc_calculator.calculate_doc()
for key, value in doc_result.items():
  print(f"{key}:\t{value}")

# Calculate IOC
ioc_result = doc_calculator.calculate_ioc()
for key, value in ioc_result.items():
  print(f"{key}:\t{value}")
```

## 📚 References / Citation

If you use `doc_calculator` for academic or research purposes, please cite:

```latex
@software{doc_calculator,
  author       = {Your Name and Contributors},
  title        = {doc_calculator: A Python tool for aircraft direct and indirect operating cost modeling},
  year         = {2025},
  publisher    = {GitHub},
  journal      = {GitHub Repository},
  howpublished = {\url{https://github.com/yourusername/doc_calculator}},
  version      = {v1.0}
}
```

## ✉️ Contact

For questions, support, or suggestions, feel free to reach out:

📧 Email: michele.tuccillo98@gmail.com

🐛 Report issues: GitHub Issues
