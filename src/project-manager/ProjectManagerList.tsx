import { ChevronDown, MoreVertical } from "lucide-react";
import { Button } from "@/components/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/dropdown-menu";
import type { Project } from "./legacy-api";

interface ProjectManagerListProps {
  projects: Project[];
  sortOrder: "az" | "newest";
  onSortChange: (order: "az" | "newest") => void;
}

export function ProjectManagerList({ 
  projects, 
  sortOrder, 
  onSortChange 
}: ProjectManagerListProps) {
  return (
    <div className="px-8 py-4">
      <div className="flex items-center justify-between mb-8">
        <h1 className="text-2xl font-bold tracking-tight">Projects</h1>
        
        <DropdownMenu>
          <DropdownMenuTrigger render={
            <Button variant="ghost" className="text-sm text-gray-500 hover:text-black gap-2 h-9 px-3 rounded-full hover:bg-gray-100">
              <span className="text-gray-400">Sort:</span>
              {sortOrder === "az" ? "A-Z" : "Newest-Oldest"}
              <ChevronDown className="size-4" />
            </Button>
          } />
          <DropdownMenuContent align="end" className="min-w-40">
            <DropdownMenuItem onClick={() => onSortChange("az")}>
              A-Z
            </DropdownMenuItem>
            <DropdownMenuItem onClick={() => onSortChange("newest")}>
              Newest-Oldest
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        {projects.map((project) => (
          <div 
            key={project.id} 
            className="group relative bg-white border border-gray-100 rounded-2xl p-5 shadow-[0_2px_8px_-2px_rgba(0,0,0,0.05)] hover:shadow-[0_8px_24px_-4px_rgba(0,0,0,0.1)] transition-all hover:border-gray-200 cursor-pointer"
          >
            <div className="flex justify-between items-start mb-2">
              <h3 className="font-semibold text-lg truncate pr-6">{project.name}</h3>
              <Button variant="ghost" size="icon" className="size-8 opacity-0 group-hover:opacity-100 transition-opacity">
                <MoreVertical className="size-4" />
              </Button>
            </div>
            <p className="text-sm text-gray-500 line-clamp-2 mb-4 h-10 leading-relaxed">
              {project.description || "No description provided."}
            </p>
            <div className="flex items-center justify-between mt-auto pt-2 border-t border-gray-50">
              <span className="text-[11px] font-medium text-gray-400 uppercase tracking-wider">
                Updated {new Date(project.updated_at).toLocaleDateString(undefined, { month: 'short', day: 'numeric' })}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
