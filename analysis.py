import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import cycler

# |%%--%%| <SUpxB8QJNA|3mwzKxMYH6>

colors = cycler(
    "color", ["#EE6666", "#3388BB", "#9988DD", "#EECC55", "#88BB44", "#FFBBBB"]
)
plt.rc(
    "axes",
    facecolor="#E6E6E6",
    edgecolor="none",
    axisbelow=True,
    grid=True,
    prop_cycle=colors,
)
plt.rc("grid", color="w", linestyle="solid")
plt.rc("xtick", direction="out", color="gray")
plt.rc("ytick", direction="out", color="gray")
plt.rc("patch", edgecolor="#E6E6E6")
plt.rc("lines", linewidth=2)

# |%%--%%| <3mwzKxMYH6|kFd9lVqhXa>

plt.rc("axes", titlecolor="#000000")
plt.rc("axes", labelcolor="#000000")

# |%%--%%| <kFd9lVqhXa|rwh5lbXU7M>

df: pd.DataFrame = pd.read_csv("data.csv")
df.head()
# |%%--%%| <rwh5lbXU7M|PC3WIbPRBY>

df.info()

# |%%--%%| <PC3WIbPRBY|mbJSqTUvQG>

df["Tamanho"] = 2 ** df["Instância"]

# |%%--%%| <mbJSqTUvQG|TnhTpLxNf8>

df_tatt = df.loc[df["Algoritmo"] == "Twice Around The Tree"]
df_tatt

# |%%--%%| <TnhTpLxNf8|O81EZ9aDPc>

df_tatt_euc = df_tatt.loc[df_tatt["Distância"] == "Euclidiana"]
df_tatt_euc

# |%%--%%| <O81EZ9aDPc|SPe4x9f9Pm>

df_tatt_man = df_tatt.loc[df_tatt["Distância"] == "Manhattan"]
df_tatt_man

# |%%--%%| <SPe4x9f9Pm|3kMexBCJHJ>

ax = plt.gca()
df_tatt_euc.plot(
    x="Instância",
    y="Custo",
    ax=ax,
)
df_tatt_man.plot(
    x="Instância",
    y="Custo",
    ylabel="Custo",
    ax=ax,
)
plt.title("Custo Euclidiana vs Manhattan")
plt.legend(["Euclidiana", "Manhattan"])
plt.savefig("met_custo_vs.png")

# |%%--%%| <3kMexBCJHJ|zEmaaqvNOs>

ax = plt.gca()
df_tatt_euc.plot(
    x="Tamanho",
    y="Tempo",
    ax=ax,
)
df_tatt_man.plot(
    x="Tamanho",
    y="Tempo",
    ylabel="Tempo",
    ax=ax,
)
plt.title("Custo Euclidiana vs Manhattan")
plt.legend(["Euclidiana", "Manhattan"])
plt.savefig("met_tempo_vs.png")

# |%%--%%| <zEmaaqvNOs|xUqhg2no4D>

df_chris = df.loc[df["Algoritmo"] == "Christofides"]
df_chris
# |%%--%%| <xUqhg2no4D|5yBjgLf9yx>

df_chris_euc = df_chris.loc[df_chris["Distância"] == "Euclidiana"]
df_chris_euc

# |%%--%%| <5yBjgLf9yx|0vjOm38vKO>

df_chris_man = df_chris.loc[df_chris["Distância"] == "Manhattan"]
df_chris_man
# |%%--%%| <0vjOm38vKO|ExPPAyViMe>

ax = plt.gca()
df_tatt_euc.plot(
    x="Instância",
    y="Custo",
    ax=ax,
)
df_chris_euc.plot(
    x="Instância",
    y="Custo",
    ylabel="Custo",
    ax=ax,
)
plt.title("Custo Christofides vs TATT")
plt.legend(["TATT", "Christofides"])
plt.savefig("custo_vs.png")
# |%%--%%| <ExPPAyViMe|f8vz81wBky>

ax = plt.gca()
df_tatt_euc.plot(
    x="Tamanho",
    y="Tempo",
    ax=ax,
)
df_chris_euc.plot(
    x="Tamanho",
    y="Tempo",
    ylabel="Tempo",
    ax=ax,
)
plt.title("Tempo Christofides vs TATT")
plt.legend(["TATT", "Christofides"])
plt.savefig("tempo_vs.png")
# |%%--%%| <f8vz81wBky|JS3SpUV3KJ>

df_tatt_euc["Custo"].div(df_chris_euc["Custo"].values).mean()
