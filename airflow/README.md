
# Criando Ambiente Virtual

Comando que permite ativar o repositório Ubuntu a ter várias versões do Python:
```
sudo add-apt-repository ppa:deadsnakes/ppa
```

Instalando Python:
```
sudo apt install python3.9
```

Pacotes do ambiente virtual:
```
sudo apt install python3.9-venv
```

Dentro da pasta de trabalho crie o ambiente virtual:
```
python3.9 -m venv airflow
```

Ativando o ambiente:
```
source airflow/bin/activate 
```

Instalando o Airflow:
```
pip install "apache-airflow[celery]==2.8.1" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.8.1/constraints-3.8.txt"
```

Exportando variável de ambiente Airflow Home:
```
export AIRFLOW_HOME=~/Documentos/github/eng_dados/airflow/airflow/
```
Iniciando o serviço:
```
airflow standalone
```


# dag
Exemplo simples sobre a ordem dos serviços.

# 01-Dados-Climaticos
Conectando na fonte de dados, busca os dados 
