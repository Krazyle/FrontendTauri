/** DeepSeek agent and transport for in-process AI chat. */
import { createDeepSeek } from "@ai-sdk/deepseek";
import { DirectChatTransport, ToolLoopAgent } from "ai";

const deepseek = createDeepSeek({
  apiKey: import.meta.env.OPENROUTER_API_KEY ?? "",
});

const agent = new ToolLoopAgent({
  model: deepseek("deepseek-chat"),
  instructions: "You are a helpful GIS assistant for a project management application.",
});

export const chatTransport = new DirectChatTransport({ agent });
