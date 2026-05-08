import { Message, MessageContent } from "@/components/ai-elements/message";

export function TypingIndicator() {
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
