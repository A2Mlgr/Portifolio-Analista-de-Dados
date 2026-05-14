import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

np.random.seed(42)
random.seed(42)

vendedores = ["Ana Souza", "Carlos Lima", "Fernanda Reis", "Marcos Alves", "Juliana Costa"]
produtos = ["Consultoria BI", "Implantação Power BI", "Treinamento Power BI", "Dashboard Personalizado", "Suporte Mensal"]
precos_base = {"Consultoria BI": 4500, "Implantação Power BI": 12000, "Treinamento Power BI": 2800, "Dashboard Personalizado": 8500, "Suporte Mensal": 1800}
regioes = ["São Paulo", "Curitiba", "Belo Horizonte", "Porto Alegre", "Rio de Janeiro", "Campinas"]
segmentos = ["Varejo", "Indústria", "Saúde", "Financeiro", "Educação", "Agronegócio"]
status_opts = ["Pago", "Pago", "Pago", "Pendente", "Cancelado"]

start = datetime(2024, 1, 1)
rows = []
for i in range(400):
    data = start + timedelta(days=random.randint(0, 364))
    produto = random.choice(produtos)
    preco = precos_base[produto] * np.random.uniform(0.85, 1.25)
    vendedor = random.choice(vendedores)
    regiao = random.choice(regioes)
    segmento = random.choice(segmentos)
    status = random.choice(status_opts)
    qtd = random.randint(1, 3)
    rows.append({
        "data_venda": data.strftime("%Y-%m-%d"),
        "vendedor": vendedor,
        "produto": produto,
        "regiao": regiao,
        "segmento": segmento,
        "quantidade": qtd,
        "valor_unitario": round(preco, 2),
        "valor_total": round(preco * qtd, 2),
        "status": status
    })

df = pd.DataFrame(rows).sort_values("data_venda").reset_index(drop=True)

metas = []
for mes in range(1, 13):
    for vendedor in vendedores:
        metas.append({"mes": mes, "vendedor": vendedor, "meta": random.choice([35000, 40000, 45000, 50000])})
df_metas = pd.DataFrame(metas)

df.to_csv("vendas.csv", index=False)
df_metas.to_csv("metas.csv", index=False)
print("Dataset gerado:")
print(df.head())
print(f"\nTotal de registros: {len(df)}")
print(f"Faturamento total: R$ {df[df['status']=='Pago']['valor_total'].sum():,.2f}")
