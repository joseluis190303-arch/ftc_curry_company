from haversine import haversine
import pandas as pd
import plotly.express as px
import folium
import streamlit as st
from datetime import datetime 
from PIL import Image
from streamlit_folium import folium_static

#====================#
     #Funções#
#====================#


def clean_code(df1):
    """""Esta funcao tema a responsabilidade de limpar o dataframe

    Tipos de Limpeza:
    1. Remoção dos dados NaN
    2. Mudança do tipo da coluna de dados
    3. Remoção dos espaços das variáveis de texto
    4. Formatação da coluna de datas
    5. Limpeza da coluna de tempo (remoção do texto da variável numérica)
    
    Input: Dataframe
    Output: Dataframe
    """""
    
    #tirando valores nan
    linhas_selecionadas = df1['Delivery_person_Age'].notna() & (df1['Delivery_person_Age'] != 'NaN ')
    df1 = df1.loc[linhas_selecionadas, :].copy()

    linhas_selecionadas = df1['Road_traffic_density'].notna() & (df1['Road_traffic_density'] != 'NaN ')
    df1 = df1.loc[linhas_selecionadas, :].copy()

    linhas_selecionadas = df1['City'].notna() & (df1['City'] != 'NaN ')
    df1 = df1.loc[linhas_selecionadas, :].copy()

    linhas_selecionadas = df1['Festival'].notna() & (df1['Festival'] != 'NaN ')
    df1 = df1.loc[linhas_selecionadas, :].copy()

    linhas_selecionadas = df1['multiple_deliveries'].notna() & (df1['multiple_deliveries'] != 'NaN ')
    df1 = df1.loc[linhas_selecionadas, :].copy()

    linhas_selecionadas = df1['Weatherconditions'].notna() & (df1['Weatherconditions'] != 'NaN ')
    df1 = df1.loc[linhas_selecionadas, :].copy()

    #convertendo
    df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype(int)
    df1['multiple_deliveries'] = df1['multiple_deliveries'].astype(int)
    df1['Order_Date'] = pd.to_datetime(df1['Order_Date'], format='%d-%m-%Y')
    df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype(float)

    #Removendo espacos
    df1.loc[:, 'ID'] = df1.loc[:, 'ID'].str.strip()
    df1.loc[:, 'Road_traffic_density'] = df1.loc[:, 'Road_traffic_density'].str.strip()
    df1.loc[:, 'Type_of_order'] = df1.loc[:, 'Type_of_order'].str.strip()
    df1.loc[:, 'Type_of_vehicle'] = df1.loc[:, 'Type_of_vehicle'].str.strip()
    df1.loc[:, 'City'] = df1.loc[:, 'City'].str.strip()
    df1.loc[:, 'Festival'] = df1.loc[:, 'Festival'].str.strip()

    #Limapando a coluna de time taken
    df1['Time_taken(min)'] = df1['Time_taken(min)'].apply(lambda x: x.split('(min) ')[1])
    df1['Time_taken(min)'] = df1['Time_taken(min)'].astype(int)

    return df1

#-------------------------------Inicio da Estrutura Lógica do código---------------------------------

# Importando dataset
df = pd.read_csv('../dataset/train.csv')

# Copiando o DataFrame
df1 = df.copy()

# Limpando os Dados
df1 = clean_code(df1)


st.set_page_config(layout="wide")

# Visão Entregador 
st.header('Marketplace - Visão Entregador')

#=============
#Barra Lateral
#=============

st.sidebar.markdown('# Cury Company')
st.sidebar.markdown('## Fastest Delivery in Town')
st.sidebar.markdown("""---""")

st.sidebar.markdown('## Selecione uma data limite')

date_slider = st.sidebar.slider(
    'Selecione uma data limite',
    value=datetime(2022, 4, 13),
    min_value=datetime(2022, 2, 11),   
    max_value=datetime(2022, 4, 6),
    format='DD-MM-YYYY')

st.sidebar.markdown("""---""")

