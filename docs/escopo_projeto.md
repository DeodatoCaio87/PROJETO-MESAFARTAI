# MESAFARTAI — Escopo do Projeto

## 1. Problema de negócio

O desperdício de alimentos ocorre diariamente em supermercados, restaurantes, produtores, distribuidores e outros estabelecimentos. Alimentos próprios para consumo podem deixar de ser aproveitados por excesso de estoque, proximidade da validade ou dificuldades de distribuição.

Ao mesmo tempo, instituições sociais, abrigos, cozinhas comunitárias e projetos de assistência enfrentam dificuldades para obter alimentos suficientes para atender pessoas em situação de vulnerabilidade.

O MESAFARTAI busca aproximar doadores e instituições cadastradas, utilizando processamento de linguagem natural para interpretar informações de doações e recursos de geolocalização para apoiar o encaminhamento logístico.

O projeto está alinhado à **ODS 2 — Fome Zero e Agricultura Sustentável**, contribuindo como proposta tecnológica para reduzir desperdício e facilitar o aproveitamento de alimentos.

## 2. Público-alvo e papéis

### Doadores

Pessoas físicas e estabelecimentos que possuem alimentos disponíveis para doação, por exemplo:
- Supermercados;
- Restaurantes;
- Produtores e distribuidores;
- Comerciantes;
- Pessoas físicas.

Na versão atual, o doador inicia a conversa no chatbot, informa os alimentos, quantidades, validade e dados de contato/localização, concede consentimento e recebe um protocolo para acompanhar o registro.

### Instituições / ONGs

ONGs, abrigos, cozinhas comunitárias, bancos de alimentos e outras instituições sociais que recebem alimentos para distribuição ou preparo de refeições.

Na versão atual, as instituições são cadastradas e gerenciadas pela área administrativa. O sistema utiliza os dados cadastrados para procurar possíveis destinatárias. **Não existe nesta versão uma área autenticada nem um fluxo de solicitação de alimentos iniciado diretamente pela ONG.** A intenção textual `solicitar_alimentos` é reconhecida pelo classificador e respondida pelo chatbot com orientação para contato com a administração. Um portal de solicitações para ONGs é uma possibilidade de evolução futura, não uma funcionalidade concluída.

### Administrador

Responsável pelo acesso protegido à área administrativa, cadastro/edição/ativação/desativação das ONGs, acompanhamento das doações, consulta dos indicadores, exportação dos registros e atualização do status de coleta.

## 3. Objetivo e limites do sistema

O objetivo é apoiar o registro e o encaminhamento de doações de alimentos por meio de uma interface conversacional e de sugestões logísticas.

O sistema é um protótipo acadêmico. A sugestão de uma ONG não representa confirmação de transporte, inspeção sanitária, retirada ou entrega física. O doador e a instituição precisam combinar os detalhes operacionais diretamente.

## 4. Intenções tratadas pelo chatbot

O classificador NLU utiliza TF-IDF e Regressão Logística. Entre as intenções reconhecidas estão:

| Intenção | Comportamento na aplicação |
|---|---|
| `saudacao_ajuda` | Apresenta o assistente e orienta o usuário a informar o que deseja doar. |
| `cadastrar_doacao` | Inicia o fluxo de coleta dos dados de uma doação. |
| `solicitar_alimentos` | Informa que este canal é destinado a doadores e orienta a ONG a entrar em contato com a administração. Não registra uma solicitação. |
| `consultar_status` | Solicita o protocolo para consultar uma doação já registrada. |
| `aceitar_opcao` | Confirma a opção de ONG apresentada no contexto da conversa. |
| `recusar_opcao` | Registra a recusa e permite verificar uma próxima opção, quando disponível. |
| `fora_de_escopo` | Explica que o assistente está limitado às funções relacionadas a doações de alimentos. |
| `fallback` | Solicita que o usuário reformule a mensagem quando a confiança da classificação é insuficiente. |

As respostas afirmativas e negativas também são interpretadas pelo estado atual da conversa, com validação por expressões regulares e classificação restrita quando necessário.

## 5. Dados tratados

### Dados do doador e da localização

- Nome;
- E-mail;
- CEP e/ou endereço informado;
- Latitude e longitude, quando a geocodificação é possível;
- Mensagem original;
- Registro de consentimento.

O nome e o e-mail só são gravados depois do consentimento solicitado no fluxo.

### Dados da doação

- Protocolo;
- Descrição dos alimentos;
- Itens individualizados;
- Quantidades e unidades;
- Categorias dos alimentos;
- Data de validade, quando informada;
- Localização de origem, quando disponível;
- Status e data do registro.

### Dados das ONGs

- Nome e tipo de instituição;
- CEP, endereço e coordenadas;
- Telefone e e-mail de contato;
- Restrições alimentares;
- Horário de recebimento;
- Capacidade e observações;
- Situação ativa/inativa.

### Dados do encaminhamento (match)

- Doação relacionada;
- ONG sugerida;
- Ordem da opção;
- Distância estimada;
- Status da sugestão (sugerida, aceita ou recusada);
- Data da sugestão e da resposta.

