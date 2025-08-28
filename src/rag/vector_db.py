import re
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, TYPE_CHECKING
import textwrap
from openai import OpenAI
from pathlib import Path
from tqdm import tqdm

from rag.embeddings import Embedder
from rag.config import load as load_config
from datamodel.app_config import AppConfig


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
        raise NotImplementedError

    @abstractmethod
    def print_number_of_embeddings(self) -> None:
        """Print the number of stored embeddings."""
        raise NotImplementedError
    
    @abstractmethod
    def load_document_from_path(self, markdown_path: Path) -> None:
        """Load and process a document into embeddings."""
        raise NotImplementedError        


class VectorDDBB(VectorDatabaseInterface):
    """
    Vector DB, en memoria:
    - Particiona por H2 (##) y añade también la introducción anterior al primer H2.
    - Genera un embedding por chunk y lo almacena junto al texto y metadatos.
    - No usa FAISS ni libs externas; el objetivo ahora es solo ingestión.
    """

    def __init__(self, cfg: Optional["AppConfig"] = None, index_name: str = "mds_guide") -> None:
        # Config por defecto desde .env para no obligar a pasar cfg en el script de ejemplo
        self._cfg = cfg or load_config()

        # Requisito: exponer el cliente OpenAI
        self.client = OpenAI(
            api_key=self._cfg.openai_api_key,
            base_url=self._cfg.base_url,
            timeout=self._cfg.timeout_s,
        )
        self._embedder = Embedder(self._cfg, client=self.client)

        # Estado in-memory (requisito de la interfaz)
        self.embeddings: List[List[float]] = []
        self.chunks: List[str] = []

        self.meta: List[Dict[str, Any]] = []
        self.index_name = index_name
        self.embedding_model = self._cfg.embedding_model


    def load_document(self, markdown_text: str) -> None:
        """
        Parte el documento por títulos H2 y crea un embedding por chunk.
        También incluye la “introducción” anterior al primer H2 si existe.
        """
        sections = self._sections_from_markdown(markdown_text)
        print("Generadas", len(sections), "secciones a partir del texto.")

        for i, sec in enumerate(tqdm(sections, desc="Generando chunks")):
            title = sec["title"]
            content = sec["content"]
            # Crear embedding de texto + título de la sección -> Me funcionó mejor
            text_for_embedding = f"{title}\n\n{content}".strip()

            if not text_for_embedding:
                # Saltamos secciones vacías
                continue
            
            # Llamada al cliente para generar los embeddings
            vec = self._embedder.embed_text(text_for_embedding)
            self.embeddings.append(vec)
            # Guardamos como chunk el texto "humano" (título + contenido) -> Separado por \n\n
            self.chunks.append(text_for_embedding)
            self.meta.append(
                {
                    "index": self.index_name,
                    "title": title,
                    "level": sec["level"],
                    "pos": i,
                    "embedding_model": self.embedding_model,
                    "char_len": len(text_for_embedding),
                }
            )

        return self.embeddings, self.chunks, self.meta


    def load_document_from_path(self, markdown_path: Path) -> None:
        """
        Carga un documento desde una ruta de archivo y lo procesa.
        """
        path = Path(markdown_path)
        if not path.is_absolute():
            path = (Path.cwd() / path).resolve()
        
        if not path.exists():
            raise FileNotFoundError(f"El archivo {path} no existe.")
        
        try:
            text = path.read_text(encoding="utf-8")
            print(f"Texto cargado y leído de {path}. Preparando embeddings...")
        except Exception as e:
            print(f"Error al leer el archivo {path}: {e}")
            return

        # Aqui ya se ha leido el documento, o sea que se lo pasasmos 
        # la funcion que hemos creado arriba para hacer los chunks
        self.load_document(text)


    def print_number_of_embeddings(self) -> None:
        print(len(self.embeddings))


    def _sections_from_markdown(self, text: str) -> List[Dict[str, Any]]:
        """
        Devuelve una lista de secciones con forma:
        [{"title": str, "content": str, "level": int, "idx": int}, ...]
        - level=1 para la introducción (si hay # … al inicio), level=2 para H2.
        """
        # Normalizamos saltos y quitamos espacios de más a la derecha
        src = textwrap.dedent(text).replace("\r\n", "\n").rstrip()

        # Localizamos H2
        h2_iter = list(re.finditer(r"(?m)^\s*##\s+(.*)$", src))
        sections: List[Dict[str, Any]] = []

        # 1) Si hay contenido antes del primer H2, lo consideramos “intro”
        intro_title = self._first_h1(src) or "Introduction"
        if h2_iter:
            intro_start = 0
            intro_end = h2_iter[0].start()
            intro_body = src[intro_start:intro_end].strip()
            # Quitamos la línea del H1 del cuerpo de la intro, si existe
            if intro_body:
                intro_body = self._strip_first_h1_line(intro_body)
            if intro_body:
                sections.append(
                    {"title": intro_title, "content": intro_body.strip(), "level": 1, "idx": 0}
                )
        else:
            # No hay H2: todo es una única sección (posible guía mínima)
            body = self._strip_first_h1_line(src).strip()
            if body:
                sections.append({"title": intro_title, "content": body, "level": 1, "idx": 0})
            return sections

        # 2) Extraemos cada H2 con su contenido hasta el siguiente H2
        for i, m in enumerate(h2_iter):
            title = m.group(1).strip()
            start = m.end()
            end = h2_iter[i + 1].start() if i + 1 < len(h2_iter) else len(src)
            body = src[start:end].strip()
            if not body and not title:
                continue
            sections.append(
                {"title": title or f"Section {i+1}", "content": body, "level": 2, "idx": i + 1}
            )

        # Filtramos secciones vacías (p.ej., dos H2 seguidos)
        sections = [s for s in sections if (s["title"] or s["content"])]
        return sections

    @staticmethod
    def _first_h1(text: str) -> Optional[str]:
        m = re.search(r"(?m)^\s*#\s+(.*)$", text)
        return m.group(1).strip() if m else None

    @staticmethod
    def _strip_first_h1_line(text: str) -> str:
        # Elimina la primera línea si es un H1; útil para que la intro no duplique el título
        return re.sub(r"(?m)^\s*#\s+.*\n?", "", text, count=1).strip()


    def _nearest_chunks(self, embedding: List[float], top_n: int = 3) -> list[str]:
        """
        Devuelve los 'top_n' chunks más cercanos al 'embedding' de entrada,
        usando el dot product como score de similitud.
        """
        if not self.embeddings:
            return []

        similarities = []
        for i, stored_embedding in enumerate(self.embeddings):
            dot_product = sum(a * b for a, b in zip(embedding, stored_embedding))
            similarities.append((dot_product, i))

        # Reordenarlo según el resultado de dot_product que está en x[0]
        similarities.sort(reverse=True, key=lambda x: x[0])
        return [self.chunks[i] for _, i in similarities[:top_n]]

    def nearest_chunks(self, text: str, top_n: int = 3) -> list[str]:
        """
        Interfaz pública: recibe TEXTO, calcula su embedding y llama a _nearest_chunks.
        """
        query_vec = self._embedder.embed_text(text)
        return self._nearest_chunks(query_vec, top_n=top_n)