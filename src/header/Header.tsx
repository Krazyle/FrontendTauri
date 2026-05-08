import { useNavigate } from "react-router-dom";
import { Button } from "./Button";
import { MousePointer2, Hand, Square, Circle, Pencil, Pentagon } from "lucide-react";
import { useDrawing } from "../map/DrawingContext";

export default function Header() {
  const { drawingControl, currentMode, setCurrentMode } = useDrawing();

  const handleDrawingMode = (mode: string | null) => {
    if (!drawingControl) return;

    const terraDraw = drawingControl.getTerraDrawInstance();
    if (!terraDraw) return;

    if (mode === null) {
      
      drawingControl.resetActiveMode();
      setCurrentMode(null);
    } else {
      
      drawingControl.activate();
      
      if (terraDraw.setMode) {
        terraDraw.setMode(mode);
        setCurrentMode(mode);
      }
    }
  };
  const navigate = useNavigate();

  return (
    <header className="flex items-center justify-between p-3 bg-white border-b border-gray-100">
      <button
        type="button"
        className="text-2xl font-bold text-black px-4 text-left"
        onClick={() => navigate("/projects")}
      >
        Geon
      </button>

      <div className="flex items-center gap-4 p-1">
        <Button
          onClick={() => handleDrawingMode('select')}
          className={currentMode === 'select' ? 'bg-blue-100' : ''}
        >
          <MousePointer2 />
        </Button>
        <Button
          onClick={() => handleDrawingMode(null)}
          className={currentMode === null ? 'bg-blue-100' : ''}
        >
          <Hand />
        </Button>
        <Button
          onClick={() => handleDrawingMode('rectangle')}
          className={currentMode === 'rectangle' ? 'bg-blue-100' : ''}
        >
          <Square />
        </Button>
        <Button
          onClick={() => handleDrawingMode('circle')}
          className={currentMode === 'circle' ? 'bg-blue-100' : ''}
        >
          <Circle />
        </Button>
        <Button
          onClick={() => handleDrawingMode('linestring')}
          className={currentMode === 'linestring' ? 'bg-blue-100' : ''}
        >
          <Pencil />
        </Button>
        <Button
          onClick={() => handleDrawingMode('polygon')}
          className={currentMode === 'polygon' ? 'bg-blue-100' : ''}
        >
          <Pentagon />
        </Button>
      </div>

      <div className="w-24" />
    </header>
  );
}