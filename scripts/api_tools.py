import numpy as np

TUSCANY_PROV = np.array([{"Pistoia": "PT"}, {"Firenze": "FI"}, {"Prato": "PO"},
                        {"Livorno": "LI"}, {"Pisa": "PI"}, {"Arezzo": "AR"}, {"Tuscany": "TU"},
                        {"Massa-Carrara": "MS"}, {"Lucca": "LU"}, {"Siena": "SI"}, {"Grosseto": "GR"}], dtype=object)

TUSCANY_EXERCISES = np.array([{"Hotels": "HOT"},
                             {"All Non-Hotel Category": "EXTRHOT"},
                             {"All": "TOT"}], dtype=object)

TURIST_RESIDENCE = np.array([{"Italy": "IT"}, {"World": "WRLD"}, {"International": "EXTR"}], dtype=object)




def get_key(val, my_list) -> str :
    """ Returns the key of a dictionary given the corrisponding value
    :param val value to use for the search of the corrisponding key
    :param my_dict used dictionary
    :return the finded key """
    for my_dict in my_list:
        print(my_list, type(my_dict))
        for key, value in my_dict.items():
            if val == value:
                return str(key)
