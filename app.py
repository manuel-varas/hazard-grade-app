import streamlit as st
import pandas as pd
from pathlib import Path
import os

# ===============================
# CAMINHOS (RAIZ DO REPO)
# ===============================
BASE_DIR = Path(__file__).parent
EXCEL_PATH = BASE_DIR / "HG_ATUALIZADOS.xlsx"
LOGO_PATH = BASE_DIR / "allianz_logo.png"

# ===============================
# CONFIG
# ===============================
st.set_page_config(
    page_title="Hazard Grade Explorer",
    page_icon="🔍",
    layout="centered"
)

# ===============================
# CSS
# ===============================
css = (
    "<style>"
    ".stApp{background-color:#0A2D82;}"
    "h1,label,p{color:white!important;font-family:'Segoe UI',Tahoma,Geneva,Verdana,sans-serif;}"
    ".stTextInput input{background-color:white!important;color:#0A2D82!important;height:50px;"
    "border-radius:12px;font-size:18px;border:none!important;}"
    "div.stButton>button{height:50px;border-radius:12px;font-weight:bold;"
    "border:2px solid white;background:transparent;color:white;transition:.2s;}"
    "div.stButton>button:hover{background:white;color:#0A2D82;}"
    ".result-card{background:white;padding:22px;border-radius:15px;margin-bottom:16px;"
    "box-shadow:0 10px 20px rgba(0,0,0,.2);border-left:10px solid #ddd;}"
    ".ativid-title{color:#0A2D82!important;font-weight:800;margin-bottom:6px;font-size:18px;}"
    ".hazard-value{font-size:26px;font-weight:900;}"
    ".alert-box{background:#ffebee;color:#c62828!important;padding:10px;border-radius:8px;"
    "font-weight:800;margin-top:10px;border:1px dashed #c62828;}"
    "</style>"
)
st.markdown(css, unsafe_allow_html=True)

# ===============================
# CABEÇALHO
# ===============================
c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    if LOGO_PATH.exists():
        st.image(str(LOGO_PATH), use_container_width=True)

st.markdown(
    "<h1 style='text-align:center;margin-top:0;'>Sistema de Consulta Hazard Grade</h1>",
    unsafe_allow_html=True
)

# ===============================
# SESSION STATE
# ===============================
if "termo" not in st.session_state:
    st.session_state.termo = ""

# ===============================
# CARREGAR EXCEL
# ===============================
@st.cache_data
def carregar_dados():
    if not EXCEL_PATH.exists():
        st.error("❌ Não encontrei o arquivo HG_ATUALIZADOS.xlsx na raiz do repositório.")
        st.write("📁 Arquivos encontrados:", sorted(os.listdir(BASE_DIR)))
        st.stop()

    df = pd.read_excel(EXCEL_PATH)
    df.columns = df.columns.str.strip().str.upper()

    if "ATIVIDADE" not in df.columns or "HAZARD GRADE" not in df.columns:
        st.error("❌ O Excel precisa conter as colunas ATIVIDADE e HAZARD GRADE.")
        st.write("Colunas encontradas:", list(df.columns))
        st.stop()

    return df

df = carregar_dados()

# ===============================
# FORM DE BUSCA
# ===============================
with st.form("form_busca", clear_on_submit=False):
    termo = st.text_input(
        "O que você deseja buscar?",
        placeholder="Ex: Fabricação de tintas...",
        value=st.session_state.termo
    )

    col1, col2 = st.columns(2)
    with col1:
        pesquisar = st.form_submit_button("🔍 Pesquisar")
    with col2:
        limpar = st.form_submit_button("🗑️ Limpar")

# ===============================
# AÇÕES DOS BOTÕES
# ===============================
if limpar:
    st.session_state.termo = ""
    st.rerun()

if pesquisar:
    st.session_state.termo = termo

# ===============================
# RENDER RESULTADO
# ===============================
def renderizar_resultado(atividade, hazard):
    try:
        hz = float(hazard)
    except Exception:
        hz = 0.0

    if hz <= 4:
        cor = "#00C853"
        alerta = ""
    elif hz <= 6:
        cor = "#FBC02D"
        alerta = ""
    else:
        cor = "#D32F2F"
        alerta = (
            "<div class='alert-box'>"
            "⚠️ HAZARD ALTO: Verifique possível solicitação de inspeção!"
            "</div>"
        )

    html = (
        "<div class='result-card' style='border-left-color:" + cor + ";'>"
        "<div class='ativid-title'>ATIVIDADE</div>"
        "<div style='color:#333;margin-bottom:10px;'>" + str(atividade) + "</div>"
        "<div class='ativid-title'>HAZARD GRADE</div>"
        "<div class='hazard-value' style='color:" + cor + ";'>" + str(hazard) + "</div>"
        + alerta +
        "</div>"
    )
    st.markdown(html, unsafe_allow_html=True)

# ===============================
# BUSCA
# ===============================
if pesquisar and st.session_state.termo:
    resultados = df[
        df["ATIVIDADE"]
        .astype(str)
        .str.contains(st.session_state.termo, case=False, na=False)
    ]

    if resultados.empty:
        st.error(f"Nenhum resultado encontrado para '{st.session_state.termo}'.")
    else:
        for _, row in resultados.iterrows():
            renderizar_resultado(row["ATIVIDADE"], row["HAZARD GRADE"])

elif not pesquisar:
    st.info(
        """👋 Digite uma atividade e clique em Pesquisar.
Use o botão Limpar para apagar o campo de busca."""
    )
