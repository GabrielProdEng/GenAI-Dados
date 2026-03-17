from __future__ import annotations

from datetime import date, datetime, timedelta

import plotly.express as px
import streamlit as st

from bacen_client import fetch_serie_periodo
from loaders import load_json
from ollama_client import chat as ollama_chat
from ollama_client import list_models
from prompt_builder import build_messages
from rules import evaluate_rule

st.set_page_config(page_title="BIA Macro Local", page_icon="📊", layout="wide")

st.title("📊 BIA Macro Local")
st.caption("Monitor de indicadores econômicos com Bacen + chat local via Ollama")

catalogo = load_json("catalogo_indicadores.json")["indicadores"]
regras = load_json("configuracao_alertas.json")["regras"]

if "df_serie" not in st.session_state:
    st.session_state.df_serie = None

if "indicador_atual" not in st.session_state:
    st.session_state.indicador_atual = None

if "alerts_text" not in st.session_state:
    st.session_state.alerts_text = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

tab1, tab2 = st.tabs(["📈 Monitoramento", "💬 Chat local"])

with tab1:
    opcoes = {f"{item['nome']} ({item['codigo']})": item for item in catalogo}

    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        escolha = st.selectbox("Indicador", list(opcoes.keys()))

    with col2:
        data_inicial = st.date_input(
            "Data inicial",
            value=date.today() - timedelta(days=365 * 2)
        )

    with col3:
        data_final = st.date_input(
            "Data final",
            value=date.today()
        )

    selecionado = opcoes[escolha]

    if st.button("Consultar série no Bacen"):
        with st.spinner("Buscando dados..."):
            df = fetch_serie_periodo(
                codigo=int(selecionado["codigo"]),
                data_inicial=datetime.combine(data_inicial, datetime.min.time()),
                data_final=datetime.combine(data_final, datetime.min.time()),
            )

        st.session_state.df_serie = df
        st.session_state.indicador_atual = selecionado
        st.session_state.alerts_text = []

        if df.empty:
            st.warning("Nenhum dado encontrado para a janela selecionada.")
        else:
            ultimo = df.sort_values("data").iloc[-1]

            st.subheader("Resumo")
            st.write(
                {
                    "indicador": selecionado["nome"],
                    "codigo": int(selecionado["codigo"]),
                    "categoria": selecionado["categoria"],
                    "ultima_data": ultimo["data"].strftime("%Y-%m-%d"),
                    "ultimo_valor": float(ultimo["valor"]),
                    "unidade": selecionado["unidade"],
                }
            )

            fig = px.line(
                df,
                x="data",
                y="valor",
                title=f"{selecionado['nome']} — código {selecionado['codigo']}"
            )
            st.plotly_chart(fig, use_container_width=True)
            st.dataframe(df.tail(20), use_container_width=True)

            regras_indicador = [
                r for r in regras
                if int(r["codigo"]) == int(selecionado["codigo"])
            ]

            st.subheader("Alertas")
            if regras_indicador:
                for regra in regras_indicador:
                    resultado = evaluate_rule(df, regra)
                    detail = f"{regra['mensagem']} | {resultado.detail}"

                    if resultado.triggered:
                        st.error(f"⚠️ {detail}")
                        st.session_state.alerts_text.append(detail)
                    else:
                        st.success(f"✅ {detail}")
            else:
                st.info("Não há regras cadastradas para este indicador.")

with tab2:
    st.subheader("Conversar com o modelo local")

    try:
        modelos = list_models()
    except Exception as exc:
        modelos = []
        st.error(
            "Não foi possível conectar ao Ollama local. "
            "Verifique se o serviço está ativo em http://localhost:11434."
        )
        st.exception(exc)

    modelo_escolhido = st.selectbox(
        "Modelo do Ollama",
        modelos if modelos else ["sem_modelos_disponiveis"]
    )

    if st.session_state.indicador_atual is None or st.session_state.df_serie is None:
        st.info("Primeiro consulte um indicador na aba de monitoramento.")
    else:
        st.write(
            f"Contexto atual: **{st.session_state.indicador_atual['nome']} "
            f"({st.session_state.indicador_atual['codigo']})**"
        )

        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        pergunta = st.chat_input("Pergunte sobre o indicador carregado")

        if pergunta and modelos:
            st.session_state.chat_history.append(
                {"role": "user", "content": pergunta}
            )

            with st.chat_message("user"):
                st.markdown(pergunta)

            with st.chat_message("assistant"):
                with st.spinner("Pensando localmente..."):
                    messages = build_messages(
                        user_question=pergunta,
                        indicador=st.session_state.indicador_atual,
                        df=st.session_state.df_serie,
                        alerts=st.session_state.alerts_text,
                        chat_history=st.session_state.chat_history[:-1],
                    )
                    try:
                        resposta = ollama_chat(
                            model=modelo_escolhido,
                            messages=messages,
                            temperature=0.2,
                        )
                    except Exception as exc:
                        resposta = (
                            "Não consegui obter resposta do Ollama. "
                            "Verifique se o modelo foi baixado e se o serviço está em execução."
                        )
                        st.exception(exc)

                st.markdown(resposta)

            st.session_state.chat_history.append(
                {"role": "assistant", "content": resposta}
            )

        if st.button("Limpar conversa"):
            st.session_state.chat_history = []
            st.rerun()

st.markdown("---")
st.markdown(
    "**Escopo:** inflação, juros, câmbio, atividade e crédito. "
    "**IA local via Ollama. Sem dados pessoais.**"
)
