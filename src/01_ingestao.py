# %%
import pandas as pd
import sqlalchemy
import json

# %%

# criando uma conexão com o banco de dados
engine = sqlalchemy.create_engine("sqlite:///../data/database.db")

with open("ingestoes.json", "r") as open_file:
    ingestoes = json.load(open_file)

for i in ingestoes:
    path = i['path']
    df = pd.read_csv(path, encoding='latin-1', sep=';')
    df.to_sql(i["table"], if_exists="replace", con=engine, index=False)
