import streamlit as st
import pandas as pd
from pathlib import Path
import base64

# ===============================
# BASE DO PROJETO (RAIZ)
# ===============================
BASE_DIR = Path(__file__).parent

# ===============================
# FUNÇÕES AUXILIARES
# ===============================
def carregar_dados():
    caminho_excel = BASE_DIR / "HG_ATUALIZADOS.xlsx"
    df = pd.read_excel(caminho_excel)
    df.columns = df.columns.str.strip().str.upper()
    return df

def carregar_logo():
    caminho_logo = BASE_DIR / "allianz_logo.png"
    if caminho_logo.exists():
        return base64.b64encode(caminho_logo.read_bytes()).decode()
    return None

# ===============================
# CONFIGURAÇÃO STREAMLIT
# ===============================
st.set_page_config(
    page_title="Sistema de Consulta Hazard Grade",
    page_icon="🔍",
    layout="centered"
)

# ===============================
# CSS BÁSICO (ESTÁVEL)
# ===============================
st.markdown("""
<style>
.stApp {
    background-color: #0A2D82;
}

h1, label, p {
    color: white !important;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.stTextInput input {
    background-color: white !important;
    color: #0A2D82 !important;
    height: 50px;
    border-radius: 10px;
    font-size: 18px;
}

div.stButton > button {
    height: 50px;
