import { useChat } from "@ai-sdk/react";
import { chatTransport } from "./chatAgent";

export function useChatState() {
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

  return {
    messages,
    setMessages,
    sendMessage,
    status,
    error,
    stop,
  };
}
