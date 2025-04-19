import os
import sys
sys.path.append(os.getcwd())
from doc_calculator.gemseo_discipline.DOC_Calculator import GemseoDirectOperatingCost
from doc_calculator.core.utils.params import Params
import numpy as np

params = Params()
params.HTONN = 45.0

doc_calc = GemseoDirectOperatingCost(params=params)


atr_72 = {
        "ADP": np.array([22.0]),
        "MTOW": np.array([23.0]),
        "PLD": np.array([7.25]),
        "MEW": np.array([13.20]),
        "BENGW": np.array([0.775]),
        "ENPRI": np.array([1.305]),
        "EN": np.array([2.0]),
        "CREWTECH": np.array([2.0]),
        "CREWC": np.array([3.0]),
        "BT": np.array([1.05]),
        "BF": np.array([1140.0]),
        "SECTOR": np.array([200.0]),
        "IENG": np.array([1.0]),
        "SHP": np.array([2475.0]),
        "AFSPARE": np.array([0.1]),
        "ENSPARE": np.array([0.3]),
        "DYRS": np.array([20.0]),
        "RVAL": np.array([0.1]),
        "RINSH": np.array([0.01]),
        "CRTECHR": np.array([70.85]),
        "CRCABHR": np.array([63.15]),
        "LABOR_RATE": np.array([84.5]),
        "FUELPRI": np.array([2.045]),
        "IOC_FACT": np.array([0.65]),
        "UTIL": np.array([2100.0]),
        "LIFESPAN": np.array([20.0]),
        "PRICO2": np.array([0.0215]),
        "CO2_VALUE": np.array([1875.0]), 
    }

out = doc_calc.execute(input_data=atr_72)

for key, value in out.items():
    print(f"{key}\t{value[0]:.3f}")