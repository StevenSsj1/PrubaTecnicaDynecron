import { useState } from 'react';
import { AppHeader } from '@/components/AppHeader';
import { Uploader } from '@/components/Uploader';
import { SearchBox } from '@/components/SearchBox';
import { QABox } from '@/components/QABox';
import { SystemStatus } from '@/components/SystemStatus';
import { useToast } from '@/hooks/use-toast';
import { 
  apiService, 
  transformSearchResultsToFrontend, 
  transformQAResponseToFrontend, 
  transformProcessedFilesToFrontend 
} from '@/services/api';

// Mock data types (replace with your actual API types)
interface FileItem {
  id: string;
  name: string;
  size: number;
  status: 'uploading' | 'success' | 'error';
}

interface SearchResult {
  id: string;
  passage: string;
  source: string;
  score: number;
  page?: number;
}

interface QAResponse {
  id: string;
  answer: string;
  citations: Array<{
    id: string;
    source: string;
    page?: number;
    text: string;
  }>;
  timestamp: Date;
}

const Index = () => {
  const [activeTab, setActiveTab] = useState('upload');
  const [indexedFiles, setIndexedFiles] = useState<FileItem[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const { toast } = useToast();

  // Función para subir archivos al backend
  const handleUpload = async (files: File[]): Promise<void> => {
    setIsLoading(true);
    
    try {
      const response = await apiService.uploadFiles(files);
      
      const newFiles: FileItem[] = transformProcessedFilesToFrontend(response.files_processed);
      
      setIndexedFiles(prev => [...prev, ...newFiles]);
      toast({
        title: "Archivos subidos correctamente",
        description: response.message,
      });
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : "Error desconocido";
      toast({
        title: "Error al subir archivos",
        description: errorMessage,
        variant: "destructive",
      });
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  const handleSearch = async (query: string): Promise<SearchResult[]> => {
    setIsLoading(true);
    
    try {
      const response = await apiService.searchPassages(query, 5);
      return transformSearchResultsToFrontend(response);
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : "Error desconocido";
      toast({
        title: "Error en la búsqueda",
        description: errorMessage,
        variant: "destructive",
      });
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  const handleAsk = async (question: string): Promise<QAResponse> => {
    setIsLoading(true);
    
    try {
      const response = await apiService.askQuestion(question);
      return transformQAResponseToFrontend(response);
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : "Error desconocido";
      toast({
        title: "Error al procesar pregunta",
        description: errorMessage,
        variant: "destructive",
      });
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-background to-muted/20">
      <AppHeader activeTab={activeTab} onTabChange={setActiveTab} />
      
      <main className="max-w-4xl mx-auto px-4 py-8">
        <div className="animate-fade-in">
          {activeTab === 'upload' && (
            <Uploader 
              onUpload={handleUpload}
              indexedFiles={indexedFiles}
              isLoading={isLoading}
            />
          )}
          
          {activeTab === 'search' && (
            <SearchBox 
              onSearch={handleSearch}
              isLoading={isLoading}
            />
          )}
          
          {activeTab === 'qa' && (
            <QABox 
              onAsk={handleAsk}
              isLoading={isLoading}
            />
          )}
          
          {activeTab === 'status' && (
            <SystemStatus />
          )}
        </div>
      </main>
    </div>
  );
};

export default Index;
