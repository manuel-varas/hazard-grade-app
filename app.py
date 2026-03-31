# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd
from pathlib import Path
import unicodedata

st.set_page_config(
    page_title="Sistema de Consulta Hazard Grade",
    page_icon="🔍",
    layout="centered"
)

USUARIO_CORRETO = "allianz"
SENHA_CORRETA = "@9A3F7C2E4BÇ!#"

st.session_state.setdefault("autenticado", False)
st.session_state.setdefault("termo", "")
st.session_state.setdefault("input_busca", "")
st.session_state.setdefault("executar_busca", False)

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

BASE_DIR = Path(__file__).parent
EXCEL_PATH = BASE_DIR / "HG_ATUALIZADOS.xlsx"
LOGO_PATH = BASE_DIR / "allianz_logo.png"

st.markdown("""
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
border:2px solid white;background:transparent;color:white;}
.result-card{background:white;padding:22px;border-radius:15px;margin-bottom:16px;
box-shadow:0 10px 20px rgba(0,0,0,.2);border-left:10px solid #ddd;}
.ativid-title{color:#0A2D82!important;font-weight:800;margin-bottom:6px;font-size:18px;}
.hazard-value{font-size:26px;font-weight:900;}
.alert-box{background:#ffebee;color:#c62828!important;padding:14px;border-radius:8px;
font-weight:900;margin-top:10px;border:2px dashed #c62828;text-align:center;}

@media (max-width: 768px){
    h1{font-size:22px!important;}
    .stTextInput input{height:46px;font-size:16px;}
    div.stButton>button{height:46px;font-size:15px;}
    .result-card{padding:16px;}
    .hazard-value{font-size:22px;}
}
</style>
""", unsafe_allow_html=True)

c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    if LOGO_PATH.exists():
        st.image(str(LOGO_PATH), use_container_width=True)

st.markdown(
    "<h1 style='text-align:center;'>Sistema de Consulta Hazard Grade</h1>",
    unsafe_allow_html=True
)

@st.cache_data
def carregar_dados():
    df = pd.read_excel(EXCEL_PATH)
    df.columns = df.columns.str.strip().str.upper()
    df["ATIVIDADE"] = df["ATIVIDADE"].astype(str)
    df["_ATIVIDADE_LIMPA"] = df["ATIVIDADE"].apply(normalizar_texto)
    base = df[["ATIVIDADE", "_ATIVIDADE_LIMPA"]].drop_duplicates()
    return df, list(base.itertuples(index=False, name=None))

df, sugestoes_base = carregar_dados()

st.text_input("O que você deseja buscar?", key="input_busca", on_change=on_change_busca)

if st.button("🔍 Pesquisar"):
    pesquisar_agora()

def renderizar_resultado(atividade, hazard):

    if isinstance(hazard, str) and hazard.strip().upper() == "ATIVIDADE PROIBIDA":
        st.markdown(
            f"""
            <div class='result-card' style='border-left-color:black;'>
                <div class='ativid-title'>ATIVIDADE</div>
                <div>{atividade}</div>
                <div class='alert-box' style='font-size:22px;'>
                    🚫 PROIBIDO SEGUIR COTAÇÃO<br>ATIVIDADE PROIBIDA
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        return

    hz = float(hazard)
    cor = "#00C853" if hz <= 4 else "#FBC02D" if hz <= 6 else "#D32F2F"

    st.markdown(
        f"""
        <div class='result-card' style='border-left-color:{cor};'>
            <div class='ativid-title'>ATIVIDADE</div>
            <div>{atividade}</div>
            <div class='ativid-title'>HAZARD GRADE</div>
            <div class='hazard-value' style='color:{cor};'>{hazard}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

if st.session_state.executar_busca:
    termo = normalizar_texto(st.session_state.termo)
    for _, r in df[df["_ATIVIDADE_LIMPA"].str.contains(termo, na=False)].iterrows():
        renderizar_resultado(r["ATIVIDADE"], r["HAZARD GRADE"])
``
