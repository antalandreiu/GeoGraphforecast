import pandas as pd
import numpy as np
from pathlib import Path
import os

# NOTA
# I varii PATH ed i dizionari di encoding verranno definiti all'interno
# di un file Json di configurazione all'interno della cartella config

# PATH del file contenente i dati grezzi
#PATH = "data/TU/datasets/toscana_e_prov_movimento_per_tipo_esercizio_annuale.csv"

# Encoding
TUSCANY_PROV_IT = np.array([{"Pistoia": "PT"}, {"Firenze": "FI"}, {"Prato": "PO"},
                            {"Livorno": "LI"}, {"Pisa": "PI"}, {"Arezzo": "AR"}, {"Toscana": "TU"},
                            {"Massa-Carrara": "MS"}, {"Lucca": "LU"}, {"Siena": "SI"}, {"Grosseto": "GR"}], dtype=object)

TUSCANY_EXERCISES_IT = np.array([{"esercizi alberghieri": "HOT"},
                                 {"alberghi di 5 stelle, 5 stelle lusso e 4 stelle ": "HOT5"},
                                 {"alberghi di 3 stelle e residenze turistico alberghiere": "HOT3"},
                                 {"alberghi di 2 stelle e alberghi di 1 stella": "HOT2"},
                                 {"esercizi extra-alberghieri": "EXTRHOT"},
                                 {"alloggi in affitto gestiti in forma imprenditoriale": "STD"},
                                 {"agriturismi": "AGR"}, {"altri esercizi ricettivi": "OTHR"},
                                 {"totale esercizi ricettivi": "TOT"}, {'bed and breakfast': "BB"},
                                 {'campeggi e villaggi turistici': "CAMP"}], dtype=object)

TURIST_RESIDENCE_IT = np.array([{"Italia": "IT"}, {"Mondo": "WRLD"}, {"Paesi esteri": "EXTR"}], dtype=object)

# Creazione file structure
OUT_DIRECTORY = Path("./data/TU/dataframes")
OUT_NAME = "tuscany_turism.csv"





def process_nan_rows(df: pd.DataFrame, column: str, target_col: str):
    """ Check for Nan values in a target-column correlated to a Series containing
    unique categorical values. If the Nan count in higher than 40% of data warns the user.

    :param df Dataframe
    :param column containing categorical value
    :param target_col column used to check for nan values
    :return Dataframe with nan values filled with 0"""


    tmp_df = df[[column, target_col]]
    unique_vals = tmp_df[column].unique()

    for val in unique_vals:
        sub_df = tmp_df.loc[tmp_df[column] == val]
        nan_vals = sub_df.isna().sum()
        nan_ratio = round((nan_vals.loc[target_col] / sub_df.size) * 100, 2)

        if (nan_vals.loc[target_col] / sub_df.size) * 100 > 40:
            #tmp_df = tmp_df.loc[tmp_df[column] != val]
            print(f"!!WARNING {nan_ratio}% missing values in: ", val)
            pass
        else:
            print(f"OK, {nan_ratio}% missing values in: ", val)
            pass
    print("\n\n")
    df.fillna(0, inplace=True)


def _replace_values(df: pd.DataFrame, encoding_list: np.array, label: str) -> pd.DataFrame:
    """Replace all value occurencies with another mapped value
    :param df  dataframe to use
    :param encoding_list list containing key-value pairs where the dict-key is the current cell value and the dict-value is the new one
    :param label
    :return df with replaced values"""
    for dictionary in encoding_list:
        for (key, value) in dictionary.items():
            df[label] = df[label].str.replace(key, value)
    return df


def encode_columns(Dataframe: pd.DataFrame) -> pd.DataFrame:
    """ Encode All the categorical values of the 'Territory', 'Type of exercise' & 'Country of residence' Series
    :param Dataframe
    :return encoded new Dataframe """

    tmp_df = Dataframe
    _replace_values(tmp_df, TUSCANY_PROV_IT, "Territorio")
    _replace_values(tmp_df, TUSCANY_EXERCISES_IT, "Tipologia di esercizio")
    _replace_values(tmp_df, TURIST_RESIDENCE_IT, "Paese di residenza dei clienti")

    #print(f"territorio: {tmp_df['Territorio'].unique()}\n\n ", f"esercizio: {tmp_df['Tipologia di esercizio'].unique()}\n\n", f"residenza: {tmp_df['Paese di residenza dei clienti'].unique()}\n\n")
    return tmp_df

def create_movement_df(PATH:str, region_code:str):
    """ Creates new dataframe with the decided standard structure
    :param df base dataframe
    :return new dataframe"""

    tmp_df = pd.read_csv(PATH).sort_values(by=["Territorio", "Tipologia di esercizio","Paese di residenza dei clienti", "TIME","Indicatori"])
    tmp_df = encode_columns(tmp_df)
    tmp_df.drop(labels=["ITTER107", "TIPO_DATO7", "CORREZ",
                        "Correzione", "TIPO_ALLOGGIO2", "ATECO_2007",
                        "Ateco 2007", "ISO", "Seleziona periodo",
                        "Flag Codes", "Flags"], axis=1, inplace=True)


    process_nan_rows(tmp_df, "Tipologia di esercizio", "Value")

    arrivals = tmp_df.loc[tmp_df["Indicatori"] == "arrivi "]
    presences = tmp_df.loc[tmp_df["Indicatori"] == "presenze"]

    #assert "presenze" not in (arrivals["Indicatori"].unique())
    #assert "arrivi " not in (presences["Indicatori"].unique())
    #assert arrivals.shape == presences.shape
    #discard = ["Value", "Indicatori"]
    #row_numb = presences.shape[0]
    #assert [arrivals.drop(discard, axis=1).iloc[i].equals(presences.drop(discard, axis=1).iloc[i]) for i in range(row_numb)]

    cod_reg_tu = np.full_like(arrivals["Value"], region_code, dtype=object)
    df = pd.DataFrame(data={"region": cod_reg_tu,
                            "province": arrivals.Territorio.to_numpy(),
                            "countryOfResidence": arrivals["Paese di residenza dei clienti"].to_numpy(),
                            "typeOfExercise": arrivals["Tipologia di esercizio"].to_numpy(),
                            "period": arrivals.TIME.to_numpy(),
                            "arrivals": arrivals["Value"].to_numpy(),
                            "presences": presences["Value"].to_numpy()}).sort_values(["region", "province", "countryOfResidence", "typeOfExercise","period", "arrivals", "presences"])
    try:
        df.to_csv(f"{OUT_DIRECTORY}/{OUT_NAME}", index=False)
    except OSError:
        OUT_DIRECTORY.mkdir(parents=True, exist_ok=True)
        df.to_csv(f"{OUT_DIRECTORY}/{OUT_NAME}", index=False)

