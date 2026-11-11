import sys, re, numpy as np, pandas as pd
from sklearn.model_selection import train_test_split
from transformers import AutoTokenizer
d = pd.read_csv(sys.argv[1]); tok = AutoTokenizer.from_pretrained("neuralmind/bert-base-portuguese-cased")
tr, te = train_test_split(d, test_size=0.2, random_state=42, stratify=d["classe"]); am = te.sample(300, random_state=42)
def info(df):
    df = df.copy()
    df["caps"] = df["texto"].apply(lambda t: sum(c.isupper() for c in t) / max(1, sum(c.isalpha() for c in t)) > 0.8)
    df["ntok"] = df["texto"].apply(lambda t: len(tok(t)["input_ids"]))
    ids = df["texto"].apply(lambda t: tok(t, truncation=True, max_length=64)["input_ids"])
    df["visto"] = ids.apply(lambda i: tok.decode(i, skip_special_tokens=True).lower())
    return df
P_SEG = r"aterramento|guarda.?corpo|prote[cç][aã]o|bloqueio|etiquetagem"
for nome, df in [("base", d), ("amostra", am)]:
    x = info(df)
    print(f"[{nome}] caixa alta: {x.caps.sum()} ({100*x.caps.mean():.1f}%)")
    print("   tokens medios caixa alta x normal: %.1f x %.1f" % (x[x.caps].ntok.mean(), x[~x.caps].ntok.mean()))
    tr_ = x[x.ntok > 64]
    print("   truncados:", len(tr_), "| desses em caixa alta:", int(tr_.caps.sum()))
    print("   classe dos truncados:", tr_.classe.value_counts().to_dict())
    perde = tr_[tr_.texto.str.lower().str.contains(P_SEG) & ~tr_.visto.str.contains(P_SEG)]
    print("   truncados que PERDEM a pista de seguranca no corte:", len(perde), perde.classe.value_counts().to_dict())
    for t in perde.texto.head(3): print("     -", t)
    print("   caixa alta por classe (%):", (x.groupby("classe").caps.mean()*100).round(1).to_dict())
