<script lang="ts">
  import { drawingControl, currentMode } from '../map/drawingStore';
  import MousePointer2 from 'lucide-svelte/icons/mouse-pointer-2';
  import Hand from 'lucide-svelte/icons/hand';
  import Square from 'lucide-svelte/icons/square';
  import Circle from 'lucide-svelte/icons/circle';
  import Pencil from 'lucide-svelte/icons/pencil';
  import Pentagon from 'lucide-svelte/icons/pentagon';

  function handleDrawingMode(mode: string | null) {
    const control = $drawingControl;
    if (!control) return;

    const terraDraw = control.getTerraDrawInstance();
    if (!terraDraw) return;

    if (mode === null) {
      control.resetActiveMode();
      currentMode.set(null);
    } else {
      control.activate();
      if (terraDraw.setMode) {
        terraDraw.setMode(mode);
        currentMode.set(mode);
      }
    }
  }

  const modes = [
    { mode: 'select', icon: MousePointer2, label: 'Select' },
    { mode: null, icon: Hand, label: 'Hand' },
    { mode: 'rectangle', icon: Square, label: 'Rectangle' },
    { mode: 'circle', icon: Circle, label: 'Circle' },
    { mode: 'linestring', icon: Pencil, label: 'Line' },
    { mode: 'polygon', icon: Pentagon, label: 'Polygon' },
  ] as const;
</script>

<header class="flex items-center justify-between p-3 bg-white border-b border-gray-100">
  <a
    href="/projects"
    class="text-2xl font-bold text-black px-4 text-left no-underline"
  >
    Geon
  </a>

  <div class="flex items-center gap-4 p-1">
    {#each modes as { mode, icon: Icon, label }}
      <button
        type="button"
        class="inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors p-2 {$currentMode === mode ? 'bg-blue-100' : ''}"
        onclick={() => handleDrawingMode(mode)}
        aria-label={label}
      >
        <Icon size={24} />
      </button>
    {/each}
  </div>

  <div class="w-24"></div>
</header>