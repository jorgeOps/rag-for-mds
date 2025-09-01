HEADER = """
<div style=\"text-align: center; padding: 2rem 0;\">
    <h1 style=\"color: #667eea; margin-bottom: 0.5rem;\">🤖 RAG Chatbot</h1>
    <p style=\"color: #666; font-size: 1.2rem; margin-top: 0;\">
        Chatea con tus documentos usando IA avanzada
    </p>
</div>
"""

SIDEBAR_CONFIG = """
<div style=\"text-align: center; padding: 1rem 0;\">
    <h2 style=\"color: #667eea;\">⚙️ Configuración</h2>
</div>
"""

NO_DOC_CHAT = """
<div style=\"text-align: center; padding: 3rem; background-color: #f8f9fa; border-radius: 12px; margin: 2rem 0;\">
    <h3 style=\"color: #667eea; margin-bottom: 1rem;\">🚀 ¡Comienza a chatear!</h3>
    <p style=\"color: #666; margin-bottom: 2rem;\">
        Primero carga un documento desde la barra lateral para poder hacer preguntas sobre su contenido.
    </p>
    <div style=\"font-size: 3rem; margin: 1rem 0;\">📄</div>
</div>
"""

SUCCESS_DOC = """
<div class=\"success-card\">
    <h4 style=\"margin-top: 0;\">✅ Documento Activo</h4>
    <p style=\"margin-bottom: 0; opacity: 0.9;\">{src}</p>
</div>
"""

WARNING_DOC = """
<div class=\"warning-card\">
    <h4 style=\"margin-top: 0;\">⚠️ Sin Documento</h4>
    <p style=\"margin-bottom: 0; opacity: 0.9;\">Carga un documento desde la barra lateral para comenzar</p>
</div>
"""

INFO_EXPANDER = """
**¿Cómo funciona?**
1. Carga un documento Markdown
2. El sistema lo divide en fragmentos
3. Cada fragmento se convierte en embeddings
4. Tus preguntas buscan fragmentos similares
5. La IA genera respuestas basadas en el contexto

**Consejos:**
- Haz preguntas específicas para mejores resultados
- Ajusta el número de chunks si necesitas más contexto
- Usa el documento por defecto para probar el sistema
"""

STATS_CONV = """
#### 📈 Estadísticas de conversación
<div class=\"metric-container\">
    <div style=\"display: flex; justify-content: space-between;\">
        <span><strong>Mensajes totales:</strong></span>
        <span>{msg_count}</span>
    </div>
    <div style=\"display: flex; justify-content: space-between;\">
        <span><strong>Preguntas realizadas:</strong></span>
        <span>{user_msgs}</span>
    </div>
</div>
"""

CHUNKS_USED = """
**Fragmentos recuperados para generar la respuesta:**
"""

CSS_STYLE = """
<style>
/* Estilos generales */
.main .block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* Mejoras en la sidebar */
.css-1d391kg {
    padding-top: 1rem;
}

/* Cards personalizados */
.status-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 1.5rem;
    border-radius: 12px;
    color: white;
    margin: 1rem 0;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}

.success-card {
    background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
    padding: 1.5rem;
    border-radius: 12px;
    color: white;
    margin: 1rem 0;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}

.warning-card {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    padding: 1.5rem;
    border-radius: 12px;
    color: white;
    margin: 1rem 0;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}

/* Botones mejorados */
.stButton > button {
    width: 100%;
    border-radius: 8px;
    border: none;
    background: linear-gradient(45deg, #667eea, #764ba2);
    color: white;
    font-weight: 600;
    transition: all 0.3s ease;
    box-shadow: 0 2px 10px rgba(102, 126, 234, 0.3);
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 20px rgba(102, 126, 234, 0.4);
}

/* Botón de acción primaria */
.primary-button > button {
    background: linear-gradient(45deg, #11998e, #38ef7d) !important;
    box-shadow: 0 2px 10px rgba(17, 153, 142, 0.3) !important;
}

/* Botón de peligro */
.danger-button > button {
    background: linear-gradient(45deg, #f093fb, #f5576c) !important;
    box-shadow: 0 2px 10px rgba(240, 147, 251, 0.3) !important;
}

/* Chat mejorado */
.stChatMessage {
    border-radius: 12px;
    margin: 0.5rem 0;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}

/* Expander personalizado */
.streamlit-expanderHeader {
    border-radius: 8px;
    background-color: #f8f9fa;
}

/* Métricas mejoradas */
.metric-container {
    background: white;
    padding: 1rem;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    margin: 0.5rem 0;
}

.block-container { padding-top: .5rem; padding-bottom: .5rem; }
main .element-container:empty { display: none; }

/* contenedor del historial: alto fijo y scroll vertical */
#chat-history {
  /* altura = alto de la ventana - cabecera (aprox) - métricas laterales - margen - altura del input */
  /* ajusta 170px si tu input o cabecera es más alta/baja */
  height: calc(100vh - 170px);
  overflow-y: auto;
  padding-right: .25rem;
  scroll-behavior: smooth;
}

/* opcional: oculta barra de scroll fea en algunos navegadores */
#chat-history::-webkit-scrollbar { width: 8px; }
#chat-history::-webkit-scrollbar-thumb { border-radius: 4px; }

/* el input ya queda al final de la página; evitamos que “empuje” */
[data-testid="stChatInput"] {
  margin-top: 0;
}

/* si hay demasiado espacio extra sobre el título de la página */
section.main > div:first-child { margin-top: 0; }
</style>
"""