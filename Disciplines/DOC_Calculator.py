from gemseo.core.discipline.discipline import Discipline
from Functions.AEA.AEA import AEA
import numpy as np
import pandas as pd
import os
import shutil


class DOC_Calculator(Discipline):

    def __init__(self, name="DOC_Calculator"):
        super().__init__(name)

        # define input grammar
        self.input_grammar.update_from_names(
            [
                "ADP",
                "HTONN",
                "MTOW",
                "PLD",
                "MEW",
                "BENGW",
                "ENPRI",
                "EN",
                "PAXN",
                "CREWC",
                "CREWTECH",
                "BT",
                "BF",
                "SECTOR",
                "IENG",
                "SHP",
                "EOC",
                "AFSPARE",
                "ENSPARE",
                "DYRS",
                "RVAL",
                "RINSH",
                "CRTECHR",
                "CRCABHR",
                "LR",
                "FUELPRI",
                "PERDOC",
                "UTIL",
                "LIFESPAN",
                "TD",
                "TA",
                "L_APP",
                "L_LAT",
                "L_FLYOV",
                "CNOISE",
                "C_NOX",
                "NOX_EM_VALUE",
                "C_CO",
                "CO_EM_VALUE",
                "AEC",
                "PRICO2",
                "CO2",
                "ENERPRI",
                "ENERREQUIREMENT",
                "H2PRI",
                "H2REQUIREMENT",
                "NBAT",
                "NFC",
                "NREPBAT",
                "BATPRICE",
                "RVBAT",
                "LRBAT",
                "TLBAT",
                "FBAT",
                "NREPFC",
                "FCPRICE",
                "RVFC",
                "LRFC",
                "TLFC",
                "FFC",
                "NREPPE",
                "PEPRICE",
                "RVPE",
                "LRPE",
                "TLPE",
                "FPE",
                "NEM",
                "EMPRICE",
                "LREM",
                "SPEML",
                "SPEMB",
                "TLEML",
                "TLEMB",
                "FEML",
                "FEMB",
            ]
        )

        # define output grammar
        self.output_grammar.update_from_names(["DOC", "TOC"])

        # define default data
        self.default_input_data = {
            "ADP": np.array([0.0]),
            "HTONN": np.array([0.0]),
            "MTOW": np.array([0.0]),
            "PLD": np.array([0.0]),
            "MEW": np.array([0.0]),
            "BENGW": np.array([0.0]),
            "ENPRI": np.array([0.0]),
            "EN": np.array([0.0]),
            "PAXN": np.array([0.0]),
            "CREWC": np.array([0.0]),
            "CREWTECH": np.array([0.0]),
            "BT": np.array([1.0]),
            "BF": np.array([0.0]),
            "SECTOR": np.array([0.0]),
            "IENG": np.array([1.0]),
            "SHP": np.array([0.0]),
            "EOC": np.array([0.0]),
            "AFSPARE": np.array([0.0]),
            "ENSPARE": np.array([0.0]),
            "DYRS": np.array([1.0]),
            "RVAL": np.array([0.0]),
            "RINSH": np.array([0.0]),
            "CRTECHR": np.array([0.0]),
            "CRCABHR": np.array([0.0]),
            "LR": np.array([0.0]),
            "FUELPRI": np.array([0.0]),
            "PERDOC": np.array([0.0]),
            "UTIL": np.array([1.0]),
            "LIFESPAN": np.array([1.0]),
            "TD": np.array([0.0]),
            "TA": np.array([0.0]),
            "L_APP": np.array([0.0]),
            "L_LAT": np.array([0.0]),
            "L_FLYOV": np.array([0.0]),
            "CNOISE": np.array([0.0]),
            "C_NOX": np.array([0.0]),
            "NOX_EM_VALUE": np.array([0.0]),
            "C_CO": np.array([0.0]),
            "CO_EM_VALUE": np.array([0.0]),
            "AEC": np.array([0.0]),
            "PRICO2": np.array([0.0]),
            "CO2": np.array([0.0]),
            "ENERPRI": np.array([0.0]),
            "ENERREQUIREMENT": np.array([0.0]),
            "H2PRI": np.array([0.0]),
            "H2REQUIREMENT": np.array([0.0]),
            "NBAT": np.array([0.0]),
            "NFC": np.array([0.0]),
            "NREPBAT": np.array([0.0]),
            "BATPRICE": np.array([0.0]),
            "RVBAT": np.array([0.0]),
            "LRBAT": np.array([0.0]),
            "TLBAT": np.array([0.0]),
            "FBAT": np.array([0.0]),
            "NREPFC": np.array([0.0]),
            "FCPRICE": np.array([0.0]),
            "RVFC": np.array([0.0]),
            "LRFC": np.array([0.0]),
            "TLFC": np.array([0.0]),
            "FFC": np.array([0.0]),
            "NREPPE": np.array([0.0]),
            "PEPRICE": np.array([0.0]),
            "RVPE": np.array([0.0]),
            "LRPE": np.array([0.0]),
            "TLPE": np.array([0.0]),
            "FPE": np.array([0.0]),
            "NEM": np.array([0.0]),
            "EMPRICE": np.array([0.0]),
            "LREM": np.array([0.0]),
            "SPEML": np.array([0.0]),
            "SPEMB": np.array([0.0]),
            "TLEML": np.array([0.0]),
            "TLEMB": np.array([0.0]),
            "FEML": np.array([0.0]),
            "FEMB": np.array([0.0]),
        }

    def _run(self, input_data):

        # get all keys
        keys = input_data.keys()

        # create dict object
        value_list = []
        for key in keys:
            value_list.append(input_data[key][0])

        # input file
        input_file = pd.DataFrame({"item": keys, "value": value_list})
        input_file.to_csv("input_DOC.csv", sep=",", index=False)
        shutil.move("input_DOC.csv", "./Functions/AEA/input/input_DOC.csv")

        # run AEA
        aea_class = AEA(filename="input_DOC.csv")
        aea_class.calculate_doc()
        aea_class.calculate_ioc()

        doc_per_flight = aea_class.doc["DOC [USD/trip]"]
        ioc_per_flight = aea_class.ioc["IOC [USD/trip]"]
        toc_per_flight = doc_per_flight + ioc_per_flight

        # delete input file
        if os.path.exists("./Functions1/AEA/input/input_DOC.csv"):
            os.remove("./Functions1/AEA/input/input_DOC.csv")

        # write output
        return {"DOC": np.array([doc_per_flight]), "TOC": np.array([toc_per_flight])}
