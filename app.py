import streamlit as st
import pandas as pd
from pathlib import Path
import os
import unicodedata

# ===============================
# CONFIG
# ===============================
st.set_page_config(
    page_title="Sistema de Consulta Hazard Grade",
    page_icon="🔍",
    layout="centered"
)

# ===============================
# CREDENCIAIS
# ===============================
USUARIO_CORRETO = "allianz"
SENHA_CORRETA = "@9A3F7C2E4BÇ!#"

# ===============================
# SESSION STATE
# ===============================
st.session_state.setdefault("autenticado", False)
st.session_state.setdefault("termo", "")
st.session_state.setdefault("input_busca", "")
st.session_state.setdefault("executar_busca", False)

# ===============================
# FUNÇÕES
# ===============================
def normalizar_texto(texto):
    if texto is None:
        return ""
    texto = str(texto).strip().lower()
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    return texto

def on_change_busca():
    st.session_state.termo = st.session_state.input_busca
    st.session_state.executar_busca = False

def limpar_tudo():
    st.session_state.input_busca = ""
    st.session_state.termo = ""
    st.session_state.executar_busca = False

def pesquisar_agora():
    st.session_state.termo = st.session_state.input_busca
    st.session_state.executar_busca = True

def selecionar_sugestao(valor):
    st.session_state.input_busca = valor
    st.session_state.termo = valor
    st.session_state.executar_busca = True

# ===============================
# LOGIN
# ===============================
if not st.session_state.autenticado:
    st.markdown("## 🔐 Acesso restrito")
    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        if usuario == USUARIO_CORRETO and senha == SENHA_CORRETA:
            st.session_state.autenticado = True
            st.success("✅ Login realizado com sucesso")
            st.rerun()
        else:
            st.error("❌ Usuário ou senha inválidos")

    st.stop()

# ===============================
# CAMINHOS
# ===============================
BASE_DIR = Path(__file__).parent
EXCEL_PATH = BASE_DIR / "HG_ATUALIZADOS.xlsx"
LOGO_PATH = BASE_DIR / "allianz_logo.png"

# ===============================
# CSS
# ===============================
css = """
<style>
.stApp{background-color:#0A2D82;}
h1,label,p{color:white!important;font-family:'Segoe UI',Tahoma,Geneva,Verdana,sans-serif;}
.stTextInput input{background-color:white!important;color:#0A2D82!important;
height:50px;border-radius:12px;font-size:18px;border:none!important;}
.chip button{background:rgba(255,255,255,.12)!important;border:1px solid rgba(255,255,255,.35)!important;
color:#fff!important;border-radius:999px!important;padding:6px 12px!important;margin:4px 6px 0 0!important;
font-weight:700!important;}
.chip button:hover{background:rgba(255,255,255,.25)!important;}
div.stButton>button{height:50px;border-radius:12px;font-weight:bold;
border:2px solid white;background:transparent;color:white;transition:.2s;}
div.stButton>button:hover{background:white;color:#0A2D82;}
.result-card{background:white;padding:22px;border-radius:15px;margin-bottom:16px;
box-shadow:0 10px 20px rgba(0,0,0,.2);border-left:10px solid #ddd;}
.ativid-title{color:#0A2D82!important;font-weight:800;margin-bottom:6px;font-size:18px;}
.hazard-value{font-size:26px;font-weight:900;}
.alert-box{background:#ffebee;color:#c62828!important;padding:12px;border-radius:8px;
font-weight:900;margin-top:10px;border:2px dashed #c62828;text-align:center;}
</style>
"""
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
# CARREGAR EXCEL
# ===============================
@st.cache_data
def carregar_dados():
    if not EXCEL_PATH.exists():
        st.error("❌ Arquivo HG_ATUALIZADOS.xlsx não encontrado.")
        st.stop()

    df = pd.read_excel(EXCEL_PATH)
    df.columns = df.columns.str.strip().str.upper()

    if "ATIVIDADE" not in df.columns or "HAZARD GRADE" not in df.columns:
        st.error("❌ O Excel deve conter ATIVIDADE e HAZARD GRADE.")
        st.stop()

    df["ATIVIDADE"] = df["ATIVIDADE"].astype(str)
    df["_ATIVIDADE_LIMPA"] = df["ATIVIDADE"].apply(normalizar_texto)

    base = df[["ATIVIDADE", "_ATIVIDADE_LIMPA"]].drop_duplicates().sort_values("ATIVIDADE")
    sugestoes = list(base.itertuples(index=False, name=None))

    return df, sugestoes

df, sugestoes_base = carregar_dados()

# ===============================
# BUSCA
# ===============================
st.text_input(
    "O que você deseja buscar?",
    placeholder="Ex: Fabricação de tintas...",
    key="input_busca",
    on_change=on_change_busca
)

col1, col2 = st.columns(2)
with col1:
    st.button("🔍 Pesquisar", on_click=pesquisar_agora)
with col2:
    st.button("🗑️ Limpar", on_click=limpar_tudo)

# ===============================
# AUTOCOMPLETE
# ===============================
termo_limpo = normalizar_texto(st.session_state.input_busca)

if termo_limpo:
    sugestoes = []
    for atividade, atividade_limpa in sugestoes_base:
        if termo_limpo in atividade_limpa:
            sugestoes.append(atividade)
        if len(sugestoes) >= 8:
            break

    if sugestoes:
        st.markdown("**Sugestões:**")
        cols = st.columns(2)
        for i, sug in enumerate(sugestoes):
            with cols[i % 2]:
                st.markdown("<div class='chip'>", unsafe_allow_html=True)
                st.button(sug, key=f"sug_{i}", on_click=selecionar_sugestao, args=(sug,))
                st.markdown("</div>", unsafe_allow_html=True)

# ===============================
# RESULTADOS
# ===============================
def renderizar_resultado(atividade, hazard):

    # >>> TRATAMENTO DE ATIVIDADE PROIBIDA <<<
    if isinstance(hazard, str) and hazard.strip().upper() == "ATIVIDADE PROIBIDA":
        html = (
            "<div class='result-card' style='border-left-color:#000;'>"
            "<div class='ativid-title'>ATIVIDADE</div>"
            "<div style='color:#333;margin-bottom:10px;'>" + str(atividade) + "</div>"
            "<div class='alert-box' style='font-size:22px;'>"
            "🚫 PROIBIDO SEGUIR COTAÇÃO<br>ATIVIDADE PROIBIDA"
            "</div>"
            "</div>"
        )
        st.markdown(html, unsafe_allow_html=True)
        return

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
        alerta = "<div class='alert-box'>⚠️ HAZARD ALTO</div>"

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

if st.session_state.executar_busca:
    termo_busca = normalizar_texto(st.session_state.termo)
    if termo_busca:
        resultados = df[df["_ATIVIDADE_LIMPA"].str.contains(termo_busca, na=False)]
        if resultados.empty:
            st.error(f"Nenhum resultado encontrado para '{st.session_state.termo}'.")
        else:
            for _, row in resultados.iterrows():
                renderizar_resultado(row["ATIVIDADE"], row["HAZARD GRADE"])
else:
    st.info("👋 Digite uma atividade ou selecione uma sugestão.")
``
