import streamlit as st
import pandas as pd
import base64
from pathlib import Path

# ===============================
# BASE DO PROJETO
# ===============================
BASE_DIR = Path(__file__).parent
ASSETS_DIR = BASE_DIR / "assets"

# ===============================
# FUNÇÕES AUXILIARES
# ===============================
def get_base64_image(image_path: Path):
    if image_path.exists():
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

@st.cache_data
def carregar_dados():
    caminho_excel = ASSETS_DIR / "HG_ATUALIZADOS (1).xlsx"
    df = pd.read_excel(caminho_excel)
    df.columns = df.columns.str.strip().str.upper()
    return df

# ===============================
# CONFIGURAÇÃO DA PÁGINA
# ===============================
st.set_page_config(
    page_title="Sistema de Consulta Hazard Grade",
    page_icon="🔍",
    layout="centered"
)

# ===============================
# ESTADO
# ===============================
if "busca_input" not in st.session_state:
    st.session_state.busca_input = ""

def limpar_texto():
    st.session_state.busca_input = ""

# ===============================
# LOGO
# ===============================
logo_base64 = get_base64_image(ASSETS_DIR / "allianz_logo.png")

# ===============================
# CSS
# ===============================
st.markdown("""
<style>
.stApp { background-color: #0A2D82; }

h1, label, p { color: white !important; }

.stTextInput input {
    background-color: white !important;
    color: #0A2D82 !important;
    height: 50px;
    border-radius: 12px;
    font-size: 18px;
}

div.stButton > button {
    height: 50px;
    border-radius: 12px;
    font-weight: bold;
    border: 2px solid white;
    background: transparent;
    color: white;
}

div.stButton > button:hover {
    background: white;
    color: #0A2D82;
}

.result-card {
    background: white;
    padding: 25px;
    border-radius: 15px;
    margin-bottom: 20px;
    border-left: 10px solid #ddd;
}

.ativid-title { font-weight: bold; color: #0A2D82; }

.hazard-value { font-size: 26px; font-weight: 900; }

.alert-box {
    background: #ffebee;
    color: #c62828;
    padding: 10px;
    border-radius: 8px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ===============================
