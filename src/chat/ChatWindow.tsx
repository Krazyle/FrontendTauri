import { Card } from "@/components/card";
import { motion } from "framer-motion";
import { ChatHeader } from "./ChatHeader";
import { ChatHistory } from "./ChatHistory";
import { ChatInput } from "./ChatInput";
import type { ChatMessage } from "./types";

interface ChatWindowProps {
  messages: ChatMessage[];
  isWaiting: boolean;
  error: Error | undefined;
  input: string;
  setInput: (value: string) => void;
  isDisabled: boolean;
  handleSubmit: (e?: React.FormEvent) => void;
  onMinimize: () => void;
}

/** Expanded chat card with header, message history, and input. */
export function ChatWindow({
  messages,
  isWaiting,
  error,
  input,
  setInput,
  isDisabled,
  handleSubmit,
  onMinimize,
}: ChatWindowProps) {
  return (
    <motion.div
      key="expanded"
      initial={{ opacity: 0, scale: 0.95, y: -10 }}
      animate={{ opacity: 1, scale: 1, y: 0 }}
      exit={{ opacity: 0, scale: 0.95, y: -10 }}
      transition={{ duration: 0.25, ease: [0.4, 0, 0.2, 1] }}
    >
      <Card className="w-96 h-128 flex flex-col border border-zinc-100 shadow-felt overflow-hidden bg-white rounded-2xl">
        <ChatHeader onMinimize={onMinimize} />
        <ChatHistory messages={messages} isWaiting={isWaiting} />
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
      </Card>
    </motion.div>
  );
}
