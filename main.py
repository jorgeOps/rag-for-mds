from typing import List

import streamlit as st
from resources.ui_strings import HEADER, CSS_STYLE, SIDEBAR_CONFIG, NO_DOC_CHAT, SUCCESS_DOC, WARNING_DOC, INFO_EXPANDER, STATS_CONV, CHUNKS_USED

from rag.config import load as load_config
from datamodel.app_config import AppConfig
from rag.llm_client import ChatLLM
from rag.vector_db import VectorDDBB
from rag.chatbot import Chatbot


st.set_page_config(
    page_title="RAG Chatbot", 
    page_icon="🤖", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown(CSS_STYLE, unsafe_allow_html=True)


# --- Helpers de inicialización ------------------------------------------------
@st.cache_resource(show_spinner=False)
def _init_base_cfg() -> AppConfig:
    return load_config()

def _make_cfg_with_model(base: AppConfig, model: str) -> AppConfig:
    return AppConfig(
        openai_api_key=base.openai_api_key,
        model=model or base.model,
        base_url=base.base_url,
        timeout_s=base.timeout_s,
        max_retries=base.max_retries,
        embedding_model=base.embedding_model,
    )

def _ensure_state():
    defaults = {
        "db": None,
        "llm": None,
        "bot": None,
        "messages": [],
        "loaded_path": None,
        "k": 3,
        "current_model": None,
        "document_loaded": False,
        "last_upload_id": None,
    }
    for key, default in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default


# --- Header principal ---------------------------------------------------------
def render_header():
    st.markdown(HEADER, unsafe_allow_html=True)


# --- Sidebar ------------------------------------------------------------------
def render_sidebar():
    with st.sidebar:
        st.markdown(SIDEBAR_CONFIG, unsafe_allow_html=True)

        # Selector de modelo
        # Es un desplegable con las dos opciones que tenemos
        st.markdown("#### Modelo")
        current_model = st.session_state.get("current_model", base_cfg.model)
        model_options = ["openai/gpt-4o-mini", "openai/gpt-4.1-nano"]
        default_idx = 0 if current_model == "gpt-4o-mini" else 1
        
        model_input = st.selectbox(
            "Selecciona el modelo",
            options=model_options,
            index=default_idx,
            help="Modelo de lenguaje para generar respuestas",
            label_visibility="collapsed"
        )

        # Configuración de búsqueda
        st.markdown("#### Parámetros de búsqueda")
        k = st.slider(
            "Chunks relevantes", 
            min_value=1, 
            max_value=10, 
            value=st.session_state["k"],
            help="Número de fragmentos de texto a recuperar para generar la respuesta"
        )
        st.session_state["k"] = k

        st.divider()

        # Sección de documentos
        st.markdown("#### Gestión de documentos")

        # Upload de archivo
        uploaded = st.file_uploader(
            "Subir documento Markdown",
            type=["md", "markdown"],
            help="Sube un archivo .md para chatear con su contenido",
            key="md_uploader"
        )
        
        # Auto-procesar archivo subido
        if uploaded is not None:
            upload_id = f"{uploaded.name}_{uploaded.size}"
            if st.session_state.get("last_upload_id") != upload_id:
                _process_uploaded_file(uploaded, upload_id)

        st.divider()

        # Acciones de chat
        st.markdown("#### Chat")
        if st.button("Limpiar conversación", type="secondary", use_container_width=True):
            st.session_state["messages"] = []
            st.toast("Conversación limpiada", icon="🧹")
            st.rerun()

    return model_input


# --- Funciones de carga de documentos -----------------------------------------
# --- AQUÍ LLEVAMOS A CABO TODA LA LÓGICA DE CHUNKING + EMBEDDING !! -----------

def _process_uploaded_file(uploaded, upload_id):
    with st.spinner("Procesando archivo subido..."):
        try:
            content = uploaded.getvalue().decode("utf-8")
            label = f"📤 {uploaded.name}"
            _init_db_and_ingest_from_text(content, label)
            st.session_state["last_upload_id"] = upload_id
            st.success("✅ Archivo procesado correctamente")
        except Exception as e:
            st.error(f"Error al procesar el archivo: {str(e)}")

def _init_db_and_ingest_from_text(md_text: str, label: str):
    try:
        db = VectorDDBB()
        db.load_document(md_text)
        st.session_state["db"] = db
        st.session_state["bot"] = Chatbot(db, st.session_state["llm"], k=st.session_state["k"])
        st.session_state["loaded_path"] = label
        st.session_state["document_loaded"] = True
    except Exception as e:
        st.error(f"Error al procesar el documento: {str(e)}")
        raise


# --- Dashboard de estado ------------------------------------------------------
def render_status_dashboard():
    st.markdown("### 📊 Estado del Sistema")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.session_state["document_loaded"]:
            embeddings_count = len(st.session_state['db'].embeddings) if st.session_state['db'] else 0
            st.metric(
                label="📚 Embeddings",
                value=f"{embeddings_count:,}",
                help="Número de fragmentos de texto indexados"
            )
        else:
            st.metric(label="📚 Embeddings", value="0")
    
    with col2:
        model_name = st.session_state.get('current_model', 'No configurado')
        # Simplificar nombre del modelo para mostrar
        display_name = model_name.replace("openai/", "").replace("gpt-", "GPT-").upper()
        st.metric(
            label="🧠 Modelo IA",
            value=display_name,
            help=f"Modelo actual: {model_name}"
        )
    
    with col3:
        k_value = st.session_state.get('k', 3)
        st.metric(
            label="🎯 Chunks",
            value=str(k_value),
            help="Fragmentos recuperados por consulta"
        )

    # Estado del documento
    if st.session_state["document_loaded"]:
        src = st.session_state.get("loaded_path", "Desconocido")
        st.markdown(SUCCESS_DOC.format(src=src), unsafe_allow_html=True)
    else:
        st.markdown(WARNING_DOC, unsafe_allow_html=True)


# --- Chat -------------------------------------------------------------
def render_chat():
    st.markdown("### 💬 Conversación")
    
    if not st.session_state["document_loaded"]:
        st.markdown(NO_DOC_CHAT, unsafe_allow_html=True)
        return

    # 1) Mostrar historial SIEMPRE arriba
    # st.markdown('<div id="chat-history">', unsafe_allow_html=True)
    for msg in st.session_state["messages"]:
        # Compat: tuplas antiguas ("role", "text") o dicts nuevos
        if isinstance(msg, dict):
            role = msg.get("role", "assistant")
            text = msg.get("text", "")
            chunks = msg.get("chunks")
        else:
            role, text = msg
            chunks = None

        with st.chat_message(role):
            st.markdown(text)
            # Si es respuesta del bot y tenemos chunks, muéstralos aquí
            if role == "assistant" and chunks:
                with st.expander("🔍 Ver contexto utilizado", expanded=False):
                    st.markdown(CHUNKS_USED)
                    for i, chunk in enumerate(chunks, start=1):
                        preview = (chunk[:700] + "...") if len(chunk) > 700 else chunk
                        st.code(preview, language="text")

    # 2) Input SIEMPRE al final (queda fijo abajo)
    prompt = st.chat_input("💭 Escribe tu pregunta sobre el documento...", key="chat_input")
    if prompt:
        _handle_chat_input(prompt)



# LOGICA PRINTIPAL DEL RAG
def _handle_chat_input(prompt: str):
    # Añadir mensaje del usuario al historial
    st.session_state["messages"].append({"role": "user", "text": prompt})

    try:
        db: VectorDDBB = st.session_state["db"]
        k = st.session_state["k"]
        chunks: List[str] = db.nearest_chunks(prompt, top_n=k)

        bot: Chatbot = st.session_state["bot"]
        bot._k = k
        answer = bot.ask_with_chunks(prompt, chunks)

        # Guardar la respuesta como dict para poder pintar el expander en el render
        st.session_state["messages"].append({
            "role": "assistant",
            "text": answer,
            "chunks": chunks,
        })

    except Exception as e:
        st.session_state["messages"].append({
            "role": "assistant",
            "text": f"❌ Error al generar respuesta: {str(e)}",
        })

    # MUY IMPORTANTE: re-renderiza para que el historial se pinte arriba y
    # el input quede abajo (no pintes nada aquí debajo).
    st.rerun()



# --- Preparar dependencias ----------------------------------------------------
def _rebuild_clients_if_needed(model_input: str):
    if (st.session_state["current_model"] != model_input or 
        st.session_state["llm"] is None):
        
        with st.spinner("Configurando modelo de IA..."):
            try:
                cfg = _make_cfg_with_model(base_cfg, model_input)
                llm = ChatLLM(cfg)
                st.session_state["llm"] = llm
                st.session_state["current_model"] = cfg.model
                
                # Reconstruir bot si hay DB
                if st.session_state["db"] is not None:
                    st.session_state["bot"] = Chatbot(
                        st.session_state["db"], 
                        llm, 
                        k=st.session_state["k"]
                    )
                    
                st.toast(f"✅ Modelo actualizado: {cfg.model}", icon="🧠")
            except Exception as e:
                st.error(f"Error al configurar el modelo: {str(e)}")


# --- Aplicación principal -----------------------------------------------------
def main():
    # Inicialización
    global base_cfg
    base_cfg = _init_base_cfg()
    _ensure_state()
    # Normaliza el historial a dicts
    if st.session_state["messages"]:
        st.session_state["messages"] = [
            m if isinstance(m, dict) else {"role": m[0], "text": m[1]}
            for m in st.session_state["messages"]
        ]


    # Header
    render_header()

    # Sidebar
    model_input = render_sidebar()

    # Actualizar clientes si es necesario
    _rebuild_clients_if_needed(model_input)

    # Layout principal
    col1, col2 = st.columns([2, 1], gap="large")

    with col1:
        render_chat()

    with col2:
        render_status_dashboard()
        
        # Información adicional
        with st.expander("ℹ️ Información del sistema"):
            st.markdown(INFO_EXPANDER)
        if st.session_state["messages"]:
            msgs = st.session_state["messages"]
            msg_count = len(msgs)
            user_msgs = sum(1 for m in msgs if m.get("role") == "user")
            st.markdown(STATS_CONV.format(msg_count=msg_count, user_msgs=user_msgs), unsafe_allow_html=True)


if __name__ == "__main__":
    main()