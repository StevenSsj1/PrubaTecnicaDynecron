/**
 * Servicio API para comunicación con el backend FastAPI
 */

// URL base del API - usa variables de entorno o proxy de Vite en desarrollo
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api/v1';

// Tipos que coinciden con el backend
export interface SearchPassage {
  text: string;
  document_name: string;
  relevance_score: number;
}

export interface SearchResultsResponse {
  query: string;
  passages: SearchPassage[];
  total_found: number;
}

export interface Citation {
  text: string;
  document_name: string;
  score: number;
}

export interface AskResponse {
  question: string;
  answer: string;
  citations: Citation[];
  has_sufficient_context: boolean;
}

export interface ProcessedFile {
  filename: string;
  chunks_count: number;
  file_size: number;
}

export interface IngestResponse {
  message: string;
  files_processed: ProcessedFile[];
  total_chunks: number;
}

export interface StatusResponse {
  indexed_documents: number;
  total_chunks: number;
  available_documents: string[];
  indexed_vectors: number;
  total_documents: number;
  llm_available: boolean;
}

export interface StatsResponse {
  faiss_stats: {
    unique_sources: number;
    total_documents: number;
    source_list: string[];
    total_vectors: number;
  };
  llm_available: boolean;
  system_status: {
    has_data: boolean;
    storage: string;
    embedding_model: string;
  };
}

class ApiService {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = `${baseUrl}/api/v1`;
  }

  /**
   * Manejo de errores de respuesta HTTP
   */
  private async handleResponse<T>(response: Response): Promise<T> {
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `Error HTTP ${response.status}`);
    }
    return response.json();
  }

  /**
   * Sube archivos para ingesta y procesamiento
   */
  async uploadFiles(files: File[]): Promise<IngestResponse> {
    const formData = new FormData();
    
    files.forEach(file => {
      formData.append('files', file);
    });

    const response = await fetch(`${this.baseUrl}/ingest`, {
      method: 'POST',
      body: formData,
    });

    return this.handleResponse<IngestResponse>(response);
  }

  /**
   * Realiza búsqueda de pasajes relevantes
   */
  async searchPassages(query: string, k: number = 5): Promise<SearchResultsResponse> {
    const url = new URL(`${this.baseUrl}/search`);
    url.searchParams.append('q', query);
    url.searchParams.append('k', k.toString());

    const response = await fetch(url.toString());
    return this.handleResponse<SearchResultsResponse>(response);
  }

  /**
   * Hace una pregunta y obtiene respuesta con citas
   */
  async askQuestion(question: string): Promise<AskResponse> {
    const response = await fetch(`${this.baseUrl}/ask`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ question }),
    });

    return this.handleResponse<AskResponse>(response);
  }

  /**
   * Obtiene el estado actual del sistema
   */
  async getStatus(): Promise<StatusResponse> {
    const response = await fetch(`${this.baseUrl}/status`);
    return this.handleResponse<StatusResponse>(response);
  }

  /**
   * Limpia todos los documentos indexados
   */
  async clearDocuments(): Promise<{ message: string }> {
    const response = await fetch(`${this.baseUrl}/documents`, {
      method: 'DELETE',
    });

    return this.handleResponse<{ message: string }>(response);
  }

  /**
   * Obtiene estadísticas detalladas del sistema
   */
  async getStats(): Promise<StatsResponse> {
    const response = await fetch(`${this.baseUrl}/stats`);
    return this.handleResponse<StatsResponse>(response);
  }
}

// Instancia singleton del servicio API
export const apiService = new ApiService();

// Funciones de utilidad para transformar datos entre frontend y backend
export const transformSearchResultsToFrontend = (backendResults: SearchResultsResponse) => {
  return backendResults.passages.map((passage, index) => ({
    id: index.toString(),
    passage: passage.text,
    source: passage.document_name,
    score: passage.relevance_score,
  }));
};

export const transformQAResponseToFrontend = (backendResponse: AskResponse) => {
  return {
    id: Math.random().toString(36).substr(2, 9),
    answer: backendResponse.answer,
    citations: backendResponse.citations.map((citation, index) => ({
      id: index.toString(),
      source: citation.document_name,
      text: citation.text,
    })),
    timestamp: new Date(),
  };
};

export const transformProcessedFilesToFrontend = (backendFiles: ProcessedFile[]) => {
  return backendFiles.map(file => ({
    id: Math.random().toString(36).substr(2, 9),
    name: file.filename,
    size: file.file_size,
    status: 'success' as const,
  }));
};
