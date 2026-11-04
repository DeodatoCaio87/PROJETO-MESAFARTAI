
import streamlit as st
import sqlite3
from pathlib import Path
import re
import pandas as pd

from database import inicializar_banco, CAMINHO_BANCO
from nlu import MotorNLU
from entities import ExtratorEntidades
from matchmaking import MotorMatchmaking


# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="MESAFARTAI",
    page_icon="🌱",
    layout="wide"
)


# INICIALIZAÇÃO DOS MÓDULOS
inicializar_banco()

nlu = MotorNLU()
extrator = ExtratorEntidades()
matchmaking = MotorMatchmaking()


# FUNÇÃO DE CONEXÃO COM O BANCO
def conectar_banco():
    return sqlite3.connect(str(CAMINHO_BANCO))


# CABEÇALHO
col_logo, col_titulo = st.columns([1, 5])

with col_logo:
    st.image(
        str(
            Path(__file__).resolve().parent.parent
            / "assents"
            / "logo_mesafartai.png"
        ),
        width=110
    )

with col_titulo:
    st.title("MESAFARTAI")
    st.caption(
        "Sistema Inteligente de Logística para Doação de Alimentos"
    )

st.divider()


# ABAS PRINCIPAIS
aba_chatbot, aba_dashboard = st.tabs([
    "💬 Chatbot",
    "📊 Dashboard"
])


# ==========================================
# ABA CHATBOT
# ==========================================

