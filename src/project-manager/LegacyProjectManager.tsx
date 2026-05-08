import { useState, useEffect, useRef } from "react";
import { Plus, FolderOpen, MoreVertical, Search, ArrowLeft, LayoutGrid, List, Loader2, X, Trash2, Edit2 } from "lucide-react";
import { listProjects, createProject, updateProject, deleteProject, type Project } from "./legacy-api";

interface ProjectManagerProps {
  onNavigate: (view: "main" | "projects") => void;
}

export default function LegacyProjectManager({ onNavigate }: ProjectManagerProps) {
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState("");
  const [sortOrder, setSortOrder] = useState<"newest" | "oldest">("newest");
  const [viewMode, setViewMode] = useState<"grid" | "list">("list");

  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
  const [newProjectName, setNewProjectName] = useState("");
  const [newProjectDesc, setNewProjectDesc] = useState("");

  const [activeMenuId, setActiveMenuId] = useState<string | null>(null);
  const [editingProjectId, setEditingProjectId] = useState<string | null>(null);
  const [editNameValue, setEditNameValue] = useState("");

  const menuRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    fetchProjects();
    
    const handleClickOutside = (event: MouseEvent) => {
      if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
        setActiveMenuId(null);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const fetchProjects = async () => {
    setLoading(true);
    try {
      const data = await listProjects();
      setProjects(data);
      setError(null);
    } catch (err) {
      setError("Failed to load projects. Please check if the backend is running.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateProject = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newProjectName.trim()) return;
    try {
      const created = await createProject(newProjectName, newProjectDesc);
      setProjects([created, ...projects]);
      setIsCreateModalOpen(false);
      setNewProjectName("");
      setNewProjectDesc("");
    } catch (err) {
      alert("Failed to create project");
    }
  };

  const handleDeleteProject = async (id: string, name: string) => {
    if (!window.confirm(`Are you sure you want to delete "${name}"?`)) return;
    try {
      await deleteProject(id);
      setProjects(projects.filter(p => p.id !== id));
      setActiveMenuId(null);
    } catch (err) {
      alert("Failed to delete project");
    }
  };

  const handleRename = async (id: string) => {
    if (!editNameValue.trim()) {
      setEditingProjectId(null);
      return;
    }
    try {
      const updated = await updateProject(id, { name: editNameValue });
      setProjects(projects.map(p => p.id === id ? updated : p));
      setEditingProjectId(null);
    } catch (err) {
      alert("Failed to rename project");
    }
  };

  const filteredProjects = projects.filter((project) =>
    project.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const sortedProjects = [...filteredProjects].sort((a, b) => {
    const aTime = new Date(a.updated_at).getTime();
    const bTime = new Date(b.updated_at).getTime();
    return sortOrder === "newest" ? bTime - aTime : aTime - bTime;
  });

  const formatDate = (dateStr: string) => {
    const date = new Date(dateStr);
    return `Last edited: ${date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}`;
  };

  return (
    <div className="min-h-screen bg-background text-foreground">
      <div className="w-full max-w-full p-8">
        <div className="flex items-center gap-4 mb-8">
          <button 
            className="p-2 rounded-md bg-transparent border-none cursor-pointer text-foreground hover:bg-accent transition-colors" 
            onClick={() => onNavigate("main")}
          >
            <ArrowLeft size={20} />
          </button>
          <h1 className="text-2xl font-semibold text-foreground">Project Manager</h1>
        </div>

        <div className="flex justify-start items-end gap-4 mb-8">
          <button 
            className="inline-flex items-center gap-2 px-4 py-2 rounded-md bg-primary text-primary-foreground border-none text-sm font-medium cursor-pointer shrink-0 hover:opacity-90 transition-opacity" 
            onClick={() => setIsCreateModalOpen(true)}
          >
            <Plus size={16} />
            New Project
          </button>

          <div className="flex-1 relative min-w-[200px]">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground" size={16} />
            <input
              type="text"
              placeholder="Search projects..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full py-2 pr-3 pl-9 rounded-md border border-border bg-background text-foreground text-sm placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring"
            />
          </div>

          <div className="flex items-center gap-3 shrink-0">
            <label htmlFor="sort-order" className="text-sm font-medium text-foreground">
              Sort by
            </label>
            <select
              id="sort-order"
              value={sortOrder}
              onChange={(e) => setSortOrder(e.target.value as "newest" | "oldest")}
              className="min-w-48 py-2 px-3 rounded-md border border-border bg-background text-foreground text-sm"
            >
              <option value="newest">Newest first</option>
              <option value="oldest">Oldest first</option>
            </select>
          </div>

          <div className="flex gap-1 border border-border rounded-md bg-background p-0.5 items-center">
            <button
              className={`flex items-center justify-center py-1 px-2 border-none cursor-pointer rounded transition-all ${viewMode === "list" ? "bg-primary text-primary-foreground" : "bg-transparent text-muted-foreground"}`}
              onClick={() => setViewMode("list")}
              title="List view"
            >
              <List size={18} />
            </button>
            <button
              className={`flex items-center justify-center py-1 px-2 border-none cursor-pointer rounded transition-all ${viewMode === "grid" ? "bg-primary text-primary-foreground" : "bg-transparent text-muted-foreground"}`}
              onClick={() => setViewMode("grid")}
              title="Grid view"
            >
              <LayoutGrid size={18} />
            </button>
          </div>
        </div>

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-800 p-4 rounded-xl mb-8 flex justify-between items-center text-sm">
            {error}
            <button className="bg-white border border-red-200 px-3 py-1 rounded-md" onClick={fetchProjects}>Retry</button>
          </div>
        )}

        <div>
          <h2 className="text-sm font-medium text-muted-foreground mb-3">All projects</h2>
          
          {loading ? (
            <div className="flex flex-col items-center justify-center py-20 px-8 text-center gap-4 text-muted-foreground">
              <Loader2 className="animate-spin" size={32} />
              <p>Loading projects...</p>
            </div>
          ) : projects.length === 0 ? (
            <div className="flex flex-col items-center justify-center py-20 px-8 text-center gap-4 text-muted-foreground">
              <FolderOpen size={48} />
              <h3 className="text-lg font-medium text-foreground">No projects found</h3>
              <p>Create your first project to get started.</p>
              <button 
                className="inline-flex items-center gap-2 px-4 py-2 rounded-md bg-secondary text-secondary-foreground border-none text-sm font-medium cursor-pointer shrink-0 hover:opacity-90 transition-opacity" 
                onClick={() => setIsCreateModalOpen(true)}
              >
                Create Project
              </button>
            </div>
          ) : (
            <div className={viewMode === "list" 
              ? "flex flex-col border border-border rounded-lg bg-card overflow-hidden" 
              : "grid grid-cols-[repeat(auto-fill,minmax(280px,1fr))] gap-4 p-4"}>
              {sortedProjects.map((project) => (
                <div key={project.id} className="flex items-center justify-between p-4 border-b border-border cursor-pointer transition-colors hover:bg-accent/50 group last:border-b-0">
                  <div className="flex items-center gap-3 flex-1">
                    <FolderOpen size={40} className="text-muted-foreground min-w-[40px]" />
                    <div className="flex-1">
                      {editingProjectId === project.id ? (
                        <input
                          autoFocus
                          className="text-base font-semibold bg-muted border border-ring rounded px-1 py-0.5 w-full outline-none"
                          value={editNameValue}
                          onChange={(e) => setEditNameValue(e.target.value)}
                          onBlur={() => handleRename(project.id)}
                          onKeyDown={(e) => e.key === 'Enter' && handleRename(project.id)}
                        />
                      ) : (
                        <h3 className="font-medium text-foreground">{project.name}</h3>
                      )}
                      <p className="text-sm text-muted-foreground">{formatDate(project.updated_at)}</p>
                      {project.description && (
                        <p className="text-sm text-muted-foreground mt-2 line-clamp-2">{project.description}</p>
                      )}
                    </div>
                  </div>
                  <div className="relative">
                    <button 
                      className="p-2 rounded-md bg-transparent border-none cursor-pointer text-muted-foreground hover:bg-accent transition-colors" 
                      onClick={(e) => {
                        e.stopPropagation();
                        setActiveMenuId(activeMenuId === project.id ? null : project.id);
                      }}
                    >
                      <MoreVertical size={18} />
                    </button>
                    {activeMenuId === project.id && (
                      <div className="absolute right-0 top-full z-50 bg-background border border-border rounded-xl shadow-lg p-2 min-w-[140px] flex flex-col" ref={menuRef}>
                        <button 
                          className="flex items-center gap-2 p-2 text-sm bg-transparent border-none rounded-md cursor-pointer text-left hover:bg-accent"
                          onClick={() => {
                            setEditingProjectId(project.id);
                            setEditNameValue(project.name);
                            setActiveMenuId(null);
                          }}
                        >
                          <Edit2 size={14} /> Rename
                        </button>
                        <button 
                          className="flex items-center gap-2 p-2 text-sm bg-transparent border-none rounded-md cursor-pointer text-left text-red-600 hover:bg-red-50" 
                          onClick={() => handleDeleteProject(project.id, project.name)}
                        >
                          <Trash2 size={14} /> Delete
                        </button>
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {isCreateModalOpen && (
        <div className="fixed inset-0 bg-black/40 backdrop-blur-sm flex items-center justify-center z-[100]">
          <div className="bg-background w-full max-w-[450px] rounded-2xl p-8 shadow-2xl animate-in fade-in zoom-in-95">
            <div className="flex justify-between items-center mb-6">
              <h3 className="text-xl font-bold">Create New Project</h3>
              <button className="bg-transparent border-none cursor-pointer text-muted-foreground" onClick={() => setIsCreateModalOpen(false)}>
                <X size={20} />
              </button>
            </div>
            <form onSubmit={handleCreateProject}>
              <div className="mb-6">
                <label className="block text-sm font-semibold mb-2">Project Name</label>
                <input
                  autoFocus
                  required
                  placeholder="e.g. My GIS Project"
                  value={newProjectName}
                  onChange={(e) => setNewProjectName(e.target.value)}
                  className="w-full p-3 rounded-xl border border-border bg-background text-sm focus:outline-none focus:border-ring"
                />
              </div>
              <div className="mb-6">
                <label className="block text-sm font-semibold mb-2">Description (Optional)</label>
                <textarea
                  placeholder="Tell us more about this project..."
                  value={newProjectDesc}
                  onChange={(e) => setNewProjectDesc(e.target.value)}
                  rows={3}
                  className="w-full p-3 rounded-xl border border-border bg-background text-sm focus:outline-none focus:border-ring"
                />
              </div>
              <div className="flex justify-end gap-4 mt-8">
                <button type="button" className="bg-transparent border-none px-4 py-2 text-sm font-semibold cursor-pointer text-muted-foreground hover:text-foreground" onClick={() => setIsCreateModalOpen(false)}>
                  Cancel
                </button>
                <button type="submit" className="inline-flex items-center gap-2 px-4 py-2 rounded-md bg-primary text-primary-foreground border-none text-sm font-medium cursor-pointer shrink-0 hover:opacity-90 transition-opacity">
                  Create Project
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
