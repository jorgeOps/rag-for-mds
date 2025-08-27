<div align="center">

# 🚀 Evaluación Técnica - AI Engineer
### Bienvenido a la prueba técnica del equipo de IA de MasOrange

<img src="./imgs/+O.gif" alt="Corporate Logo" width="120"/>

</div>

---

## 🎯 **¿Qué vas a construir?**

Vas a crear un sistema de **RAG (Retrieval Augmented Generation)** paso a paso. No te preocupes si no has trabajado con RAG antes - lo importante es tu proceso de pensamiento y cómo estructuras el código.

La idea es terminar con un chatbot inteligente que puede responder preguntas basándose en documentos.

Te recomendamos que antes de comenzar leas completamente el documento para que tengas una visión del sistema que vas a montar y puedas ir tomando decisiones que te ayuden desde el principio a conseguir el objetivo final.

---

## 📋 **Preparación del entorno**

### <img src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" alt="GitHub Logo" width="20" style="vertical-align:middle;"/> **Setup de GitHub**

- [ ] **Repo público** → Crea un repositorio público en GitHub (¡lo necesitamos para revisar tu trabajo!)
- [ ] **Un commit por ejercicio** → Cada paso numerado = un commit (así vemos tu evolución). Puedes elegir si creas una carpeta por ejercicio, un fichero por ejercicio, o vas incrementando la funcionalidad sobre el mismo fichero/ficheros.
- [ ] **README.md** → Documenta tu proceso, decisiones y cómo ejecutar tu código

> 💡 **Tip**: Usa mensajes de commit descriptivos como "✨ Ejercicio 1: Conexión básica con OpenAI"

---

## 🛠️ **Roadmap de desarrollo**

### **Nivel 1: Fundamentos** 🌱
- **Ejercicio 1** - Conexión con LLM: Tu primer "Hello World" con IA
- **Ejercicio 2.1** - Embedding simple: Convierte texto en vectores
- **Ejercicio 2.2** - Base de datos vectorial: Almacena embeddings y chunks

### **Nivel 2: Funcionalidad RAG** 🔧
- **Ejercicio 3.1** - Búsqueda por similitud: Encuentra chunks más cercanos
- **Ejercicio 3.2** - Ingesta de documentos: Carga archivos markdown
- **Ejercicio 3.3** - Búsqueda práctica: Encuentra contenido específico

### **Nivel 3: Chatbot inteligente** 🤖
- **Ejercicio 4** - Chatbot RAG: Sistema completo de preguntas y respuestas

---

## 📚 **Recursos que tienes disponibles**

#### **Credenciales**
```yaml
# Archivo: ./secrets/secrets.yaml
# Tu persona de contacto te facilitará/habrá facilitado la API key para poder hacer las peticiones a los modelos
```

#### **Modelos disponibles**
| Modelo | Uso | Coste |
|--------|-----|-------|
| `text-embedding-3-small` | Embeddings | Muy bajo |
| `gpt-4o-mini` | Chat | Bajo |
| `gpt-4o-nano` | Chat | Muy bajo |

#### Base URL
Vas a usar los modelos a través de un proxy de modelos que nos permite un mayor control, para ello puedes usar de forma normal la api de OpenAI pero tendrás que especificar la base url *https://llmproxy.ai.orange*

```python
import openai
client = openai.OpenAI(
    api_key="your_api_key",
    base_url="https://llmproxy.ai.orange"
)
```

💰 **Presupuesto Límite: $10 USD** - Más que suficiente para toda la evaluación

---
**¡Manos a la obra! 🚀**
---

## **Ejercicio 1: Tu primera conexión IA** 🔌

Crea un script simple que se conecte a OpenAI y responda una pregunta básica:
> ¿Cuantas 'a' tiene la palabra MasOrange?

**Lo mínimo esperado:**
- Script simple que haga una llamada a la API
- Respuesta con print
- Fichero para manejo de environment (requirements.txt o pyproject.toml)

**Bonus points:**
- Manejo de environment con uv

No te preocupes si el modelo no responde de forma correcta :)

## **Ejercicio 2: Sistema de embeddings**
### 2.1. Crear un embedding simple
Crea un script simple que se conecte a OpenAI y cree el vector-embedding de la siguiente frase:
> You shall not pass!

**Lo mínimo esperado:**
- Script simple que haga una llamada a la API para obtener el embedding
- Print de la longitud del embedding
- Print del embedding

**Bonus points:**
- Conocer el origen de la frase :) Es broma, en este apartado no hay bonus points específicos.

### 2.2. Crea una base de datos vectorial
Haz una base de datos vectorial que implemente la siguiente interfaz.
```python
class VectorDatabaseInterface(ABC):
    """
    Abstract interface for vector database implementations.
    
    Expected constructor signature:
        __init__(self) -> None
            Should initialize:
            - self.client: openai.OpenAI client
            - self.embeddings: List for storing embeddings
            - self.chunks: List for storing text chunks
    """
    
    @abstractmethod
    def load_document(self, markdown_text: str) -> None:
        """Load and process a document into embeddings."""
        pass
    
    @abstractmethod
    def print_number_of_embeddings(self) -> None:
        """Print the number of stored embeddings."""
        pass
```

