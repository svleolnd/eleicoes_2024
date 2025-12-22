# %% 
import pandas as pd
import sqlalchemy
import matplotlib.pyplot as plt
import seaborn as sns
from adjustText import adjust_text

#%%

with open("partidos.sql", "r") as open_file:
    query = open_file.read()

engine = sqlalchemy.create_engine("sqlite:///../data/database.db")

df = pd.read_sql_query(query, engine)
df = df.drop(df[df['SG_PARTIDO'] == 'PRD'].index)
df

#%%

txGenFeminino = df["totalGenFeminino"].sum() / df["totalCandidaturas"] .sum() 
txCorRacaPreta = df["totalCorRacaPreta"].sum() / df["totalCandidaturas"] .sum()
txCorRacaNaoBranca = df["totalCorRacaNaoBranca"].sum() / df["totalCandidaturas"] .sum() * 100
txCorRacaPretaParda = df["totalCorRacaPretaParda"].sum() / df["totalCandidaturas"] .sum() * 100

# %%
plt.figure(dpi=500)

sns.scatterplot(data=df, 
                 x='txGenFemininoBR',
                 y='txCorRacaPretaBR')

texts = []
for i in df['SG_PARTIDO']:
        data = df[df['SG_PARTIDO'] == i]
        x = data['txGenFemininoBR'].values[0]
        y = data['txCorRacaPretaBR'].values[0]
        texts.append(plt.text(x, y, i, fontsize=9))

adjust_text(texts, only_move={'points':'y', 'texts': 'x,y'}, arrowprops=dict(arrowstyle='->'))

plt.grid(True)
plt.title("Cor vs Genero - Eleições 2024")
plt.xlabel("Taxa de Mulheres")
plt.ylabel("Taxa de Pessoas Pretas")

plt.hlines(y=txCorRacaPreta, xmin=0.3, xmax=0.55, color='black', linestyles="--", label=f"Pessoas Pretas Geral: {100*txCorRacaPreta:.0f} %")
plt.vlines(x=txGenFeminino, ymin=0.03, ymax=0.35, color='tomato', linestyles="--", label=f"Mulheres Geral: {100*txGenFeminino:.0f} %")
plt.legend()

plt.savefig("../img/partidos_cor_raca_genero.png")

# %%
