#%%
import pandas as pd
import sqlalchemy
import matplotlib.pyplot as plt
import seaborn as sn
from adjustText import adjust_text


#%%

with open("partidos.sql", "r") as open_file:
    query = open_file.read()
    
engine = sqlalchemy.create_engine("sqlite:///../data/database.db")

df = pd.read_sql_query(query, engine)

df.head()
# %%

txGenFeminino = df['totalGenFeminino'].sum() / df['totalCandidaturas'].sum()
txCorRacaPreta = df['totalCorRacaPreta'].sum() / df['totalCandidaturas'].sum()
txCorRacaNaoBranca = df['totalCorRacaNaoBranca'].sum() / df['totalCandidaturas'].sum()
txCorRacaPretaParda = df['totalCorRacaPretaParda'].sum() / df['totalCandidaturas'].sum()

# %%
plt.figure(dpi=500)


sn.scatterplot(data=df, 
               x="txGenFemininoBR", 
               y="txCorRacaPretaBR",
              )

text = []
for i in df["SG_PARTIDO"]:
    data = df[df['SG_PARTIDO']==i]
    x = data['txGenFemininoBR']
    y = data['txCorRacaPretaBR']
    text.append(plt.text(x, y, i, fontsize=9))

adjust_text(text, only_move={'points': 'y', 'texts': 'xy'}, arrowprops=dict(arrowstyle='->'))
    
plt.grid(True)
plt.title("Partidos: Cor vs Gênero - Eleições 2024")
plt.xlabel("Taxa de Mulheres")
plt.ylabel("Taxa de Pessoas Pretas")

plt.hlines(y=txCorRacaPreta, xmin=0.3, xmax=0.55, colors='black', alpha=0.6, linestyles='--', label=f'Taxa Pretos: {100*txCorRacaPreta:.2f}%')
plt.vlines(x=txGenFeminino, ymin=0.05, ymax=0.35, colors='tomato', alpha=0.6, linestyles='--', label=f'Taxa Mulheres: {100*txGenFeminino:.2f}%')

plt.legend()

plt.savefig("../img/partidos_cor_raca_genero.png")
 # %%
plt.figure(dpi=500)


sn.scatterplot(data=df, 
               x="txGenFemininoBR", 
               y="txCorRacaPretaBR",
               size="totalCandidaturas",
               sizes=(15,200)
              )

text = []
for i in df["SG_PARTIDO"]:
    data = df[df['SG_PARTIDO']==i]
    x = data['txGenFemininoBR']
    y = data['txCorRacaPretaBR']
    text.append(plt.text(x, y, i, fontsize=9))

adjust_text(text, only_move={'points': 'y', 'texts': 'xy'}, arrowprops=dict(arrowstyle='->'))
    
plt.grid(True)
plt.title("Partidos: Cor vs Gênero - Eleições 2024")
plt.xlabel("Taxa de Mulheres")
plt.ylabel("Taxa de Pessoas Pretas")

plt.hlines(y=txCorRacaPreta, xmin=0.3, xmax=0.55, colors='black', alpha=0.6, linestyles='--', label=f'Taxa Pretos: {100*txCorRacaPreta:.2f}%')
plt.vlines(x=txGenFeminino, ymin=0.05, ymax=0.35, colors='tomato', alpha=0.6, linestyles='--', label=f'Taxa Mulheres: {100*txGenFeminino:.2f}%')

handles, labels = plt.gca().get_legend_handles_labels()
handles = handles[5:]
labels = labels[5:]

plt.legend(handles=handles, labels=labels)

plt.savefig("../img/partidos_cor_raca_genero_bolha_size.png")
# %%

from sklearn import cluster

#%% 
X = df[["txGenFemininoBR", "txCorRacaPretaBR"]]
model = cluster.KMeans(n_clusters=6)
model.fit(X)

df["clusterBR"] = model.labels_

df.groupby(["clusterBR"])["txGenFemininoBR"].count()

# %%

plt.figure(dpi=500)

sn.scatterplot(data=df, 
               x="txGenFemininoBR", 
               y="txCorRacaPretaBR",
               size="totalCandidaturas",
               sizes=(15,200),
               hue="clusterBR",
               palette="viridis",
               alpha=0.6,
              )

text = []
for i in df["SG_PARTIDO"]:
    data = df[df['SG_PARTIDO']==i]
    x = data['txGenFemininoBR']
    y = data['txCorRacaPretaBR']
    text.append(plt.text(x, y, i, fontsize=9))

adjust_text(text, only_move={'points': 'y', 'texts': 'xy'}, arrowprops=dict(arrowstyle='->'))
    
plt.grid(True)
plt.title("Maior a bolha, maior o número de candidatos", fontdict={"size":9})
plt.suptitle("Partidos: Cor vs Gênero - Eleições 2024")
plt.xlabel("Taxa de Mulheres")
plt.ylabel("Taxa de Pessoas Pretas")

plt.hlines(y=txCorRacaPreta, xmin=0.3, xmax=0.55, colors='black', alpha=0.6, linestyles='--', label=f'Taxa Pretos: {100*txCorRacaPreta:.2f}%')
plt.vlines(x=txGenFeminino, ymin=0.05, ymax=0.35, colors='tomato', alpha=0.6, linestyles='--', label=f'Taxa Mulheres: {100*txGenFeminino:.2f}%')

handles, labels = plt.gca().get_legend_handles_labels()
handles = handles[13:]
labels = labels[13:]

plt.legend(handles=handles, labels=labels)

plt.savefig("../img/partidos_cor_raca_genero_clusterBR_size.png")

# %%

df.to_csv("../data/dataframe_old.csv", sep=";")

# %%
