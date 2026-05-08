import { ArrowUp } from "lucide-react";
import { Button } from "@/components/button";
import { Badge } from "@/components/badge";
import { SUGGESTIONS } from "./constants";

interface ChatInputProps {
  input: string;
  setInput: (value: string) => void;
  isWaiting: boolean;
  onSubmit: (e?: React.FormEvent) => void;
}

/** Message input form with suggestion chips. */
export function ChatInput({ input, setInput, isWaiting, onSubmit }: ChatInputProps) {
  return (
    <div className="px-3 pb-3 flex flex-col gap-2">
      <div 
        className="flex items-center gap-2 overflow-x-auto pb-2 [&::-webkit-scrollbar]:h-1.5 [&::-webkit-scrollbar-thumb]:bg-zinc-300 [&::-webkit-scrollbar-thumb]:rounded-full [&::-webkit-scrollbar-track]:bg-transparent"
        onWheel={(e) => { e.currentTarget.scrollBy({ left: e.deltaY < 0 ? -50 : 50 }); }}
      >
        {SUGGESTIONS.map((suggestion, i) => (
          <Badge
            key={i}
            variant="outline"
            className="cursor-pointer whitespace-nowrap text-xs text-zinc-700 bg-white shadow-sm border-zinc-200 hover:border-zinc-300 hover:bg-zinc-50 font-medium py-1.5 px-3 transition-all"
            onClick={() => setInput(suggestion)}
          >
            {suggestion}{!suggestion.endsWith('?') && '...'}
          </Badge>
        ))}
      </div>
      <form
        onSubmit={onSubmit}
        className="flex items-center gap-2 p-1.5 bg-zinc-50 border border-zinc-200 rounded-full transition-colors focus-within:border-zinc-300 focus-within:bg-white"
      >
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask anything..."
          disabled={isWaiting}
          className="flex-1 bg-transparent text-sm text-zinc-700 placeholder:text-zinc-400 pl-3 outline-none disabled:opacity-50"
        />
        <Button
          type="submit"
          size="icon"
          className={`rounded-full size-7 shrink-0 transition-opacity ${!input.trim() || isWaiting
            ? "opacity-40"
            : "opacity-100"
            }`}
          disabled={!input.trim() || isWaiting}
        >
          <ArrowUp className="size-3.5" />
        </Button>
      </form>
    </div>
  );
}
