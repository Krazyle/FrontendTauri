import { Plus, Search, X } from "lucide-react";
import { Button } from "@/components/button";
import { Input } from "@/components/input";

interface ProjectManagerHeaderProps {
  onNewProject: () => void;
  searchTerm: string;
  onSearchChange: (value: string) => void;
}

export function ProjectManagerHeader({ 
  onNewProject, 
  searchTerm, 
  onSearchChange
}: ProjectManagerHeaderProps) {
  return (
    <header className="flex items-center justify-between px-8 py-6">
      <div className="flex-1">
        <div className="text-3xl font-bold tracking-tighter text-black">Geon</div>
      </div>
      
      <div className="flex-[2] flex justify-center px-4">
        <div className="relative w-full max-w-xl">
          <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 size-4 text-gray-400 pointer-events-none" />
          <Input 
            type="search"
            placeholder="Search projects..."
            value={searchTerm}
            onChange={(e) => onSearchChange(e.target.value)}
            className="pl-11 pr-11 bg-[#F1F0EE] border-none shadow-none ring-0 focus-visible:ring-0 focus:bg-[#E8E7E5] transition-all h-11 rounded-full w-full [&::-webkit-search-cancel-button]:appearance-none"
          />
          {searchTerm && (
            <button 
              onClick={() => onSearchChange("")}
              className="absolute right-3.5 top-1/2 -translate-y-1/2 p-1 text-gray-400 hover:text-black transition-colors rounded-full hover:bg-gray-200"
            >
              <X className="size-3.5" />
            </button>
          )}
        </div>
      </div>

      <div className="flex-1 flex items-center justify-end gap-4">
        <Button 
          onClick={onNewProject}
          className="bg-black text-white hover:bg-gray-800 rounded-full px-6 h-11 flex items-center gap-2"
        >
          <Plus className="size-4" />
          New project
        </Button>
      </div>
    </header>
  );
}
