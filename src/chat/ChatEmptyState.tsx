import { Sparkles } from "lucide-react";

/** Placeholder shown when the chat has no messages yet. */
export function ChatEmptyState() {
  return (
    <div className="flex flex-col items-center justify-center gap-3 py-12 text-center">
      <div className="size-10 rounded-full bg-zinc-100 flex items-center justify-center">
        <Sparkles className="size-5 text-zinc-400" />
      </div>
      <div className="space-y-1">
        <h3 className="font-medium text-sm text-zinc-700">How can I help?</h3>
        <p className="text-zinc-400 text-sm">
          Ask about your map data or get help with analysis.
        </p>
      </div>
    </div>
  );
}
