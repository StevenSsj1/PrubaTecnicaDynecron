import { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Badge } from '../components/ui/badge';
import { Alert, AlertDescription } from '../components/ui/alert';
import { useToast } from '../hooks/use-toast';
import { apiService, type StatusResponse } from '../services/api';
import { 
  RefreshCw, 
  Database, 
  FileText, 
  Zap, 
  Trash2, 
  AlertCircle, 
  CheckCircle,
  Server
} from 'lucide-react';

export const SystemStatus = () => {
  const [status, setStatus] = useState<StatusResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isClearing, setIsClearing] = useState(false);
  const { toast } = useToast();

  const fetchStatus = async () => {
    setIsLoading(true);
    try {
      const statusData = await apiService.getStatus();
      setStatus(statusData);
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : "Error desconocido";
      toast({
        title: "Error al obtener estado",
        description: errorMessage,
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleClearDocuments = async () => {
    setIsClearing(true);
    try {
      await apiService.clearDocuments();
      toast({
        title: "Documentos eliminados",
        description: "Todos los documentos han sido eliminados del sistema",
      });
      // Actualizar el estado después de limpiar
      await fetchStatus();
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : "Error desconocido";
      toast({
        title: "Error al eliminar documentos",
        description: errorMessage,
        variant: "destructive",
      });
    } finally {
      setIsClearing(false);
    }
  };

  useEffect(() => {
    fetchStatus();
  }, []);

  if (!status && !isLoading) {
    return (
      <Alert>
        <AlertCircle className="h-4 w-4" />
        <AlertDescription>
          No se pudo cargar el estado del sistema
        </AlertDescription>
      </Alert>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold">Estado del Sistema</h2>
          <p className="text-muted-foreground">
            Información detallada sobre el estado actual del sistema
          </p>
        </div>
        <Button
          onClick={fetchStatus}
          disabled={isLoading}
          variant="outline"
          size="sm"
        >
          <RefreshCw className={`h-4 w-4 mr-2 ${isLoading ? 'animate-spin' : ''}`} />
          Actualizar
        </Button>
      </div>

      {status && (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {/* Estado del LLM */}
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Estado del LLM</CardTitle>
              <Server className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="flex items-center space-x-2">
                {status.llm_available ? (
                  <>
                    <CheckCircle className="h-5 w-5 text-green-500" />
                    <Badge variant="default" className="bg-green-100 text-green-800">
                      Disponible
                    </Badge>
                  </>
                ) : (
                  <>
                    <AlertCircle className="h-5 w-5 text-red-500" />
                    <Badge variant="destructive">
                      No disponible
                    </Badge>
                  </>
                )}
              </div>
            </CardContent>
          </Card>

          {/* Documentos indexados */}
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Documentos</CardTitle>
              <FileText className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{status.indexed_documents}</div>
              <p className="text-xs text-muted-foreground">
                documentos indexados
              </p>
            </CardContent>
          </Card>

          {/* Fragmentos procesados */}
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Fragmentos</CardTitle>
              <Database className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{status.total_chunks}</div>
              <p className="text-xs text-muted-foreground">
                fragmentos procesados
              </p>
            </CardContent>
          </Card>

          {/* Vectores indexados */}
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Vectores</CardTitle>
              <Zap className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{status.indexed_vectors}</div>
              <p className="text-xs text-muted-foreground">
                vectores en FAISS
              </p>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Lista de documentos disponibles */}
      {status && status.available_documents.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>Documentos Disponibles</CardTitle>
            <CardDescription>
              Lista de documentos actualmente indexados en el sistema
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              {status.available_documents.map((doc, index) => (
                <div
                  key={index}
                  className="flex items-center space-x-2 p-2 bg-muted rounded-md"
                >
                  <FileText className="h-4 w-4 text-muted-foreground" />
                  <span className="text-sm">{doc}</span>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Acción para limpiar documentos */}
      {status && status.indexed_documents > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="text-red-600">Zona de Peligro</CardTitle>
            <CardDescription>
              Acciones que afectarán permanentemente el sistema
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <Alert>
                <AlertCircle className="h-4 w-4" />
                <AlertDescription>
                  Eliminar todos los documentos borrará permanentemente todos los archivos 
                  indexados y sus datos asociados.
                </AlertDescription>
              </Alert>
              
              <Button
                onClick={handleClearDocuments}
                disabled={isClearing}
                variant="destructive"
                className="w-full"
              >
                <Trash2 className={`h-4 w-4 mr-2 ${isClearing ? 'animate-pulse' : ''}`} />
                {isClearing ? 'Eliminando...' : 'Eliminar Todos los Documentos'}
              </Button>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Mensaje cuando no hay documentos */}
      {status && status.indexed_documents === 0 && (
        <Alert>
          <FileText className="h-4 w-4" />
          <AlertDescription>
            No hay documentos indexados en el sistema. 
            Sube algunos archivos para comenzar a usar el asistente.
          </AlertDescription>
        </Alert>
      )}
    </div>
  );
};
