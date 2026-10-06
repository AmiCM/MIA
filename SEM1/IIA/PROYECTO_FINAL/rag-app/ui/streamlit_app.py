import os

import httpx
import streamlit as st

API = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(page_title="RAG", page_icon="📚")
st.title("📚 Sistema RAG")


def call(method: str, path: str, **kw):
    try:
        r = httpx.request(method, f"{API}{path}", timeout=120, **kw)
    except httpx.HTTPError:
        st.error(f"No se pudo conectar con la API en {API}. ¿Está levantada?")
        return None
    if r.status_code >= 400:
        st.error(f"Error {r.status_code}: {r.json().get('detail', r.text)}")
        return None
    return r.json()


health = call("GET", "/health")
if health:
    if not health["api_key_set"]:
        st.warning("La API no tiene GOOGLE_API_KEY configurada.")
    st.caption(f"Chunks indexados: {health['chroma_chunks']}")

with st.sidebar:
    st.header("Cargar documentos")
    files = st.file_uploader("PDF, MD o TXT", type=["pdf", "md", "txt"], accept_multiple_files=True)
    if st.button("Indexar", disabled=not files):
        with st.spinner("Incrustando e indexando..."):
            res = call("POST", "/ingest", files=[("files", (f.name, f.getvalue())) for f in files])
        if res:
            st.success(f"{res['documents']} documentos, {res['chunks']} chunks.")
            if res["skipped"]:
                st.warning(f"Sin texto (omitidos): {', '.join(res['skipped'])}")

    srcs = (call("GET", "/sources") or {}).get("sources", [])
    if srcs:
        st.header("Documentos indexados")
        to_delete = st.selectbox("Borrar documento", [x["source"] for x in srcs], index=None,
                                 placeholder="Elige uno...")
        if to_delete and st.button(f"Borrar {to_delete}"):
            if call("DELETE", f"/sources/{to_delete}"):
                st.rerun()
        st.caption("Para reindexar un documento, vuelve a subirlo: reemplaza sus chunks.")

st.header("Pregunta")
st.session_state.setdefault("history", [])
question = st.text_input("Escribe tu pregunta")
top_k = st.slider("top-k", 1, 8, 4)
names = [x["source"] for x in (call("GET", "/sources") or {}).get("sources", [])]
only = st.selectbox("Limitar a un documento (opcional)", names, index=None, placeholder="Todos")

if st.button("Preguntar"):
    if not question.strip():
        st.warning("Escribe una pregunta.")
    elif health and health["chroma_chunks"] == 0:
        st.warning("El índice está vacío. Carga documentos primero.")
    else:
        with st.spinner("Consultando..."):
            res = call("POST", "/query", json={"question": question, "top_k": top_k, "source": only})
        if res:
            st.session_state["history"].insert(0, {"q": question, "res": res})
            (st.info if res["abstained"] else st.success)(res["answer"])
            st.subheader("Chunks recuperados")
            for i, c in enumerate(res["citations"], 1):
                with st.expander(f"[{i}] {c['source']} · chunk {c['chunk_index']} · score {c['score']:.3f}"):
                    st.text(c["text"])

if st.session_state["history"]:
    st.divider()
    st.header("Histórico de la sesión")
    for h in st.session_state["history"]:
        with st.expander(("🚫 " if h["res"]["abstained"] else "✅ ") + h["q"]):
            st.write(h["res"]["answer"])
            st.caption("Fuentes: " + ", ".join(sorted({c["source"] for c in h["res"]["citations"]})))
