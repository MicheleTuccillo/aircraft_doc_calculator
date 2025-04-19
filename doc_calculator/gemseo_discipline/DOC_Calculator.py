from gemseo.core.discipline.discipline import Discipline
from doc_calculator.core.DOC_Calculator import DOC
from doc_calculator.core.utils.params import Params
from doc_calculator.gemseo_discipline.utils.utils_functions import create_default_gemseo_grammar
import numpy as np


class DOC_Calculator(Discipline):

    def __init__(self, name="DOC_Calculator", **kwargs):
        super().__init__(name)

        # define input grammar
        self.input_grammar.update_from_data(create_default_gemseo_grammar())

        # define output grammar
        self.output_grammar.update_from_names(["DOC", "IOC", "TOC"])

        # define default data
        self.default_input_data = create_default_gemseo_grammar()

        # read kwargs params
        if kwargs:
            self._params = kwargs["params"]
        else:
            self._params = Params()

    def _run(self, input_data):

        # create DOC class aircraft dict
        aircraft = {}

        for key, value in input_data.items():
            aircraft[key] = value[0]
        
        # instance of the DOC class
        doc_calc_object = DOC(aircraft, params=self._params)

        # DOC [USD/flight]
        doc_dict = doc_calc_object.calculate_doc()

        # IOC [USD/flight]
        ioc_dict = doc_calc_object.calculate_ioc()

        doc_per_flight = doc_dict["DOC [USD/flight]"]
        ioc_per_flight = ioc_dict["IOC [USD/flight]"]
        toc_per_flight = doc_per_flight + ioc_per_flight

        # write output
        return {
                "DOC": np.array([doc_per_flight]), 
                "IOC": np.array([ioc_per_flight]), 
                "TOC": np.array([toc_per_flight])
                }
