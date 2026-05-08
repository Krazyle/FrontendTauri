import { Sparkles, Minus } from "lucide-react";
import { Button } from "@/components/button";

interface ChatHeaderProps {
  onMinimize: () => void;
}

/** Title bar with minimize button for the chat window. */
export function ChatHeader({ onMinimize }: ChatHeaderProps) {
  return (
    <div className="flex items-center justify-between px-4 py-3 border-b border-zinc-100">
      <div className="flex items-center gap-2">
        <Sparkles className="size-4 text-zinc-400" />
        <span className="text-sm font-medium text-zinc-700">AI Assistant</span>
      </div>
      <Button
        variant="ghost"
        size="icon-xs"
        className="rounded-full text-zinc-400 hover:text-zinc-600"
        onClick={onMinimize}
      >
        <Minus className="size-3.5" />
      </Button>
    </div>
  );
}
