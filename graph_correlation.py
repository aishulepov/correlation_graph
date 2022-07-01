'''
streamlit run --server.port  8500 streamlit_pyvis.py
'''

import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import networkx as nx
from pyvis.network import Network
st.set_page_config(layout="wide")

QUANTILE_DEFAULT = 0.99
ZOOM_RATIO = 2000
FONT_SIZE = 25
st.title('Графопостроитель')

uploaded_corr = st.file_uploader("Загрузите файл корреляции или оставьте пустым для загрузки корреляции регионов") or './input_data/Корреляция.xlsx'
uploaed_info =  st.file_uploader("Опционально: файл с частной информацией об узлах") #or './input_data/Информация.xlsx'

df_info = pd.read_excel(uploaed_info) if uploaed_info else pd.DataFrame([], 
                                                                                    columns = ["node", "color","size"])
if uploaded_corr is not None:
    df_corr = pd.read_excel(uploaded_corr)
    quantile = st.slider('Фильтрация по квантилям', min_value= 0.0, max_value=1.0, value=QUANTILE_DEFAULT)
    zoom = st.slider('Визуальное отдаление узлов', min_value = ZOOM_RATIO, max_value=ZOOM_RATIO*100, step=ZOOM_RATIO//10,  value=ZOOM_RATIO)
    font_size = st.slider('Размер шрифта', min_value = FONT_SIZE, max_value=FONT_SIZE*10,  value=FONT_SIZE)
    node_color = st.select_slider(
        'Цвет узлов',
        value = 'blue',
        options=['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet', 'black', 'gray'])
    font_color = st.select_slider(
        'Цвет подписей',
        value = 'gray',
        options=['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet', 'black', 'gray'])

    if df_corr["value"].dtype!='float64':
        df_corr["value"] = df_corr.value.str.replace(",", ".").astype(float)
    df_corr = df_corr[df_corr["to"] != df_corr["from"]]
    df_corr = df_corr[df_corr.value>df_corr.value.quantile(quantile)]
    df_corr["value"] = df_corr.value

    if st.button('Построить граф'):
        G = nx.from_pandas_edgelist(df_corr, 'from', 'to', edge_attr=True, create_using=nx.Graph())
        edges = G.edges()
        weights = list(df_corr.value)
        pos = nx.spring_layout(G, weight='weight')
        nc = nx.draw_networkx(G, pos, with_labels=True, node_color='yellow')
        nt = Network(width='100%',height='2000px')
        for k, v in pos.items():
            current_node_color = df_info.loc[df_info.node== k, "color"].values[0] if any(df_info.loc[df_info.node== k, "color"]) else node_color
            current_node_size = df_info.loc[df_info.node== k, "size"].values[0] if any(df_info.loc[df_info.node== k, "size"]) else FONT_SIZE
            nt.add_node(k, 
            title=k, 
            x = v[0]*zoom, 
            y=v[1]*zoom, 
            label=k, 
            physics=False, 
            color=current_node_color, 
            font=f'{font_size}px arial {font_color}',
            value=int(current_node_size))

        for src,tgt in edges:
            nt.add_edge(src,tgt, title=G[src][tgt]["value"], color = "gray")
        components.html(nt.generate_html(), height=2000)