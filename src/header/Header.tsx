import { useNavigate } from "react-router-dom";
import { Button } from "./Button";
import { MousePointer2, Hand, Square, Circle, Pencil } from "lucide-react";

export default function Header() {
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