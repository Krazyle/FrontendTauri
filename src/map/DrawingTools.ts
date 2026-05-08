import maplibregl from "maplibre-gl";
import "maplibre-gl/dist/maplibre-gl.css";
import { MaplibreTerradrawControl } from "@watergis/maplibre-gl-terradraw";

export function initializeDrawingTools(map: maplibregl.Map) {
  const draw = new MaplibreTerradrawControl({
    modes: [
        "point",
        "linestring",
        "polygon",
        "rectangle",
        "circle",
        "freehand",
        "select",
        "delete-selection",
        "delete",
        "download",
    ],
    open: true,
  });

  map.addControl(draw, "top-right");

  return draw;
}
