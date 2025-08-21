import { FileSearch, Upload, Search, MessageCircle, Settings } from 'lucide-react';

interface AppHeaderProps {
  activeTab: string;
  onTabChange: (tab: string) => void;
}

export function AppHeader({ activeTab, onTabChange }: AppHeaderProps) {
  const tabs = [
    { id: 'upload', name: 'Subir', icon: Upload },
    { id: 'search', name: 'Buscar', icon: Search },
    { id: 'qa', name: 'Q&A', icon: MessageCircle },
    { id: 'status', name: 'Estado', icon: Settings }
  ];

  return (
    <header className="bg-background border-b shadow-sm sticky top-0 z-10">
      <div className="max-w-6xl mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="flex items-center gap-2">
              <FileSearch className="h-8 w-8 text-primary" />
              <h1 className="text-2xl font-bold bg-gradient-primary bg-clip-text text-transparent">
                DocSearch
              </h1>
            </div>
            <div className="hidden sm:block text-sm text-muted-foreground">
              Busca y analiza documentos con IA
            </div>
          </div>
          
          <nav className="flex items-center gap-1 bg-muted/30 rounded-lg p-1">
            {tabs.map((tab) => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => onTabChange(tab.id)}
                  className={`
                    flex items-center gap-2 px-4 py-2 rounded-md text-sm font-medium transition-all
                    ${activeTab === tab.id 
                      ? 'bg-background text-primary shadow-sm' 
                      : 'text-muted-foreground hover:text-foreground hover:bg-background/50'
                    }
                  `}
                >
                  <Icon className="h-4 w-4" />
                  <span className="hidden sm:inline">{tab.name}</span>
                </button>
              );
            })}
          </nav>
        </div>
      </div>
    </header>
  );
}