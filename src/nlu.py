from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier


class MotorNLU:
    def __init__(self):
        # Exemplos de mensagens para treinar o modelo
        frases = [
            # Registrar doação
            "Quero doar alimentos",
            "Tenho comida para doar",
            "Gostaria de fazer uma doação",
            "Tenho 10 kg de arroz para doar",
            "Quero cadastrar uma doação",
            "Estou oferecendo alimentos",
            "Tenho alimentos disponíveis",
            "Quero ajudar doando comida",

            # Solicitar alimentos
            "Preciso de alimentos",
            "Quero receber uma doação",
            "Nossa ONG precisa de comida",
            "Estamos precisando de arroz",
            "Como faço para solicitar alimentos",
            "Gostaria de receber alimentos",
            "Precisamos de doações para nossa instituição",
            "Quero solicitar uma doação",

            # Mensagens desconhecidas
            "Olá, tudo bem?",
            "Qual é o horário de funcionamento?",
            "Como funciona esse sistema?",
            "Quem desenvolveu esse projeto?",
            "Quero saber mais informações",
            "Obrigado pela ajuda",
        ]

        intencoes = [
            "registrar_doacao",
            "registrar_doacao",
            "registrar_doacao",
            "registrar_doacao",
            "registrar_doacao",
            "registrar_doacao",
            "registrar_doacao",
            "registrar_doacao",

            "solicitar_alimentos",
            "solicitar_alimentos",
            "solicitar_alimentos",
            "solicitar_alimentos",
            "solicitar_alimentos",
            "solicitar_alimentos",
            "solicitar_alimentos",
            "solicitar_alimentos",

            "desconhecida",
            "desconhecida",
            "desconhecida",
            "desconhecida",
            "desconhecida",
            "desconhecida",
        ]

        # Transformação dos textos em dados numéricos
        self.vetorizador = TfidfVectorizer(
            lowercase=True,
            strip_accents="unicode"
        )

        X = self.vetorizador.fit_transform(frases)

        # Treinamento do classificador
        self.modelo = RandomForestClassifier(
            n_estimators=100,
            random_state=42
        )

        self.modelo.fit(X, intencoes)

        # Confiança mínima para aceitar uma intenção
        self.limite_confianca = 0.60

    def classificar_intencao(self, mensagem):
        if not mensagem or not mensagem.strip():
            return {
                "intencao": "desconhecida",
                "confianca": 0.0
            }

        # Converte a mensagem para o formato utilizado no treinamento
        mensagem_vetorizada = self.vetorizador.transform([mensagem])

        # Calcula as probabilidades de cada intenção
        probabilidades = self.modelo.predict_proba(mensagem_vetorizada)[0]

        indice = probabilidades.argmax()

        intencao = self.modelo.classes_[indice]
        confianca = float(probabilidades[indice])

        # Verifica se a confiança atingiu o limite mínimo
        if confianca < self.limite_confianca:
            intencao = "desconhecida"

        return {
            "intencao": intencao,
            "confianca": round(confianca, 2)
        }

    def processar_mensagem(self, mensagem):
        resultado = self.classificar_intencao(mensagem)

        respostas = {
            "registrar_doacao": "Entendi! Você deseja registrar uma doação de alimentos.",
            "solicitar_alimentos": "Entendi! Você deseja solicitar alimentos para sua instituição.",
            "desconhecida": "Não consegui identificar sua intenção. Poderia explicar de outra maneira?"
        }

        resultado["resposta"] = respostas[resultado["intencao"]]

        return resultado


# Teste do módulo
if __name__ == "__main__":
    nlu = MotorNLU()

    print("--- TESTE DO MOTOR NLU ---")

    mensagens = [
        "Tenho 15 kg de arroz para doar",
        "Nossa ONG precisa de alimentos",
        "Como está o tempo hoje?"
    ]

    for mensagem in mensagens:
        resultado = nlu.processar_mensagem(mensagem)

        print(f"\nMensagem: {mensagem}")
        print(f"Intenção: {resultado['intencao']}")
        print(f"Confiança: {resultado['confianca']}")
        print(f"Resposta: {resultado['resposta']}")