import { useState } from "react";
import { useChat } from "@ai-sdk/react";
import { chatTransport } from "./chatAgent";

/** Hook wrapping the AI SDK's useChat with project-specific config. */
export function useChatState() {
  const [input, setInput] = useState("");

  const {
    messages,
    setMessages,
    sendMessage,
    status,
    error,
    stop,
  } = useChat({
    transport: chatTransport,
    onFinish: ({ message }) => {
      console.log("[chat] response complete:", message.id);
    },
    onError: (error) => {
      console.error("[chat] error:", error);
    },
    experimental_throttle: 50,
  });

  const isWaiting = status === "submitted";
  const isStreaming = status === "streaming";
  const isDisabled = isWaiting || isStreaming;

  const handleSubmit = (e?: React.FormEvent) => {
    e?.preventDefault();
    if (!input.trim() || isDisabled) return;
    sendMessage({ text: input });
    setInput("");
  };

  return {
    messages,
    setMessages,
    sendMessage,
    status,
    error,
    stop,
    input,
    setInput,
    isWaiting,
    isStreaming,
    isDisabled,
    handleSubmit,
  };
}
