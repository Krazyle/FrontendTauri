import { memo } from "react";
import { Streamdown } from "streamdown";
import { cjk } from "@streamdown/cjk";
import { code } from "@streamdown/code";
import { math } from "@streamdown/math";
import { mermaid } from "@streamdown/mermaid";
import type { ChatMessage as ChatMessageType } from "./types";

const plugins = { cjk, code, math, mermaid };

interface ChatMessageProps {
  message: ChatMessageType;
}

export const ChatMessage = memo(function ChatMessage({ message }: ChatMessageProps) {
  const textContent = (message as any).parts
    ?.filter((p: any) => p.type === "text")
    .map((p: any) => p.text)
    .join("") ?? (message as any).content ?? "";

  const isUser = message.role === "user";

  return (
    <div className={`flex w-full max-w-[95%] ${isUser ? "ml-auto justify-end" : ""}`}>
      <div
        className={
          isUser
            ? "rounded-2xl bg-black text-white px-4 py-2.5 text-sm"
            : "text-zinc-800 px-1 py-1 text-sm"
        }
      >
        {message.role === "assistant" ? (
          <Streamdown plugins={plugins}>{textContent}</Streamdown>
        ) : (
          textContent
        )}
      </div>
    </div>
  );
});

