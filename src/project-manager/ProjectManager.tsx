import { useState, useEffect, useMemo } from "react";
import { ProjectManagerHeader } from "./ProjectManagerHeader";
import { ProjectManagerList } from "./ProjectManagerList";
import { listProjects } from "./legacy-api";

interface ProjectManagerProps {
  onNavigate: (view: "main" | "projects") => void;
}

export default function ProjectManager({ }: ProjectManagerProps) {
  const [projects, setProjects] = useState<any[]>([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [sortOrder, setSortOrder] = useState<"az" | "newest">("newest");

  useEffect(() => {
    fetchProjects();
  }, []);

  const fetchProjects = async () => {
    try {
      const data = await listProjects();
      setProjects(data);
    } catch (err) {
      console.error("Failed to load projects:", err);
    }
  };

  const processedProjects = useMemo(() => {
    return projects
      .filter((p) =>
        p.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        (p.description && p.description.toLowerCase().includes(searchTerm.toLowerCase()))
      )
      .sort((a, b) => {
        if (sortOrder === "az") {
          return a.name.localeCompare(b.name);
        }
        return new Date(b.updated_at).getTime() - new Date(a.updated_at).getTime();
      });
  }, [projects, searchTerm, sortOrder]);

  return (
    <div className="min-h-screen bg-[#FDFCFB] text-[#1C1917] font-sans">
      <ProjectManagerHeader
        searchTerm={searchTerm}
        onSearchChange={setSearchTerm}
        onNewProject={() => { }}
      />

      <main className="max-w-7xl mx-auto py-4">
        <ProjectManagerList
          projects={processedProjects}
          sortOrder={sortOrder}
          onSortChange={setSortOrder}
        />
      </main>
    </div>
  );
}
