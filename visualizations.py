import seaborn as sns
import pandas as pd

df=pd.read_csv("Device Profiles - Attacks.csv")
fig=sns.relplot(kind="line",data=df, x="intensity", y="average rtt", hue="attack", col="device", facet_kws={'sharey': True, 'sharex': False})
fig.savefig("rtt_profile.png")
fig=sns.relplot(kind="line",data=df, x="intensity", y="loss", hue="attack", col="device", facet_kws={'sharey': True, 'sharex': False})
fig.savefig("loss_profile.png")