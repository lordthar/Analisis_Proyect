from flask import Flask, render_template
from  Estadisticas.Estadisticas_Autores import estadisticas_autores
from  Estadisticas.Estadisticas_AnioTipo import estadisticas_aniotipo
from  Estadisticas.Estadisticas_Producto import estadisticas_producto
from  Estadisticas.Estadisticas_journals import estadisticas_journals
from  Estadisticas.Estadisticas_Publisher import estadisticas_publisher
from Estadisticas.word_cloud import WordCloud_Generator
from Estadisticas.agrupador_jerarquico import AgrupadorJerarquico
from convertidor_ris_csv import risACsv
import csv, time
import io, base64, matplotlib.pyplot as plt

app = Flask(__name__)


def fig_to_base64(fig):
    buf = io.BytesIO()
    if hasattr(fig, '_constrained'):
        fig._constrained = False
    if hasattr(fig, 'set_constrained_layout'):
        fig.set_constrained_layout(False)
    
    fig.set_size_inches(12, 8) 
    
    fig.savefig(buf, format='png', dpi=100)

    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)
    return f"data:image/png;base64,{img_base64}"

@app.route("/")
def index():
    risACsv("referencias.csv", "Articulos/articulos_unicos.ris")
    time.sleep(5)
    with open("referencias.csv", "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        data = list(reader)
    
    
    key="abstract"
    
    if not data or key not in data[0]:
        return "Error cargando CSV o campo 'abstract' no existe."
    
    total_articulos= len(data)
    
    fig_autores = estadisticas_autores(data,"authors")
    fig_aniotipo = estadisticas_aniotipo(data,"type_of_reference")
    fig_producto= estadisticas_producto(data,"type_of_reference")
    fig_journals= estadisticas_journals(data,"journal")
    fig_publisher= estadisticas_publisher(data,"publisher")

    img_requerimiento2 ={
        "autores": fig_to_base64(fig_autores),
        "aniotipo": fig_to_base64(fig_aniotipo),
        "producto": fig_to_base64(fig_producto),
        "journals": fig_to_base64(fig_journals),
        "publisher": fig_to_base64(fig_publisher)

    }

    words = WordCloud_Generator('referencias.csv', 'categorias_variables.csv')
    words.cargar_datos()
    fig_wordcloud = words.generar_nube_words()
    fig_coword = words.generar_grafo_coword()

    imgs_requerimiento3 = {
    "wordcloud": fig_to_base64(fig_wordcloud),
    "coword": fig_to_base64(fig_coword)
    }


    #------------------------------------------------------------------------------

    agrupador = AgrupadorJerarquico('referencias.csv') 
    agrupador.cargar_datos()
    agrupador.vectorizar_textos()
    fig_dendrograma = agrupador.comparar_metodos()

    abstract, categoria= agrupador.cargar_datos()

    dendrograma_abstract = len(abstract)
    dendrograma_categoria = len(categoria)

    img_requerimiento5 = {
        "dendrograma-ward": fig_to_base64(fig_dendrograma['ward']),
        "dendrograma-average": fig_to_base64(fig_dendrograma['average'])
    }

    total_datos= {
        "dendrograma-abstract": dendrograma_abstract,
        "dendrograma-categoria": dendrograma_categoria,
        "estadistico": total_articulos
    }
    #-------------------------------------------------------------------------

    tabla_categoria = words.contar_y_mostrar_tabla_ocurrencias()

    return render_template("index.html",
                           requerimiento2=img_requerimiento2,requerimiento3= imgs_requerimiento3, 
                           requerimiento5=img_requerimiento5, total=total_datos,
                           tabla_categoria=tabla_categoria)

if __name__ == "__main__":
    app.run(debug=True)