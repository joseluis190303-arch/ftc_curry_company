import streamlit as st

st.set_page_config(
    page_title="Home",
    page_icon="🏠",
    layout="wide"
)

st.sidebar.markdown('# Cury Company')
st.sidebar.markdown('## Fastest Delivery in Town')
st.sidebar.markdown("""---""")

st.write('# Curry Company Growth Dashboard 🏠')

st.markdown(
    """
    Growth Dashboard foi construído para acompanhar os indicadores de crescimento da empresa
    em diferentes visões: Visão Gerencial, Visão Restaurante e Visão Entregador.
    ### Como utilizar esse Growth Dashboard?
    - Visão Empresa:
        - Visão Gerencial: Métricas gerais de comportamento.
        - Visão Tática: Indicadores semnais de crescimento.
        - Visão Geográfica: Insights de geolocalização.
    - Visão Restaurante:
        - Indicadores semanais de crescimento dos restaurantes.
    - Visão Entregador:
        - Acompanhamento dos indicadores semanais de crescimento dos entregadores.
    

    """
)