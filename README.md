# 🌱 MESAFARTAI — Versão 2

**ODS 2 — Fome Zero e Agricultura Sustentável**

Sistema de apoio à doação de alimentos que conecta doadores a ONGs compatíveis e próximas. A aplicação usa Streamlit, SQLite, processamento de linguagem natural, extração de entidades, geocodificação e matchmaking geográfico.

## Funcionalidades

- Chatbot conversacional para registrar doações e consultar protocolos.
- NLU com TF-IDF e Regressão Logística, treinado com `data/dataset_intencoes.csv`.
- Extração de alimentos, quantidades, unidades, validade, CEP/endereço e contato.
- Geocodificação por BrasilAPI, ViaCEP e Nominatim/OpenStreetMap, com cache.
- Matchmaking KNN com distância de Haversine, restrições alimentares e até duas opções de ONG.
- Área administrativa protegida por usuário e senha com hash PBKDF2.
- Cadastro e gerenciamento de ONGs, dashboard e acompanhamento das doações.

## Estrutura

```text
MESAFARTAI/
├── requirements.txt
├── src/
│   ├── app.py
│   ├── auth.py
│   ├── chatbot.py
│   ├── database.py
│   ├── entities.py
│   ├── geocoding.py
│   ├── matchmaking.py
│   └── nlu.py
├── data/
│   ├── alimentos.csv
│   ├── dataset_intencoes.csv
│   └── dataset_teste.csv
├── scripts/
│   ├── gerar_hash_senha.py
│   └── gerar_dataset.py
└── .streamlit/
    └── secrets.toml.example
```

## Instalação — Windows (PowerShell)

1. Clone o repositório ou atualize sua cópia local:

```powershell
git clone https://github.com/DeodatoCaio87/PROJETO-MESAFARTAI.git
cd PROJETO-MESAFARTAI
```

Se já possui o projeto, entre na pasta e execute `git pull origin main`.

2. Crie e ative o ambiente virtual:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

3. Instale as dependências:

```powershell
pip install -r requirements.txt
```

4. Configure os segredos. Copie o exemplo:

```powershell
Copy-Item .streamlit/secrets.toml.example .streamlit/secrets.toml
```

Gere a senha do administrador:

```powershell
python scripts/gerar_hash_senha.py
```

Copie o bloco `[admin]` exibido pelo script para `.streamlit/secrets.toml`, substituindo os valores de exemplo. Em `[app]`, substitua o contato em `nominatim_user_agent` por um e-mail real. **Nunca publique `.streamlit/secrets.toml` no GitHub.**

5. Execute:

```powershell
streamlit run src/app.py
```

## Testes e dados

Se quiser regenerar os conjuntos de dados a partir dos modelos e exemplos do projeto, execute na raiz:

```powershell
python scripts/gerar_dataset.py
```

O script recria `data/dataset_intencoes.csv` e `data/dataset_teste.csv`. Em seguida, o NLU pode ser avaliado com `python src/nlu.py`.

- Acesse **Administração** e entre com o usuário e senha configurados.
- Cadastre pelo menos quatro ONGs com CEP/endereço, coordenadas e restrições alimentares adequadas.
- Faça cinco conversas de doação no chatbot, incluindo consentimento e escolha/recusa de ONG.
- Teste a consulta de protocolo e confira o dashboard.
- O conjunto de teste do NLU pode ser avaliado executando `python src/nlu.py`.

O banco SQLite é criado em `data/mesafartai.db`. Ele é local e está excluído do Git.

## Privacidade e mapas

O chatbot solicita consentimento antes de gravar a doação. Os dados de contato são usados para o fluxo de doação. O Nominatim exige identificação no User-Agent, respeito ao limite de requisições e atribuição © OpenStreetMap contributors nos mapas.

## Tecnologias

Python · Streamlit · SQLite · Pandas · NumPy · scikit-learn · spaCy · Regex · BrasilAPI · ViaCEP · OpenStreetMap/Nominatim · Git/GitHub
