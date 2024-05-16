<a id="topo"></a>

<h1 align="center">
  <img src="../../image/yfinance.png" alt="airflow" width=700 height=250px >
  <br>
  Extraindo Cotações da Bolsa de Valores
</h1>

<div align="center">

<!-- [![Status](https://img.shields.io/badge/version-1.0-blue)]() -->
[![Status](https://img.shields.io/badge/status-active-success.svg)]()

</div>

Coletando dados do mercado financeiro.

[01 - Configurando o ambiente](#1)<br>
[02 - Local Executor](#2)<br>
[03 - Configurando Tarefas em Paralelo](#3)<br>
[04 - Celery](#4)<br>

<a id="1"></a>

# 01 - Configurando o ambiente

<div align="right">
    <a href="#topo">Voltar ao topo</a>
</div>

* Adicionando repositório
  ```
  sudo add-apt-repository ppa:deadsnakes/ppa
  ```

* Criando ambiente virtual
    ```
    python3.9 -m venv venv
    ```

* Ativando o ambiente virtual<br>
    ```
    source venv/bin/activate
    ```

* Instalando bibliotecas
  ```
  pip install --upgrade pip
  pip install yfinance
  ```

* Definindo a versão
  ```
  AIRFLOW_VERSION=2.9.1

  PYTHON_VERSION=3.9

  CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"

  pip install "apache-airflow[postgres,celery,redis]==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"

  airflow db upgrade
  ```

* Exportando a variável de ambiente e criando uma pasta para colocar todos os arquivos do Airflow
  ```
  export AIRFLOW_HOME=$(pwd)/agenda
  ```

* Inciando o banco [PostgreSQL](#3)
  ```
  airflow db init
  ```

* Iniciando o Airflow
  ```
  airflow standalone
  ```

* Acessando
  http://localhost:8080

* Finalizar
  ```
  ctrl + c
  . deactivate
  ```

<a id="2"></a>

# 02 - Local Executor

<div align="right">
    <a href="#topo">Voltar ao topo</a>
</div>

O Executor Local oferece paralelismo na execução das tarefas e para isso precisamos configurar um banco de dados que aceite mais de uma conexão simultânea, como o Postgres.

Vantagens
* Fácil de configurar.
* Oferece paralelismo.

Desvantagem
* Depende do funcionamento de uma única máquina.

Quando utilizar
* Cargs de trabalho de produção leves.
* Para realizar múltiplas tarefas paralelas e/ou DAGs.
* Para testes.

Executores locais:
* Executor Sequencial.
* Executor Local.

Executores remotos:
* Executor Celery.
* Executor Kubernetes.
* Executor CeleryKubernetes.
* Executor LocalKubernetes.
* Executor Dask.


<a id="3"></a>

# 03 - Configurando Tarefas em Paralelo
<div align="right">
    <a href="#topo">Voltar ao topo</a>
</div>


* Configurando o Airflow
  ```
  executor = LocalExecutor
  ```

* Instalando o PostgreSQL
  ```
  # instalando
  sudo apt install postgresql postgresql-contrib
  # acessando o usuário  
  sudo -i -u postgres
  # criando o banco de dados
  createdb airflow_db
  # acessando o banco
  psql airflow_db
  # criando usuario e senha
  CREATE USER airflow_user WITH PASSWORD 'airflow_pass';
  # configurando privilégios
  GRANT ALL PRIVILEGES ON DATABASE airflow_db TO airflow_user;

  ```

* Configurando o Postgresql no Airflow
  ```
  sql_alchemy_conn = postgresql+psycopg2://airflow_user:airflow_pass@localhost/airflow_db
  ```
* Inciando o banco
  ```
  airflow db init
  ```

> [!NOTE]  
> Quantidade máxima de tarefas que pode ser executadas em pararelo <br>
> max_active_tasks_per_dag = 16<br>
> max_active_tasks_per_dag = 2<br>
>
> Quantidade máxima de DAGs que pode ser executadas em pararelo <br>
> max_active_runs_per_dag = 16<br>
> max_active_runs_per_dag = 4<br>
>
> Airflow Webserver, para evitar erros de update ajuste a variável <br>
> update_fab_perms = False <br>

<a id='4'></a>

# 04 - Celery

<div align="right">
    <a href="#topo">Voltar ao topo</a>
</div>

Trabalha com filas de tarefas, mecanismo que admite a distribuição dessas tarefas em processos distintos, sendo cada um executado por diferentes workers. Os workers funcionam, basicamente, como máquinas individuais que aguardam as tarefas chegarem na fila para executá-las.

O Celery nos permite criar workers em máquinas diferentes, gerando o processamento distribuído de tarefas, o que resolve o problema de depender unicamente de um ponto de falha. Sendo assim, caso uma máquina venha a falhar, somente um worker também falhará, e as tarefas executadas por ele serão enviadas para um worker que permanece em funcionamento, impedindo uma quebra no fluxo de execução dessas tarefas.

Vantagens:
  * Oferece paralelismo
  * Alta disponibilidade
  * Processamento distríbuido

Desvantagens:
  * Mais trabalhoso para configurar
  * Manutenção do worker

Quantdo utiliza:
  * Executar DAGs em produção
  * Carga de trabalho mais pesadas

Download do Redis [aqui](https://caelum-online-public.s3.amazonaws.com/2606-aprofundando-airflow-executor-celery/01/redis-7.0.4.tar.gz).

* Instalando
  ```
  # descompactar
  tar -xf redis-7.0.4.tar.gz
  # entrando na pasta
  cd redis-7.0.4/
  # módulos
  make
  # instalando
  sudo make install
  # verificando se foi instalado
  redis-server
  ```
* Configurando o Airflow
  ```
  executor = CeleryExecutor
  result_backend = db+postgresql://airflow_user:airflow_pass@localhost/airflow_db
  broker_url = redis://0.0.0.0:6379/0
  ```
## Iniciando o Serviço com Celery
  > [!NOTE]  
  > Airflow Webserver, para evitar erros de update ajusta a variável <br>
  > update_fab_perms = False <br>
  >
  > Quantidade máxima de tarefas por worker n+1, para corretaconfiguração o **worker_concurrency** receber o valor do **max_active_tasks_per_dag** +1
  > max_active_tasks_per_dag = 2<br>
  > worker_concurrency = 3<br>
  > Com isso vai ser executado no máximo 3 tarefas ao mesmo tempo.<br>
  >
  * No terminal
    ```
    redis-server
    ```
  * Em outro terminal na pasta do projeto
    ```
    source venv/bin/activate
    export AIRFLOW_HOME=$(pwd)/agenda
    airflow scheduler
    ```

  * Em outro terminal na pasta do projeto
    ```
    source venv/bin/activate
    export AIRFLOW_HOME=$(pwd)/agenda
    airflow webserver
    ```
  
  * Dashboard - Em outro terminal na pasta do projeto, no terminal vai mostrar o url de acesso para o celery
    ```
    source venv/bin/activate
    export AIRFLOW_HOME=$(pwd)/agenda
    airflow celery flower
    ```

  * Em outro terminal na pasta do projeto, agora irá executar as tarefas
    ```
    source venv/bin/activate
    export AIRFLOW_HOME=$(pwd)/agenda
    airflow celery worker
    ```

  * Acessando
    http://localhost:8080

***
<a href="#topo">Voltar ao topo</a>
