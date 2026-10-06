def chunk_text(text: str, size: int = 250, overlap: int = 50) -> list[str]:
    """Parte el texto en ventanas de `size` palabras con `overlap` de solape."""
    if overlap >= size:
        raise ValueError("overlap debe ser menor que size")
    words = text.split()
    step = size - overlap
    chunks = []
    for start in range(0, len(words), step):
        piece = words[start:start + size]
        if piece:
            chunks.append(" ".join(piece))
        if start + size >= len(words):
            break
    return chunks
