# Código-fonte do MESAFARTAI

Esta pasta contém os módulos Python da aplicação.

| Arquivo | Responsabilidade |
|---|---|
| `app.py` | Interface Streamlit, navegação pública e área administrativa. |
| `auth.py` | Verificação de credenciais administrativas e limitação de tentativas. |
| `chatbot.py` | Máquina de estados da conversa, registro e consulta de doações. |
| `database.py` | Persistência SQLite, cadastro de ONGs, doações, itens e matches. |
| `entities.py` | Extração de alimentos, quantidades, unidades, datas e dados informados pelo usuário. |
| `geocoding.py` | Consulta de CEP/endereço e conversão em coordenadas geográficas. |
| `matchmaking.py` | Filtro de compatibilidade e ordenação de ONGs por distância. |
| `nlu.py` | Classificação de intenções com TF-IDF e Regressão Logística. |

## Execução

Execute os comandos a partir da raiz do repositório, com o ambiente virtual ativado:

```powershell
streamlit run src/app.py
```

A instalação, configuração dos segredos, estrutura do banco e orientações de privacidade estão documentadas no [README principal](../README.md) e em [docs/operacao_privacidade.md](../docs/operacao_privacidade.md).

**Importante:** não execute nem versione um arquivo `.streamlit/secrets.toml` com credenciais reais em repositório público. O banco `data/mesafartai.db` é local e não deve conter dados pessoais em commits.
