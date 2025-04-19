from doc_calculator.core.utils.params import default_dict
import numpy as np

def create_default_gemseo_grammar() -> dict:
    default_grammar_dict = {}

    for key, value in default_dict.items():
        default_grammar_dict[key] = np.array([value])

    return default_grammar_dict
