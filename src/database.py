import sqlite3


def inicializar_banco():
    # Conecta ao banco de dados SQLite
    conn = sqlite3.connect("mesafartai.db")
    cursor = conn.cursor()

    # Ativa o uso de chaves estrangeiras
    cursor.execute("PRAGMA foreign_keys = ON")

    # ============================================================
    # 1. TABELA DE USUÁRIOS
    # Armazena Doadores e ONGs
    # ============================================================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            tipo TEXT CHECK(tipo IN ('DOADOR', 'ONG')) NOT NULL,
            cep TEXT NOT NULL,
            latitude REAL,
            longitude REAL,
            telefone TEXT
        )
    """)

    # ============================================================
    # 2. TABELA DE DOAÇÕES
    # Armazena os alimentos disponibilizados pelos doadores
    # ============================================================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS doacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            doador_id INTEGER,
            descricao_alimento TEXT NOT NULL,
            quantidade_kg REAL,
            data_validade TEXT,
            status TEXT DEFAULT 'DISPONIVEL',
            FOREIGN KEY (doador_id) REFERENCES usuarios(id)
        )
    """)

    # ============================================================
    # 3. TABELA DE MATCHES LOGÍSTICOS
    # Relaciona uma doação com uma ONG
    # ============================================================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS matches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            doacao_id INTEGER,
            ong_id INTEGER,
            distancia_km REAL,
            data_match TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (doacao_id) REFERENCES doacoes(id),
            FOREIGN KEY (ong_id) REFERENCES usuarios(id)
        )
    """)

    # ============================================================
    # CARGA INICIAL DE DADOS DE TESTE
    # ============================================================

    cursor.execute("SELECT COUNT(*) FROM usuarios")

    quantidade_usuarios = cursor.fetchone()[0]

    if quantidade_usuarios == 0:

        # --------------------------------------------------------
        # ONGs DE TESTE
        # --------------------------------------------------------

        cursor.execute("""
            INSERT INTO usuarios
            (nome, tipo, cep, latitude, longitude, telefone)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            "ONG Prato Quente",
            "ONG",
            "06700-000",
            -23.612,
            -46.781,
            "11999990001"
        ))

        cursor.execute("""
            INSERT INTO usuarios
            (nome, tipo, cep, latitude, longitude, telefone)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            "Abrigo Esperanca",
            "ONG",
            "06705-000",
            -23.625,
            -46.795,
            "11999990002"
        ))

        # --------------------------------------------------------
        # DOADORES DE TESTE
        # --------------------------------------------------------

        cursor.execute("""
            INSERT INTO usuarios
            (nome, tipo, cep, latitude, longitude, telefone)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            "Supermercado Silva",
            "DOADOR",
            "06701-000",
            -23.615,
            -46.785,
            "11999990003"
        ))

        cursor.execute("""
            INSERT INTO usuarios
            (nome, tipo, cep, latitude, longitude, telefone)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            "Restaurante Sabor",
            "DOADOR",
            "06703-000",
            -23.618,
            -46.789,
            "11999990004"
        ))

        print("Dados iniciais de teste inseridos com sucesso!")

    else:
        print("Dados de teste já existem. Nenhuma inserção foi realizada.")

    # Salva as alterações
    conn.commit()

    # Fecha a conexão
    conn.close()

    print("Banco de dados 'mesafartai.db' inicializado com sucesso!")


# ================================================================
# EXECUÇÃO PRINCIPAL
# ================================================================

if __name__ == "__main__":
    inicializar_banco()