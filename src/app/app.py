# %%
import sqlalchemy
import pandas    as pd
import streamlit as st

from pathlib import Path
from utils   import make_scatter, make_clusters
import gdown

import os 

#%%

app_path = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.dirname(app_path)
base_path = os.path.dirname(src_path)
data_path = os.path.join(base_path, "data")

database_path = os.path.join(data_path, "database.db")
engine = sqlalchemy.create_engine(f"sqlite:///{database_path}")

@st.cache_data(ttl=60*60*24)
def dowload_db():
    url_database = "https://drive.google.com/uc?export=download&id=1CMEZX2FK_gFyJEM4sqMNZ1ROvtDCKrTh"
    gdown.download(url_database, database_path, quiet=False)

@st.cache_data(ttl=60*60*24)
def create_df():
    query_path = os.path.join(app_path, "etl_partidos.sql")
    with open(query_path,  "r") as open_file:
        query = open_file.read()

    return pd.read_sql_query(query, engine)


# %%
dowload_db()
df = create_df()

welcome = """
# TSE Analytics - Eleições 2024

"""
st.markdown(welcome)

uf_options = df["SG_UF"].unique().tolist()
uf_options.remove("BR")
uf_options = ["BR"] + uf_options



estado = st.sidebar.selectbox(label="Estado", 
                      placeholder="Selecione o estado para o filtro",
                      options=uf_options)

size = st.sidebar.checkbox("Tamanho das bolhas")
cluster = st.sidebar.checkbox("Definir clusters")
n_cluster = st.sidebar.number_input("Quantidade clusters", 
                                    value=6, format="%d", 
                                    max_value=10, 
                                    min_value=1)

data = df[df["SG_UF"]==estado].copy()

if cluster:
    data = make_clusters(data, n_cluster)

fig = make_scatter(data, cluster=cluster, size=size)

st.pyplot(fig)
