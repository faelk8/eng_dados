import yfinance
from airflow.decorators import dag, task
from airflow.macros import ds_add
from pathlib import Path
import pendulum

TICKERS = [
            "AAPL",
            "MSFT",
            "GOOG",
            "TSLA"
            ]

@task()
def get_history(ticker, ds=None, ds_nodash=None):
    """
    Coleta os dados do dia anterio e armazena em um csv.

    Input:
        ticker: código da ação
        ds: data separada por "-"
        ds_nodash: data completa sem "-"
    """
    file_path = f"/home/rafael/MEGA/github/eng_dados/airflow/yfinance/dados/stocks/{ticker}//{ticker}_{ds_nodash}.csv"
    # cria a pasta
    Path(file_path).parent.mkdir(parents=True, exist_ok=True)
    yfinance.Ticker(ticker).history(period="1d", interval="1h", start=ds_add(ds, -1), end=ds, prepost=True).to_csv(file_path)

@dag(
    # define a data para inicio da coleta dos dados
    schedule_interval = "0 0 * * 2-6",
    start_data = pendulum.datetime(2024, 5, 12, tz="UTC"), catchup=True)

def get_stocks_dag():
    """
    Percorre a lista e baixa os dados
    """
    for ticker in TICKERS:
        get_history.override(task_id=ticker)(ticker)

dag = get_stocks_dag()