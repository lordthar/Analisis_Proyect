import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import networkx as nx
from sklearn.feature_extraction.text import CountVectorizer
from itertools import combinations
from collections import Counter
from tabulate import tabulate

class WordCloud_Generator:

    def __init__(self, ruta_csv, ruta_categorias):
        self.ruta_csv = ruta_csv
        self.ruta_categorias = ruta_categorias

    def cargar_datos(self):
        df_abstracts = pd.read_csv(self.ruta_csv)
        df_categorias = pd.read_csv(self.ruta_categorias)
        abstracts = ' '.join(df_abstracts['abstract'].dropna().astype(str).iloc[:500]).lower()
        categorias_dict = df_categorias.groupby('categoría')['variable'].apply(list).to_dict()
        return abstracts, categorias_dict

    def generar_nube_words(self):
        abstracts, variables = self.cargar_datos()

        palabras_totales = []
        for categoria, variables_lista in variables.items():
            for variable in variables_lista:
                sinonimos = [s.strip() for s in variable.split('-')]
                for sin in sinonimos:
                    ocurrencias = abstracts.count(sin)
                    palabras_totales.extend([sin] * ocurrencias)

        if palabras_totales:
            texto = ' '.join(palabras_totales)
            nube = WordCloud(width=1000, height=1000, background_color='white', colormap='viridis').generate(texto)

            fig, ax = plt.subplots(figsize=(10, 6))
            ax.imshow(nube, interpolation='bilinear')
            ax.axis('off')
            ax.set_title("Nube de Palabras Unificada")
            return fig

    def generar_grafo_coword(self):
        abstracts, categorias_dict = self.cargar_datos()

        sinonimos_filtrados = []
        for variables in categorias_dict.values():
            for variable in variables:
                if isinstance(variable, str):
                    sinonimos = [s.strip() for s in variable.split('-')]
                    sinonimos_filtrados.extend(sinonimos)

        vectorizer = CountVectorizer(vocabulary=set(sinonimos_filtrados), lowercase=True, token_pattern=r"(?u)\b\w+\b")
        X = vectorizer.fit_transform([abstracts])
        cooc_matrix = (X.T @ X).toarray()  # co-ocurrencias

        vocab = vectorizer.get_feature_names_out()
        G = nx.Graph()

        for i in range(len(vocab)):
            for j in range(i + 1, len(vocab)):
                peso = cooc_matrix[i][j]
                if peso > 0:
                    G.add_edge(vocab[i], vocab[j], weight=peso)

        if G.number_of_edges() > 0:
            fig, ax = plt.subplots(figsize=(12, 10))
            pos = nx.spring_layout(G, k=0.5)
            weights = [G[u][v]['weight'] for u, v in G.edges()]
            nx.draw(
                G, pos, ax=ax, with_labels=True, node_size=600,
                node_color='lightblue', edge_color=weights,
                edge_cmap=plt.cm.Oranges, width=2, font_size=9
            )
            ax.set_title("Grafo de Co-palabras usando CountVectorizer")
            ax.axis('off')
            return fig
        else:
            print("No se encontraron co-ocurrencias suficientes para generar el grafo.")
            return None
    def contar_y_mostrar_tabla_ocurrencias(self):
        abstracts, categorias_dict = self.cargar_datos()
        resumen = []

        for categoria, variables_lista in categorias_dict.items():
            total_categoria = 0
            for variable in variables_lista:
                sinonimos = [s.strip() for s in variable.split('-')]
                for sin in sinonimos:
                    total_categoria += abstracts.count(sin)
            resumen.append([categoria, total_categoria])

        return resumen
