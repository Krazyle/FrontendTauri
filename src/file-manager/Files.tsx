import { useState, useMemo } from "react";
import { Button } from "@/components/button";
import { Search, File, Plus, Map, X, ChevronRight, CheckCircle2 } from "lucide-react";
import { SimulationFile } from "./Types";
import { mockFiles } from "./mockData";

const viewableMapExtensions = new Set(["json", "geojson"])  ;

function getFileExtension(fileName: string) {
  return fileName.split(".").pop()?.toLowerCase() ?? "";
}

function getFileIcon(fileName: string) {
  const ext = getFileExtension(fileName);
  if (viewableMapExtensions.has(ext)) return Map;
  return File;
}

function isMapFile(fileName: string) {
  const ext = getFileExtension(fileName);
  return viewableMapExtensions.has(ext);
}

function getFileType(fileName: string) {
  const ext = getFileExtension(fileName);
  return ext.toUpperCase() || "FILE";
}

export default function Files() {
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedFolder, setSelectedFolder] = useState<string | null>(null);
  const [selectedFile, setSelectedFile] = useState<SimulationFile | null>(null);
  const [viewMode, setViewMode] = useState<"grid" | "table">("table");
  const [selectedRows, setSelectedRows] = useState<Set<string>>(new Set());

  const filteredFiles = useMemo(() => {
    return mockFiles.filter(file => {
      const matchesSearch = file.name.toLowerCase().includes(searchQuery.toLowerCase());
      const matchesFolder = !selectedFolder || file.path.startsWith(selectedFolder);
      return matchesSearch && matchesFolder;
    });
  }, [searchQuery, selectedFolder]);

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return "0 Bytes";
    const k = 1024;
    const sizes = ["Bytes", "KB", "MB", "GB"];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return `${parseFloat((bytes / Math.pow(k, i)).toFixed(2))} ${sizes[i]}`;
  };

  const toggleRowSelection = (filePath: string) => {
    const newSelected = new Set(selectedRows);
    if (newSelected.has(filePath)) {
      newSelected.delete(filePath);
    } else {
      newSelected.add(filePath);
    }
    setSelectedRows(newSelected);
  };

  const toggleAllRows = () => {
    if (selectedRows.size === filteredFiles.length) {
      setSelectedRows(new Set());
    } else {
      setSelectedRows(new Set(filteredFiles.map(f => f.path)));
    }
  };

  const showRightPanel = selectedFile && isMapFile(selectedFile.name);

  // Generate breadcrumb segments
  const breadcrumbSegments = useMemo(() => {
    if (!selectedFolder) return [{ label: "All Files", path: null }];
    const segments = selectedFolder.split("/").filter(Boolean);
    const breadcrumbs = [{ label: "All Files", path: null as string | null }];
    let currentPath = "";
    segments.forEach(segment => {
      currentPath += "/" + segment;
      breadcrumbs.push({ label: segment, path: currentPath });
    });
    return breadcrumbs;
  }, [selectedFolder]);

  return (
    <div className="flex h-screen bg-slate-50 p-4 gap-4">
      {/* MAIN CONTENT: Full-width file list */}
      <main className="flex-1 flex flex-col overflow-hidden rounded-[24px] border border-slate-200 bg-white shadow-sm">
        {/* Header with breadcrumbs, search, and controls */}
        <div className="border-b border-slate-200 p-4 space-y-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              {/* Breadcrumb Navigation */}
              <nav className="flex items-center gap-1 text-sm">
                {breadcrumbSegments.map((segment, index) => (
                  <div key={segment.path || "root"} className="flex items-center gap-1">
                    {index > 0 && <ChevronRight className="h-3 w-3 text-slate-400" />}
                    <button
                      onClick={() => setSelectedFolder(segment.path)}
                      className={`px-2 py-1 rounded text-xs font-medium transition ${
                        selectedFolder === segment.path
                          ? "bg-slate-100 text-slate-900"
                          : "text-slate-600 hover:bg-slate-50 hover:text-slate-900"
                      }`}
                    >
                      {segment.label}
                    </button>
                  </div>
                ))}
              </nav>

              <div className="text-sm text-slate-500">
                {filteredFiles.length} files
              </div>
            </div>

            <div className="flex items-center gap-3">
              {/* Industrial-style view toggle */}
              <div className="flex border border-slate-300 rounded">
                <button
                  className={`px-3 py-1.5 text-xs font-medium transition ${
                    viewMode === "grid"
                      ? "bg-slate-900 text-white"
                      : "text-slate-600 hover:bg-slate-50"
                  }`}
                  onClick={() => setViewMode("grid")}
                >
                  Grid
                </button>
                <button
                  className={`px-3 py-1.5 text-xs font-medium transition ${
                    viewMode === "table"
                      ? "bg-slate-900 text-white"
                      : "text-slate-600 hover:bg-slate-50"
                  }`}
                  onClick={() => setViewMode("table")}
                >
                  Table
                </button>
              </div>

              <Button variant="outline" size="sm">
                <Plus className="w-4 h-4" />
              </Button>
            </div>
          </div>

          {/* Integrated search input */}
          <div className="relative max-w-md">
            <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />
            <input
              type="text"
              placeholder="Search files..."
              value={searchQuery}
              onChange={(event) => setSearchQuery(event.target.value)}
              className="w-full pl-10 pr-4 py-2 text-sm bg-transparent border-b border-slate-200 focus:border-slate-400 focus:outline-none transition-colors placeholder:text-slate-400"
            />
          </div>
        </div>

        {/* File List / Table with Scrolling */}
        <div className="flex-1 overflow-auto">
          {viewMode === "table" ? (
            <div className="w-full">
              <table className="w-full border-collapse text-sm">
                <thead className="sticky top-0 bg-slate-50 border-b border-slate-200">
                  <tr>
                    <th className="w-12 px-4 py-3 text-left">
                      <input
                        type="checkbox"
                        checked={selectedRows.size === filteredFiles.length && filteredFiles.length > 0}
                        onChange={toggleAllRows}
                        className="rounded border-slate-300"
                      />
                    </th>
                    <th className="px-4 py-3 text-left font-semibold text-slate-600">Name</th>
                    <th className="w-20 px-4 py-3 text-left font-semibold text-slate-600">Type</th>
                    <th className="w-28 px-4 py-3 text-left font-semibold text-slate-600">Size</th>
                    <th className="w-24 px-4 py-3 text-left font-semibold text-slate-600">Status</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredFiles.map((file) => {
                    const Icon = getFileIcon(file.name);
                    const isSelected = selectedRows.has(file.path);
                    const isFileSelected = selectedFile?.path === file.path;

                    return (
                      <tr
                        key={file.path}
                        className={`border-b border-slate-200 transition ${isFileSelected ? "bg-sky-50" : isSelected ? "bg-slate-50" : "hover:bg-slate-50"}`}
                      >
                        <td className="px-4 py-3">
                          <input
                            type="checkbox"
                            checked={isSelected}
                            onChange={() => toggleRowSelection(file.path)}
                            onClick={(e) => e.stopPropagation()}
                            className="rounded border-slate-300"
                          />
                        </td>
                        <td
                          className="px-4 py-3 cursor-pointer"
                          onClick={() => setSelectedFile(file)}
                        >
                          <div className="flex items-center gap-3">
                            <Icon className="h-4 w-4 text-sky-500" />
                            <div className="min-w-0">
                              <p className="font-medium text-slate-900 truncate">{file.name}</p>
                              <p className="text-xs text-slate-500 truncate">{file.path}</p>
                            </div>
                          </div>
                        </td>
                        <td className="px-4 py-3 text-slate-600 text-xs font-medium">
                          {getFileType(file.name)}
                        </td>
                        <td className="px-4 py-3 text-slate-600">
                          {formatFileSize(file.size)}
                        </td>
                        <td className="px-4 py-3">
                          <div className="flex items-center gap-1.5 text-slate-600">
                            <CheckCircle2 className="h-4 w-4 text-green-500" />
                            <span className="text-xs">Ready</span>
                          </div>
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>

              {filteredFiles.length === 0 && (
                <div className="flex flex-col items-center justify-center py-12 text-slate-500">
                  <File className="h-10 w-10 mb-3 text-slate-400" />
                  <p className="text-sm font-medium">No files found</p>
                  <p className="text-xs">Try adjusting your search or folder filter</p>
                </div>
              )}
            </div>
          ) : (
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 p-4">
              {filteredFiles.map((file) => {
                const Icon = getFileIcon(file.name);
                const isFileSelected = selectedFile?.path === file.path;

                return (
                  <button
                    key={file.path}
                    type="button"
                    onClick={() => setSelectedFile(file)}
                    className={`group rounded-xl border p-4 text-left transition ${isFileSelected ? "border-sky-400 bg-sky-50 shadow-md" : "border-slate-200 bg-white hover:border-slate-300 hover:shadow-sm"}`}
                  >
                    <Icon className="h-8 w-8 text-sky-500 mb-3" />
                    <h3 className="truncate text-sm font-semibold text-slate-900 mb-1">
                      {file.name}
                    </h3>
                    <p className="text-xs text-slate-500 mb-3">{getFileType(file.name)}</p>
                    <div className="text-xs text-slate-400">
                      {formatFileSize(file.size)}
                    </div>
                  </button>
                );
              })}

              {filteredFiles.length === 0 && (
                <div className="col-span-full flex flex-col items-center justify-center py-12 text-slate-500">
                  <File className="h-10 w-10 mb-3 text-slate-400" />
                  <p className="text-sm font-medium">No files found</p>
                  <p className="text-xs">Try adjusting your search or folder filter</p>
                </div>
              )}
            </div>
          )}
        </div>
      </main>

      {/* RIGHT PANEL: Map Preview (only for geo-files) */}
      {showRightPanel && (
        <aside className="w-80 shrink-0 flex flex-col rounded-[24px] border border-slate-200 bg-white shadow-sm overflow-hidden animate-in fade-in slide-in-from-right-4 duration-300">
          <div className="flex items-center justify-between border-b border-slate-200 px-4 py-3">
            <div>
              <h3 className="text-sm font-semibold text-slate-900">Map Preview</h3>
              <p className="text-xs text-slate-500">Geo-spatial file</p>
            </div>
            <button type="button" className="rounded-full p-1.5 text-slate-500 hover:bg-slate-100" onClick={() => setSelectedFile(null)}>
              <X className="h-4 w-4" />
            </button>
          </div>

          <div className="flex-1 flex flex-col items-center justify-center p-4">
            <div className="flex h-48 w-full items-center justify-center rounded-xl border-2 border-dashed border-slate-300 bg-slate-50">
              <div className="text-center">
                <Map className="mx-auto h-10 w-10 text-slate-400 mb-2" />
                <p className="text-sm font-medium text-slate-900">Map Placeholder</p>
                <p className="text-xs text-slate-500 mt-1">Integrate Mapbox or Leaflet</p>
              </div>
            </div>

            <div className="mt-4 w-full space-y-3">
              <div className="rounded-lg border border-slate-200 bg-slate-50 p-3">
                <p className="text-xs uppercase tracking-wider font-semibold text-slate-600">File Details</p>
                <div className="mt-2 space-y-1.5 text-xs text-slate-600">
                  <div className="flex items-center gap-2">
                    <span className="font-medium">Name:</span>
                    <span className="truncate">{selectedFile?.name}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="font-medium">Type:</span>
                    <span>{getFileType(selectedFile?.name || "")}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="font-medium">Size:</span>
                    <span>{formatFileSize(selectedFile?.size || 0)}</span>
                  </div>
                </div>
              </div>

              <Button className="w-full" variant="secondary" onClick={() => alert(`View map for ${selectedFile?.name}`)}>
                View on Map
              </Button>
              <Button className="w-full" onClick={() => alert(`Run simulation for ${selectedFile?.name}`)}>
                Run Simulation
              </Button>
            </div>
          </div>
        </aside>
      )}
    </div>
  );
}
