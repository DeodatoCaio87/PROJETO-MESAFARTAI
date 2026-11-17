# Operação, privacidade e publicação

Este documento complementa o README com orientações práticas para executar e apresentar o protótipo acadêmico MESAFARTAI.

## 1. Configuração local

- Utilize o ambiente virtual do projeto e instale as dependências de `requirements.txt`.
- Crie `.streamlit/secrets.toml` a partir de `.streamlit/secrets.toml.example`.
- Gere o hash da senha administrativa com `python scripts/gerar_hash_senha.py`.
- Informe um contato real no User-Agent do Nominatim e ajuste o contexto geográfico.
- Não compartilhe o arquivo real de segredos, a senha, o hash administrativo nem o banco de dados com terceiros.

## 2. Dados de demonstração

O projeto contém registros de demonstração de ONGs definidos em `src/database.py`. A inserção é opcional e controlada por `inserir_ongs_demonstracao` em `secrets.toml`. Quando habilitada, as instituições fictícias só são inseridas se a tabela estiver vazia.

Esses registros são exclusivamente demonstrativos. Não representam entidades reais e não devem ser usados para organizar doações reais.

## 3. Banco de dados e cópias de segurança

O SQLite é armazenado em `data/mesafartai.db`. O banco não é versionado no Git para evitar publicar dados pessoais ou registros operacionais.

Para preservar os dados:
1. Encerre a aplicação antes de copiar o arquivo do banco.
2. Armazene a cópia em local com acesso restrito.
3. Não envie o arquivo por canais públicos ou junto do repositório.
4. Para restauração, substitua o banco local somente com a aplicação encerrada.

O SQLite local é adequado ao protótipo e à execução em uma única instância. Em hospedagens com disco efêmero, o banco pode desaparecer após reinicializações ou novas implantações. Antes de disponibilizar o serviço continuamente, adote banco gerenciado ou volume persistente e defina rotina de backup.

## 4. Privacidade e proteção de dados

O fluxo solicita consentimento antes de registrar a doação e os dados de contato. A consulta pública por protocolo deve exibir somente informações necessárias para acompanhar a doação, sem expor nome ou e-mail do doador.

Boas práticas para a equipe:
- Acesso administrativo somente a integrantes autorizados.
- Senha administrativa forte e não compartilhada.
- Exportações CSV tratadas como dados restritos, pois podem conter informações operacionais e de contato.
- Não incluir dados pessoais reais em capturas de tela, exemplos de documentação, commits ou materiais públicos.
- Definir com a instituição responsável um prazo de retenção e um procedimento para atender pedidos de correção ou exclusão de dados antes de qualquer uso real.

Este protótipo não constitui, por si só, uma avaliação jurídica de conformidade com a LGPD. O uso real requer definição formal de controlador, finalidade, base legal, transparência, retenção, segurança e atendimento aos titulares.

## 5. Geolocalização e atribuição

O projeto consulta BrasilAPI, ViaCEP e Nominatim/OpenStreetMap. Resultados de CEP podem ser aproximados e devem ser conferidos antes de aceitar a sugestão logística.

Ao utilizar o Nominatim público:
- Configure um User-Agent identificável com contato válido.
- Respeite os limites e a política de uso do serviço.
- Preserve a atribuição © OpenStreetMap contributors nos mapas.
- Não trate coordenadas aproximadas como confirmação de endereço ou de disponibilidade para coleta.

## 6. Limites operacionais

- A sugestão de ONG é uma recomendação logística, não uma confirmação de retirada ou entrega.
- Doador e instituição devem combinar diretamente horário, transporte, condições e responsabilidade pela retirada.
- A aplicação não realiza inspeção sanitária nem certifica a qualidade dos alimentos.
- As instituições de demonstração são fictícias.
- O canal de ONG não registra solicitações de alimentos nesta versão; o cadastro de instituições é feito pela administração.

## 7. Antes de uma apresentação ou entrega

- Confirme que o README não contém campos de equipe em aberto.
- Verifique que o repositório não contém `secrets.toml`, banco SQLite, senhas ou dados pessoais.
- Execute a aplicação a partir do ambiente virtual e confirme a tela inicial.
- Utilize somente dados fictícios ou autorizados na demonstração.
- Informe ao professor que o projeto é um protótipo acadêmico e apresente com clareza os limites funcionais descritos neste documento.
