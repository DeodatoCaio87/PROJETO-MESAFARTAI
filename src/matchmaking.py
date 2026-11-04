
"""
MESAFARTAI - Motor de Matchmaking Logístico via KNN
Arquivo: src/matchmaking.py
"""

import sqlite3
from pathlib import Path

import numpy as np
from sklearn.neighbors import NearestNeighbors


CAMINHO_BANCO = Path(__file__).resolve().parent.parent / "mesafartai.db"


class MotorMatchmaking:

    def __init__(self, db_path=None):
        self.db_path = str(db_path or CAMINHO_BANCO)
        self._verificar_banco()

    def _verificar_banco(self):
        """Verifica se o banco principal possui a tabela de usuários."""

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type = 'table' AND name = 'usuarios'
        """)

        tabela = cursor.fetchone()
        conn.close()

        if tabela is None:
            raise RuntimeError(
                "Tabela usuarios não encontrada. "
                "Inicialize o banco antes de executar o matchmaking."
            )

    def buscar_ongs(self):
        """Busca ONGs cadastradas com coordenadas válidas."""

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, nome, latitude, longitude
            FROM usuarios
            WHERE tipo = 'ONG'
            AND latitude IS NOT NULL
            AND longitude IS NOT NULL
        """)

        ongs = cursor.fetchall()
        conn.close()

        return ongs

    def encontrar_ong_mais_proxima(self, lat_doador, long_doador):
        """Utiliza KNN para encontrar a ONG geograficamente mais próxima."""

        ongs = self.buscar_ongs()

        if not ongs:
            return None

        coords_ongs = np.array([
            [ong[2], ong[3]] for ong in ongs
        ])

        knn = NearestNeighbors(
            n_neighbors=1,
            metric="euclidean"
        )

        knn.fit(coords_ongs)

        ponto_doador = np.array([
            [lat_doador, long_doador]
        ])

        distancias, indices = knn.kneighbors(ponto_doador)

        idx_ong_proxima = indices[0][0]
        distancia_calculada = distancias[0][0]

        ong_selecionada = ongs[idx_ong_proxima]

        return {
            "ong_id": ong_selecionada[0],
            "ong_nome": ong_selecionada[1],
            "distancia_estimada": round(
                float(distancia_calculada * 111), 2
            )
        }


if __name__ == "__main__":

    motor = MotorMatchmaking()

    lat_teste = -23.615
    long_teste = -46.785

    match = motor.encontrar_ong_mais_proxima(
        lat_teste,
        long_teste
    )

    print("--- TESTE DE MATCHMAKING LOGÍSTICO (KNN) ---")

    if match:
        print(
            f"ONG Encontrada: {match['ong_nome']} "
            f"(ID: {match['ong_id']})"
        )

        print(
            f"Distância Estimada: "
            f"{match['distancia_estimada']} km"
        )
    else:
        print("Nenhuma ONG cadastrada para realizar o match.")
