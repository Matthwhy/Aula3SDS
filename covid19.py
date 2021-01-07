import pandas as pd
import streamlit as st

import altair as alt

st.cache()


def load_data():
    cov19 = pd.read_csv('Covid-19_sp.csv')
    cov19['data'] = pd.to_datetime(cov19['data'], format='%Y-%m-%d')
    last = cov19[cov19['data'] == '2020-11-19'][['cidade', 'confirmado', 'populacao', 'mortes', 'indice_morte']]
    return cov19, last


cov19, last = load_data()

st.dataframe(cov19)

st.title('Covid-19 Dashboard')
st.sidebar.markdown('Covid-19 Dashboard')
st.sidebar.markdown('''
    Esse aplicativo web tem o intuito de mostrar de forma visual as informações sobre o covid-19 em são paulo
''')

st.header('Selecionar a cidade que você quer acompanhar: ')
city = st.selectbox(' ', cov19['cidade'].unique())

st.header('Escolha o indice desejado para acompanhar da cidade {0}'.format(city))
daily = st.selectbox(' ', ('Casos confirmados', 'mortes', 'Indice de mortes'))
graph = st.radio('Selecione tipo de gráfico: ',('Gráfico de linha','Gráfico Scatter'))

st.header(' ')

ca = alt.Chart(cov19[cov19['cidade'] == city]).encode(
    x = 'data',
    y = 'confirmado',
    tooltip = ['data','cidade','confirmado']
).interactive()

re = alt.Chart(cov19[cov19['cidade'] == city]).encode(
    x = 'data',
    y = 'mortes',
    tooltip = ['data', 'cidade', 'mortes']
).interactive()

de = alt.Chart(cov19[cov19['cidade'] == city]).encode(
    x = 'data',
    y = 'indice_morte',
    tooltip = ['data', 'cidade', 'indice_morte']
).interactive()

cas = alt.Chart(cov19[cov19['cidade'] == city],title='Scatter', width=1000,height=400).mark_circle(color='green').encode(
    x = 'data',
    y = 'confirmado',
    size = 'mortes',
    color = 'indice_morte',
    tooltip = ['data','cidade','confirmado','mortes','indice_morte']
).interactive()

if daily == 'Casos confirmados':
    if graph == 'Gráfico de linha':
        st.altair_chart(ca.mark_line(color='firebrick'))
    else:
        st.altair_chart(ca.mark_circle(color='firebrick'))
elif daily == 'Mortes':
    if graph == 'Gráfico de linha':
        st.altair_chart(ca.mark_line(color='green'))
    else:
        st.altair_chart(ca.mark_circle(color='green'))

elif daily == 'Indice de mortes':
    if graph == 'Gráfico de linha':
        st.altair_chart(ca.mark_line(color='blue'))
    else:
        st.altair_chart(ca.mark_circle(color='blue'))

st.altair_chart(cas)

a = alt.Chart(cov19[cov19['cidade'] == city], width=500, height=400).mark_bar().encode(
    x = 'dia(data):0',
    y = 'mes(data):0',
    color= 'sum(mortes)',
    tooltip = 'sum(mortes)'
)

b = alt.Chart(cov19[cov19['cidade']== city], width=500, height=400).mark_text().encode(
    x = 'dia(data):0',
    y = 'mes(data):0',
    text = 'sum(mortes)'

)
c = alt.Chart(cov19[cov19['cidade'] == city], width=500, height=400).mark_bar().encode(
    x='dia(data):0',
    y='mes(data):0',
    color='sum(mortes)',
    tooltip='sum(mortes)'
)

d = alt.Chart(cov19[cov19['cidade'] == city], width=500, height=400).mark_text().encode(
    x='dia(data):0',
    y='mes(data):0',
    text='sum(mortes)'

)

st.header('Total de Casos confirmados vs Total de casos de mortes {0}'.format(city))

con = alt.Chart(cov19[cov19['cidade'] == city]).mark_area(color='firebrick').encode(
    x = 'data',
    y= 'mortes',
    tooltip = ['data','mortes']
).interactive()

rec = alt.Chart(cov19[cov19['cidade'] == city]).mark_area(color='green').encode(
    x = 'data',
    y= 'confirmado',
    tooltip = ['data','confirmado']
).interactive()

opt = st.radio(
    'Selecione uma opção: ',
    ('Casos cnfirmados','Mortes confirmadas')
)

if opt == 'Mortes confirmadas':
    st.altair_chart(con)
else:
    st.altair_chart(rec)

