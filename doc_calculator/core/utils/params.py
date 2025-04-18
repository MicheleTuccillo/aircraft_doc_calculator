from dataclasses import dataclass

@dataclass
class Params():
    """
    ### Description
    The dataclass stores the main unit rates and constants necessary to conduct
    a cost analysis
    
    - AEC: Portion of free allocated certificate for CO2 emissions.
    - ENR: Enroute navigation charges unit rate.
    - LANDINGUR: Landing charge unit rate.
    - HTONN: Coefficient of cost of handling per tonn of payload
    """

    AEC: float = 0.15
    ENR: float = 68.5
    LANDINGUR: float = 10.0
    HTONN: float = 45.0

default_dict = {"ADP": 0.0,
        "MTOW": 0.0,
        "PLD": 0.,
        "MEW": 0.0,
        "BENGW": 0.0,
        "ENPRI": 0.0,
        "EN": 0.0,
        "CREWTECH": 0.0,
        "CREWC": 0.0,
        "BT": 1.0,
        "BF": 0.0,
        "SECTOR": 0.0,
        "IENG": 1.0,
        "SHP": 0.0,
        "AFSPARE": 0.0,
        "ENSPARE": 0.0,
        "DYRS": 1.0,
        "RVAL": 0.0,
        "RINSH": 0.0,
        "CRTECHR": 0.0,
        "CRCABHR": 0.0,
        "LABOR_RATE": 0.0,
        "FUELPRI": 0.0,
        "IOC_FACT": 0.0,
        "UTIL": 1.0,
        "LIFESPAN": 1.0,
        "TD": 0.0,
        "TA": 0.0,
        "L_APP": 0.0,
        "L_LAT": 0.0,
        "L_FLYOV": 0.0,
        "CNOISE": 0.0,
        "CNOX": 0.0,
        "NOX_VALUE":0.0,
        "CCO": 0.0,
        "CO_VALUE": 0.0,
        "PRICO2": 0.0,
        "CO2_VALUE": 0.0, 
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