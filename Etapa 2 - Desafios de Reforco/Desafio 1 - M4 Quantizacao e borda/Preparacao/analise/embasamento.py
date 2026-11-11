"""Embasamento pre-E1 do Desafio 1 (M4). Nenhum modelo e treinado nem medido.
Uso: python embasamento.py <caminho do relatos_de_campo.csv>"""
import re
import sys

import numpy as np
import pandas as pd
import torch
from sklearn.model_selection import train_test_split

CSV = sys.argv[1]

print("=== 1. Notebook de estudo: celulas 5 e 7 (quantizacao linear 768x768) ===")
torch.manual_seed(0)
pesos = torch.randn(768, 768) * 0.05
escala = pesos.abs().max() / 127
inteiros = torch.round(pesos / escala).to(torch.int8)
de_volta = inteiros.float() * escala
print("bytes float32:", pesos.element_size() * pesos.numel())
print("bytes int8:   ", inteiros.element_size() * inteiros.numel())
print("escala:", escala.item())
print("erro medio absoluto:", (pesos - de_volta).abs().mean().item())
print("maior erro:", (pesos - de_volta).abs().max().item(), "| escala/2 =", (escala / 2).item())
com_extremo = pesos.clone()
com_extremo[0, 0] = 5.0
escala2 = com_extremo.abs().max() / 127
de_volta2 = torch.round(com_extremo / escala2).to(torch.int8).float() * escala2
print("[com peso extremo] escala:", escala2.item())
print("[com peso extremo] erro medio absoluto:", (com_extremo - de_volta2).abs().mean().item())
q = torch.round(com_extremo / escala2)
print("[com peso extremo] fracao de pesos que viram 0:", (q == 0).float().mean().item())
print("[com peso extremo] niveis int8 distintos usados:", q.unique().numel(), "(antes:", inteiros.unique().numel(), ")")

print("\n=== 2. Dados e divisao identica ao notebook 02 (etapa 3) ===")
CLASSES = ["eletrica", "mecanica", "hidraulica", "instrumentacao", "seguranca"]
SEMENTE = 42
dados = pd.read_csv(CSV)
treino, teste = train_test_split(dados, test_size=0.2, random_state=SEMENTE, stratify=dados["classe"])
AMOSTRA = teste.sample(300, random_state=SEMENTE)
print("treino", len(treino), "| teste", len(teste), "| amostra", len(AMOSTRA))
print(AMOSTRA["classe"].value_counts().reindex(CLASSES).to_string())

print("\n=== 3. Tokenizador BERTimbau: truncamento em max_length=64 ===")
from transformers import AutoTokenizer
tok = AutoTokenizer.from_pretrained("neuralmind/bert-base-portuguese-cased")
n_tok = np.array([len(tok(t)["input_ids"]) for t in dados["texto"]])
print("tokens por relato (com [CLS]/[SEP]): media %.1f | mediana %d | p95 %d | max %d"
      % (n_tok.mean(), np.median(n_tok), np.percentile(n_tok, 95), n_tok.max()))
print("relatos com > 64 tokens (seriam truncados):", int((n_tok > 64).sum()))
n_tok_am = np.array([len(tok(t)["input_ids"]) for t in AMOSTRA["texto"]])
print("na amostra de 300: media %.1f | max %d" % (n_tok_am.mean(), n_tok_am.max()))
ex = dados["texto"].iloc[int(np.argmax(n_tok))]
print("maior relato:", ex)
print("  tokens:", tok.tokenize(ex))
palavras = sum(len(t.split()) for t in dados["texto"])
print("fertilidade (subtokens por palavra): %.2f" % ((n_tok - 2).sum() / palavras))
oov_like = ["rolate", "perot", "paienl", "cntator", "etqiuetagem", "bba", "mot."]
for w in oov_like:
    print(f"  {w!r} -> {tok.tokenize(w)}")

print("\n=== 4. Vocabulario: palavras da amostra que o TF-IDF nunca viu no treino ===")
tokenizar = re.compile(r"(?u)\b\w\w+\b")  # mesmo token_pattern padrao do TfidfVectorizer
vocab_treino = {w for t in treino["texto"] for w in tokenizar.findall(t.lower())}
fora = [[w for w in tokenizar.findall(t.lower()) if w not in vocab_treino] for t in AMOSTRA["texto"]]
com_fora = sum(1 for f in fora if f)
tot = sum(len(tokenizar.findall(t.lower())) for t in AMOSTRA["texto"])
print("vocabulario do treino:", len(vocab_treino))
print("relatos da amostra com >=1 palavra fora do vocabulario: %d de 300" % com_fora)
print("palavras fora do vocabulario: %d de %d (%.1f%%)" % (sum(map(len, fora)), tot, 100 * sum(map(len, fora)) / tot))
print("exemplos:", sorted({w for f in fora for w in f})[:40])

print("\n=== 5. Relatos mistos com pista de seguranca (heuristica de 01_leitura_dos_dados) ===")
P_SEG = r"aterramento|guarda.?corpo|prote[cç][aã]o|bloqueio|etiquetagem|epi\b|sinaliza|vazamento de g[aá]s|risco"
P_ELE = r"disjuntor|isolamento|borne|inversor|contator|cntator|\bfase|curto|rel[eé]|tens[aã]o|corrente|motor el|fus[ií]vel"


def marcar(df):
    t = df["texto"].str.lower()
    seg = t.str.contains(P_SEG, regex=True)
    ele = t.str.contains(P_ELE, regex=True)
    return seg, ele


for nome, df in [("base completa", dados), ("teste (600)", teste), ("amostra (300)", AMOSTRA)]:
    seg, ele = marcar(df)
    misto = seg & ele
    print(f"[{nome}] pista seguranca: {int(seg.sum())} | seguranca+eletrica: {int(misto.sum())}")
    print("   rotulo dos mistos:", df.loc[misto, "classe"].value_counts().to_dict())
    nao_seg = seg & (df["classe"] != "seguranca")
    print("   com pista de seguranca mas rotulo != seguranca:", int(nao_seg.sum()),
          df.loc[nao_seg, "classe"].value_counts().to_dict())

seg, ele = marcar(AMOSTRA)
misto = seg & ele
print("\nmistos da amostra (rotulo | texto):")
for _, r in AMOSTRA.loc[misto].iterrows():
    print(f"  {r['classe']:<10} | {r['texto']}")

print("\n=== 6. Duplicados e vazamento treino/teste ===")
comuns = set(treino["texto"]) & set(AMOSTRA["texto"])
print("textos da amostra que aparecem identicos no treino:", len(comuns))

print("\n=== 7. Ruido de rotulo: textos quase iguais com rotulo diferente ===")
norm = dados["texto"].str.lower().str.replace(r"[^a-z0-9 ]", " ", regex=True).str.split().apply(lambda p: " ".join(sorted(set(p))))
g = dados.assign(norm=norm).groupby("norm")["classe"].nunique()
print("grupos de mesmo conjunto de palavras com >1 rotulo:", int((g > 1).sum()))
