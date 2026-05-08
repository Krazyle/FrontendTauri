import Header from "./header/Header";
import Files from "./file-manager/Files";
import Chat from "./chat/Chat";
import Map from "./map/Map";
import { DrawingProvider } from "./map/DrawingContext";
import "./App.css";
import ProjectManager from "./project-manager/ProjectManager"; //
import { BrowserRouter, Routes, Route } from "react-router-dom"; //


function App() {
  return (
     <BrowserRouter>
      <Routes>
        <Route path="/" element={
          <main className="h-screen w-screen overflow-hidden flex flex-col">
            <Header />
            <div className="flex-1 relative">
              <Files />
              <Chat />
              <Map />
            </div>
          </main>
        } />
        
        <Route path="/projects" element={<ProjectManager />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
