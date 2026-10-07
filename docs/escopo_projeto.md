# MESAFARTAI — Escopo do Projeto

## 1. Problema de Negócio

O desperdício de alimentos ocorre diariamente em supermercados, restaurantes, produtores, distribuidores e outros estabelecimentos. Produtos próximos da data de validade, com pequenas imperfeições estéticas ou provenientes de excesso de estoque podem deixar de ser comercializados mesmo estando próprios para consumo.

Ao mesmo tempo, instituições como ONGs, abrigos, cozinhas comunitárias e projetos sociais enfrentam dificuldades para obter alimentos suficientes para atender pessoas em situação de vulnerabilidade.

O MESAFARTAI foi desenvolvido com o objetivo de aproximar doadores e instituições que necessitam de alimentos, utilizando Inteligência Artificial para auxiliar na interpretação das mensagens, identificação das informações das doações e encaminhamento logístico.

O projeto está alinhado ao **ODS 2 — Fome Zero e Agricultura Sustentável**, contribuindo para a redução do desperdício e para o melhor aproveitamento dos alimentos.

---

## 2. Público-Alvo

### Doadores

Estabelecimentos e pessoas que possuem alimentos disponíveis para doação, como:

* Supermercados;
* Restaurantes;
* Produtores;
* Distribuidores;
* Comerciantes;
* Pessoas físicas.

O doador poderá informar, por meio de uma conversa, quais alimentos possui, suas quantidades e informações relacionadas à validade.

### Instituições / ONGs

Instituições que recebem alimentos para distribuição ou preparo de refeições, como:

* ONGs;
* Abrigos;
* Cozinhas comunitárias;
* Instituições sociais;
* Projetos de assistência alimentar.

Essas instituições poderão solicitar alimentos e acompanhar informações relacionadas às solicitações e doações.

---

## 3. Objetivo do Sistema

O MESAFARTAI tem como objetivo utilizar Inteligência Artificial para facilitar o processo de conexão entre doadores de alimentos e instituições que necessitam desses recursos.

O sistema utiliza processamento de linguagem natural (NLU) para interpretar mensagens enviadas pelos usuários, identificar suas intenções e extrair informações relevantes.

Após a identificação dos dados da doação, o sistema poderá utilizar informações de localização e distância para auxiliar na escolha de uma instituição adequada.

---

## 4. Intenções do Chatbot

O chatbot trabalhará inicialmente com quatro intenções principais:

### `cadastrar_doacao`

Utilizada quando o usuário deseja informar alimentos disponíveis para doação.

Exemplo:

> "Tenho 20 kg de arroz e 10 caixas de leite para doar."

### `solicitar_alimentos`

Utilizada quando uma instituição deseja solicitar alimentos.

Exemplo:

> "Precisamos de arroz e feijão para nossa cozinha comunitária."

### `consultar_status`

Utilizada quando o usuário deseja consultar o andamento de uma doação ou solicitação.

Exemplo:

> "Gostaria de saber o status da minha doação."

### `fora_de_escopo`

Utilizada quando a mensagem não está relacionada às funcionalidades do MESAFARTAI.

Exemplo:

> "Qual é a previsão do tempo para amanhã?"

---

## 5. Informações Coletadas

Durante a conversa, o sistema poderá identificar e armazenar informações necessárias para realizar o encaminhamento das doações.

### Informações do usuário

* Nome;
* Tipo de usuário (DOADOR ou ONG);
* CEP;
* Latitude;
* Longitude;
* Telefone.

### Informações da doação

* Descrição do alimento;
* Quantidade em quilogramas;
* Data de validade;
* Status da doação.

### Informações do Match

* Identificação da doação;
* Identificação da ONG;
* Distância entre doador e instituição;
* Data do encaminhamento.

---

## 6. Inteligência Artificial Utilizada

O sistema será desenvolvido utilizando diferentes técnicas de Inteligência Artificial e processamento de dados.

### NLU

O módulo de NLU será responsável por identificar a intenção presente na mensagem do usuário.

As intenções previstas são:

* `cadastrar_doacao`;
* `solicitar_alimentos`;
* `consultar_status`;
* `fora_de_escopo`.

### Regex

Expressões regulares serão utilizadas para identificar informações estruturadas presentes nas mensagens, como:

* Quantidade de alimentos;
* Unidades;
* Datas;
* Informações relacionadas aos produtos.

### KNN

O algoritmo KNN será utilizado para auxiliar no processo de matchmaking entre doações e instituições, considerando a proximidade geográfica.

### SQLite

O sistema utilizará SQLite para armazenar os dados dos usuários, doações e matches.

---

## 7. Fluxo Geral

O fluxo básico do MESAFARTAI será:

1. O usuário envia uma mensagem ao chatbot;
2. O sistema identifica a intenção da mensagem;
3. Caso seja uma doação, os dados relevantes são extraídos;
4. As informações são armazenadas no banco de dados;
5. O sistema identifica instituições compatíveis;
6. O KNN auxilia na escolha considerando a proximidade;
7. O sistema apresenta o encaminhamento ao usuário.

---

## 8. Prompt Utilizado para Geração da Logo

A identidade visual do MESAFARTAI foi criada utilizando Inteligência Artificial.

**Prompt utilizado:**

> Crie um logotipo profissional e moderno para um projeto chamado "MESAFARTAI — Logística e Inteligência Assistiva no Combate à Fome". O logo deve combinar elementos relacionados à alimentação, doação e combate à fome com elementos visuais de inteligência artificial e tecnologia assistiva. Utilize uma representação estilizada de alimentos, uma mão ou elemento de acolhimento e circuitos digitais de IA. O resultado deve transmitir solidariedade, tecnologia, logística, sustentabilidade e impacto social. Criar uma identidade visual limpa, moderna e adequada para um projeto acadêmico de tecnologia e inteligência artificial. O nome "MESAFARTAI" deve estar presente de forma legível no logotipo.
