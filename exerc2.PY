#ESTE CÓDIGO É UMA VARIAÇÃO DA RESOLUÇÃO APRESENTADA PELO PROFESSOR DA DISCIPLINA PARA A RESOLULÇÃO DO PROBLEMA PROPOSTO

import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Dados fornecidos
anos = ['2020', '2021', '2022']
Dem_Elet = [47, 49, 50]
Dem_Tr_Carga = [37953, 41442, 40600]
Dem_Tr_Pessoas = [35472, 36939, 39346]

# Dados de saída
Imp_Diesel = [0, 0, 0]
Imp_Gasolina = [0, 0, 0]
Imp_HFO = [0, 0, 0]

Imp_Diesel_2 = [0, 0, 0]
Imp_Gasolina_2 = [0, 0, 0]
Imp_HFO_2 = [0, 0, 0]

Dem_Elet_nov = [0, 0, 0]  # vetor intermediário para calcular consumo novo de eletricidade
Imp_total = [0, 0, 0]
Imp_total_2 = [0, 0, 0]

# Constantes
nTC = 0.2  # eficiencia transporte carga
nTP = 0.15  # eficiencia transporte pessoas
nDiesel = 0.3  # eficiencia termoletrica diesel
nHFO = 0.39  # eficiencia termoeletrica HFO

parc_elet_Diesel = 0.05  # parcela demanda da eletricidade fornecida pelo termoeletrico a diesel
parc_elet_HFO = 1 - parc_elet_Diesel

elet_transp_carga = 0.1  # porcentagem de eletrificação de transporte de carga
elet_transp_pessoas = 0.2  # porcentagem de eletrificação de transporte de pessoas

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

maximo = max(Imp_total + Imp_total_2)  # calculo o valor máximo para ajustar os gráficos com a mesma escala

# Criando a figura com subplots
fig = make_subplots(rows=1, cols=2, subplot_titles=("BAU", "Eletrificação"))

# Gráfico BAU (Business as Usual)
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
    title_text="Comparação de Consumo de Energia - BAU vs Eletrificação",
    template="plotly_white"
)

# Ajustando a escala do eixo Y em ambos os gráficos
fig.update_yaxes(range=[0, maximo], title_text="Consumo (kTEP)", row=1, col=1)
fig.update_yaxes(range=[0, maximo], title_text="Consumo (kTEP)", row=1, col=2)

# Exibindo o gráfico
fig.show()
