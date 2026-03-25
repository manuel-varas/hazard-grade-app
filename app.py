import streamlit as st
import pandas as pd
import base64
import os

# --- FUNÇÕES DE SUPORTE ---
def get_base64_image(image_path):
    try:
        if os.path.exists(image_path):
            with open(image_path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode()
    except Exception:
        return None
    return None

@st.cache_data
def carregar_dados():
    try:
        df = pd.read_excel(r"C:\Hazard Grade\HG_ATUALIZADOS.xlsx", header=0)
        df.columns = df.columns.str.strip().str.upper()
        return df
    except Exception:
        return pd.DataFrame()

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Hazard Grade Explorer",
    page_icon="🔍",
    layout="centered" # "centered" dá um ar mais elegante para sistemas de busca
)

# --- LÓGICA DE ESTADO (LIMPAR) ---
if 'busca_input' not in st.session_state:
    st.session_state.busca_input = ""

def limpar_texto():
    st.session_state.busca_input = ""

# --- DESIGN CUSTOMIZADO (CSS) ---
caminho_logo = r"C:\Hazard Grade\allianz_logo.png"
img_base64 = get_base64_image(caminho_logo)
logo_html_src = f"data:image/png;base64,{img_base64}" if img_base64 else ""

st.markdown(f"""
    <style>
    /* Fundo Principal */
    .stApp {{
        background-color: #0A2D82;
    }}
    
    /* Títulos e textos */
    h1, p, label {{
        color: white !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }}

    /* Barra de busca */
    .stTextInput input {{
        color: #0A2D82 !important;
        background-color: white !important;
        height: 50px;
        border-radius: 12px !important;
        border: none !important;
        font-size: 18px !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }}

    /* Estilização dos Botões */
    div.stButton > button {{
        border-radius: 12px;
        height: 50px;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 1px;
        border: 2px solid white;
        background-color: transparent;
        color: white;
        transition: 0.3s;
    }}
    
    div.stButton > button:hover {{
        background-color: white;
        color: #0A2D82;
    }}

    /* Card de Resultado */
    .result-card {{
        background-color: white;
        padding: 25px;
        border-radius: 15px;
        margin-bottom: 20px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.2);
        border-left: 10px solid #ddd;
    }}
    
    .ativid-title {{ color: #0A2D82 !important; font-weight: bold; margin-bottom: 5px; font-size: 20px; }}
    .hazard-value {{ font-size: 24px; font-weight: 900; }}
    
    /* Alerta de Inspeção */
    .alert-box {{
        background-color: #ffebee;
        color: #c62828 !important;
        padding: 10px;
        border-radius: 8px;
        font-weight: bold;
        margin-top: 10px;
        border: 1px dashed #c62828;
    }}

    .logo-container {{
        text-align: center;
        margin-bottom: 40px;
    }}
    .logo-container img {{ height: 80px; margin-bottom: 10px; }}
    </style>
""", unsafe_allow_html=True)

# --- CABEÇALHO ---
st.markdown(f"""
    <div class="logo-container">
        <img src="{logo_html_src}">
        <h1>Sistema de Consulta Hazard Grade</h1>
    </div>
""", unsafe_allow_html=True)

# --- ÁREA DE INPUT ---
termo = st.text_input("O que você deseja buscar?", key="busca_input", placeholder="Ex: Fabricação de tintas...")

col1, col2 = st.columns(2)
with col1:
    st.button("🔍 Pesquisar")
with col2:
    st.button("🗑️ Limpar", on_click=limpar_texto)

st.markdown("<br>", unsafe_allow_html=True)

# --- LÓGICA DE NEGÓCIO ---
def renderizar_resultado(atividade, hazard):
    # Definir cor e mensagem de alerta
    if hazard <= 4:
        cor, border = "#00C853", "#00C853" # Verde
        alerta = ""
    elif hazard <= 6:
        cor, border = "#FBC02D", "#FBC02D" # Amarelo
        alerta = ""
    else:
        cor, border = "#D32F2F", "#D32F2F" # Vermelho
        alerta = """<div class="alert-box">⚠️ HAZARD ALTO: Verifique possível solicitação de inspeção!</div>"""

    # Gerar o Card HTML
    card_html = f"""
    <div class="result-card" style="border-left-color: {border};">
        <div class="ativid-title">ATIVIDADE</div>
        <div style="color: #333; margin-bottom: 15px;">{atividade}</div>
        <div class="ativid-title">HAZARD GRADE</div>
        <div class="hazard-value" style="color: {cor};">{hazard}</div>
        {alerta}
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)

df = carregar_dados()

if termo and not df.empty:
    resultados = df[df["ATIVIDADE"].str.contains(termo, case=False, na=False)]
    
    if not resultados.empty:
        for _, row in resultados.iterrows():
            renderizar_resultado(row['ATIVIDADE'], row['HAZARD GRADE'])
    else:
        st.error(f"Nenhum registro encontrado para '{termo}'.")
elif not termo:
    st.write("👋 Bem-vindo! Utilize o campo acima para pesquisar.")
