import { useEffect, useRef } from 'react';
import maplibregl from 'maplibre-gl';
import 'maplibre-gl/dist/maplibre-gl.css';
import { initializeDrawingTools } from './DrawingTools';
import { MaplibreTerradrawControl } from '@watergis/maplibre-gl-terradraw';
import { drawingControl } from './drawingStore';

interface MapProps {
  className?: string;
}

export default function Map({ className }: MapProps) {
  const mapContainer = useRef<HTMLDivElement>(null);
  const map = useRef<maplibregl.Map | null>(null);
  const drawControl = useRef<MaplibreTerradrawControl | null>(null);

  useEffect(() => {
    if (map.current || !mapContainer.current) return;

    map.current = new maplibregl.Map({
      container: mapContainer.current,
      style: 'https://tiles.openfreemap.org/styles/liberty',
      center: [121.7740, 12.8797],
      zoom: 5, 
    }); 

    drawControl.current = initializeDrawingTools(map.current);
    drawingControl.set(drawControl.current);

    return () => {
      map.current?.remove();
      map.current = null;
      drawControl.current = null;
    };
  }, []);

  return (
    <div 
      ref={mapContainer} 
      className={`w-full h-full ${className ?? ''}`}
    />
  );
}
