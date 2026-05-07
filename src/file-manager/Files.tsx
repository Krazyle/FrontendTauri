import { Button } from "@/components/button";
import { Plus } from "lucide-react";

export default function Files() {
  return (
    <aside className="absolute top-4 left-4 z-10 w-72 h-128 bg-white rounded-lg p-4">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-semibold text-black">Layers</h2>
        <Button variant="outline" size="sm">
          <Plus className="w-4 h-4" />
          Add
        </Button>
      </div>
    </aside>
  );
}
