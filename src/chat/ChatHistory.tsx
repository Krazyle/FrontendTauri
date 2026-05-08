import { useEffect, useRef } from "react";
import { AnimatePresence, motion } from "framer-motion";
import { ChatMessage } from "./ChatMessage";
import { TypingIndicator } from "./TypingIndicator";
import { ChatEmptyState } from "./ChatEmptyState";
import type { ChatMessage as ChatMessageType } from "./types";

interface ChatHistoryProps {
  messages: ChatMessageType[];
  isWaiting: boolean;
}

/** Scrollable message list with auto-scroll and entry animations. */
export function ChatHistory({ messages, isWaiting }: ChatHistoryProps) {
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTo({
        top: scrollRef.current.scrollHeight,
        behavior: "smooth",
      });
    }
  }, [messages.length, isWaiting]);

  return (
    <div
      ref={scrollRef}
      className="flex-1 min-h-0 overflow-y-auto px-4 py-4"
    >
      <div className="flex flex-col gap-4">
        {messages.length === 0 ? (
          <ChatEmptyState />
        ) : (
          <AnimatePresence initial={false}>
            {messages.map((m) => (
              <motion.div
                key={m.id}
                initial={{ opacity: 0, y: 12 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.25, ease: "easeOut" }}
              >
                <ChatMessage message={m} />
              </motion.div>
            ))}
          </AnimatePresence>
        )}
        {isWaiting && (
          <motion.div
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
          >
            <TypingIndicator />
          </motion.div>
        )}
      </div>
    </div>
  );
}


