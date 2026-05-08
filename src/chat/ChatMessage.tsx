import { Message, MessageContent, MessageResponse } from "@/components/ai-elements/message";
import type { ChatMessage as ChatMessageType } from "./types";

interface ChatMessageProps {
  message: ChatMessageType;
}

export function ChatMessage({ message }: ChatMessageProps) {
  const textContent = message.parts
    ?.filter((p: any) => p.type === "text")
    .map((p: any) => p.text)
    .join("") ?? message.content ?? "";

  return (
    <Message from={message.role}>
      <MessageContent
        className={
          message.role === "user"
            ? "rounded-2xl bg-black text-white px-4 py-2.5"
            : "text-black px-1 py-1"
        }
      >
        {message.role === "assistant" ? (
          <MessageResponse>{textContent}</MessageResponse>
        ) : (
          textContent
        )}
      </MessageContent>
    </Message>
  );
}
