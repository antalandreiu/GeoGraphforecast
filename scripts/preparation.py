from scripts import data_entry as data_e, model
import numpy as np


PATH_MOVEMENTS = "../data/TU/datasets/toscana_e_prov_movimento_per_tipo_esercizio_annuale.csv"
PATH_ORIGINS = "../data/TU/datasets/toscana_e_prov_paese_di_origine.csv"
PATH_RESIDENTS = "../data/TU/datasets/italia_residenti_per_regione_di_origine_annuale.csv"

df_movements = data_e.create_movement_df(PATH_MOVEMENTS, "TU")
df_origins = data_e.create_movement_df(PATH_ORIGINS, "TU")
df_residents = data_e.create_movement_df(PATH_RESIDENTS, "TU")

df_movements.to_csv("./../data/TU/dataframes/tuscany_turism.csv", index=False)
df_origins.to_csv("./../data/TU/dataframes/tuscany_origins.csv", index=False)
df_residents.to_csv("./../data/TU/dataframes/tuscany_residents.csv", index=False)

# --------------------------------------------------------
# ML  MODELS

REGIONS = np.array(["TU"])
PROVINCES = np.array(["AR", "FI", "GR", "LI", "LU", "MS", "PI", "PO", "PT", "SI", "TU"], dtype=object)
RESIDENCES = np.array(["EXTR", "IT", "WLD"])
EXERCISES = np.array(["EXTRHOT", "HOT", "TOT"])


model.create_file_structure(regions=REGIONS, provinces=PROVINCES, exercises=EXERCISES, residences=RESIDENCES)




