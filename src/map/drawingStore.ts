import { writable } from 'svelte/store';
import type { MaplibreTerradrawControl } from '@watergis/maplibre-gl-terradraw';

export const drawingControl = writable<MaplibreTerradrawControl | null>(null);
export const currentMode = writable<string | null>(null);