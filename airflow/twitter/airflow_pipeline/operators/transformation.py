from pyspark.sql import functions as f
from pyspark.sql import SparkSession

from os.path import join
import argparse


def get_tweets_data(df):
    """
    Responsável por passar os dados no formato original.
    
    Output: pyspark dataframe
    """
    tweet_df = df.select(f.explode("data").alias("tweets"))\
                .select("tweets.author_id", "tweets.conversation_id",
                        "tweets.created_at", "tweets.id",
                        "tweets.public_metrics.*", "tweets.text")
    return tweet_df

def get_users_data(df):
    """
    Extrai os dados do usuário.

    Output: pyspark dataframe
    """
    user_df = df.select(f.explode("includes.users").alias("users")).select("users.*")
    return user_df

def export_json(df, dest):
    """
    Salva os dados no formato json.

    Input: 
        dest: Caminho onde vair ser salvo o json
    """
    df.coalesce(1).write.mode("overwrite").json(dest)

def twitter_transformation(spark, src, dest, process_date):
    """
    Carrega os dados e faz o processamento dos dados.
    
    Input:
        src: Caminho da origem dos dados
        dest: Caminho onde vai ser salvo os arquivos
        process_data: Caminho dos dados processados
    """
    df = spark.read.json(src)

    tweet_df = get_tweets_data(df)
    user_df = get_users_data(df)

    table_dest = join(dest, "{table_name}", f"process_date={process_date}")

    export_json(tweet_df, table_dest.format(table_name="tweet"))
    export_json(user_df, table_dest.format(table_name="user"))

if __name__ == "__main__":
    """
    Execução do código. Solicita a entrada dos argumentos que são obrigatórios.

    Input:
        src: Caminho da origem dos dados
        dest: Caminho onde vai ser salvo os arquivos
        process_data: Caminho dos dados processados
    """
    parser = argparse.ArgumentParser(
        description="Spark Twitter Transformation"
    )
    parser.add_argument("--src", required=True)
    parser.add_argument("--dest", required=True)
    parser.add_argument("--process-date", required=True)

    args = parser.parse_args()

    spark = SparkSession\
        .builder\
        .appName("twitter_transformation")\
        .getOrCreate()

    twitter_transformation(spark, args.src, args.dest, args.process_date)