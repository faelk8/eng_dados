<a id="topo"></a>

<h1 align="center">
  <img src="../../image/airflow.png" alt="airflow" width=700 height=250px >
  <br>
  Extração de Dados 
</h1>

<div align="center">

<!-- [![Status](https://img.shields.io/badge/version-1.0-blue)]() -->
[![Status](https://img.shields.io/badge/status-active-success.svg)]()

</div>


Extração de Dados do Twitter utilizando o Airflow para agendar a tarefa. Os dados são coletados informando o assunto, data de início e fim.<br>


> [!IMPORTANT]  
> Os dados do código não são coletados diretamente do Twitter.


[Configurando o ambiente](#1)<br>
[Hook](#2)<br>
[Operador](#3)<br>
[DAG](#4)<br>
[Configurações](#5)<br>
[Arquitetura de Medalhão](#6)<br>
[Spark](#7)<br>


<a id="1"></a>

# Configurando o ambiente

<div align="right">
    <a href="#topo">Voltar ao topo</a>
</div>

* Criando ambiente virtual
    ```
    python3.9 -m venv venv 
    ```

* Ativando o ambiente virtual<br>
    ```
    source venv/bin/activate
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
  export AIRFLOW_HOME=$(pwd)/airflow_pipeline
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

# Hook

<div align="right">
    <a href="#topo">Voltar ao topo</a>
</div>

Gerencia as conexões, ficando responsavel por todas as conexões.<br>
Testando:
  ```
  export AIRFLOW_HOME=$(pwd)/airflow_pipeline
  python3.9 airflow_pipeline/hook/twitter_hook.py  
  ```
Configurando a conexão do Airflow com o Twitter

<h1 align="center">
  <img src="../../image/airflow_fluxo.png" alt="conexao" width=450px height=250px>
  <br>
</h1>

<a id="3"></a>

# Operador

<div align="right">
    <a href="#topo">Voltar ao topo</a>
</div>

Executa as tarefas.<br>
  * Atomidicade - O operador realiza apenas uma tarefa<br>
  * Idempotência - O operador semrpe obtém os mesmo resultados se receber os mesmo parâmetros<br>
  * Isolamento - O código roda de maneira individual, sem outros módulos ou operadores<br>
Faz a extração dos dados e salva na pasta datalake, uma pasta para cada dia da execução.

<a id="4"></a>

# DAG

<div align="right">
    <a href="#topo">Voltar ao topo</a>
</div>

Orquestra quando vai ser executada cada tarefa.

<a id="5"></a>

# Configurações

<div align="right">
    <a href="#topo">Voltar ao topo</a>
</div>

Ajuste nas configurações no arquivo `airflow.cfg`:
* load_examples = False | Não exibe os exemplos.

<a id="6"></a>

# Arquitetura de Medalhão
<div align="right">
    <a href="#topo">Voltar ao topo</a>
</div>

Separa os dados em camadas.<br>
 * Dados Bronze: Dados brutos<br>
 * Dados Prata: Dados limpos<br>
 * Dados Ouro: Dados processados para alimentar um dashboard<br>


<a id="7"></a>

# Spark

<div align="right">
    <a href="#topo">Voltar ao topo</a>
</div>

Utilizado para analisar os dados, exploração e transformação.