with aba_chatbot:

    st.header("Assistente MESAFARTAI")

    st.write(
        "Olá! Sou o assistente do MESAFARTAI. "
        "Posso ajudar você a doar ou solicitar alimentos."
    )

    if "resultado_nlu" not in st.session_state:
        st.session_state.resultado_nlu = None

    if "mensagem_processada" not in st.session_state:
        st.session_state.mensagem_processada = ""

    if "doacao_confirmada" not in st.session_state:
        st.session_state.doacao_confirmada = False

    if "match_resultado" not in st.session_state:
        st.session_state.match_resultado = None

    if "solicitacao_confirmada" not in st.session_state:
        st.session_state.solicitacao_confirmada = False

    mensagem = st.text_input(
        "Digite sua mensagem:",
        placeholder="Ex.: Tenho 15 kg de arroz para doar",
        key="mensagem_chat"
    )

    if st.button("Enviar mensagem"):

        if mensagem.strip():

            st.session_state.resultado_nlu = (
                nlu.processar_mensagem(mensagem)
            )

            st.session_state.mensagem_processada = mensagem
            st.session_state.doacao_confirmada = False
            st.session_state.match_resultado = None
            st.session_state.solicitacao_confirmada = False

        else:
            st.warning("Digite uma mensagem antes de enviar.")

    resultado = st.session_state.resultado_nlu

    if resultado:

        st.write(
            "**Intenção identificada:**",
            resultado["intencao"]
        )

        st.write(
            "**Confiança:**",
            resultado["confianca"]
        )

        st.info(resultado["resposta"])

        # ----------------------------------
        # REGISTRO DE DOAÇÃO
        # ----------------------------------

        if resultado["intencao"] == "registrar_doacao":

            entidades = extrator.processar_texto(
                st.session_state.mensagem_processada
            )

            st.subheader("Informações identificadas")

            st.write("Alimento:", entidades["alimento"])
            st.write("Quantidade:", entidades["quantidade_kg"], "kg")
            st.write("Validade:", entidades["data_validade"])

            conn = conectar_banco()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT id, nome, latitude, longitude
                FROM usuarios
                WHERE tipo = 'DOADOR'
                ORDER BY nome
            """)

            doadores = cursor.fetchall()
            conn.close()

            if not doadores:

                st.error("Nenhum doador cadastrado.")

            elif entidades["quantidade_kg"] <= 0:

                st.error("A quantidade deve ser maior que zero.")

            elif entidades["quantidade_kg"] > 25:

                st.error(
                    "O limite máximo permitido por doação é de 25 kg."
                )

            elif st.session_state.doacao_confirmada:

                st.success("Esta doação já foi registrada!")

                match = st.session_state.match_resultado

                if match:

                    st.info(
                        f"ONG mais próxima: {match['ong_nome']}"
                    )

                    st.write(
                        "Distância estimada:",
                        match["distancia_estimada"],
                        "km"
                    )

            else:

                doador = st.selectbox(
                    "Selecione o responsável pela doação:",
                    doadores,
                    format_func=lambda x: x[1],
                    key="selecao_doador"
                )

                if st.button("Confirmar doação"):

                    conn = conectar_banco()
                    cursor = conn.cursor()

                    cursor.execute("""
                        INSERT INTO doacoes (
                            doador_id,
                            descricao_alimento,
                            quantidade_kg,
                            data_validade
                        )
                        VALUES (?, ?, ?, ?)
                    """, (
                        doador[0],
                        entidades["alimento"],
                        entidades["quantidade_kg"],
                        entidades["data_validade"]
                    ))

                    doacao_id = cursor.lastrowid

                    conn.commit()
                    conn.close()

                    st.session_state.doacao_confirmada = True

                    st.success(
                        f"Doação de {entidades['quantidade_kg']} kg "
                        f"de {entidades['alimento']} registrada!"
                    )

                    if doador[2] is not None and doador[3] is not None:

                        match = matchmaking.encontrar_ong_mais_proxima(
                            doador[2],
                            doador[3]
                        )

                        if match:

                            conn = conectar_banco()
                            cursor = conn.cursor()

                            cursor.execute("""
                                INSERT INTO matches (
                                    doacao_id,
                                    ong_id,
                                    distancia_km
                                )
                                VALUES (?, ?, ?)
                            """, (
                                doacao_id,
                                match["ong_id"],
                                match["distancia_estimada"]
                            ))

                            conn.commit()
                            conn.close()

                            st.session_state.match_resultado = match

                            st.info(
                                f"ONG mais próxima: {match['ong_nome']}"
                            )

                            st.write(
                                "Distância estimada:",
                                match["distancia_estimada"],
                                "km"
                            )

                        else:

                            st.warning(
                                "Nenhuma ONG disponível para o match."
                            )

                    else:

                        st.warning(
                            "O doador não possui coordenadas cadastradas."
                        )

        # ----------------------------------
        # SOLICITAÇÃO DE ALIMENTOS
        # ----------------------------------

        elif resultado["intencao"] == "solicitar_alimentos":

            mensagem_original = st.session_state.mensagem_processada

            entidades = extrator.processar_texto(mensagem_original)

            st.subheader("Informações da solicitação")

            st.write("Alimento:", entidades["alimento"])

            quantidade_informada = re.search(
                extrator.padrao_quantidade,
                mensagem_original,
                re.IGNORECASE
            )

            if not quantidade_informada:

                st.warning(
                    "Não identifiquei a quantidade necessária. "
                    "Informe, por exemplo: Precisamos de 10 kg de arroz."
                )

            elif entidades["quantidade_kg"] <= 0:

                st.error("A quantidade deve ser maior que zero.")

            else:

                st.write(
                    "Quantidade solicitada:",
                    entidades["quantidade_kg"],
                    "kg"
                )

                conn = conectar_banco()
                cursor = conn.cursor()

                cursor.execute("""
                    SELECT id, nome
                    FROM usuarios
                    WHERE tipo = 'ONG'
                    ORDER BY nome
                """)

                ongs = cursor.fetchall()
                conn.close()

                if not ongs:

                    st.error("Nenhuma ONG cadastrada.")

                elif st.session_state.solicitacao_confirmada:

                    st.success("Solicitação registrada com sucesso!")

                else:

                    ong = st.selectbox(
                        "Selecione a ONG solicitante:",
                        ongs,
                        format_func=lambda x: x[1],
                        key="selecao_ong"
                    )

                    if st.button("Confirmar solicitação"):

                        conn = conectar_banco()
                        cursor = conn.cursor()

                        cursor.execute("""
                            INSERT INTO solicitacoes (
                                ong_id,
                                descricao_alimento,
                                quantidade_kg
                            )
                            VALUES (?, ?, ?)
                        """, (
                            ong[0],
                            entidades["alimento"],
                            entidades["quantidade_kg"]
                        ))

                        conn.commit()
                        conn.close()

                        st.session_state.solicitacao_confirmada = True

                        st.success(
                            f"Solicitação de "
                            f"{entidades['quantidade_kg']} kg de "
                            f"{entidades['alimento']} registrada para "
                            f"{ong[1]}!"
                        )

                        conn = conectar_banco()
                        cursor = conn.cursor()

                        cursor.execute("""
                            SELECT
                                descricao_alimento,
                                SUM(quantidade_kg)
                            FROM doacoes
                            WHERE status = 'DISPONIVEL'
                            AND LOWER(descricao_alimento) = LOWER(?)
                            GROUP BY descricao_alimento
                        """, (entidades["alimento"],))

                        disponibilidade = cursor.fetchone()
                        conn.close()

                        if disponibilidade:

                            total_disponivel = disponibilidade[1]

                            st.info(
                                f"Encontramos {total_disponivel} kg "
                                f"de {entidades['alimento']} disponíveis."
                            )

                            if total_disponivel >= entidades["quantidade_kg"]:

                                st.success(
                                    "Há quantidade suficiente de alimentos "
                                    "disponíveis para atender à solicitação."
                                )

                            else:

                                st.warning(
                                    "Ainda não há quantidade suficiente "
                                    "para atender completamente à solicitação."
                                )

                        else:

                            st.warning(
                                "Não encontramos doações disponíveis "
                                "desse alimento no momento."
                            )


# ==========================================
# ABA DASHBOARD
# ==========================================

with aba_dashboard:

    st.header("📊 Dashboard MESAFARTAI")

    conn = conectar_banco()

    # INDICADORES

    total_ongs = pd.read_sql_query("""
        SELECT COUNT(*) AS total
        FROM usuarios
        WHERE tipo = 'ONG'
    """, conn).iloc[0]["total"]

    total_kg = pd.read_sql_query("""
        SELECT COALESCE(SUM(quantidade_kg), 0) AS total
        FROM doacoes
        WHERE status = 'DISPONIVEL'
    """, conn).iloc[0]["total"]

    total_doacoes = pd.read_sql_query("""
        SELECT COUNT(*) AS total
        FROM doacoes
    """, conn).iloc[0]["total"]

    total_refeicoes = int(total_kg * 2)

    total_solicitacoes = pd.read_sql_query("""
        SELECT COUNT(*) AS total
        FROM solicitacoes
    """, conn).iloc[0]["total"]

    # CARDS DE INDICADORES

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("ONGs cadastradas", int(total_ongs))
    col2.metric("Alimentos disponíveis", f"{total_kg:.1f} kg")
    col3.metric("Doações registradas", int(total_doacoes))
    col4.metric("Refeições estimadas", total_refeicoes)

    st.metric(
        "Solicitações registradas",
        int(total_solicitacoes)
    )

    st.divider()

    # META DE ARRECADAÇÃO

    st.subheader("🎯 Meta de arrecadação")

    meta_kg = 200
    progresso = min(total_kg / meta_kg, 1.0)

    st.progress(progresso)

    st.write(
        f"{total_kg:.1f} kg arrecadados de {meta_kg} kg "
        f"({progresso * 100:.1f}%)"
    )

    st.divider()

    # HISTÓRICO DE DOAÇÕES

    st.subheader("📦 Histórico de doações")

    doacoes = pd.read_sql_query("""
        SELECT
            d.id AS 'ID',
            u.nome AS 'Doador',
            d.descricao_alimento AS 'Alimento',
            d.quantidade_kg AS 'Quantidade (kg)',
            d.data_validade AS 'Validade',
            d.status AS 'Status',
            ong.nome AS 'ONG selecionada',
            m.distancia_km AS 'Distância (km)'
        FROM doacoes d
        INNER JOIN usuarios u
            ON d.doador_id = u.id
        LEFT JOIN matches m
            ON d.id = m.doacao_id
        LEFT JOIN usuarios ong
            ON m.ong_id = ong.id
        ORDER BY d.id DESC
    """, conn)

    if not doacoes.empty:

        st.dataframe(
            doacoes,
            width="stretch",
            hide_index=True
        )

    else:

        st.info("Nenhuma doação registrada até o momento.")

    st.divider()

    # HISTÓRICO DE SOLICITAÇÕES

    st.subheader("📋 Histórico de solicitações de alimentos")

    solicitacoes = pd.read_sql_query("""
        SELECT
            s.id AS 'ID',
            u.nome AS 'ONG solicitante',
            s.descricao_alimento AS 'Alimento',
            s.quantidade_kg AS 'Quantidade necessária (kg)',
            s.data_solicitacao AS 'Data da solicitação',
            s.status AS 'Status'
        FROM solicitacoes s
        INNER JOIN usuarios u
            ON s.ong_id = u.id
        ORDER BY s.id DESC
    """, conn)

    conn.close()

    if not solicitacoes.empty:

        st.dataframe(
            solicitacoes,
            width="stretch",
            hide_index=True
        )

    else:

        st.info("Nenhuma solicitação registrada até o momento.")
