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
pip install doc-calculator
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

Create DirectOperatingCost Object and Run Calculations

```python
doc_calculator = DirectOperatingCost(aircraft=aircraft_data)

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
doc_calculator = DirectOperatingCost(aircraft=aircraft_data, params=parameters)

# GemseoDirectOperatingCost
doc_displine = GemseoDirectOperatingCost(params=parameters)
```

> ⚠️ **Note:** See the `Params` class source code for all available unit rates and economic scenario constants

## 📚 References / Citation

If you use `doc_calculator` for academic or research purposes, please cite:

```latex
@article{MARCIELLO2024118517,
  title   = {Evaluating the economic landscape of hybrid-electric regional aircraft: A cost analysis across three time horizons},
  journal = {Energy Conversion and Management},
  volume  = {312},
  pages   = {118517},
  year    = {2024},
  issn    = {0196-8904},
  doi     = {https://doi.org/10.1016/j.enconman.2024.118517},
  url     = {https://www.sciencedirect.com/science/article/pii/S0196890424004588},
  author  = {Valerio Marciello and Vincenzo Cusati and Fabrizio Nicolosi and Karen Saavedra-Rubio and Eleonore Pierrat and Nils Thonemann and Alexis Laurent},
  keywords = {Direct operating costs, Hybrid electric propulsion, Regional aviation, Technology roadmap, Sustainable aviation},
}

@manual{EUETS,
    title = {EU emissions trading system (EU ETS)},
    key   = {European commission},
    url   = {https://climate.ec.europa.eu/eu-action/eu-emissions-trading-system-eu-ets_en},
    year  = {2023}
}

@book{ATA,
  author    = {Air Transport Association of America},
  year      = {1967},
  title     = {Air Transport Association of America. Standard Method of Estimating Comparative Direct Operating Costs of Turbine Powered Transport Airplanes.},
  publisher = {The Association},
  address   = {},
  edition   = {}
}

@book{association1989short,
  title  = {Short medium range aircraft: AEA requirements},
  author = {Association of European Airlines},
  url    = {https://books.google.it/books?id=6dz0jgEACAAJ},
  year   = {1989}
}
```

## ✉️ Contact

For questions, support, or suggestions, feel free to reach out:

📧 Email: michele.tuccillo98@gmail.com

🐛 Report issues: GitHub Issues
