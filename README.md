# 🌱 PROJETO-MESAFARTAI

## ODS 2 – Fome Zero e Agricultura Sustentável

### 📌 Sobre o projeto

O MESAFARTAI é um sistema inteligente de logística para doação de alimentos, desenvolvido com o objetivo de auxiliar na conexão entre doadores e organizações não governamentais (ONGs).

A solução utiliza técnicas de inteligência artificial e processamento de dados para facilitar o registro de doações, a identificação de necessidades alimentares e a aproximação entre doadores e instituições.

### 🎯 Objetivo

Desenvolver uma plataforma tecnológica que contribua para o combate à fome, facilitando a distribuição de alimentos e reduzindo dificuldades logísticas entre doadores e instituições beneficiárias.

### 🌱 ODS relacionada

**ODS 2 – Fome Zero e Agricultura Sustentável**

O projeto está relacionado aos seguintes objetivos:

- Combater a fome e a insegurança alimentar.
- Contribuir para o acesso a alimentos.
- Incentivar o aproveitamento de alimentos disponíveis para doação.
- Facilitar a distribuição de recursos alimentares.
- Utilizar a tecnologia como ferramenta de impacto social.

### 💡 Solução proposta

O MESAFARTAI oferece uma aplicação com interface interativa desenvolvida em Streamlit.

O sistema possui as seguintes funcionalidades:

- **Chatbot inteligente:** identifica solicitações e intenções dos usuários.
- **Processamento de linguagem natural (NLU):** utiliza TF-IDF e Random Forest para classificar mensagens.
- **Extração de entidades:** utiliza expressões regulares (Regex) para identificar alimentos, quantidades e datas de validade.
- **Matchmaking:** utiliza KNN para identificar ONGs geograficamente próximas aos doadores.
- **Banco de dados:** utiliza SQLite para armazenar usuários, doações, solicitações e correspondências.
- **Solicitação de alimentos:** permite que ONGs registrem suas necessidades alimentares.
- **Dashboard:** apresenta indicadores, meta de arrecadação e históricos de doações e solicitações.

### 🛠️ Tecnologias utilizadas

- Python
- Streamlit
- Scikit-learn
- Pandas
- NumPy
- SQLite
- Git e GitHub

### ▶️ Como executar o projeto

**1. Clonar o repositório**

```bash
git clone https://github.com/DeodatoCaio87/PROJETO-MESAFARTAI.git
```

**2. Acessar a pasta do projeto**

```bash
cd PROJETO-MESAFARTAI
```

**3. Instalar as dependências**

```bash
pip install -r requirements.txt
```

**4. Executar a aplicação**

```bash
python -m streamlit run src/app.py
```

Após a execução, o Streamlit disponibilizará o