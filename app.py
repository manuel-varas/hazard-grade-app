import streamlit as st
import pandas as pd
from pathlib import Path

# ===============================
# BASE DO PROJETO (RAIZ DO REPO)
# ===============================
BASE_DIR = Path(__file__).parent
EXCEL_PATH = BASE_DIR / "HG_ATUALIZADOS.xlsx"
LOGO_PATH = BASE_DIR / "allianz_logo.png"

# ===============================
# CONFIGURAÇÃO
# ===============================
st.set_page_config(
    page_title="Sistema de Consulta Hazard Grade",
    page_icon="🔍",
    layout="centered"
)

# ===============================
# CSS (✅ TRIPLE QUOTES FECHADAS)
# ===============================
st.markdown(
    """
    <style>
    .stApp { background-color: #0A2D82; }

    h1, label, p {
        color: white !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    .stTextInput input {
        background-color: white !important;
        color: #0A2D82 !important;
        height: 50px;
        border-radius: 12px;
        font-size: 18px;
        border: none !important;
    }

    div.stButton > button {
        height: 50px;
        border-radius: 12px;
        font-weight: bold;
        border: 2px solid white;
        background: transparent;
        color: white;
        transition: 0.2s;
    }

    div.stButton > button:hover {
        background: white;
        color: #0A2D82;
    }

    .result-card {
        background-color: white;
        padding: 25px;
        border-radius: 15px;
        margin-bottom: 20px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.2);
        border-left: 10px solid #ddd;
    }

    .ativid-title {
        color: #0A2D82 !important;
        font-weight: bold;
        margin-bottom: 5px;
        font-size: 18px;
    }

    .hazard-value {
        font-size: 26px;
        font-weight: 900;
    }

    .alert-box {
        background-color: #ffebee;
        color: #c62828 !important;
        padding: 10px;
        border-radius: 8px;
        font-weight: bold;
        margin-top: 10px;
        border: 1px dashed #c62828;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ===============================
# CABEÇALHO (✅ SEM HTML DOIDO: usa st.image)
# ===============================
col_logo1, col_logo2, col_logo3 = st.columns([1, 2, 1])
with col_logo2:
    if LOGO_PATH.exists():
        st.image(str(LOGO_PATH), use_container_width=True)
st.markdown("<h1 style='text-align:center;'>Sistema de Consulta Hazard Grade</h1>", unsafe_allow_html=True)

# ===============================
# CARREGAR DADOS
# ===============================
@st.cache_data
def carregar_dados():
    df = pd.read_excel(EXCEL_PATH)
    df.columns = df.columns.str.strip().str.upper()
    return df

try:
    df = carregar_dados()
except Exception as e:
    st.error("Não consegui carregar o Excel na raiz do repositório.")
    st.write("Procurando por:", str(EXCEL_PATH))
    st.exception(e)
    st.stop()

# ===============================
# FORM (BOTÃO PESQUISAR FUNCIONA)
# ===============================
with st.form("form_busca"):
    termo = st.text_input("O que você deseja buscar?", placeholder="Ex: Fabricação de tintas...")
    col1, col2 = st.columns(2)
    with col1:
        pesquisar = st.form_submit_button("🔍 Pesquisar")
    with col2:
        limpar = st.form_submit_button("🗑️ Limpar")

if limpar:
    termo = ""

# ===============================
# RENDER RESULTADO
# ===============================
def renderizar_resultado(atividade, hazard):
    try:
        hazard_num = float(hazard)
    except Exception:
        hazard_num = 0

    if hazard_num <= 4:
        cor = "#00C853"
        alerta = ""
    elif hazard_num <= 6:
        cor = "#FBC02D"
        alerta = ""
    else:
        cor = "#D32F2F"
        alerta = '<div class="alert-box">⚠️ HAZARD ALTO: Verifique possível solicitação de inspeção!</div>'

    st.markdown(
        f"""
        <div class="result-card" style="border-left-color:{cor};">
            <div class="ativid-title">ATIVIDADE</div>
            <div style="color:#333; margin-bottom:10px;">{atividade}</div>
