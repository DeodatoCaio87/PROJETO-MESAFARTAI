# MESAFARTAI – Logística e Inteligência Assistiva no Combate à Fome

**ODS 2 – Fome Zero e Agricultura Sustentável**

O MESAFARTAI é uma aplicação acadêmica que apoia a conexão entre pessoas e estabelecimentos que desejam doar alimentos e instituições sociais cadastradas. A solução utiliza processamento de linguagem natural para interpretar mensagens, extrair dados das doações e sugerir instituições compatíveis considerando localização e restrições alimentares.

## Equipe

> Complete os campos de RA/RGM e curso antes da entrega acadêmica. Esses dados não foram preenchidos porque não constam de forma confirmada no repositório.

| Integrante | RA/RGM | Curso |
|---|---|---|
| Caio Veloso Lima Deodato | **[PREENCHER]** | **[PREENCHER]** |
| André Sousa Lima | **[PREENCHER]** | **[PREENCHER]** |
| Lucas Aparecido Rolim Costa | **[PREENCHER]** | **[PREENCHER]** |

## Objetivo e alinhamento à ODS 2

O projeto busca reduzir o desperdício e facilitar o encaminhamento de alimentos próprios para consumo a instituições que atendem pessoas em situação de vulnerabilidade. A proposta está alinhada à ODS 2 da ONU, que trata da erradicação da fome, da segurança alimentar, da melhoria da nutrição e da promoção da agricultura sustentável.

## Funcionalidades implementadas

- Chatbot público para iniciar o registro de doações.
- Classificação de intenções com TF-IDF e Regressão Logística.
- Extração de alimentos, quantidades, unidades, validade e dados de contato com regras e expressões regulares.
- Coleta de nome, e-mail, localização e consentimento antes de gravar uma doação.
- Geração de protocolo e consulta pública do andamento da doação.
- Geocodificação de CEP/endereço com BrasilAPI, ViaCEP e Nominatim/OpenStreetMap, com cache local.
- Cadastro, edição e ativação/desativação de ONGs pela administração.
- Matchmaking geográfico com KNN e distância de Haversine, considerando restrições alimentares e apresentando até duas opções.
- Registro da aceitação/recusa de uma instituição e registro administrativo da coleta.
- Painel administrativo com indicadores, visualizações, mapa e exportação CSV.
- Autenticação administrativa com hash PBKDF2.

**Limite funcional desta versão:** as ONGs são cadastradas pela administração. O chatbot não oferece um fluxo autenticado para que uma ONG solicite alimentos; quando identifica essa intenção, explica que a participação deve ser tratada com a administração. Essa funcionalidade pode ser desenvolvida em uma etapa futura.

## Tecnologias

Python 3.11 ou superior (recomendado), Streamlit, SQLite, Pandas, NumPy, scikit-learn, spaCy, Regex, BrasilAPI, ViaCEP, OpenStreetMap/Nominatim e Git/GitHub.

## Estrutura do repositório

```text
PROJETO-MESAFARTAI/
├── .streamlit/
│   └── secrets.toml.example
├── assets/
│   ├── arquitetura_mesafarta.png
│   ├── diag_fluxo_mesafartai.png
│   └── logo_mesafartai.png
├── data/
│   ├── alimentos.csv
│   ├── dataset_intencoes.csv
│   └── dataset_teste.csv
├── docs/
│   ├── escopo_projeto.md
│   ├── operacao_privacidade.md
│   └── regras.txt
├── scripts/
│   ├── gerar_dataset.py
│   └── gerar_hash_senha.py
├── src/
│   ├── app.py
│   ├── auth.py
│   ├── chatbot.py
│   ├── database.py
│   ├── entities.py
│   ├── geocoding.py
│   ├── matchmaking.py
│   └── nlu.py
├── .gitignore
└── requirements.txt
```

