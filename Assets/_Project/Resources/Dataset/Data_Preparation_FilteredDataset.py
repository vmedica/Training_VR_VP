
#Esecuzione:
#1. Aprire cmd
#2. Lanciare: python C:\Training_VR_VP\Assets\_Project\Resources\Dataset\Data_Preparation_FilteredDataset.py

import pandas as pd

# r serve per evitare che Python interpreta \T come una sequenza di escape.
ds = pd.read_csv(r"C:\Training_VR_VP\Assets\_Project\Resources\Dataset\filteredDataset.csv")
#print(fds.head())
print(ds["WHQ070"].head(5))

ds["WHQ070"] = ds["WHQ070"].map({1:"Yes", 2: "No"}).astype(str)

print(ds["WHQ070"].head(5))
#print(df.read_csv(r"C:\Training_VR_VP\Assets\_Project\Resources\Dataset\filteredDataset.csv"))


#Esportazione del dataset pulito:
#CORREGGI IL PERCORSO ds.to_csv(r"C:\Users\Vincenzo\Progetti\PazientiVirtuali\pazienti_puliti.csv", index=False) 
#Ogni DataFrame ha un indice (numeri da 0 a N-1 per le righe).
# Se non metti index=False, il CSV salverebbe anche questa colonna “extra” con i numeri delle righe.