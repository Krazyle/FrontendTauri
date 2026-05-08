import { useState } from "react";
import Header from "./header/Header";
import Chat from "./chat/Chat";
import Map from "./map/Map";
import "./App.css";
import ProjectManager from "./project-manager/ProjectManager";

function App() {
  const [currentView, setCurrentView] = useState<"main" | "projects">("main");

  const navigate = (view: "main" | "projects") => {
    setCurrentView(view);
  };

  return (
    <>
      {currentView === "main" ? (
        <main className="h-screen w-screen overflow-hidden flex flex-col">
          <Header onNavigate={navigate} />
          <div className="flex-1 relative">
            <Chat />
            <Map />
          </div>
        </main>
      ) : (
        <ProjectManager onNavigate={navigate} />
      )}
    </>
  );
}

export default App;
