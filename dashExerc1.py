import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# Inicializando a aplicação Dash
app = dash.Dash(__name__)

# Dados iniciais
data = {
    'Fonte': ['Biodiesel', 'Gasolina Automotiva', 'Gás Natural',
              'Álcool Etílico Anidro', 'Álcool Etílico Hidratado', 'Óleo Diesel'],
    '2020': [4007.2, 20136.5, 1658.7, 5221.7, 10115.5, 33946.3],
    '2021': [4282.9, 22100.3, 1907.9, 5893.5, 8946.1, 37160.3],
    '2022': [4005.2, 24192.4, 1991.4, 6513.6, 8641.8, 38595.5]
}
df = pd.DataFrame(data)
df.set_index('Fonte', inplace=True)

# Layout da aplicação
app.layout = html.Div([
    html.H1("EXERCÍCIO 1) Projeção de Consumo de Energia por Fonte"),

    # Criação dos campos de input para modificar os dados de 2020, 2021 e 2022
    html.Div([
        html.Label("Modificar dados de 2020, 2021 e 2022:"),
        # Envolver a compreensão de lista com parênteses
        *(html.Div([
            html.Label(f"{fonte} - {year}: "),
            dcc.Input(id=f"{fonte.lower()}_{year}", type="number", value=df.loc[fonte, year], step=0.1)
        ]) for fonte in df.index for year in ['2020', '2021', '2022'])
    ]),

    # Botão para atualizar o gráfico
    html.Button('Atualizar Gráfico', id='submit-val', n_clicks=0),

    # Gráfico interativo
    dcc.Graph(id='energy-consumption-graph'),
])

# Função para atualizar o gráfico com base nas entradas dos inputs
@app.callback(
    Output('energy-consumption-graph', 'figure'),
    Input('submit-val', 'n_clicks'),
    [State(f"{fonte.lower()}_{year}", 'value') for fonte in df.index for year in ['2020', '2021', '2022']]
)
def update_graph(n_clicks, *values):
    # Atualizando os dados no DataFrame com os valores modificados pelo usuário
    updated_data = np.array(values).reshape(len(df.index), 3)
    df_updated = df.copy()
    df_updated[['2020', '2021', '2022']] = updated_data

    # Calculando a taxa de crescimento médio anual e projetando até 2030
    avg_growth_rates = df_updated.pct_change(axis='columns').mean(axis=1)
    years = np.arange(2023, 2031)
    projections = pd.DataFrame({
        year: df_updated.iloc[:, -1] * (1 + avg_growth_rates)**(year - 2022) for year in years
    })

    # Concatenando os dados históricos com as projeções
    df_final = pd.concat([df_updated, projections], axis=1)
    df_final.columns = df_final.columns.astype(str)

    # Criando o gráfico com Plotly
    fig = go.Figure()
    for fonte in df_final.index:
        fig.add_trace(go.Scatter(x=df_final.columns, y=df_final.loc[fonte], mode='lines', name=fonte))

    # Ajustando o layout do gráfico
    fig.update_layout(
        title='Projeção de Consumo de Energia até 2030',
        xaxis_title='Ano',
        yaxis_title='Consumo (kTEP)',
        xaxis=dict(tickmode='linear'),
        legend_title='Fonte',
        template='plotly_white'
    )

    return fig

# Rodando a aplicação
if __name__ == '__main__':
    app.run_server(debug=True)
