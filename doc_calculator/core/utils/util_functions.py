from .params import default_dict as dt

def _assign_input(input:dict) -> dict:
    default_dict = {k.lower(): v for k, v in dt.items()} 
    input        = {k.lower(): v for k, v in input.items()} 

    for key, value in default_dict.items():
        if key in input:
            default_dict[key] = input[key]

    return default_dict