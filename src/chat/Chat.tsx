import { useState } from "react";
import { Button } from "@/components/button";
import { Badge } from "@/components/badge";
import {
  Conversation,
  ConversationContent,
  ConversationEmptyState,
  ConversationScrollButton,
} from "@/components/ai-elements/conversation";
import {
  Message,
  MessageContent,
  MessageResponse,
} from "@/components/ai-elements/message";
import { ArrowUp, Minus, Sparkles } from "lucide-react";

type Role = "user" | "assistant";

interface ChatMessage {
  id: string;
  role: Role;
  content: string;
}

const suggestions = [
  "Generate/simulate a flood zone in ",
  "Generate a shelter in ",
  "Can you find which areas don't have a shelter near to them by 30 minutes of travel time by foot?",
];

const INITIAL_MESSAGES: ChatMessage[] = [
  {
    id: "1",
    role: "user",
    content: "Generate/simulate a flood zone in",
  },
  {
    id: "2",
    role: "assistant",
    content: "Based on your current layer filters, there are 142 points within the selected region. Would you like me to export them as GeoJSON or add a buffer analysis?",
  },
  {
    id: "3",
    role: "user",
    content: "Generate/simulate a flood zone in",
  },
  {
    id: "4",
    role: "assistant",
    content: "The elevation data shows a gradual slope from 45m to 12m across your study area. I can generate a contour map at 5m intervals if that would help with your analysis.",
  },
];

function TypingIndicator() {
  return (
    <Message from="assistant">
      <MessageContent className="px-1 py-2">
        <div className="flex items-center gap-1.5">
          <span className="typing-dot" />
          <span className="typing-dot" />
          <span className="typing-dot" />
        </div>
      </MessageContent>
    </Message>
  );
}

export default function Chat() {
  const [minimized, setMinimized] = useState(false);
  const [messages, setMessages] = useState<ChatMessage[]>(INITIAL_MESSAGES);
  const [input, setInput] = useState("");
  const [isWaiting, setIsWaiting] = useState(false);

  const handleSubmit = (e?: React.FormEvent) => {
    e?.preventDefault();
    if (!input.trim() || isWaiting) return;

    const userMsg: ChatMessage = {
      id: Date.now().toString(),
      role: "user",
      content: input.trim(),
    };

    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setIsWaiting(true);

    // Simulate assistant response
    setTimeout(() => {
      const assistantMsg: ChatMessage = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: "[Skeleton] This is a mock response. The API is not yet connected.",
      };
      setMessages((prev) => [...prev, assistantMsg]);
      setIsWaiting(false);
    }, 1500);
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
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-3 border-b border-zinc-100">
        <div className="flex items-center gap-2">
          <Sparkles className="size-4 text-zinc-400" />
          <span className="text-sm font-medium text-zinc-700">AI Assistant</span>
        </div>
        <Button
          variant="ghost"
          size="icon-xs"
          className="rounded-full text-zinc-400 hover:text-zinc-600"
          onClick={() => setMinimized(true)}
        >
          <Minus className="size-3.5" />
        </Button>
      </div>

      {/* Message area — AI Elements Conversation */}
      <Conversation className="flex-1">
        <ConversationContent className="gap-4 px-4 py-4">
          {messages.length === 0 ? (
            <ConversationEmptyState
              icon={
                <div className="size-10 rounded-full bg-zinc-100 flex items-center justify-center">
                  <Sparkles className="size-5 text-zinc-400" />
                </div>
              }
              title="How can I help?"
              description="Ask about your map data or get help with analysis."
            />
          ) : (
            messages.map((m) => (
              <Message key={m.id} from={m.role}>
                <MessageContent
                  className={
                    m.role === "user"
                      ? "rounded-2xl bg-black text-white px-4 py-2.5"
                      : "text-black px-1 py-1"
                  }
                >
                  {m.role === "assistant" ? (
                    <MessageResponse>{m.content}</MessageResponse>
                  ) : (
                    m.content
                  )}
                </MessageContent>
              </Message>
            ))
          )}
          {isWaiting && <TypingIndicator />}
        </ConversationContent>
        <ConversationScrollButton />
      </Conversation>

      {/* Input area — kept as Felt-style pill */}
      <div className="px-3 pb-3 flex flex-col gap-2">
        <div 
          className="flex items-center gap-2 overflow-x-auto pb-2 [&::-webkit-scrollbar]:h-1.5 [&::-webkit-scrollbar-thumb]:bg-zinc-300 [&::-webkit-scrollbar-thumb]:rounded-full [&::-webkit-scrollbar-track]:bg-transparent"
          onWheel={(e) => { e.currentTarget.scrollBy({ left: e.deltaY < 0 ? -50 : 50 }); }}
        >
          {suggestions.map((suggestion, i) => (
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
          onSubmit={handleSubmit}
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
    </aside>
  );
}
