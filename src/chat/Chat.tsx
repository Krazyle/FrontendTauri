import { Button } from "@/components/button";
import { ArrowUp } from "lucide-react";

export default function Chat() {
  return (
    <aside className="absolute top-4 right-4 z-10 w-96 h-128 bg-white rounded-lg p-4 flex flex-col justify-end border border-zinc-200 shadow-xl">
      <div className="flex items-center gap-2 p-1.5 bg-zinc-200 rounded-full">
        <div className="flex-1 text-zinc-500 text-sm pl-3">
          Ask anything, @ to mention, / for workflows
        </div>
        <Button size="icon" className="rounded-full">
          <ArrowUp className="size-4" />
        </Button>
      </div>
    </aside>
  );
}