O banco SQLite é criado localmente em `data/mesafartai.db` na primeira inicialização. O arquivo de banco e as credenciais reais não devem ser enviados ao Git.

## Instalação e execução — Windows (PowerShell)

1. Clone o repositório e entre na pasta:

```powershell
git clone https://github.com/DeodatoCaio87/PROJETO-MESAFARTAI.git
cd PROJETO-MESAFARTAI
```

Se o projeto já estiver na máquina, atualize-o:

```powershell
git pull origin main
```

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

4. Crie o arquivo local de configuração:

```powershell
Copy-Item .streamlit/secrets.toml.example .streamlit/secrets.toml
python scripts/gerar_hash_senha.py
```

Copie a seção `[admin]` impressa pelo script para `.streamlit/secrets.toml`, substituindo os valores de exemplo. Em `[app]`, configure um e-mail de contato real em `nominatim_user_agent` e informe o contexto geográfico adequado em `contexto_geografico`.

5. Inicie a aplicação:

```powershell
streamlit run src/app.py
```

O navegador abrirá a aplicação local. Para encerrar, pressione `Ctrl+C` no terminal.

## Configuração opcional de dados demonstrativos

O arquivo `.streamlit/secrets.toml.example` mantém `inserir_ongs_demonstracao = false` por padrão. Para uma apresentação exclusivamente demonstrativa, é possível alterar essa opção para `true` no arquivo local `.streamlit/secrets.toml`. As quatro instituições de demonstração são fictícias e só são inseridas quando a tabela de ONGs está vazia. Não as apresente como organizações reais.

## Fluxo de utilização

1. O doador acessa **Quero doar** e descreve os alimentos disponíveis.
2. O chatbot identifica a intenção e extrai os itens e quantidades.
3. A conversa solicita os dados necessários, localização e consentimento.
4. Após a confirmação, a doação é gravada e recebe um protocolo.
5. O sistema procura ONGs ativas compatíveis, considerando restrições e proximidade geográfica.
6. O doador pode aceitar ou recusar a opção apresentada; quando disponível, uma segunda opção pode ser oferecida.
7. O protocolo permite consultar a situação da doação.
8. A administração acompanha os registros e pode marcar uma doação aceita como coletada.

## Privacidade, segurança e operação

- O nome e o e-mail do doador só são persistidos após o consentimento solicitado no fluxo.
- O painel administrativo exige autenticação. Use uma senha forte e não compartilhe o arquivo `.streamlit/secrets.toml`.
- O arquivo real de segredos, bancos de dados, ambientes virtuais e arquivos locais sensíveis estão cobertos pelo `.gitignore`.
- O banco SQLite é local. Em hospedagens com armazenamento efêmero, os registros podem ser perdidos após reinicializações ou nova implantação. Para uso contínuo em produção, configure um banco persistente e faça cópias de segurança.
- A exportação CSV contém dados operacionais e deve ser acessada e compartilhada somente por pessoas autorizadas.
- O uso do Nominatim público deve respeitar a política do serviço, incluindo identificação no User-Agent e intervalo entre requisições. Mapas devem manter a atribuição © OpenStreetMap contributors.
- Consulte [docs/operacao_privacidade.md](docs/operacao_privacidade.md) para orientações complementares.

## Identidade visual

O logotipo e os diagramas do projeto estão em `assets/`. O prompt de geração da identidade visual está registrado em [docs/escopo_projeto.md](docs/escopo_projeto.md).

## Documentação

- [Escopo do projeto](docs/escopo_projeto.md)
- [Regras e orientações acadêmicas da etapa](docs/regras.txt)
- [Operação, privacidade e publicação](docs/operacao_privacidade.md)

## Observação acadêmica

Este repositório apresenta um protótipo acadêmico. As instituições de demonstração são fictícias, e a aplicação não substitui validações sanitárias, acordos de transporte, confirmação presencial ou procedimentos legais necessários à doação de alimentos.
