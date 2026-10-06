from google.genai import types

from . import config
from .embed import _get_client

ABSTAIN_MSG = "No tengo evidencia suficiente en los documentos para responder esa pregunta."

SYSTEM = (
    "Eres un asistente experto en perfumería. La evidencia está en inglés; responde siempre en español usando EXCLUSIVAMENTE la evidencia "
    "numerada que se te da. Cita cada afirmación con [n]. Si la evidencia no "
    "contiene la respuesta, responde exactamente: NO_EVIDENCIA. No uses conocimiento propio."
)


def answer(question: str, chunks: list[dict]) -> tuple[str, bool]:
    """Devuelve (respuesta, abstained)."""
    evidence = "\n\n".join(f"[{i}] ({c['source']}) {c['text']}" for i, c in enumerate(chunks, 1))
    prompt = f"EVIDENCIA:\n{evidence}\n\nPREGUNTA: {question}"
    res = _get_client().models.generate_content(
        model=config.GEN_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(system_instruction=SYSTEM, temperature=0.1),
    )
    text = (res.text or "").strip()
    if not text or "NO_EVIDENCIA" in text:
        return ABSTAIN_MSG, True
    return text, False
