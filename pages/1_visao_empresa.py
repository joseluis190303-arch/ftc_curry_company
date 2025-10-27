from haversine import haversine
import pandas as pd
import plotly.express as px
import folium
import streamlit as st
from datetime import datetime 
from PIL import Image
from streamlit_folium import folium_static

#====================
#Funções
#====================
def country_maps(df1):

    df_aux = df.loc[:, ['City', 'Road_traffic_density', 'Delivery_location_latitude', 'Delivery_location_longitude']].groupby(['City', 'Road_traffic_density']).median().reset_index()
        
    map = folium.Map()
    for index, location_info in df_aux.iterrows():
        folium.Marker([location_info['Delivery_location_latitude'],
                    location_info['Delivery_location_longitude']],
                    popup=location_info[['City', 'Road_traffic_density']]).add_to(map)
    folium_static(map, width=1024, height=600)

def order_by_week(df1):

    df1['week_of_year'] = df1['Order_Date'].dt.strftime('%U')
    df_aux = df1.loc[:, ['ID', 'week_of_year']].groupby('week_of_year').count().reset_index()
    fig = px.line(df_aux, x='week_of_year', y='ID')
    return fig

def traffic_order_share( df1 ):     
    df_aux= df1.loc[:, ['ID', 'Road_traffic_density']].groupby('Road_traffic_density').count().reset_index()

    fig = px.pie(df_aux, values='ID', names='Road_traffic_density')

    return fig

def traffic_order_city (df1):
    df_aux = df1.loc[:, ['ID','City', 'Road_traffic_density']].groupby(['City', 'Road_traffic_density']).count().reset_index()

    fig = px.scatter(df_aux, x='City', y='Road_traffic_density', size='ID', color='City')

    return fig

def order_by_day(df1):

        #Order metrics
        cols = ['ID', 'Order_Date']

            # selecao de linhas 
        df_aux = df1.loc[:, cols].groupby('Order_Date').count().reset_index()

        fig = px.bar(df1.loc[:, cols].groupby('Order_Date').count().reset_index(), x='Order_Date', y='ID')

        return fig

def clean_code(df1):
    """""Esta funcao tema a responsabilidade de limpar o dataframe

    Tipos de Limpeza:
    1. Remoção dos dados NAN
    2. Mudança do tipo da coluns de dados
    3. Remoção dos espaço das variáveis de texto
    4. Formatação da coluna de tempo (remoção do texto da variavel numérico)

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

#Importando dataset
df = pd.read_csv('../dataset/train.csv')
df1 = df.copy()

#Limpando os Dados
df1 = clean_code(df)

#====================================================
# Barra Lateral
#====================================================

st.set_page_config(layout="wide")

st.header('Marketplace - Visão Empresa')

st.sidebar.markdown('# Cury Company')
st.sidebar.markdown('## Fastest Delivery in Town')
st.sidebar.markdown( """___""" )

st.sidebar.markdown('## Selecionar uma data limite')

date_slider = st.sidebar.slider(
    'Até qual valor?',
    value=datetime(2022, 4, 13),
    min_value=datetime(2022, 2, 11),
    max_value=datetime(2022, 4, 6),
    format='DD-MM-YYYY')


st.sidebar.markdown( """___""" )


traffic_optios = st.sidebar.multiselect(
    'Quais as condições do trânsito',
    ['Low', 'Medium', 'High', 'Jam'],
    default=['Low', 'Medium', 'High', 'Jam']
)

st.sidebar.markdown( """___""" )
st.sidebar.markdown('### Powered by Comunidade DS')

#filtro de data
linhas_selecionadas = df1['Order_Date'] < date_slider
df1 = df1.loc[linhas_selecionadas, :]

#Filtro de transito 
linhas_selecionadas = df1['Road_traffic_density'].isin( traffic_optios )
df1 = df1.loc[linhas_selecionadas, :]
st.dataframe(df1)


#====================================================
# Layout no Streamlit
#====================================================
tab1,tab2, tab3 = st.tabs(['Visão Gerencial', 'Visão Tática', 'Visão Geográfica'])

with tab1:
    with st.container(): 
        
        st.markdown('# Orders by Day')
        fig = order_by_day(df1)
        st.plotly_chart(fig, use_container_width=True)
    

    with st.container():
        col1, col2 = st.columns(2)

        with col1:
            
            st.header('traffic Order Share')
            fig = traffic_order_share( df1 )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            
            st.header('Traffic Order City')
            fig = traffic_order_city(df1)
            st.plotly_chart(fig, use_container_width=True)


with tab2:
    with st.container():
        st.header('Order by Week')
        fig = order_by_week(df1)
        st.plotly_chart(fig, use_container_width=True)
    
with tab3:
    st.header('Country Maps')
    country_maps(df1)

    
