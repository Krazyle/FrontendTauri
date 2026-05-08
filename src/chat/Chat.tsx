import { useState } from "react";
import { Button } from "@/components/button";
import { Sparkles } from "lucide-react";
import { ChatHeader } from "./ChatHeader";
import { ChatHistory } from "./ChatHistory";
import { ChatInput } from "./ChatInput";
import { useChatState } from "./useChatState";
export default function Chat() {
  const [minimized, setMinimized] = useState(false);
  const [input, setInput] = useState("");
  const { messages, sendMessage, status, error } = useChatState();
  const isWaiting = status === "submitted";
  const isStreaming = status === "streaming";
  const isDisabled = isWaiting || isStreaming;

  const handleSubmit = (e?: React.FormEvent) => {
    e?.preventDefault();
    if (!input.trim() || isDisabled) return;
    sendMessage({ text: input });
    setInput("");
  };

  if (minimized) {
    return (
      <aside
        className="absolute top-4 right-4 z-10"
        style={{ fontFamily: 'var(--font-chat)' }}
      >
        <Button
          variant="ghost"
          size="icon"
          className="rounded-full bg-white border border-zinc-100 shadow-felt text-zinc-500 hover:text-zinc-700"
          onClick={() => setMinimized(false)}
        >
          <Sparkles className="size-4" />
        </Button>
      </aside>
    );
  }

  return (
    <aside
      className="absolute top-4 right-4 z-10 w-96 h-128 bg-white rounded-2xl flex flex-col border border-zinc-100 shadow-felt overflow-hidden"
      style={{ fontFamily: 'var(--font-chat)' }}
    >
      <ChatHeader onMinimize={() => setMinimized(true)} />

      <ChatHistory
        messages={messages}
        isWaiting={isWaiting}
      />

      {error && (
        <div className="px-4 py-2 text-xs text-red-500 bg-red-50 border-t border-red-100">
          Something went wrong. Please try again.
        </div>
      )}

      <ChatInput
        input={input}
        setInput={setInput}
        isWaiting={isDisabled}
        onSubmit={handleSubmit}
      />
    </aside>
  );
}
