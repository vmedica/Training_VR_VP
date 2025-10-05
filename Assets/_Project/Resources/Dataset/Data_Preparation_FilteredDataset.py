
#Esecuzione:
#1. Aprire cmd
#2. Posizionarsi nella cartella in cui si trova Data_Preparation_FilteredDataset.py
#3. Lanciare: python Data_Preparation_FilteredDataset.py

import pandas as pd

# r serve per evitare che Python interpreta \T come una sequenza di escape.
cds = pd.read_csv(r"C:\Training_VR_VP\Assets\_Project\Resources\Dataset\filteredDataset.csv")
#print(fds.head())
#print(ds["WHQ070"].head(5))

pd.set_option('display.max_columns', None)  
#None significa nessun limite sul numero di colonne mostrate.
# Mostra tutte le colonne



#print(cds["RIDAGEYR"].to_string())


#CONVERSIONE DEI DATI IN FORMATO PIU' SEMPLICE DA LEGGERE

cds["DIQ010"] = cds["DIQ010"].map({1:"Si", 2:"No", 3:"Borderline"}).astype(str)  #DIQ010 – Diagnosi di diabete dal medico:
#LBXGLU – Glucosio a digiuno (mg/dL):
#LBXIN – Livello di insulina:
#LBDHDD – Colesterolo HDL ("buono")


cds["WHQ070"] = cds["WHQ070"].map({1:"Yes", 2: "No"}).astype(str)  #WHQ070 – Ha provato a perdere peso nell’ultimo anno:

#Se il valore della colonna è 80, sostituiscilo con la stringa "Dagli 80 in poi" altrimenti lascia il valore che trovi.
cds["RIDAGEYR"] = cds["RIDAGEYR"].map(lambda x: "Dagli 80 in poi" if x == 80 else x).astype(str) #RIDAGEYR – Eta' (anni)


cds["RIAGENDR"] = cds["RIAGENDR"].map({1:"Maschio", 2:"Femmina"}).astype(str) #RIAGENDR – Genere

cds["RIDRETH1"] = cds["RIDRETH1"].map({
    1: "Messicano-Americano",
    2: "Altro ispanico",
    3: "Bianco non ispanico",
    4: "Nero non ispanico",
    5: "Altro/Multirazziale"
}).astype(str)  # Origine etnica

cds["DMDEDUC2"] = cds["DMDEDUC2"].map({
    1: "Meno della terza media",
    2: "Scuola media / superiore senza diploma",
    3: "Diploma superiore o equivalente",
    4: "Universita' (alcuni corsi o laurea breve)",
    5: "Laurea o superiore"
}).astype(str)  # Livello di istruzione (solo adulti 20+)

# I valori 7, 9 e . erano indicati come missing, quindi li gestiamo
cds["DMDEDUC2"] = cds["DMDEDUC2"].replace(["7", "9", "."], pd.NA)
cds["WHQ070"] = cds["WHQ070"].replace(["7", "9", "."], pd.NA)
cds["PAD680"] = cds["PAD680"].replace([7777, 9999, "."], pd.NA)
cds["PAD800"] = cds["PAD800"].replace([7777, 9999, "."], pd.NA)
cds["PAD820"] = cds["PAD820"].replace([7777, 9999, "."], pd.NA)
cds["INDFMPIR"] = cds["INDFMPIR"].replace(["."], pd.NA)

# Attivita' fisica: non categoriali ma gestiamo i missing gia' sopra

# Rapporto reddito/famiglia
# I valori numerici rimangono, ma possiamo sostituire 5 con un’etichetta testuale
cds["INDFMPIR"] = cds["INDFMPIR"].map({5: "maggiore o uguale di 5"}).astype(str)  # Rapporto reddito/famiglia rispetto soglia poverta'



# GESTIONE MISSING / VALORI SPECIALI

cds["DIQ010"] = cds["DIQ010"].replace(["7", "9", "."], pd.NA)
'''
Seleziona la colonna DIQ010 e tramite il metodo replace() sostituisce i valori:
- "7" valore speciale che indica dati mancanti o non applicabili nel dataset NHANES
- "9"  un altro codice per dati mancanti
- "."  spesso usato per rappresentare missing value nei dataset esportati da software statistici
Tutti questi valori vengono sostituiti con pd.NA, che è il tipo di Pandas per i missing values (equivalente a NaN).

'''
# Storia del peso e istruzione
cds["DMDEDUC2"] = cds["DMDEDUC2"].replace([7, 9, "."], pd.NA)
cds["WHQ070"] = cds["WHQ070"].replace([7, 9, "."], pd.NA)

