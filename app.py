import streamlit as st
import pandas as pd
from pathlib import Path
import base64

# ===============================
# BASE DO PROJETO
# ===============================
BASE_DIR = Path(__file__).parent
ASSETS_DIR = BASE_DIR / "assets"

# ===============================
# FUNÇÕES
# ===============================
def carregar_dados():
    caminho = ASSETS_DIR / "HG_ATUALIZADOS (1).xlsx"
    df = pd.read_excel(caminho)
    df.columns = df.columns.str.strip().str.upper()
    return df

def img_base64(path: Path):
    if path.exists():
        return base64.b64encode(path.read_bytes()).decode()
    return ""

# ===============================
# CONFIG STREAMLIT
# ===============================
st.set_page_config(
    page_title="Sistema de Consulta Hazard Grade",
    page_icon="🔍",
    layout="centered"
)

# ===============================
# CSS (FUNDO AZUL OK)
# ===============================
st.markdown("""
<style>
.stApp { background-color: #0A2D82; }
h1, label, p { color: white !important; }
</style>
""", unsafe_allow_html=True)

# ===============================
# CABEÇALHO ✅ CORRETO
# ===============================
logo = img_base64(ASSETS_DIR / "allianz_logo.png")

st.markdown(f"""
<div style="text-align:center; margin-bottom:30px;">
    <img src="data:image/png;base64,{logo}" height="80"/>
    <h1>Sistema de Consulta Hazard Grade</h1>
</div>
""", unsafe_allow_html=True)

# ===============================
# FORMULÁRIO ✅
# ===============================
pesquisar = False

with st.form("form_busca"):
    termo = st.text_input(
        "O que você deseja buscar?",
        placeholder="Ex: Fabricação de tintas..."
    )
    pesquisar = st.form_submit_button("🔍 Pesquisar")

# ===============================
# LÓGICA
# ===============================
df = carregar_dados()

if pesquisar:
    if termo:
        resultados = df[df["ATIVIDADE"].str.contains(termo, case=False, na=False)]

        if resultados.empty:
            st.error("Nenhum resultado encontrado.")
        else:
            for _, row in resultados.iterrows():
                st.success(f"{row['ATIVIDADE']} — Hazard Grade {row['HAZARD GRADE']}")
    else:
        st.warning("Digite um termo para pesquisar.")
else:
    st.info("Digite uma atividade e clique em Pesquisar.")
