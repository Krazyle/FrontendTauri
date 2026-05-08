import { createContext, useContext, useState, ReactNode } from 'react';
import { MaplibreTerradrawControl } from '@watergis/maplibre-gl-terradraw';

interface DrawingContextType {
  drawingControl: MaplibreTerradrawControl | null;
  setDrawingControl: (control: MaplibreTerradrawControl) => void;
  currentMode: string | null;
  setCurrentMode: (mode: string | null) => void;
}

const DrawingContext = createContext<DrawingContextType | undefined>(undefined);

export function DrawingProvider({ children }: { children: ReactNode }) {
  const [drawingControl, setDrawingControl] = useState<MaplibreTerradrawControl | null>(null);
  const [currentMode, setCurrentMode] = useState<string | null>(null);

  return (
    <DrawingContext.Provider value={{
      drawingControl,
      setDrawingControl,
      currentMode,
      setCurrentMode,
    }}>
      {children}
    </DrawingContext.Provider>
  );
}

export function useDrawing() {
  const context = useContext(DrawingContext);
  if (context === undefined) {
    throw new Error('useDrawing must be used within a DrawingProvider');
  }
  return context;
}