import React, { useState, useCallback } from 'react';
import { Upload, FileText, X, Check, AlertCircle } from 'lucide-react';
import { Button } from '../components/ui/button';
import { Card } from '../components/ui/card';
import { cn } from '../lib/utils';

interface FileItem {
  id: string;
  name: string;
  size: number;
  status: 'uploading' | 'success' | 'error';
  progress?: number;
}

interface UploaderProps {
  onUpload: (files: File[]) => Promise<void>;
  indexedFiles: FileItem[];
  isLoading?: boolean;
}

export function Uploader({ onUpload, indexedFiles, isLoading }: UploaderProps) {
  const [isDragOver, setIsDragOver] = useState(false);
  const [uploadingFiles, setUploadingFiles] = useState<FileItem[]>([]);

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
  }, []);

  const handleDrop = useCallback(async (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);

    const files = Array.from(e.dataTransfer.files);
    if (files.length === 0) return;
    
    if (files.length < 3) {
      alert('Debes subir un mínimo de 3 documentos');
      return;
    }
    
    if (files.length > 10) {
      alert('No puedes subir más de 10 documentos a la vez');
      return;
    }

    const newUploadingFiles = files.map(file => ({
      id: Math.random().toString(36).substr(2, 9),
      name: file.name,
      size: file.size,
      status: 'uploading' as const,
      progress: 0
    }));

    setUploadingFiles(newUploadingFiles);

    try {
      await onUpload(files);
      setUploadingFiles(prev => 
        prev.map(file => ({ ...file, status: 'success' as const, progress: 100 }))
      );
      setTimeout(() => setUploadingFiles([]), 2000);
    } catch (error) {
      setUploadingFiles(prev => 
        prev.map(file => ({ ...file, status: 'error' as const }))
      );
    }
  }, [onUpload]);

  const handleFileSelect = useCallback(async (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(e.target.files || []);
    if (files.length === 0) return;
    
    if (files.length < 3) {
      alert('Debes subir un mínimo de 3 documentos');
      e.target.value = '';
      return;
    }
    
    if (files.length > 10) {
      alert('No puedes subir más de 10 documentos a la vez');
      e.target.value = '';
      return;
    }

    const newUploadingFiles = files.map(file => ({
      id: Math.random().toString(36).substr(2, 9),
      name: file.name,
      size: file.size,
      status: 'uploading' as const,
      progress: 0
    }));

    setUploadingFiles(newUploadingFiles);

    try {
      await onUpload(files);
      setUploadingFiles(prev => 
        prev.map(file => ({ ...file, status: 'success' as const, progress: 100 }))
      );
      setTimeout(() => setUploadingFiles([]), 2000);
    } catch (error) {
      setUploadingFiles(prev => 
        prev.map(file => ({ ...file, status: 'error' as const }))
      );
    }
    
    e.target.value = '';
  }, [onUpload]);

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const removeUploadingFile = (id: string) => {
    setUploadingFiles(prev => prev.filter(file => file.id !== id));
  };

  return (
    <div className="space-y-6">
      <Card className="p-6">
        <div className="space-y-4">
          <div className="flex items-center gap-2">
            <Upload className="h-5 w-5 text-primary" />
            <h2 className="text-lg font-semibold">Subir Documentos</h2>
          </div>
          
          <div
            className={cn(
              "border-2 border-dashed rounded-lg p-8 text-center transition-all duration-200",
              isDragOver
                ? "border-upload-border bg-upload-active scale-[1.02]"
                : "border-upload-border bg-upload-bg hover:bg-upload-active",
              isLoading && "opacity-50 pointer-events-none"
            )}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
          >
            <Upload className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
            <p className="text-lg font-medium mb-2">
              Arrastra documentos aquí o haz clic para seleccionar
            </p>
            <p className="text-sm text-muted-foreground mb-4">
              Admite PDF, DOCX, TXT y más formatos<br />
              <span className="text-xs">Mínimo 3 documentos, máximo 10</span>
            </p>
            
            <input
              type="file"
              multiple
              onChange={handleFileSelect}
              className="hidden"
              id="file-upload"
              accept=".pdf,.doc,.docx,.txt,.md"
              disabled={isLoading}
            />
            <Button asChild variant="outline">
              <label htmlFor="file-upload" className="cursor-pointer">
                Seleccionar archivos
              </label>
            </Button>
          </div>
        </div>
      </Card>

      {uploadingFiles.length > 0 && (
        <Card className="p-4">
          <h3 className="font-medium mb-3">Subiendo archivos</h3>
          <div className="space-y-2">
            {uploadingFiles.map((file) => (
              <div key={file.id} className="flex items-center gap-3 p-2 rounded-md bg-muted/30">
                <FileText className="h-4 w-4 text-muted-foreground" />
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium truncate">{file.name}</p>
                  <p className="text-xs text-muted-foreground">{formatFileSize(file.size)}</p>
                </div>
                <div className="flex items-center gap-2">
                  {file.status === 'uploading' && (
                    <div className="animate-pulse-soft">
                      <div className="h-2 w-16 bg-primary/20 rounded-full overflow-hidden">
                        <div className="h-full bg-primary rounded-full animate-pulse" />
                      </div>
                    </div>
                  )}
                  {file.status === 'success' && (
                    <Check className="h-4 w-4 text-success" />
                  )}
                  {file.status === 'error' && (
                    <AlertCircle className="h-4 w-4 text-destructive" />
                  )}
                  <Button
                    size="sm"
                    variant="ghost"
                    onClick={() => removeUploadingFile(file.id)}
                    className="h-6 w-6 p-0"
                  >
                    <X className="h-3 w-3" />
                  </Button>
                </div>
              </div>
            ))}
          </div>
        </Card>
      )}

      {indexedFiles.length > 0 && (
        <Card className="p-4">
          <h3 className="font-medium mb-3">Documentos indexados ({indexedFiles.length})</h3>
          <div className="space-y-2 max-h-64 overflow-y-auto">
            {indexedFiles.map((file) => (
              <div key={file.id} className="flex items-center gap-3 p-2 rounded-md hover:bg-muted/30 transition-colors">
                <FileText className="h-4 w-4 text-muted-foreground" />
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium truncate">{file.name}</p>
                  <p className="text-xs text-muted-foreground">{formatFileSize(file.size)}</p>
                </div>
                <div className="flex items-center gap-2">
                  {file.status === 'success' && (
                    <Check className="h-4 w-4 text-success" />
                  )}
                  {file.status === 'error' && (
                    <AlertCircle className="h-4 w-4 text-destructive" />
                  )}
                </div>
              </div>
            ))}
          </div>
        </Card>
      )}
    </div>
  );
}