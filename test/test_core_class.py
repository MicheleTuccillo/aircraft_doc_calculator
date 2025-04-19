import os
import sys
sys.path.append(os.getcwd())
from doc_calculator.core.DOC_Calculator import DOC
from doc_calculator.core.utils.params import Params 

def main() -> None:

    # Data for regional turboprop
    atr_72 = {
        "ADP": 22.0,
        "MTOW": 23.0,
        "PLD": 7.25,
        "MEW": 13.20,
        "BENGW": 0.775,
        "ENPRI": 1.305,
        "EN": 2.0,
        "CREWTECH": 2.0,
        "CREWC": 3.0,
        "BT": 1.05,
        "BF": 1140.0,
        "SECTOR": 200.0,
        "IENG": 1,
        "SHP": 2475.0,
        "AFSPARE": 0.1,
        "ENSPARE": 0.3,
        "DYRS": 20.0,
        "RVAL": 0.1,
        "RINSH": 0.01,
        "CRTECHR": 70.85,
        "CRCABHR": 63.15,
        "LABOR_RATE": 84.5,
        "FUELPRI": 2.045,
        "IOC_FACT": 0.65,
        "UTIL": 2100.0,
        "LIFESPAN": 20.0,
        "L_APP": 0.0,
        "L_LAT": 0.0,
        "L_FLYOV": 0.0,
        "CNOX": 3.7,
        "NOX_VALUE":0.0,
        "CCO": 3.7,
        "CO_VALUE": 0.0,
        "PRICO2": 0.0215,
        "CO2_VALUE": 1875.0, 
    }

    # assign Coefficient of cost of handling per tonn
    parameters = Params()
    parameters.HTONN = 45.0

    # create an instance of the DOC calculator
    doc_calc_object = DOC(atr_72, params=parameters)

    # calculate operating costs
    doc_dict = doc_calc_object.calculate_doc()
    ioc_dict = doc_calc_object.calculate_ioc()


    # display 
    for key, value in doc_dict.items():
        print(f"{key}\t{value:.3f}")

    return None


if __name__ == "__main__":
    main()