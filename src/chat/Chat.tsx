import { useState } from "react";
import { Button } from "@/components/button";
import { Card } from "@/components/card";
import { Sparkles } from "lucide-react";
import { AnimatePresence, motion } from "framer-motion";
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

  return (
    <div className="absolute top-4 right-4 z-10" style={{ fontFamily: 'var(--font-chat)' }}>
      <AnimatePresence mode="wait">
        {minimized ? (
          <motion.div
            key="minimized"
            initial={{ scale: 0.8, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0.8, opacity: 0 }}
            transition={{ duration: 0.2, ease: "easeOut" }}
          >
            <Button
              variant="ghost"
              size="icon"
              className="rounded-full bg-white border border-zinc-100 shadow-felt text-zinc-500 hover:text-zinc-700 h-10 w-10"
              onClick={() => setMinimized(false)}
            >
              <Sparkles className="size-4" />
            </Button>
          </motion.div>
        ) : (
          <motion.div
            key="expanded"
            initial={{ opacity: 0, scale: 0.95, y: -10 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.95, y: -10 }}
            transition={{ duration: 0.25, ease: [0.4, 0, 0.2, 1] }}
          >
            <Card className="w-96 h-128 flex flex-col border border-zinc-100 shadow-felt overflow-hidden bg-white rounded-2xl">
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
            </Card>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

