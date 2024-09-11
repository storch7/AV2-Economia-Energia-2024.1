import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Inicializando o app Dash
app = dash.Dash(__name__)

# Layout do app
app.layout = html.Div([
    html.H1("EXERCÍCIO 2) Simulação de Consumo de Energia: BAU vs Eletrificação"),

    # Inputs para modificar os dados de 2020, 2021, 2022
    html.Div([
        html.Label("Demanda Elétrica (2020, 2021, 2022):"),
        dcc.Input(id='dem_elet_2020', type='number', value=47),
        dcc.Input(id='dem_elet_2021', type='number', value=49),
        dcc.Input(id='dem_elet_2022', type='number', value=50),
    ], style={'margin-bottom': '20px'}),

    html.Div([
        html.Label("Demanda Transporte de Carga (2020, 2021, 2022):"),
        dcc.Input(id='dem_carga_2020', type='number', value=37953),
        dcc.Input(id='dem_carga_2021', type='number', value=41442),
        dcc.Input(id='dem_carga_2022', type='number', value=40600),
    ], style={'margin-bottom': '20px'}),

    html.Div([
        html.Label("Demanda Transporte de Pessoas (2020, 2021, 2022):"),
        dcc.Input(id='dem_pessoas_2020', type='number', value=35472),
        dcc.Input(id='dem_pessoas_2021', type='number', value=36939),
        dcc.Input(id='dem_pessoas_2022', type='number', value=39346),
    ], style={'margin-bottom': '20px'}),

    # Botão para atualizar o gráfico
    html.Button('Atualizar Gráficos', id='atualizar_grafico', n_clicks=0),

    # Gráfico
    dcc.Graph(id='grafico_simulacao')
])

# Callback para atualizar o gráfico quando o botão é clicado
@app.callback(
    Output('grafico_simulacao', 'figure'),
    [Input('atualizar_grafico', 'n_clicks')],
    [State('dem_elet_2020', 'value'),
     State('dem_elet_2021', 'value'),
     State('dem_elet_2022', 'value'),
     State('dem_carga_2020', 'value'),
     State('dem_carga_2021', 'value'),
     State('dem_carga_2022', 'value'),
     State('dem_pessoas_2020', 'value'),
     State('dem_pessoas_2021', 'value'),
     State('dem_pessoas_2022', 'value')]
)
def atualizar_grafico(n_clicks, dem_elet_2020, dem_elet_2021, dem_elet_2022,
                      dem_carga_2020, dem_carga_2021, dem_carga_2022,
                      dem_pessoas_2020, dem_pessoas_2021, dem_pessoas_2022):
    
    if n_clicks > 0: 
        # Atualizando os dados de entrada conforme os valores modificados
        anos = ['2020', '2021', '2022']
        Dem_Elet = [dem_elet_2020, dem_elet_2021, dem_elet_2022]
        Dem_Tr_Carga = [dem_carga_2020, dem_carga_2021, dem_carga_2022]
        Dem_Tr_Pessoas = [dem_pessoas_2020, dem_pessoas_2021, dem_pessoas_2022]

        # Constantes
        nTC = 0.2
        nTP = 0.15
        nDiesel = 0.3
        nHFO = 0.39

        parc_elet_Diesel = 0.05
        parc_elet_HFO = 1 - parc_elet_Diesel

        elet_transp_carga = 0.1
        elet_transp_pessoas = 0.2

        # Inicializando vetores
        Imp_Diesel = [0, 0, 0]
        Imp_Gasolina = [0, 0, 0]
        Imp_HFO = [0, 0, 0]
        Imp_total = [0, 0, 0]

        Imp_Diesel_2 = [0, 0, 0]
        Imp_Gasolina_2 = [0, 0, 0]
        Imp_HFO_2 = [0, 0, 0]
        Imp_total_2 = [0, 0, 0]

        Dem_Elet_nov = [0, 0, 0]

        # Cálculo do cenário Business as Usual (BaU)
        for i in [0, 1, 2]:
            Imp_Diesel[i] = Dem_Tr_Carga[i] / nTC + parc_elet_Diesel * Dem_Elet[i] / nDiesel
            Imp_Gasolina[i] = Dem_Tr_Pessoas[i] / nTP
            Imp_HFO[i] = parc_elet_HFO * Dem_Elet[i] / nHFO
            Imp_total[i] = Imp_Diesel[i] + Imp_Gasolina[i] + Imp_HFO[i]

        # Cálculo do cenário com eletrificação do transporte
        for i in [0, 1, 2]:
            Dem_Elet_nov[i] = Dem_Elet[i] + elet_transp_carga * Dem_Tr_Carga[i] + elet_transp_pessoas * Dem_Tr_Pessoas[i]
            Imp_Diesel_2[i] = (1 - elet_transp_carga) * Dem_Tr_Carga[i] / nTC + parc_elet_Diesel * Dem_Elet_nov[i] / nDiesel
            Imp_Gasolina_2[i] = (1 - elet_transp_pessoas) * Dem_Tr_Pessoas[i] / nTP
            Imp_HFO_2[i] = parc_elet_HFO * Dem_Elet_nov[i] / nHFO
            Imp_total_2[i] = Imp_Diesel_2[i] + Imp_Gasolina_2[i] + Imp_HFO_2[i]

        maximo = max(Imp_total + Imp_total_2)

        # Criando os gráficos
        fig = make_subplots(rows=1, cols=2, subplot_titles=("BAU", "Eletrificação"))

        # Gráfico BAU
        fig.add_trace(go.Scatter(x=anos, y=Imp_Diesel, mode='lines', fill='tonexty', name='Diesel - BAU'),
                      row=1, col=1)
        fig.add_trace(go.Scatter(x=anos, y=Imp_Gasolina, mode='lines', fill='tonexty', name='Gasolina - BAU'),
                      row=1, col=1)
        fig.add_trace(go.Scatter(x=anos, y=Imp_HFO, mode='lines', fill='tonexty', name='HFO - BAU'),
                      row=1, col=1)

        # Gráfico Eletrificação
        fig.add_trace(go.Scatter(x=anos, y=Imp_Diesel_2, mode='lines', fill='tonexty', name='Diesel - Eletrificação'),
                      row=1, col=2)
        fig.add_trace(go.Scatter(x=anos, y=Imp_Gasolina_2, mode='lines', fill='tonexty', name='Gasolina - Eletrificação'),
                      row=1, col=2)
        fig.add_trace(go.Scatter(x=anos, y=Imp_HFO_2, mode='lines', fill='tonexty', name='HFO - Eletrificação'),
                      row=1, col=2)

        # Ajustando o layout
        fig.update_layout(
            height=600,
            title_text="Simulação: BAU vs Eletrificação",
            template="plotly_white"
        )

        # Ajustando a escala do eixo Y em ambos os gráficos
        fig.update_yaxes(range=[0, maximo], title_text="Consumo (kTEP)", row=1, col=1)
        fig.update_yaxes(range=[0, maximo], title_text="Consumo (kTEP)", row=1, col=2)

        return fig

    return go.Figure()  # Retorna um gráfico vazio até que o botão seja clicado

# Executando o app
if __name__ == '__main__':
    app.run_server(debug=True)