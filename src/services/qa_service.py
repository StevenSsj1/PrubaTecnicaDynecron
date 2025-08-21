import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from documents.schemas import AskResponse


def answer_question(llm_service, embeddings_service, question: str) -> AskResponse:
    """Responde una pregunta de forma simple"""
    
    if not llm_service.is_available():
        raise ValueError("El servicio de LLM no está disponible")
    
    if not question or question.strip() == "":
        raise ValueError("La pregunta no puede estar vacía")
    
    search_results = embeddings_service.similarity_search_with_threshold(
        question.strip(), threshold=1.2, k=5
    )
    
    if not search_results:
        search_results = embeddings_service.similarity_search(question.strip(), k=3)
    
    if not search_results:
        return AskResponse(
            question=question,
            answer="No encuentro esa información en los documentos cargados.",
            citations=[],
            has_sufficient_context=False
        )
    
    context_passages = []
    for i, result in enumerate(search_results, 1):
        context_passages.append(f"[Fuente {i}: {result.document_name}]\n{result.text}")
    
    context = "\n\n".join(context_passages)
    
    prompt = f"""Basándote en la siguiente información, responde la pregunta de manera concisa en 3-4 líneas máximo.

INFORMACIÓN DISPONIBLE:
{context}

INSTRUCCIONES:
1. Responde en 3-4 líneas máximo
2. Usa principalmente la información proporcionada
3. Cita las fuentes como (Fuente 1), (Fuente 2), etc.
4. Si la información es parcial, responde lo que puedas y menciona que la información es limitada
5. Solo di "No encuentro esa información en los documentos cargados" si realmente no hay nada relacionado

PREGUNTA: {question}

RESPUESTA:"""
    answer = llm_service.generate_response(question, prompt)
    answer = answer.strip()
    
    if answer.lower().startswith("respuesta:"):
        answer = answer[10:].strip()
    
    citations = []
    for result in search_results[:3]:
        citation_text = result.text[:150] + "..." if len(result.text) > 150 else result.text
        citations.append({
            "text": citation_text,
            "document_name": result.document_name,
            "score": round(1.0 / (1.0 + result.score), 4)
        })
    
    no_info_phrases = ["no encuentro esa información en los documentos cargados"]
    has_sufficient_context = not any(phrase in answer.lower() for phrase in no_info_phrases)
    
    return AskResponse(
        question=question,
        answer=answer,
        citations=citations if has_sufficient_context else [],
        has_sufficient_context=has_sufficient_context
    )
