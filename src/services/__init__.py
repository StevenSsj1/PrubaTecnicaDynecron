"""
Servicios simples
"""

from .search_service import search_passages
from .qa_service import answer_question

__all__ = ['search_passages', 'answer_question']
