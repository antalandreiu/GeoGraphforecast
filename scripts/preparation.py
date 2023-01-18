
import data_entry as data_e
import model
import numpy as np




PATH_MOVEMENTS = "./../Datasets/toscana_e_prov_movimento_per_tipo_esercizio_annuale.csv"
PATH_ORIGINS = "./../Datasets/Paesi_di_origine_annuale_Toscana.csv.csv"
PATH_RESIDENTS = "./../Datasets/Paesi_di_origine_mensile_italia.csv.csv"

data_e.create_movement_df(PATH_MOVEMENTS, "TU")
#df_origins = data_e.create_movement_df(PATH_ORIGINS, "TU")
#df_residents = data_e.create_movement_df(PATH_RESIDENTS, "TU")

# --------------------------------------------------------
# ML  MODELS

REGIONS = np.array(["TU"])
PROVINCES = np.array(["AR", "FI", "GR", "LI", "LU", "MS", "PI", "PO", "PT", "SI", "TU"], dtype=object)
RESIDENCES = np.array(["EXTR", "IT", "WRLD"])
EXERCISES = np.array(["EXTRHOT", "HOT", "TOT"])

model.create_file_structure(regions=REGIONS, provinces=PROVINCES, exercises=EXERCISES, residences=RESIDENCES)

