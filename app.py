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
    try:
        if image_path.exists():
            with open(image_path, "rb") as f:
                return base64.b64encode(f.read()).decode()
    except Exception:
        return None
    return None


@st.cache_data
def carregar_dados():
    try:
        caminho_excel = ASSETS_DIR / "HG_ATUALIZADOS (1).xlsx"
        df = pd.read_excel(caminho_excel)
        df.columns = df.columns.str.strip().str.upper()
        return df
    except Exception as e:
        st.error(f"Erro ao carregar Excel: {e}")
        return pd.DataFrame()

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
logo_path = ASSETS_DIR / "allianz_logo.png"
logo_base64 = get_base64_image(logo_path)
logo_html = f'<img src="data:image/png;base64,{logo_base64}" height="80">' if logo_base64 else ""

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
# CABEÇALHO
# ===============================
st.markdown(f"""
<div style="text-align:center; margin-bottom:40px;">
    {logo_html}
    <h1>Sistema de Consulta Hazard Grade</h1>
</div>
""", unsafe_allow_html=True)

# ===============================
# FORMULÁRIO (BOTÃO FUNCIONAL ✅)
# ===============================
with st.form("form_busca"):
    termo = st.text_input(
        "O que você deseja buscar?",
        key="busca_input",
        placeholder="Ex: Fabricação de tintas..."
    )

    col1, col2 = st.columns(2)
    with col1:
        pesquisar = st.form_submit_button("🔍 Pesquisar")
    with col2:
        st.form_submit_button("🗑️ Limpar", on_click=limpar_texto)

# ===============================
# FUNÇÃO DE RESULTADO
# ===============================
def renderizar_resultado(atividade, hazard):
    if hazard <= 4:
        cor = "#00C853"
        alerta = ""
    elif hazard <= 6:
        cor = "#FBC02D"
        alerta = ""
    else:
        cor = "#D32F2F"
        alerta = '<div class="alert-box">⚠️ HAZARD ALTO: Verifique possível inspeção!</div>'

    st.markdown(f"""
    <div class="result-card" style="border-left-color:{cor}">
        <div class="ativid-title">ATIVIDADE</div>
        <div>{atividade}</div>
        <div class="ativid-title" style="margin-top:10px;">HAZARD GRADE</div>
        <div class="hazard-value" style="color:{cor}">{hazard}</div>
        {alerta}
    </div>
    """, unsafe_allow_html=True)

# ===============================
# LÓGICA PRINCIPAL
# ===============================
df = carregar_dados()

if pesquisar:
    if termo and not df.empty:
        resultados = df[df["ATIVIDADE"].str.contains(termo, case=False, na=False)]

        if not resultados.empty:
            for _, row in resultados.iterrows():
                renderizar_resultado(row["ATIVIDADE"], row["HAZARD GRADE"])
        else:
            st.error(f"Nenhum resultado encontrado para '{termo}'.")
    else:
        st.warning("Digite um termo para pesquisar.")
else:
    st.write("👋 Bem-vindo! Utilize o campo acima para pesquisar.")
``
