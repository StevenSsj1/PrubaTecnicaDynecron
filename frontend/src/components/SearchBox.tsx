import React, { useState } from 'react';
import { Search, FileText, ExternalLink, Loader2 } from 'lucide-react';
import { Button } from './ui/button';
import { Card } from './ui/card';
import { Input } from './ui/input';

interface SearchResult {
  id: string;
  passage: string;
  source: string;
  score: number;
  page?: number;
}

interface SearchBoxProps {
  onSearch: (query: string) => Promise<SearchResult[]>;
  isLoading?: boolean;
}

export function SearchBox({ onSearch, isLoading }: SearchBoxProps) {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<SearchResult[]>([]);
  const [hasSearched, setHasSearched] = useState(false);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim() || isLoading) return;

    setHasSearched(true);
    try {
      const searchResults = await onSearch(query.trim());
      setResults(searchResults);
    } catch (error) {
      console.error('Search error:', error);
      setResults([]);
    }
  };

  const highlightText = (text: string, query: string) => {
    if (!query) return text;
    
    const regex = new RegExp(`(${query.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')})`, 'gi');
    const parts = text.split(regex);
    
    return parts.map((part, index) => 
      regex.test(part) ? (
        <mark key={index} className="bg-primary/20 text-primary-dark px-1 rounded">
          {part}
        </mark>
      ) : part
    );
  };

  return (
    <div className="space-y-6">
      <Card className="p-6">
        <div className="space-y-4">
          <div className="flex items-center gap-2">
            <Search className="h-5 w-5 text-primary" />
            <h2 className="text-lg font-semibold">Búsqueda de Documentos</h2>
          </div>
          
          <form onSubmit={handleSearch} className="flex gap-2">
            <Input
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Buscar en documentos..."
              className="flex-1"
              disabled={isLoading}
            />
            <Button type="submit" disabled={!query.trim() || isLoading}>
              {isLoading ? (
                <Loader2 className="h-4 w-4 animate-spin" />
              ) : (
                <Search className="h-4 w-4" />
              )}
            </Button>
          </form>
        </div>
      </Card>

      {hasSearched && (
        <div className="space-y-4">
          {results.length > 0 ? (
            <>
              <div className="flex items-center justify-between">
                <h3 className="font-medium">Resultados encontrados</h3>
                <span className="text-sm text-muted-foreground">
                  {results.length} {results.length === 1 ? 'resultado' : 'resultados'}
                </span>
              </div>
              
              <div className="space-y-3">
                {results.map((result) => (
                  <Card key={result.id} className="p-4 hover:shadow-md transition-shadow">
                    <div className="space-y-3">
                      <div className="flex items-start justify-between gap-3">
                        <div className="flex items-center gap-2 text-sm text-muted-foreground">
                          <FileText className="h-4 w-4" />
                          <span className="font-medium">{result.source}</span>
                          {result.page && (
                            <span>• Página {result.page}</span>
                          )}
                        </div>
                        <div className="flex items-center gap-2">
                          <span className="text-xs px-2 py-1 bg-primary/10 text-primary rounded-full">
                            {Math.round(result.score * 100)}% relevancia
                          </span>
                          <Button size="sm" variant="ghost" className="h-6 w-6 p-0">
                            <ExternalLink className="h-3 w-3" />
                          </Button>
                        </div>
                      </div>
                      
                      <div className="text-sm leading-relaxed">
                        <p className="text-foreground">
                          {highlightText(result.passage, query)}
                        </p>
                      </div>
                    </div>
                  </Card>
                ))}
              </div>
            </>
          ) : (
            <Card className="p-8 text-center">
              <Search className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
              <h3 className="font-medium mb-2">No se encontraron resultados</h3>
              <p className="text-sm text-muted-foreground">
                Intenta con términos diferentes o verifica que los documentos estén indexados
              </p>
            </Card>
          )}
        </div>
      )}
    </div>
  );
}