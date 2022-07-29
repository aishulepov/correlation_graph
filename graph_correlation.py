'''
streamlit run --server.port  8500 streamlit_pyvis.py
'''

import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import networkx as nx
from pyvis.network import Network
st.set_page_config(layout="wide")

QUANTILE_DEFAULT = 0.97
ZOOM_RATIO = 1000
FONT_SIZE = 25
col1, col2 = st.columns([1, 3])
physics = col1.radio('Физика узлов', [True, False])
df_info = pd.DataFrame([], 
                                                                                  columns = ["node", "color","size"])
dataset = col1.select_slider(
     'Выберите вспышку',
     value="I",
     options = ('I', 'II', 'III', 'IV', 'V'))
df_corr = pd.read_csv(f'./data/{dataset}_increase.csv', sep=';')
quantile = col1.slider('Фильтрация по квантилям', min_value= 0.97, max_value=0.99, value=QUANTILE_DEFAULT)
zoom = col1.slider('Визуальное отдаление узлов', min_value = ZOOM_RATIO//100, max_value=ZOOM_RATIO*100, step=ZOOM_RATIO//10,  value=ZOOM_RATIO)
font_size = col1.slider('Размер шрифта', min_value = FONT_SIZE, max_value=FONT_SIZE*10,  value=FONT_SIZE)
node_color = col1.select_slider(
    'Цвет узлов',
    value = '#E2CDC9',
    options=['red', 'orange', 'yellow','#E2CDC9', 'green', 'blue', 'indigo', 'violet', 'black', 'gray'])

font_color = col1.select_slider(
    'Цвет подписей',
    value = 'black',
    options=['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet', 'black', 'gray'])

if df_corr["value"].dtype!='float64':
    df_corr["value"] = df_corr.value.str.replace(",", ".").astype(float)
df_corr = df_corr[df_corr["to"] != df_corr["from"]]
df_corr = df_corr[df_corr.value>df_corr.value.quantile(quantile)]
df_corr["value"] = df_corr.value


G = nx.from_pandas_edgelist(df_corr, 'from', 'to', edge_attr=True, create_using=nx.Graph())
edges = G.edges()
weights = list(df_corr.value)
def get_pose():
    
    with open('pos.json', 'r') as f:
        import json
        return json.loads(f.read())
    return nx.spring_layout(G, weight='weight')
    
         
pos=get_pose()
nc = nx.draw_networkx(G, pos, with_labels=True, node_color='yellow')
nt = Network(width='100%',height='1000px')
for k, v in pos.items():
    current_node_color = df_info.loc[df_info.node == k, "color"].values[0] if any(df_info.loc[df_info.node== k, "color"]) else node_color
    current_node_size = df_info.loc[df_info.node == k, "size"].values[0] if any(df_info.loc[df_info.node== k, "size"]) else FONT_SIZE
    nt.add_node(
        k, 
        title=k, 
        x = v[0]*zoom, 
        y = v[1]*zoom, 
        label=k, 
        physics=physics, 
        color=current_node_color, 
        font=f'{font_size}px arial {font_color}',
        value=int(current_node_size)
    )

for src,tgt in edges:
    nt.add_edge(src,tgt, title=G[src][tgt]["value"], value = G[src][tgt]["value"], color = "gray")
    
with col2:
    components.html(nt.generate_html(), height=1000)

pos = {k: list(v) for k,v in pos.items()}
'''with open('pos.json', 'w') as f:
    import json
    f.write(json.dumps(pos))'''