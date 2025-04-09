import os
import sys
sys.path.append(os.getcwd())
from doc_calculator.core.DOC_Calculator import DOC

def main() -> None:

    # Data for regional turboprop
    input_dict = {
        "ADP": 22.0,
        "HTONN": 45.0,
        "MTOW": 23.0,
        "PLD": 7.25,
        "MEW": 13.20,
        "BENGW": 0.775,
        "ENPRI": 1.305,
        "EN": 2.0,
        "CREWTECH": 2.0,
        "CREWC": 3.0,
        "BT": 1.35,
        "BF": 1140.0,
        "SECTOR": 200.0,
        "IENG": 1,
        "SHP": 2475.0,
        "AFSPARE": 0.3,
        "ENSPARE": 0.1,
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
        "TD": 92.0,
        "TA": 89.0,
        "L_APP": 0.0,
        "L_LAT": 0.0,
        "L_FLYOV": 0.0,
        "CNOISE": 4.15,
        "CNOX": 3.7,
        "NOX_VALUE":0.0,
        "CCO": 3.7,
        "CO_VALUE": 0.0,
        "AEC": 0.15,
        "PRICO2": 0.0215,
        "CO2_VALUE": 1875.0, 
        "ENERPRI": 0.0,
        "ENER_REQ": 0.0,
        "H2_PRI": 0.0,
        "H2_REQ": 0.0,
        "N_BAT": 0.0,
        "N_FC": 0.0,
        "N_REPBAT": 0.0,
        "BATPRICE": 0.0,
        "RVBAT": 0.0,
        "LRBAT": 0.0,
        "TLBAT": 0.0,
        "F_BAT": 0.0,
        "N_REPFC": 0.0,
        "FCPRICE": 0.0,
        "RVFC": 0.0,
        "LRFC": 0.0,
        "TLFC": 0.0,
        "F_FC": 0.0,
        "N_REPPE": 0.0,
        "PEPRICE": 0.0,
        "RVPE": 0.0,
        "LRPE": 0.0,
        "TLPE": 0.0,
        "F_PE": 0.0,
        "N_EM": 0.0,
        "EMPRICE": 0.0,
        "LREM": 0.0,
        "SPEML": 0.0,
        "SPEMB": 0.0,
        "TLEML": 0.0,
        "TLEMB": 0.0,
        "F_EML": 0.0,
        "F_EMB": 0.0
    }

    # create an instance of the DOC calculator
    doc_calc_object = DOC(input_dict)

    # calculate operating costs
    doc_calc_object.calculate_doc()
    doc_calc_object.calculate_ioc()

    # display 
    for key, value in doc_calc_object.doc.items():
        print(f"{key}\t{value:.2f}")

    return None


if __name__ == "__main__":
    main()