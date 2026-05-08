import type { UIMessage } from "ai";

export type Role = "user" | "assistant";
export type ChatMessage = UIMessage;

/** Extract plain text from a UIMessage's parts array. */
export function getMessageText(message: UIMessage): string {
  const parts = (message as any).parts;
  const content = (message as any).content;
  
  if (!parts) return typeof content === "string" ? content : "";
  
  return parts
    .filter((p: any): p is { type: "text"; text: string } => p.type === "text")
    .map((p: { text: string }) => p.text)
    .join("");
}
