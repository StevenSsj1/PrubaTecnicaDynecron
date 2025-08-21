from langchain_google_genai import ChatGoogleGenerativeAI
from typing import Optional
import sys
import os

# Agregar el directorio padre al path para importar config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import settings


class LLMService:
    """Servicio para el manejo del modelo de lenguaje (LLM)"""
    
    def __init__(self):
        self.llm: Optional[ChatGoogleGenerativeAI] = None
        self._initialize_llm()

    def _initialize_llm(self):
        """Inicializa el modelo de lenguaje Gemini"""
        try:
            if settings.gemini_api_key:
                self.llm = ChatGoogleGenerativeAI(
                    model=settings.llm_model,
                    temperature=settings.llm_temperature,
                    max_tokens=settings.llm_max_tokens,
                    top_p=settings.llm_top_p,
                    top_k=settings.llm_top_k,
                    google_api_key=settings.gemini_api_key,
                )
                print(f"LLM {settings.llm_model} inicializado correctamente")
            else:
                print("Warning: No se encontró API key para Gemini")
                
        except Exception as e:
            print(f"Error: No se pudo inicializar Gemini LLM: {e}")
            self.llm = None

    def generate_response(self, query: str, context: str = "") -> str:
        """
        Genera una respuesta usando el LLM con el contexto proporcionado
        
        Args:
            query: Pregunta del usuario
            context: Contexto relevante para responder la pregunta
            
        Returns:
            Respuesta generada por el LLM
        """
        if not self.llm:
            return "Error: El modelo de lenguaje no está disponible"
            
        try:
            if context:
                prompt = self._create_context_prompt(query, context)
            else:
                prompt = query
                
            response = self.llm.invoke(prompt)
            return response.content
            
        except Exception as e:
            print(f"Error generando respuesta: {e}")
            return f"Error al generar respuesta: {str(e)}"

    def _create_context_prompt(self, query: str, context: str) -> str:
        """
        Crea un prompt estructurado con contexto
        
        Args:
            query: Pregunta del usuario
            context: Contexto relevante
            
        Returns:
            Prompt formateado
        """
        prompt_template = """Usa la siguiente información para responder la pregunta:

{context}

Pregunta: {query}

Respuesta:"""
        
        return prompt_template.format(context=context, query=query)

    def is_available(self) -> bool:
        """
        Verifica si el LLM está disponible
        
        Returns:
            True si el LLM está disponible, False en caso contrario
        """
        return self.llm is not None

    def get_model_info(self) -> dict:
        """
        Obtiene información sobre el modelo actual
        
        Returns:
            Diccionario con información del modelo
        """
        return {
            "model": settings.llm_model,
            "temperature": settings.llm_temperature,
            "max_tokens": settings.llm_max_tokens,
            "top_p": settings.llm_top_p,
            "top_k": settings.llm_top_k,
            "available": self.is_available()
        }
