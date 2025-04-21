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
from doc_calculator import DirectOperatingCost
```

Prepare Aircraft Input Dictionary

```python
aircraft_data = {
    "adp": 85,            # Aircraft Delivery Price (USD M)
    "mtow": 70,           # Max Take-off Weight (Tonnes)
    "pld": 18,            # Payload (Tonnes)
    "mew": 40,            # Manufacturer Empty Weight (Tonnes)
    "bengw": 1.2,         # Bare engine weight (Tonnes)
    "enpri": 6.5,         # Engine Price (USD M)
    "en": 2,              # Number of engines
    "crewtech": 2,
    "crewc": 4,
    "bt": 1.5,            # Sector Block Time (Hours)
    "bf": 2500,           # Sector Block Fuel (KG)
    "sector": 600,        # Sector length (NM)
    "ieng": 1,
    "shp": 25000,         # Shaft Horse Power (for ieng = 1)
    "eoc": 0.0,           # (Only used if ieng = 2)
    "afspare": 0.1,
    "enspare": 0.3,
    "dyrs": 15,
    "rval": 0.15,
    "rinsh": 0.005,
    "crtechr": 200,
    "crcabhr": 50,
    "labor_rate": 90,
    "fuelpri": 1.8,
    "ioc_fact": 0.65,
    "util": 2800,
    "lifespan": 20,
    "l_app": 95.0,
    "l_lat": 94.0,
    "l_flyov": 96.0,
    "cnox": 5,
    "nox_value": 200,
    "cco": 4,
    "co_value": 150,
    "co2_value": 10000,
    "prico2": 0.02,
}
```
> ⚠️ **Note:** Many parameters are optional depending on configuration. Refer to the full list of accepted keys in the docstring of the `__init__` method for more customization.

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
---

To use the GEMSEO discipline, import the `GemseoDirectOperatingCost` class

```python
from doc_calculator import GemseoDirectOperatingCost
import numpy as np
```

Prepare Aircraft Input Dictionary. Make sure to use Numpy arrays.

```python
aircraft_data = {
    "adp": np.array([85]),            # Aircraft Delivery Price (USD M)
    "mtow": np.array([70]),           # Max Take-off Weight (Tonnes)
    "pld": np.array([18]),            # Payload (Tonnes)
    "mew": np.array([40]),            # Manufacturer Empty Weight (Tonnes)
    "bengw": np.array([1.2]),         # Bare engine weight (Tonnes)
    "enpri": np.array([6.5]),         # Engine Price (USD M)
    "en": np.array([2]),              # Number of engines
    "crewtech": np.array([2]),
    "crewc": np.array([4]),
    "bt": np.array([1.5]),            # Sector Block Time (Hours)
    "bf": np.array([2500]),           # Sector Block Fuel (KG)
    "sector": np.array([600]),        # Sector length (NM)

    # add all other required keys
}
```

Create the disciplne and Run Calculations

```python
doc_displine = GemseoDirectOperatingCost()

out = doc_displine.execute(input_data=aircraft_data)
```


---

To fully customize the analysis of aircraft operating costs the `Params` dataclass helps you modify typical unit rates, depending on the economic scenario

Import the class

```python
from doc_calculator.core.utils.params import Params
```

Modify economic assumptions and pass the object through the `params` keyword

```python
parameters = Params()
parameters.ENR = 85.0   # Unit Rate for the En-route Navigation Charge

# DirectOperatingCost
doc_calculator = DOC(aircraft=aircraft_data, params=parameters)

# GemseoDirectOperatingCost
doc_displine = GemseoDirectOperatingCost(params=parameters)
```

> ⚠️ **Note:** See the `Params` class source code for all available unit rates and economic scenario constants

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
