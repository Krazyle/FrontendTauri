import Header from "./header/Header";
import Files from "./file-manager/Files";
import Chat from "./chat/Chat";
import Map from "./map/Map";
import { DrawingProvider } from "./map/DrawingContext";
import "./App.css";

function App() {
  return (
    <DrawingProvider>
      <main className="h-screen w-screen overflow-hidden flex flex-col">
        <Header />
        <div className="flex-1 relative">
          <Files />
          <Chat />
          <Map />
        </div>
      </main>
    </DrawingProvider>
  );
}

export default App;
