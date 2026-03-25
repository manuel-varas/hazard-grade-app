import streamlit as st
import pandas as pd

st.set_page_config(page_title="Hazard Grade - Allianz", page_icon="🛡️")

@st.cache_data
def load_data():
    try:
        # Lê a planilha
        df = pd.read_excel("HG_ATUALIZADOS.xlsx")
        
        # ESSA LINHA É A CHAVE: Remove espaços invisíveis dos nomes das colunas
        df.columns = df.columns.astype(str).str.strip().str.upper()
        
        # Remove espaços de dentro das células da coluna ATIVIDADE
        if 'ATIVIDADE' in df.columns:
            df['ATIVIDADE'] = df['ATIVIDADE'].astype(str).str.strip().str.upper()
            
        return df
    except Exception as e:
        st.error(f"Erro ao carregar planilha: {e}")
        return None

df = load_data()

if df is not None:
    st.image("allianz_logo.png", width=200)
    st.title("Pesquisa de Hazard Grade")

    # Campo de busca
    busca = st.text_input("Digite a ATIVIDADE:").strip().upper()

    if busca:
        if 'ATIVIDADE' in df.columns:
            # Busca por "contém", assim se você digitar só parte da palavra ele acha
            resultado = df[df['ATIVIDADE'].str.contains(busca, na=False)]

            if not resultado.empty:
                for i in range(len(resultado)):
                    ativ = resultado.iloc[i]['ATIVIDADE']
                    hazard = resultado.iloc[i]['HAZARD']
                    st.success(f"**Atividade:** {ativ}")
                    st.metric(label="HAZARD GRADE", value=str(hazard))
                    st.divider()
            else:
                st.error(f"Nenhuma atividade encontrada para: {busca}")
        else:
            st.warning(f"Coluna 'ATIVIDADE' não encontrada. Colunas detectadas: {list(df.columns)}")

st.caption("v1.2 - Sistema Atualizado")
