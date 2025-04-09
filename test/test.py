from Disciplines.DOC_Calculator import DOC_Calculator
import numpy as np

doc_calc = DOC_Calculator()


input_dict = {
    "ADP": np.array([5.55]),
    "MTOW": np.array([5.67]),
    "PLD": np.array([1.529]),
    "MEW": np.array([3.274]),
    "BENGW": np.array([0.143]),
    "ENPRI": np.array([0.485]),
    "EN": np.array([2.0]),
    "PAXN": np.array([16.0]),
    "CREWTECH": np.array([2.0]),
    "BT": np.array([1.125]),
    "BF": np.array([372.06]),
    "SECTOR": np.array([140.0]),
    "IENG": np.array([1.0]),
    "AFSPARE": np.array([0.3]),
    "ENSPARE": np.array([0.1]),
    "DYRS": np.array([21.0]),
    "RVAL": np.array([0.1]),
    "RINSH": np.array([0.0135]),
    "CRTECHR": np.array([70.88]),
    "LR": np.array([102.8]),
    "FUELPRI": np.array([1.827]),
    "UTIL": np.array([1275.49]),
    "LIFESPAN": np.array([21.0]),
    "SHP": np.array([680.0]),
}


out = doc_calc.execute(input_data=input_dict)

print(f"DOC = {out["DOC"][0]}")