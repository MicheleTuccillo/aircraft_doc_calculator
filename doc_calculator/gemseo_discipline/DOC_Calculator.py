from gemseo.core.discipline.discipline import Discipline
from ..core.DOC_Calculator import DirectOperatingCost
from ..core.utils.params import Params
from .utils.utils_functions import create_default_gemseo_grammar
import numpy as np


class GemseoDirectOperatingCost(Discipline):

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
        doc_calc_object = DirectOperatingCost(aircraft, params=self._params)

        # DOC [USD/flight]
        direct_operating_cost = doc_calc_object.calculate_doc()

        # IOC [USD/flight]
        indirect_operating_cost = doc_calc_object.calculate_ioc()

        direct_operating_cost_per_flight   = direct_operating_cost["DOC [USD/flight]"]
        indirect_operating_cost_per_flight = indirect_operating_cost["IOC [USD/flight]"]
        total_operating_cost_per_flight    = direct_operating_cost_per_flight + indirect_operating_cost_per_flight

        # write output
        return {
                "DOC": np.array([direct_operating_cost_per_flight]), 
                "IOC": np.array([indirect_operating_cost_per_flight]), 
                "TOC": np.array([total_operating_cost_per_flight])
                }
