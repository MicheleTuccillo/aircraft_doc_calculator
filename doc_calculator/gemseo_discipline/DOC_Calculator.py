from gemseo.core.discipline.discipline import Discipline
from doc_calculator.core.DOC_Calculator import DOC
from doc_calculator.gemseo_discipline.utils.utils_functions import create_default_gemseo_grammar
import numpy as np


class DOC_Calculator(Discipline):

    def __init__(self, name="DOC_Calculator"):
        super().__init__(name)

        # define input grammar
        self.input_grammar.update_from_data(create_default_gemseo_grammar())

        # define output grammar
        self.output_grammar.update_from_names(["DOC", "IOC", "TOC"])

        # define default data
        self.default_input_data = create_default_gemseo_grammar()

    def _run(self, input_data):

        doc_per_flight = 0.0
        ioc_per_flight = 0.0
        toc_per_flight = doc_per_flight + ioc_per_flight

        # write output
        return {
                "DOC": np.array([doc_per_flight]), 
                "IOC": np.array([ioc_per_flight]), 
                "TOC": np.array([toc_per_flight])
                }
