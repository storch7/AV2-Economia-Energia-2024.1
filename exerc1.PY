import numpy as np
import pandas as pd
import plotly.graph_objects as go

# Recriando o DataFrame com todos os dados fornecidos
data = {
    'Fonte': ['Biodiesel', 'Gasolina Automotiva', 'Gás Natural',
              'Álcool Etílico Anidro', 'Álcool Etílico Hidratado', 'Óleo Diesel'],
    '2020': [4007.2, 20136.5, 1658.7, 5221.7, 10115.5, 33946.3],
    '2021': [4282.9, 22100.3, 1907.9, 5893.5, 8946.1, 37160.3],
    '2022': [4005.2, 24192.4, 1991.4, 6513.6, 8641.8, 38595.5]
}

df_all = pd.DataFrame(data)
df_all.set_index('Fonte', inplace=True)

# Calculando o crescimento médio anual para todas as fontes
avg_growth_rates_all = df_all.pct_change(axis='columns').mean(axis=1)

# Projetando o consumo até 2030 para todas as fontes
years = np.arange(2023, 2031)
projections_all = pd.DataFrame({
    year: df_all.iloc[:, -1] * (1 + avg_growth_rates_all)**(year - 2022) for year in years
})

# Concatenando os dados históricos com as projeções para todas as fontes
df_final_all = pd.concat([df_all, projections_all], axis=1)

# Convertendo todos os anos para strings
df_final_all.columns = df_final_all.columns.astype(str)

# Criando o gráfico com Plotly para todas as fontes
fig_all = go.Figure()

# Adicionando as linhas para cada fonte
for fonte in df_final_all.index:
    fig_all.add_trace(go.Scatter(x=df_final_all.columns,
                                 y=df_final_all.loc[fonte],
                                 mode='lines',
                                 name=fonte))

# Ajustando o layout do gráfico
fig_all.update_layout(
    title='Projeção de Consumo de Energia por Fonte até 2030',
    xaxis_title='Ano',
    yaxis_title='Consumo (kTEP)',
    xaxis=dict(tickmode='linear'),
    legend_title='Fonte',
    template='plotly_white'
)

# Exibindo o gráfico
fig_all.show()