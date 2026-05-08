const API_BASE = "http://localhost:8000";

export interface Project {
  id: string;
  name: string;
  description: string | null;
  created_at: string;
  updated_at: string;
}

export async function listProjects(): Promise<Project[]> {
  const res = await fetch(`${API_BASE}/projects/`);
  if (!res.ok) throw new Error(`Failed to list projects: ${res.status}`);
  return res.json();
}

export async function createProject(name: string, description?: string): Promise<Project> {
  const res = await fetch(`${API_BASE}/projects/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name, description: description ?? null }),
  });
  if (!res.ok) throw new Error(`Failed to create project: ${res.status}`);
  return res.json();
}

export async function updateProject(id: string, data: { name?: string; description?: string }): Promise<Project> {
  const res = await fetch(`${API_BASE}/projects/${id}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error(`Failed to update project: ${res.status}`);
  return res.json();
}

export async function deleteProject(id: string): Promise<void> {
  const res = await fetch(`${API_BASE}/projects/${id}`, { method: "DELETE" });
  if (!res.ok) throw new Error(`Failed to delete project: ${res.status}`);
}