- ¿Qué vamos a procesar? **¡Esta misma guía!** Al final crearemos un chatbot capaz de responder preguntas sobre la guía, así que vamos a procesar la guía, para las particiones del documento, utiliza los títulos de la guía, particiona por nivel de título 2 (##). Con ello, aproximadamente nos quedará un chunk por cada ejercicio.

**Lo mínimo esperado:**
- Clase que implementa la interfaz especificada
- Método load_document que parte el texto markdown por el separador "##" y procesa cada uno de los chunks a embeddings
- Print del número de embeddings en la bbdd
- Por el momento puedes utilizar un texto de ejemplo a tu gusto directamente en el código, por ejemplo, el main del programa podría ser el siguiente:

```python
if __name__ == "__main__":
    vector_db = VectorDDBB()

    sample_markdown = """
    # Introduction
    This is the introduction section.
    
    ## First Section
    This is the first section with some content.
    
    ## Second Section
    This is the second section with different content.
    
    ## Third Section
    And this is the third section.
    """
    
    # Load document and create embeddings
    vector_db.load_document(sample_markdown)
    
    # Print number of embeddings
    vector_db.print_number_of_embeddings()
    # Output: 4
```


**Bonus points:**
- Conocer el origen de la frase :) Es broma, en este apartado no hay bonus points específicos.

## **Ejercicio 3: Dándole funcionalidad**
Añade el siguiente método a tu clase:
```python
    def _nearest_chunks(self, embedding: [int], top_n: int = 3) -> list[str]:
        """Return the nearest chunks to the given embedding with the dot product similarity"""
        # Calculate dot product similarity for each stored embedding
        similarities = []
        for i, stored_embedding in enumerate(self.embeddings):
            dot_product = sum(a * b for a, b in zip(embedding, stored_embedding))
            similarities.append((dot_product, i))
        
        similarities.sort(reverse=True, key=lambda x: x[0])
        
        return [self.chunks[i] for _, i in similarities[:top_n]]
```
Este método devuelve los top embeddings almacenados en la base de datos dado un embedding de entrada.
### 3.1. Implementa la búsqueda por texto
Implementa el método **nearest_chunks** en tu clase. Recibe un texto y devuelve los chunks más cercanos, internamente debería hacer uso de la función **_nearest_chunks**.
> def nearest_chunks(self, text: str) -> list[str]:


### 3.2. Implementa la ingesta de markdown
Modifica la interfaz **VectorDatabaseInterface** añadiendo el siguiente método abstracto:
```python
    @abstractmethod
        def load_document_from_path(self, markdown_path: Path) -> None:
            """Load and process a document into embeddings."""
            pass
```
Implementa el método correspondiente en tu clase, debe recibir el path al documento markdown de la guía y cargar los embeddings y los chunks en los atributos de la clase correspondientes.

Tu main debería parecerse a lo siguiente:
```python
    if __name__ == "__main__":
    # Create instance
    vector_db = VectorDDBB()
    
    # Load document and create embeddings
    vector_db.load_document_from_path("../ai-engineer-evaluation-test.md")
    
    # Print number of embeddings
    vector_db.print_number_of_embeddings()
```

### 3.3. Busca el apartado más parecido
Adicionalmente a lo anterior haz que en tu programa se muestre el chunk que mas se parece a la frase:
> Darle funcionalidad a la base de datos

Ejemplo de parte del main:
```python
    nearest_chunk = vector_db.nearest_chunks("Darle funcionalidad a la base de datos")[0]
    print(nearest_chunk)
```

## 4. Chatbot! 🤖
En este apartado dejamos más libertad, implementa un microchatbot que sea capaz de responder preguntas concretas sobre este documento. Para ello es importante que en la llamada al LLM no se le pase el documento completo, sino utilizar el sistema RAG que hemos creado para acotar la información que se envía. Implementa una clase **Chatbot** que tenga el método **ask_question(question: str)**.

- Puedes limitarte a que la entrada (la pregunta) sea por consola con el método input() de python
- No es necesario que envíes un único chunk al llm, es tu decisión cuántos enviar.

### Ejemplos de preguntas a las que se enfrentará el chatbot
- ¿Cuál es la pregunta que se debe responder en el **ejercicio 1: Tu primera conexión IA**?
- ¿Cuáles son los Bonus Points generales que engloban todo el proceso?
- ¿Qué modelos hay disponibles para el uso en el ejercicio?

**Lo mínimo esperado:**
- Clase Chatbot implementada
- Ejecución permite introducir una frase y el chatbot la responde
- El Chatbot hace uso de la base de datos vectorial que hemos creado anteriormente

**Bonus points:**
- Interfaz de la clase chatbot que nos permita ver de forma rápida sus métodos y firmas
- Sistema de tests para las preguntas de ejemplo (añadirlo al Makefile)


## BONUS POINTS GENERALES
- Makefile para ejecutar cada uno de los ejercicios o comandos necesarios
- Buen manejo del environment para poder ejecutar (bonus points si usas uv como gestor de entornos :P)
- No usar librerías de ragging como faiss o ragas, limitarlas sirve para demostrar que se entiende el trasfondo de lo que ocurre en esas herramientas. (Tranquilo luego en el día a día sí que las usamos, no queremos reinventar la rueda).
- No publiques la api key! Utiliza un sistema como python-dotenv para cargarla como variable de entorno y asegúrate de añadir ".env" a tu .gitignore.

### 📁 **Archivos de configuración recomendados**

### `.gitignore`
```gitignore
# Environment variables
.env
```

### `.env`
```bash
LITELLM_KEY=sk-your-api-key-here
```
