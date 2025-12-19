import pandas as pd
import streamlit as st

st.title("Sostituzioni Professori")

# upload del file Excel
uploaded_file = st.file_uploader("Carica il file Excel con l'orario", type="xlsx")

if uploaded_file:
    df = pd.read_excel(uploaded_file, index_col=0)
    
    # scelta giorno
    giorno = st.selectbox("Seleziona il giorno", ["Lun","Mar","Mer","Gio","Ven"])
    
    # scelta professore
    prof_assente = st.selectbox("Seleziona il professore assente", df.index)
    
    # bottone per cercare sostituti
    if st.button("Cerca sostituti"):
        rigaprof = df.loc[prof_assente]
        ore_giorno = [str(col).strip() for col in df.columns if str(col).strip().startswith(giorno)]
        altri_prof = df.drop(prof_assente)
        
        risultato = []
        
        for ora in ore_giorno:
            classe = rigaprof[ora]
            if pd.isna(classe) or str(classe).strip() == "":
                continue
            
            riga = f"**Ora {ora} - Classe da sostituire: {classe}**\n"
            
            # cerca compresenza
            compresenza = altri_prof[altri_prof[ora] == classe]
            if not compresenza.empty:
                riga += "Possibile sostituto in compresenza:\n"
                for p in compresenza.index:
                    riga += f"- {p}\n"
                risultato.append(riga)
                continue
            
            # cerca prof liberi
            liberi = altri_prof[altri_prof[ora].isna() | (altri_prof[ora].astype(str).str.strip() == "")]
            if not liberi.empty:
                riga += "Prof libero disponibile:\n"
                for p in liberi.index:
                    riga += f"- {p}\n"
            else:
                riga += "Nessun prof disponibile!\n"
            
            risultato.append(riga)
        
        if risultato:
            st.markdown("\n".join(risultato))
        else:
            st.write("Nessuna sostituzione necessaria per questo giorno.")
