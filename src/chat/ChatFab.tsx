import { Button } from "@/components/button";
import { Sparkles } from "lucide-react";
import { motion } from "framer-motion";

interface ChatFabProps {
  onExpand: () => void;
}

/** Floating sparkles button shown when the chat is minimized. */
export function ChatFab({ onExpand }: ChatFabProps) {
  return (
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
        onClick={onExpand}
      >
        <Sparkles className="size-4" />
      </Button>
    </motion.div>
  );
}
