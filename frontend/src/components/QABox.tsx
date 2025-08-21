import React, { useState } from 'react';
import { MessageCircle, Send, Bot, User, Quote, FileText, Loader2 } from 'lucide-react';
import { Button } from './ui/button';
import { Card } from './ui/card';
import { Textarea } from './ui/textarea';

interface Citation {
  id: string;
  source: string;
  page?: number;
  text: string;
}

interface QAResponse {
  id: string;
  answer: string;
  citations: Citation[];
  timestamp: Date;
}

interface Conversation {
  id: string;
  question: string;
  response?: QAResponse;
  timestamp: Date;
}

interface QABoxProps {
  onAsk: (question: string) => Promise<QAResponse>;
  isLoading?: boolean;
}

export function QABox({ onAsk, isLoading }: QABoxProps) {
  const [question, setQuestion] = useState('');
  const [conversations, setConversations] = useState<Conversation[]>([]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!question.trim() || isLoading) return;

    const newConversation: Conversation = {
      id: Math.random().toString(36).substr(2, 9),
      question: question.trim(),
      timestamp: new Date()
    };

    setConversations(prev => [newConversation, ...prev]);
    setQuestion('');

    try {
      const response = await onAsk(newConversation.question);
      setConversations(prev => 
        prev.map(conv => 
          conv.id === newConversation.id 
            ? { ...conv, response }
            : conv
        )
      );
    } catch (error) {
      console.error('Q&A error:', error);
      // Handle error state if needed
    }
  };

  const formatTime = (date: Date) => {
    return new Intl.DateTimeFormat('es-ES', {
      hour: '2-digit',
      minute: '2-digit'
    }).format(date);
  };

  return (
    <div className="space-y-6">
      <Card className="p-6">
        <div className="space-y-4">
          <div className="flex items-center gap-2">
            <MessageCircle className="h-5 w-5 text-primary" />
            <h2 className="text-lg font-semibold">Preguntas y Respuestas</h2>
          </div>
          
          <form onSubmit={handleSubmit} className="space-y-3">
            <Textarea
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="Haz una pregunta sobre los documentos..."
              className="min-h-[100px] resize-none"
              disabled={isLoading}
            />
            <div className="flex justify-end">
              <Button type="submit" disabled={!question.trim() || isLoading}>
                {isLoading ? (
                  <Loader2 className="h-4 w-4 animate-spin mr-2" />
                ) : (
                  <Send className="h-4 w-4 mr-2" />
                )}
                Preguntar
              </Button>
            </div>
          </form>
        </div>
      </Card>

      {conversations.length > 0 && (
        <div className="space-y-4">
          <h3 className="font-medium">Conversación</h3>
          
          <div className="space-y-6">
            {conversations.map((conversation) => (
              <div key={conversation.id} className="space-y-4">
                {/* User Question */}
                <div className="flex gap-3">
                  <div className="flex-shrink-0">
                    <div className="w-8 h-8 rounded-full bg-secondary flex items-center justify-center">
                      <User className="h-4 w-4" />
                    </div>
                  </div>
                  <Card className="flex-1 p-4">
                    <div className="space-y-2">
                      <div className="flex items-center justify-between">
                        <span className="text-sm font-medium">Tú</span>
                        <span className="text-xs text-muted-foreground">
                          {formatTime(conversation.timestamp)}
                        </span>
                      </div>
                      <p className="text-sm">{conversation.question}</p>
                    </div>
                  </Card>
                </div>

                {/* AI Response */}
                {conversation.response ? (
                  <div className="flex gap-3">
                    <div className="flex-shrink-0">
                      <div className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center">
                        <Bot className="h-4 w-4 text-primary" />
                      </div>
                    </div>
                    <Card className="flex-1 p-4">
                      <div className="space-y-4">
                        <div className="flex items-center justify-between">
                          <span className="text-sm font-medium">Asistente</span>
                          <span className="text-xs text-muted-foreground">
                            {formatTime(conversation.response.timestamp)}
                          </span>
                        </div>
                        
                        <div className="prose prose-sm max-w-none">
                          <p className="text-sm leading-relaxed whitespace-pre-wrap">
                            {conversation.response.answer}
                          </p>
                        </div>

                        {conversation.response.citations.length > 0 && (
                          <div className="space-y-3 pt-3 border-t">
                            <div className="flex items-center gap-2">
                              <Quote className="h-4 w-4 text-muted-foreground" />
                              <span className="text-sm font-medium">Fuentes</span>
                            </div>
                            <div className="space-y-2">
                              {conversation.response.citations.map((citation) => (
                                <div key={citation.id} className="bg-muted/30 rounded-md p-3">
                                  <div className="flex items-center gap-2 mb-2">
                                    <FileText className="h-3 w-3 text-muted-foreground" />
                                    <span className="text-xs font-medium text-muted-foreground">
                                      {citation.source}
                                      {citation.page && ` • Página ${citation.page}`}
                                    </span>
                                  </div>
                                  <p className="text-xs text-muted-foreground italic">
                                    "{citation.text}"
                                  </p>
                                </div>
                              ))}
                            </div>
                          </div>
                        )}
                      </div>
                    </Card>
                  </div>
                ) : (
                  <div className="flex gap-3">
                    <div className="flex-shrink-0">
                      <div className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center">
                        <Bot className="h-4 w-4 text-primary" />
                      </div>
                    </div>
                    <Card className="flex-1 p-4">
                      <div className="flex items-center gap-2">
                        <Loader2 className="h-4 w-4 animate-spin text-primary" />
                        <span className="text-sm text-muted-foreground">Procesando pregunta...</span>
                      </div>
                    </Card>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {conversations.length === 0 && (
        <Card className="p-8 text-center">
          <MessageCircle className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
          <h3 className="font-medium mb-2">Comienza una conversación</h3>
          <p className="text-sm text-muted-foreground">
            Haz preguntas en lenguaje natural sobre tus documentos
          </p>
        </Card>
      )}
    </div>
  );
}