traffic_optios = st.sidebar.multiselect(
    'Quais as condições do trânsito',
    ['Low', 'Medium', 'Higt', 'Jam'],
    default=['Low', 'Medium', 'Higt', 'Jam'])

st.sidebar.markdown("""---""")  
 #Filtros de data
linhas_selecionadas = df1['Order_Date'] < date_slider   
df1 = df1.loc[linhas_selecionadas, :]

#Filtro de transito
linhas_selecionadas = df1['Road_traffic_density'].isin(traffic_optios)
df1 = df1.loc[linhas_selecionadas, :]

#===================#
#Layout no Streamlit#
#===================#

tab1, tab2, tab3 = st.tabs(['Visão Gerencial', '_', '_'])

with tab1:
    with st.container():
        st.title('Overall Metrics')
        
        col1, col2, col3, col4 = st.columns(4, gap='large')
        with col1:
            
            # A MAIOR IDADE DOS ENTREGADORES 
            maior_idade = df1.loc[:, 'Delivery_person_Age'].max()
            col1.metric('Maior Idade', maior_idade)
            
    
        with col2:
            # A menor idade dos entregadfores 
            
            menor_idade = df1.loc[:, 'Delivery_person_Age'].min()
            col2.metric('Menor Idade', menor_idade)
           

        with col3:
            # A melhor avaliação dos entregadores
            melhor_avaliação = df1['Delivery_person_Ratings'].max()
            st.metric('Melhor Avaliação', melhor_avaliação)
   
    
        with col4:
            # A pior avaliação dos entregadores
            pior_avaliação = df1['Delivery_person_Ratings'].min()
            st.metric('Pior Avaliação', pior_avaliação)

    with st.container():
        st.markdown("""---""")
        st.title('Avaliações')

        col1, col2 =st.columns (2)
        with col1:
            st.subheader('Avaliação média por entregador')
            df_avg_rating_per_deliver = (df1.loc[:, ['Delivery_person_ID', 'Delivery_person_Ratings']]
                                        .groupby('Delivery_person_ID')
                                        .mean()
                                        .reset_index())
            st.dataframe(df_avg_rating_per_deliver)

        with col2:
            st.subheader('Avaliação Média por Entregador')
            df_avg_rating_by_traffic = (df1.loc[:, ['Delivery_person_Ratings', 'Road_traffic_density']]
                                        .groupby('Road_traffic_density')
                                        .agg({'Delivery_person_Ratings': ['mean', 'std']}))
            
            # mudança de nome das colunas
            df_avg_rating_by_traffic.columns = ['delivery_mean', 'delivery_std']

            # Reset do index
            df_avg_rating_by_traffic = df_avg_rating_by_traffic.reset_index()


            st.dataframe(df_avg_rating_by_traffic)
        
            st.subheader('Avaliação Média por Tipo de Trânsito')
            df_avg_rating_by_weather = (df1.loc[:, ['Delivery_person_Ratings', 'Weatherconditions']]
                                        .groupby('Weatherconditions')
                                        .agg({'Delivery_person_Ratings': ['mean', 'std']}))
            # mudança de nome das colunas
            df_avg_rating_by_weather.columns = ['delivery_mean', 'delivery_std']
            # Reset do index
            df_avg_rating_by_weather = df_avg_rating_by_weather.reset_index()
            st.dataframe(df_avg_rating_by_weather)

    with st.container():
        st.markdown("""---""")
        st.title('Velocidade de Entrega')

        col1, col2 = st.columns(2)
        with col1:
            st.subheader('Top Entregadores mais rápidos')
            df3 = df1.loc[:, ['Delivery_person_ID', 'Time_taken(min)']].groupby('Delivery_person_ID').min().reset_index()
            df3 = df3.sort_values(by='Time_taken(min)', ascending=True)
            st.dataframe(df3)
           

        with col2:
            st.subheader('Top Entregadores mais lentos')
            df4 = df1.loc[:, ['Delivery_person_ID', 'Time_taken(min)']].groupby('Delivery_person_ID').max().reset_index()
            df4 = df4.sort_values(by='Time_taken(min)', ascending=False)
            st.dataframe(df4)


            