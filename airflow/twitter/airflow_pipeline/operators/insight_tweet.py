import argparse
from os.path import join

from pyspark.sql import SparkSession
from pyspark.sql import functions as f

def get_tweet_conversas(df_tweet):
    """
    Transforma os dados para alimentar o dashboard.

    Input:
        df_tweet: spark dataframe
    """
    return df_tweet.alias("tweet")\
        .groupBy(f.to_date("created_at").alias("created_date"))\
        .agg(
            f.countDistinct("author_id").alias("n_tweets"),
            f.sum("like_count").alias("n_like"),
            f.sum("quote_count").alias("n_quote"),
            f.sum("reply_count").alias("n_reply"),
            f.sum("retweet_count").alias("n_retweet")
        ).withColumn("weekday", f.date_format("created_date", "E"))

def export_json(df, dest):
    """
    Salva os dados.

    Input: 
        df: spark dataframe
        dest: local onde será salvo os arquivos
    """
    df.coalesce(1).write.mode("overwrite").json(dest)

def twitter_insight(spark, src, dest, process_date):
    """
    Carrega os dados em seguida faz a transformação e salva.

    Input:
        spark: sessão spark
        src: dados de origem
        dest: local onde vai salvar os dados
        process_date: data de processamento
    """
    df_tweet = spark.read.json(join(src, 'tweet'))
    tweet_conversas = get_tweet_conversas(df_tweet)
    export_json(tweet_conversas, join(dest, f"process_date={process_date}"))

if __name__ == "__main__":
    """
    Execução do código. Solicita a entrada dos argumentos que são obrigatórios.

    Input:
        src: Caminho da origem dos dados
        dest: Caminho onde vai ser salvo os arquivos
        process_data: Caminho dos dados processados
    """
    parser = argparse.ArgumentParser(
        description="Spark Twitter Transformation Silver"
    )
    parser.add_argument("--src", required=True)
    parser.add_argument("--dest", required=True)
    parser.add_argument("--process-date", required=True)
    args = parser.parse_args()

    spark = SparkSession\
        .builder\
        .appName("twitter_transformation")\
        .getOrCreate()

    twitter_insight(spark, args.src, args.dest, args.process_date)