## 6. Técnicas e tecnologias utilizadas

### NLU — Processamento de Linguagem Natural

O módulo `src/nlu.py` utiliza TF-IDF para transformar mensagens em atributos numéricos e Regressão Logística para classificar intenções. O treinamento utiliza `data/dataset_intencoes.csv`; existe também um conjunto separado em `data/dataset_teste.csv` para avaliação manual do classificador.

### Regex e extração de entidades

O módulo `src/entities.py` identifica informações estruturadas nas mensagens, como alimentos, quantidades, unidades, datas, CEP, e-mail e outros dados necessários ao fluxo. A conversa é conduzida por etapas para solicitar os dados que ainda estiverem faltando.

### Geocodificação

O módulo `src/geocoding.py` consulta cache local e serviços como BrasilAPI, ViaCEP e Nominatim/OpenStreetMap para obter endereço e coordenadas. Os resultados podem ter diferentes níveis de precisão e devem ser conferidos pelo usuário. O Nominatim exige identificação adequada no User-Agent, respeito à política de uso e atribuição dos dados cartográficos.

### Matchmaking geográfico

O módulo `src/matchmaking.py` calcula distâncias com a fórmula de Haversine e utiliza KNN para ordenar instituições por proximidade. Antes da classificação, instituições inativas e aquelas cujas restrições conflitam com as categorias da doação são descartadas. O sistema pode apresentar até duas opções ao doador.

### Banco de dados

O módulo `src/database.py` utiliza SQLite para armazenar ONGs, doações, itens, matches e cache de geocodificação. O banco é criado em `data/mesafartai.db` localmente.

### Interface e autenticação

O módulo `src/app.py` implementa as telas públicas de doação, acompanhamento por protocolo e informações sobre o funcionamento, além da área administrativa protegida. O módulo `src/auth.py` valida as credenciais administrativas com hash PBKDF2 e controle de tentativas.

## 7. Fluxo principal da doação

1. O doador abre a opção **Quero doar**.
2. Envia uma mensagem com os alimentos disponíveis.
3. O NLU identifica a intenção e o extrator reconhece os itens e quantidades.
4. O chatbot solicita as informações que faltarem, como validade, nome, e-mail e localização.
5. O sistema apresenta o resumo e solicita consentimento antes de persistir os dados pessoais e a doação.
6. A doação é registrada no SQLite e recebe um protocolo.
7. O matchmaking procura ONGs ativas, compatíveis com as categorias e restrições, e ordena as opções por distância.
8. O doador pode aceitar ou recusar a opção apresentada. Se houver outra instituição elegível, o sistema poderá oferecer uma segunda opção.
9. O usuário consulta o andamento usando o protocolo.
10. O administrador acompanha a doação e pode marcar como coletada uma doação previamente aceita.

Se não houver ONG compatível, ou se as opções forem recusadas, a doação permanece sem destino definido. O cadastro posterior de uma ONG não deve ser interpretado como uma aceitação automática de doação anterior; o encaminhamento precisa ser realizado pelo fluxo administrativo/conversacional disponível na versão instalada.

## 8. Estrutura de dados

O banco atual contém as tabelas:
- `ongs`: instituições destinatárias e seus dados operacionais;
- `doacoes`: registro principal, protocolo, dados do doador, consentimento e status;
- `itens_doacao`: alimentos, quantidades, unidades e categorias de cada doação;
- `matches`: opções de ONG sugeridas e respostas;
- `cache_geocodificacao`: resultados de localização reutilizáveis.

O arquivo SQLite é local e está excluído do Git. Em ambientes de hospedagem com armazenamento efêmero, é necessário configurar persistência externa antes de utilizar o sistema continuamente.

## 9. Identidade visual e prompt de geração do logotipo

A identidade visual do MESAFARTAI foi criada utilizando Inteligência Artificial.

**Prompt registrado para geração da logo:**

> Crie um logotipo profissional e moderno para um projeto chamado "MESAFARTAI — Logística e Inteligência Assistiva no Combate à Fome". O logo deve combinar elementos relacionados à alimentação, doação e combate à fome com elementos visuais de inteligência artificial e tecnologia assistiva. Utilize uma representação estilizada de alimentos, uma mão ou elemento de acolhimento e circuitos digitais de IA. O resultado deve transmitir solidariedade, tecnologia, logística, sustentabilidade e impacto social. Criar uma identidade visual limpa, moderna e adequada para um projeto acadêmico de tecnologia e inteligência artificial. O nome "MESAFARTAI" deve estar presente de forma legível no logotipo.

O arquivo de logo e os diagramas do projeto ficam na pasta `assets/`.

## 10. Evoluções possíveis (fora do escopo implementado)

- Portal autenticado para ONGs solicitarem alimentos e acompanharem solicitações;
- Persistência gerenciada para implantação em nuvem;
- Rotinas de auditoria, retenção e exclusão de dados pessoais;
- Integração com transportadoras ou gestão de retirada/entrega;
- Ampliação e atualização contínua do conjunto de frases de treinamento com dados reais anonimizados e consentidos.

Esses itens são possibilidades de evolução e não devem ser apresentados como recursos já entregues.