st.header('Resumo de dados do covid-19 {}'.format(city))
'De 01-04-2020 a 19-11-2020'
total = last[last['cidade'] == city]['confirmado'].sum()

mort =  last[last['cidade'] == city]['mortes'].sum()

ind =  last[last['cidade'] == city]['indice_morte'].sum()

conf =  cov19[cov19['cidade'] == city]['confirmados_100k'].max()

pop = last[last['cidade'] == city]['populacao'].max()

tab = {'categorias': ['casos totais confirmados','Total de Mortes','Indice de mortes','Casos confirmados por 100 mil habitantes','População total'],
       'Números:': [total,mort,ind,conf,pop]}

stat = pd.DataFrame(tab)
st.table(stat)

st.header('Total de casos e Total de mortes')

opcao = st.multiselect(
    'Selecione multiplas cidades:',
    cov19['cidade'].unique()
)

fire = alt.Chart(cov19[cov19['cidade'].isin(opcao)],width=500,height=300).mark_circle().encode(
    x = 'data',
    y = 'cidade',
    tooltip = ['data','cidade','confirmado'],
    color = 'cidade',
    size = 'confirmado'
).interactive()

bar1 = alt.Chart(cov19[cov19['cidade'].isin(opcao)]).mark_bar().encode(
    y = 'max(confirmado)',
    x = alt.X('cidade', sort ="-y"),
    color = 'cidade',
    tooltip = 'max(confirmado)'
).interactive()
st.altair_chart(fire | bar1)

confirm = last.sort_values('confirmado', ascending=False)[['cidade','confirmado']].head()

confirm.reset_index(inplace=True, drop=True)

bar2 = alt.Chart(confirm, width=800, height=400).mark_bar().encode(
    x = 'confirmado',
    y = alt.Y('cidade', sort='-x'),
    color = alt.Color('cidade', legend=None),
    tooltip = 'confirmado'
).interactive()

death = last.sort_values('mortes', ascending=False)[['cidade','mortes']].head()
death.reset_index(inplace=True, drop=True)

bar3 = alt.Chart(death, width=800, height=400).mark_bar().encode(
    x = 'mortes',
    y = alt.Y('cidade', sort='-x'),
    color = alt.Color('cidade', legend=None),
    tooltip = 'mortes'
).interactive()


ind_mortes = last.sort_values('indice_morte', ascending=False)[['cidade','indice_morte']].head()
ind_mortes.reset_index(inplace=True, drop=True)

bar4 = alt.Chart(death, width=800, height=400).mark_bar().encode(
    x = 'indice_morte',
    y = alt.Y('cidade', sort='-x'),
    color = alt.Color('cidade', legend=None),
    tooltip = 'indice_morte'
).interactive()


st.header('Top 5 cidades mais atingidas pelo covid-19')
top = st.selectbox('Selecione uma opção:',
                   ['Casos confirmados','Mortes', 'Indice de mortes'])
if top == 'Casos confirmados':
    st.altair_chart(bar2)
elif top == 'Mortes':
    st.altair_chart(bar3)
else:
    st.altair_chart(bar4)

st.header('Ver a classificação do covid-19 por cidades')

ques2 = st.radio('Selecione uma opção para saber mais detalhes:',
                 ['Total de casos confirmados', 'Total de Mortes','População total','Posição da cidade'])

if ques2 == 'Total de casos confirmados':
    dff = last.sort_values(by = 'confirmado', ascending=False)[['cidade','confirmado']].reset_index(drop=True)
    dff.index = dff.index + 1
    st.dataframe(dff)
elif ques2 == 'Total de Mortes':
    dff = last.sort_values(by = 'mortes', ascending=False)[['cidade','mortes']].reset_index(drop=True)
    dff.index = dff.index + 1
    st.dataframe(dff)
elif ques2 == 'População total':
    dff = last.sort_values(by = 'populacao', ascending=False)[['cidade','populacao']].reset_index(drop=True)
    dff.index = dff.index + 1
    st.dataframe(dff)
else:
    dff = last.sort_values(by='ordem_local', ascending=False)[['cidade', 'ordem_local']].reset_index(drop=True)
    dff.index = dff.index + 1
    st.dataframe(dff)


st.header('Visualizar o dataset por mês')
if st.checkbox('CLique aqui para ver o dataset', False):
    'Selecione o mês'
    nc = st.slider('Mês',2,11,2,1)
    covid = cov19[cov19['data'].dt.month==nc]
    'data', covid