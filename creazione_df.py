import pandas as pd
import numpy as np
"""------------------------------------------------------------------------------------------------------------------"""

# Compongo il dataframe finale mettendo insieme i diversi dataset su valori mensili riguardanti i paesi della EU si
# tenga presente che i dati per l'inflazione sono ordinati dai più vecchi ai più recenti mentre quelli sulla moneta
# in circolazione sono ordinati in maniera inversa, si è deciso di seguire il secondo approccio, partendo quindi dal
# dataset sull'aggregato M2 e inserendo partendo dal basso i valori dell'inflazione per i mesi corrispondenti
inflazione = pd.read_csv("inflazione_EU_00-22.csv")

M2 = pd.read_csv("M2_EU_area.csv")

temp = M2.reindex(columns=M2.columns.tolist() + ['Obs_inflazione'])

inverted_index = []
for index, row in inflazione.iloc[::-1].iterrows():
    inverted_index.append(inflazione.index[index])


for i in np.arange(len(temp)):
    temp.loc[i, ['Obs_inflazione']] = inflazione['OBS_VALUE'].iloc[inverted_index[i]]

# Al termine delle operazioni si ottiene il dataframe temp che contiene i valori mensili dell'aggregato M2 e dell'
# inflazione per i diversi mesi a partire da marzo 2022, a questo andranno poi aggiunti i valori della sentiment degli
# articoli usciti nel mese corrispondente
