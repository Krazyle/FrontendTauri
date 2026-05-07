import { Button } from "./Button";
import { MousePointer2, Hand, Square, Circle, Pencil } from "lucide-react";

export default function Header() {
  return (
    <header className="flex items-center justify-between p-3 bg-white border-b border-gray-100">
      <h1 className="text-2xl font-bold text-black px-4">
        Geon
      </h1>

      <div className="flex items-center gap-4 p-1">
        <Button>
          <MousePointer2 />
        </Button>
        <Button>
          <Hand />
        </Button>
        <Button>
          <Square />
        </Button>
        <Button>
          <Circle />
        </Button>
        <Button>
          <Pencil />
        </Button>
      </div>

      <div className="w-24" />
    </header>
  );
}
