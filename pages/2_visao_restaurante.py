from haversine import haversine
import pandas as pd
import plotly.express as px
import folium
import streamlit as st
from datetime import datetime 
from PIL import Image
from streamlit_folium import folium_static
import plotly.graph_objects as go
import numpy as np

df = pd.read_csv('../dataset/train.csv')
df1 = df.copy()

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

# Visão Restaurante

st.set_page_config(layout="wide")

st.header('Marketplace - Visão Restaurante')

#=============
#Barra Lateral
#=============

st.sidebar.markdown('# Cury Company')
st.sidebar.markdown('## Fastast Delivery in town')
st.sidebar.markdown("""---""")

st.sidebar.markdown('## Selecione uma Data Limite')
date_slider = st.sidebar.slider(
    'Selecione uma data limite',
    value=datetime(2022, 4, 13),
    min_value=datetime(2022, 2, 11),
    max_value=datetime(2022, 4, 6),
    format='DD-MM-YYYY'
)

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

#===================
#Layout no Streamlit
#===================

tab1, tab2, tab3, tab4 = st.tabs(['Visão Gerencial', '_', '_', '_'])

with tab1:
    with st.container():
        st.title('Overall Metrics')

        col1, col2, col3, col4, col5 = st.columns(5, gap='large')
        with col1:
            delivery_unique = len(df1.loc[:, 'Delivery_person_ID'].unique())
            col1.metric('Entregadores Únicos', delivery_unique)


        with col2:
            # DISTANCIA MEDIA
            cols = ['Restaurant_latitude', 'Restaurant_longitude', 'Delivery_location_latitude', 'Delivery_location_longitude']

            df1['Distance'] = df1.loc[:, cols].apply(lambda x: haversine((x['Restaurant_latitude'], x['Restaurant_longitude']), (x['Delivery_location_latitude'], x['Delivery_location_longitude'])), axis=1)

            df_aux = df1.loc[:, ['City', 'Distance']].groupby('City').mean().reset_index()
            avg_distance = round(df_aux['Distance'].mean(), 2)
            col2.metric('Distância Média', avg_distance)

        with col3:
            
            df_aux = df1.loc[:, ['Festival', 'Time_taken(min)']].groupby('Festival').agg({'Time_taken(min)': ['mean', 'std']}).reset_index()
            df_aux.columns = ['Festival', 'avg_time', 'std_time']
            df_aux = round(df_aux.loc[df_aux['Festival'] == 'Yes', 'avg_time'], 2)

            col3.metric(' Tempo Médio', df_aux)


        with col4:
            
            df_aux = df1.loc[:, ['Festival', 'Time_taken(min)']].groupby('Festival').agg({'Time_taken(min)': ['mean', 'std']}).reset_index()
            df_aux.columns = ['Festival', 'avg_time', 'std_time']
            df_aux = round(df_aux.loc[df_aux['Festival'] == 'Yes', 'std_time'], 2)

            col4.metric(' STD Entrega', df_aux)

        with col5:
            
            df_aux = df1.loc[:, ['Festival', 'Time_taken(min)']].groupby('Festival').agg({'Time_taken(min)': ['mean', 'std']}).reset_index()
            df_aux.columns = ['Festival', 'avg_time', 'std_time']
            df_aux = round(df_aux.loc[df_aux['Festival'] == 'No', 'avg_time'], 2)

            col5.metric(' Tempo Médio de Entrega', df_aux)

    with st.container():
       
        st.markdown("""---""")
        st.title('Tempo Médio de Entrega por Cidade')

        df_aux =df1.loc[:, ['City', 'Time_taken(min)']].groupby('City').agg({'Time_taken(min)' : ['mean', 'std']})
        df_aux.columns = ['avg_time', 'std_time']
        df_aux = df_aux.reset_index()

        fig = go.Figure()
        fig.add_trace( go.Bar(name='Control', x=df_aux['City'], y=df_aux['avg_time'], error_y=dict( type='data', array=df_aux['std_time'])))

        fig.update_layout(barmode='group')
        st.plotly_chart(fig)

    with st.container():
        st.title('Distribuição do Tempo')

        col1, col2 = st.columns(2)
        with col1:
            st.markdown('###### col1')

            cols = ['Delivery_location_latitude', 'Delivery_location_longitude', 'Restaurant_latitude', 'Restaurant_longitude']
            df1['distance'] = df1.loc[:, cols].apply( lambda x:
                                                  haversine( (x['Restaurant_latitude'], x['Restaurant_longitude']),
                                                            (x['Delivery_location_latitude'], x['Delivery_location_longitude'])), axis=1)
        
            avg_distance = df1.loc[:, ['City', 'distance']].groupby('City').mean().reset_index()

            fig = go.Figure( data=[ go.Pie( labels=avg_distance['City'], values=avg_distance['distance'], pull=[0, 0.1, 0])])
            st.plotly_chart(fig)

        with col2:
            st.markdown('###### col2')

            cols = ['City', 'Time_taken(min)', 'Road_traffic_density']
            df_aux = df1.loc[: , cols].groupby(['City', 'Road_traffic_density']).agg({'Time_taken(min)': ['mean', 'std']})
            df_aux.columns = ['avg_time', 'std_time']

            df_aux = df_aux.reset_index()

            fig = px.sunburst(
            df_aux,
            path=['City', 'Road_traffic_density'],  # por exemplo, usando colunas existentes
            values='avg_time',
            color='std_time',
            color_continuous_scale='RdBu',
            color_continuous_midpoint=np.average(df_aux['std_time']))

            st.plotly_chart(fig)