# Attivita' fisica
cds["PAD680"] = cds["PAD680"].replace([7777, 9999, "."], pd.NA)
cds["PAD800"] = cds["PAD800"].replace([7777, 9999, "."], pd.NA)
cds["PAD820"] = cds["PAD820"].replace([7777, 9999, "."], pd.NA)

# Rapporto reddito/famiglia
cds["INDFMPIR"] = cds["INDFMPIR"].replace(["."], pd.NA)

# Esami clinici e misure corporee: valori out-of-range o '.' -> missing
#pd.to_numeric() prova a convertire i valori in numeri (int o float).
#errors="coerce" dice a Pandas: Se un valore non può essere convertito in numero (es. "." o stringhe non numeriche), sostituiscilo con NaN.
for col in ["LBXGLU", "LBXIN", "LBDHDD", "LBXTC", "BMXWT", "BMXHT", "BMXBMI"]:
    cds[col] = pd.to_numeric(cds[col], errors="coerce")  # converte '.' in NaN



# RINOMINA LE COLONNE
cds = cds.rename(columns={

    # Diabete
    "DIQ010": "Diagnosi_diabete_positiva",                # DIQ010 – Diagnosi di diabete

    # Esami clinici
    "LBXGLU": "Glucosio_a_digiuno",             # LBXGLU – Glucosio a digiuno
    "LBXIN": "Livello_di_insulina",             # LBXIN – Livello di insulina
    "LBDHDD": "Colesterolo_HDL",                # LBDHDD – Colesterolo HDL
    "LBXTC": "Colesterolo_totale",              # LBXTC – Colesterolo totale

    # Misure corporee
    "BMXWT": "Peso_kg",                          # BMXWT – Peso (kg)
    "BMXHT": "Altezza_cm",                       # BMXHT – Altezza (cm)
    "BMXBMI": "BMI",                             # BMXBMI – Indice di massa corporea (BMI)


    # Dieta
    "DR1TKCAL": "Calorie_totali_kcal",            # Calorie totali (kcal)
    "DR1TPROT": "Proteine_g",                     # Proteine (g)
    "DR1TCARB": "Carboidrati_g",                  # Carboidrati (g)
    "DR1TSUGR": "Zuccheri_totali_g",              # Zuccheri totali (g)
    "DR1TFIBE": "Fibre_alimentari_g",             # Fibre alimentari (g)
    "DR1TTFAT": "Grassi_totali_g",                # Grassi totali (g)
    "DR1TSFAT": "Grassi_saturi_g",                # Grassi saturi (g)

    # Attivita' fisica
    "PAD680": "Minuti_sedentari_giornalieri",     # Minuti giornalieri sedentari
    "PAD800": "Minuti_attivita_moderata",         # Minuti giornalieri attività moderate
    "PAD820": "Minuti_attivita_vigorosa",         # Minuti attività vigorosa per sessione

    # Storia del peso
    "WHQ070": "Ha_provato_a_perdere_peso",        # Ha provato a perdere peso nell’ultimo anno

    # Demografia
    "RIDAGEYR": "Eta",                            # Età (anni)
    "RIAGENDR": "Genere",                         # Genere
    "RIDRETH1": "Origine_etnica",                 # Origine etnica
    "DMDEDUC2": "Livello_istruzione",             # Livello di istruzione (solo adulti 20+)
    "INDFMPIR": "Rapporto_reddito_famiglia",      # Rapporto reddito/famiglia rispetto alla soglia di povertà
})

print(cds.head(50))

#print(df.read_csv(r"C:\Training_VR_VP\Assets\_Project\Resources\Dataset\filteredDataset.csv"))


#Esportazione del dataset pulito:
cds.to_csv(r"C:\Training_VR_VP\Assets\_Project\Resources\Dataset\Clean_filteredDataset.csv", index=False) 
#Ogni DataFrame ha un indice (numeri da 0 a N-1 per le righe).
# Se non metti index=False, il CSV salverebbe anche questa colonna “extra” con i numeri delle righe.

#NOTE: Quando si esegue non bisogna avere il file Clean_filteredDataset.csv aperto.
