# RAG for MDs

Proyecto para montar un sistema RAG desde cero y terminar con un chatbot capaz de responder preguntas sobre un documento Markdown (la guía de la prueba por ejemplo).

## Roadmap del desarrollo

He creado una carpeta llamada `scripts/` que contiene un archivo por cada ejercicio. Estos scripts podríamos decir que son los *main.py* de cada ejercicio. Sin embargo, las clases y funciones que se han creado para cada ejercicio se van reusando en los ejercicios posteriores, incluyendo el chatbot final. 

Cada apartado tiene su propia rama en GitHub y un único commit. Tras la finalización de cada punto, la rama se ha hecho un merge a la rama principal (main) del repositorio, pero sin eliminar la rama feature. De esta manera, al inspeccionar los commits de la main, se puede ir viendo la evolución a lo largo de los ejercicios.

La rama main del repositorio es la que contiene el chatbot final, con la interfaz de usuario que corre en `main.py`.

Se ha incluido también un `Makefile` para ejecutar:
- Cada uno de los apartados de la prueba por separado
- El chatbot final en local
- El chatbot con docker

## Estructura del proyecto
```
├── Dockerfile
├── Makefile
├── README.md
├── ai-engineer-evaluation-test.md
├── docker-compose.yml
├── main.py
├── pyproject.toml
├── resources
│   └── ui_strings.py
├── scripts
│   ├── ej1.py
│   ├── ej2_1.py
│   ├── ej2_2.py
│   ├── ej3_1.py
│   ├── ej3_2.py
│   └── ej3_3.py
├── src
│   ├── datamodel
│   │   └── app_config.py
│   └── rag
│       ├── __init__.py
│       ├── chatbot.py
│       ├── config.py
│       ├── embeddings.py
│       ├── llm_client.py
│       └── vector_db.py
└── uv.lock
```

## Requisitos y setup

- Python 3.12
- uv instalado
- Docker si se quiere contenerizar
- API key de Openai

Cómo hacer el setup para tener todo preparado:

Se ha incluido un archivo `.env.example` a modo de ejemplo de las variables de entorno que se usan. Se puede copiar este archivo, y completar con los datos necesarios.

```bash
cp .env.example .env
# editar .env y añade OPENAI_API_KEY
make setup
```


## Ejercicio 1: Conexión básica con OpenAI

El objetivo de este primer ejercicio es realizar una conexión básica con la API de OpenAI a través de un proxy, y obtener una respuesta a una pregunta sencilla usando un modelo LLM.

Creación de la clase `ChatLLM` en `llm_client.py`, que actúa como la capa más próxima al cliente, para realizar la llamada a la API de completions. La función de pregunta se hace lo más parametrizable posible, para poder usarla con user y system prompts personalizados en los ejercicios posteriores (y en el chatbot). 

Se incluye también una función de carga de variables y configuración en `config.py`, y un dataclass separado en `datamodel/app_config.py`. Este directorio sería util si se quisiera ampliar la funcionalidad en un futuro con nuevos dataclasses (estructura de requests y responses, estructura de mensajes, etc).

El runner es `scripts/ej1.py` que se puede ejecutar con:

```bash
make ex1
```

## Ejercicio 2: Sistema de embeddings

### Ejercicio 2.1

Se añade una clase `Embedder` que puede o bien recibir un cliente como parámetro de entrada (es decir, pasarle un conector), o inicializar un cliente en caso de que este campo esté vacío, a partir de un `AppConfig` con todos los datos necesarios. 

En esta clase se crea el método `embed_text` que acepta como entrada un string (el texto al que crear embeddings) y devuelve una lista de floats. Se tienen en cuenta fallos de la API y se hace con reintentos.

El runner es `scripts/ej2_1.py` que se puede ejecutar con:

```bash
make ex2_1
```

### Ejercicio 2.2

Se crea la clase VectorDDBB dentro de `rag/vector_db.py`. Esta clase funciona como factory de vectores. Se le puede pasar una configuración personalizada a través de un AppConfig, o en su ausencia, cargar la configuración por defecto usando `load_config`, que cargará a través del `.env`. 

