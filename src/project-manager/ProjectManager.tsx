import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Plus, FolderOpen, MoreVertical, Search, ArrowLeft, LayoutGrid, List } from "lucide-react";
import "./ProjectManager.css";

export default function ProjectManager() {
  const navigate = useNavigate();
  const [searchTerm, setSearchTerm] = useState("");
  const [sortOrder, setSortOrder] = useState<"newest" | "oldest">("newest");
  const [viewMode, setViewMode] = useState<"grid" | "list">("list");

  const projects = [
    { id: 1, name: "public", type: "folder", items: 3, updatedAt: "2025-12-14" },
    { id: 2, name: "public", type: "folder", items: 3, updatedAt: "2025-12-11" },
    { id: 3, name: "public", type: "folder", items: 3, updatedAt: "2025-12-09" },
    { id: 4, name: "Test Project", type: "project", date: "Last edited: Dec 12, 2025", updatedAt: "2025-12-12" },
    { id: 5, name: "Project 1", type: "project", date: "Last edited: Dec 10, 2025", updatedAt: "2025-12-10" },
    { id: 6, name: "New Project", type: "project", date: "Last edited: Dec 08, 2025", updatedAt: "2025-12-08" },
  ];

  const filteredProjects = projects.filter((project) =>
    project.name.toLowerCase().includes(searchTerm.toLowerCase()) &&
    (project.updatedAt ?? project.date) !== undefined &&
    !(project.type === "folder" && project.name.toLowerCase() === "public")
  );

  const sortedProjects = [...filteredProjects].sort((a, b) => {
    const aTime = new Date(a.updatedAt ?? a.date).getTime();
    const bTime = new Date(b.updatedAt ?? b.date).getTime();
    return sortOrder === "newest" ? bTime - aTime : aTime - bTime;
  });

  return (
    <div className="project-manager">
      <div className="pm-container">
        {/* Header */}
        <div className="pm-header">
          <button className="pm-back-btn" onClick={() => navigate("/")}>
            <ArrowLeft size={20} />
          </button>
          <h1 className="pm-title">Project Manager</h1>
        </div>

        {/* Search & Sort Bar */}
        <div className="pm-search-sort-container">
          <button className="pm-btn-primary">
            <Plus size={16} />
            New Project
          </button>

          <div className="pm-search-wrapper">
            <Search className="pm-search-icon" size={16} />
            <input
              type="text"
              placeholder="Search projects..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pm-search-input"
            />
          </div>

          <div className="pm-sort-row">
            <label htmlFor="sort-order" className="pm-sort-label">
              Sort by
            </label>
            <select
              id="sort-order"
              value={sortOrder}
              onChange={(e) => setSortOrder(e.target.value as "newest" | "oldest")}
              className="pm-sort-select"
            >
              <option value="newest">Newest first</option>
              <option value="oldest">Oldest first</option>
            </select>
          </div>

          <div className="pm-view-toggle">
            <button
              className={`pm-view-btn ${viewMode === "list" ? "active" : ""}`}
              onClick={() => setViewMode("list")}
              title="List view"
            >
              <List size={18} />
            </button>
            <button
              className={`pm-view-btn ${viewMode === "grid" ? "active" : ""}`}
              onClick={() => setViewMode("grid")}
              title="Grid view"
            >
              <LayoutGrid size={18} />
            </button>
          </div>
        </div>

        {/* Projects Section */}
        <div>
          <h2 className="pm-section-title">All projects</h2>
          
          <div className={`pm-projects-list pm-${viewMode}-view`}>
            {sortedProjects.map((project) => (
              <div key={project.id} className="pm-project-item">
                <div className="pm-project-info">
                  <FolderOpen size={40} className="pm-project-icon" />
                  <div>
                    <h3 className="pm-project-name">{project.name}</h3>
                    {project.type === "folder" ? (
                      <p className="pm-project-meta">{project.items} items</p>
                    ) : (
                      <p className="pm-project-meta">{project.date}</p>
                    )}
                  </div>
                </div>
                <button className="pm-project-menu">
                  <MoreVertical size={18} />
                </button>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}