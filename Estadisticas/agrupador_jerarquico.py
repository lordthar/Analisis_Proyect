import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import re
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import adjusted_rand_score, normalized_mutual_info_score
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import linkage, dendrogram, cophenet
from scipy.spatial.distance import pdist

nltk.download('stopwords')

class AgrupadorJerarquico:
    def __init__(self, ruta_csv):
        self.ruta_csv = ruta_csv
        self.abstracts = []
        self.etiquetas = []
        self.X = None
        self.categorias = []
        self.labels_reales = []

    def cargar_datos(self):
        df = pd.read_csv(self.ruta_csv)
        df = df.dropna(subset=['abstract', 'keywords']) 
        self.abstracts = df['abstract'].tolist()
        self.categorias = df['keywords'].tolist()
        self.abstracts = [self.limpiar_texto(abs) for abs in self.abstracts]
        self.abstracts = self.abstracts[:50]
        self.categorias = self.categorias[:50]
        self.etiquetas = [' '.join(abs.split()[:3]) for abs in self.abstracts]
    
        categoria_unica = list(set(self.categorias))
        self.labels_reales = [categoria_unica.index(cat) for cat in self.categorias]
        print(f"[INFO] {len(self.abstracts)} abstracts y categorías cargadas y limpiadas.")
        return self.abstracts, self.categorias

    def limpiar_texto(self, texto):
        texto = texto.lower()
        texto = re.sub(r'[^\w\s]', '', texto)
        palabras = texto.split()
        palabras_limpias = [palabra for palabra in palabras if palabra not in stopwords.words('english')]
        return ' '.join(palabras_limpias)

    def vectorizar_textos(self):
        vectorizer = TfidfVectorizer()
        self.X = vectorizer.fit_transform(self.abstracts).toarray()
        print("[INFO] Vectorización TF-IDF completada.")

    def aplicar_clustering(self, metodo):
        if self.X is None:
            raise ValueError("Debes vectorizar los textos antes de aplicar clustering.")
        linkage_matrix = linkage(self.X, method=metodo)
        return linkage_matrix

    def comparar_metodos(self):
        metodos = ['ward', 'average']
        resultados = {}
        imagenes_base64 = {}

        for metodo in metodos:
            print(f"\n[INFO] Aplicando clustering con método: {metodo}")
            linkage_matrix = self.aplicar_clustering(metodo)
            imagen_base64 = self.graficar_dendrograma(linkage_matrix, metodo)
            imagenes_base64[metodo] = imagen_base64

            c = self.evaluar_calidad(linkage_matrix)
            print(f"[RESULTADO] Coeficiente cophenético para '{metodo}': {c:.4f}")
            resultados[metodo] = c

            self.evaluar_agrupamientos_categorias(metodo)

        mejor = max(resultados, key=resultados.get)
        print(f"\nEl método con mejor coeficiente cophenético es: '{mejor}' con {resultados[mejor]:.4f}")

        return imagenes_base64

    def graficar_dendrograma(self, linkage_matrix, titulo):
        fig = plt.figure(figsize=(10, 7))
        dendrogram(linkage_matrix, labels=self.etiquetas)
        plt.title(f'Dendrograma - Método {titulo}')
        plt.xlabel('Abstracts')
        plt.ylabel('Distancia')
        plt.xticks(rotation=90)
        plt.tight_layout()
        return fig 


    def evaluar_calidad(self, linkage_matrix):
        c, _ = cophenet(linkage_matrix, pdist(self.X))
        return c

    def evaluar_agrupamientos_categorias(self, metodo):
        clustering = AgglomerativeClustering(n_clusters=len(set(self.labels_reales)), linkage=metodo)
        labels_pred = clustering.fit_predict(self.X)

        ari = adjusted_rand_score(self.labels_reales, labels_pred)
        nmi = normalized_mutual_info_score(self.labels_reales, labels_pred)

        print(f"[EVALUACIÓN CATEGORÍAS] ARI: {ari:.4f}, NMI: {nmi:.4f} usando método '{metodo}'")