Esta clase tiene un método helper para dividir un Markdown en chunks, usando un H2 (##) como delimitador.

De esta forma, al invocar `load_document` dentro de esta clase, pasándole un string, se divide el texto en chunks, y para cada uno de estos chunks, se usa el método creado en el ejercicio 2.1 para crear los embeddings.

Los embeddings se almacenan en memoria, en una variable `embeddings`, así como sus correspondientes chunks. El mapeo entre embeddings y chunks va simplemente por orden. En un principio se pensó persistir embeddings y chunks en una pequeña BBDD estilo Opensearch, donde se persisten *documentos* en un índice, que contienen el chunk, el embedding, y una serie de metadatos. Sin embargo esta aproximación no se acabó usando en el chatbot final, y se optó por la "persistencia" en memoria.

El runner es `scripts/ej2_2.py` que se puede ejecutar con:

```bash
make ex2_2
```

En esta sección el texto a embeder está *hardcodeado* en el propio script, por sencillez.

## Ejercicio 3: Dándole funcionalid

### Ejercicio 3.1

De la manera en que se ha pensado el proyecto, se pueden ir añadiendo funcionalidades a los *microservicios*. De esta forma, para implementar una búsqueda por similitud, se añade en la clase VectorDDBB un método, `nearest_chunks`, que busca los embeddings más similares a una query dada. 

El flujo es el siguiente: dada una query, se crean los embeddings de la misma. Por cada uno de los embeddings que tenemos almacenados en memoria, se hace el dot product de la query con el embedding. Los resultados con mayor valor serán los chunks que más relación semántica tengan con la query dada. Se crea una lista de "similitudes" en la que se almacena el resultado del dot product, y el índice que ocupa el embedding dentro de la lista de embeddings (que se mapea a su vez con el chunk correspondiente). De esta forma, podemos localizar fácilmente el chunk que queremos recuperar. 

Una forma de mejorar este apartado sería probando alguna otra medida de similitud, ya que un dot product puede resultar muy simple. Por ejemplo, con cosine similarity.

El runner es `scripts/ej3_1.py` que se puede ejecutar con:

```bash
make ex3_1
```

en caso de querer usar la query por defecto, o

```bash
make ex3_1 PROMPT="..."
```

en caso de querer usar un prompt personalizado.

### Ejercicio 3.2

Se amplían las funcionaliades de la clase VectorDDBB, esta vez para introducir un método que pueda leer el archivo .md a partir de un path. Usando la librería `pathlib` se lee el archivo, que se castea a string, y se le pasa al método `load_document` que teníamos ya creado de antes.

En estos últimos apartados se puede ver la ventaja de hacer un proyecto de una manera tan modular a la hora de incorporar una nueva funcionalidad, ya que los cambios necesarios son mínimos y no hace falta hacer ninguna refactorización.

El runner es `scripts/ej3_2.py` que se puede ejecutar con:

```bash
make ex3_2
```

### Ejercicio 3.3

Este ejercicio es simplemente un orquestador de todo lo que tenemos, ya que no se introduce nueva funcionalidad. Se hacen los siguientes pasos:

- Se carga el md que tenemos en la carpeta raíz del proyecto (a partir de la ruta, usando lo introducido en el ej 3.2)
- Esta carga genera los embeddings (usando lo introducido en el ej 2.1 y 2.2)
- Se hace una query, y se buscan los n chunks más cercanos (usando lo introducido en el ej 3.1)

Esto es un RAG casi al completo. Simplemente falta devolverle este contexto al LLM para que nos de una respuesta.

El runner es `scripts/ej3_3.py` que se puede ejecutar con:

```bash
make ex3_3
```

en caso de querer usar la query por defecto, o

```bash
make ex3_3 PROMPT="..."
```

## Ejercicio 4: Chatbot completo

La rama `main` del proyecto es la que contiene el chatbot al completo. 

Se crea una clase nueva, `Chatbot`, con el método `ask_with_chunks`. Este método tiene un prompt *plantilla* que se completa con el contexto recuperado y la query del usuario. Se le dice al LLM que solo responda a preguntas cuya respuesta pueda encontrar en el contexto proporcionado, a modo de guardarraíl. Estos system y user prompts se le pasan al método `ask` de la clase ChatLLM que creamos en el primer ejercicio. 

Se crea una UI sencilla con Streamlit en `main.py`, desde la que:
- Se puede elegir qué modelo usar para generar la respuesta (mini o nano)
- Se puede cargar un archivo md desde los archivos del usuario
- Se puede elegir el número de chunks que traerse como contexto (por defecto 3: es un número razonable teniendo en cuenta el tamaño del md. Con menos puede faltar contexto, y con más se puede generar demasiado ruido)
- Se puede mantener una conversación con el bot (no tiene en cuenta el histórico, y recupera *n* chunks sea cual sea el prompt)
- Muestra una serie de estadísticas

El flujo que se sigue es el siguiente:
1. El usuario carga un documento, que se divide en chunks a los cuales se les generan embeddings. Los embeddings y los chunks se quedan guardados en memoria (no persistimos).
2. Al hacer una pregunta, el método `nearest_chunks` de `VectorDDBB` recupera el contexto a partir de la query (embedding de la pregunta, dot product con los embeddings almacenados).
3. Se le pasan al método `ask_with_chunks` mencionado antes tanto la query como el contexto recuperado. De esta manera, `Chatbot.ask_with_chunks(...)` construye el prompt con estos chunks.
4. `ChatLLM.ask(...)` llama al LLM y devuelve la respuesta.

Para correr el chatbot junto a su interfaz se usa el siguiente comando

```bash
make ui
```

## Contenedores

Se han incluido también una serie de comandos en el Makefile para correr la app final de forma contenerizada en caso de que fuerade interés. Para ello se puede correr
```bash
make docker-build
make docker-run`

# O si se usa podman en lugar de docker
make podman-build
make podman-run
```

O en caso de querer usar compose, usar

```bash
make compose-up    
make compose-logs  
make compose-down 
```
O con podman
```bash
make podman-compose-up
make podman-compose-logs
make podman-compose-down
```

