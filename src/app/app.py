# %%
import pandas as pd
import sqlalchemy
from pathlib import Path
import streamlit as st

from utils import make_scatter, make_clusters


#%%
engine = sqlalchemy.create_engine("sqlite:///../../data/database.db")

with open('etl_partidos.sql',  "r") as open_file:
    query = open_file.read()

df = pd.read_sql_query(query, engine)


# %%
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
