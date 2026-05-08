import { Sparkles } from "lucide-react";
import {
  Conversation,
  ConversationContent,
  ConversationEmptyState,
  ConversationScrollButton,
} from "@/components/ai-elements/conversation";
import { ChatMessage } from "./ChatMessage";
import { TypingIndicator } from "./TypingIndicator";
import type { ChatMessage as ChatMessageType } from "./types";

interface ChatHistoryProps {
  messages: ChatMessageType[];
  isWaiting: boolean;
}

export function ChatHistory({ messages, isWaiting }: ChatHistoryProps) {
  return (
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
            <ChatMessage key={m.id} message={m} />
          ))
        )}
        {isWaiting && <TypingIndicator />}
      </ConversationContent>
      <ConversationScrollButton />
    </Conversation>
  );
}
