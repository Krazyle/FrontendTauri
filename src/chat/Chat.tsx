import { useState } from "react";
import { AnimatePresence } from "framer-motion";
import { ChatFab } from "./ChatFab";
import { ChatWindow } from "./ChatWindow";
import { useChatState } from "./useChatState";

/** Root chat widget — handles minimize/expand state and animation. */
export default function Chat() {
  const [minimized, setMinimized] = useState(true);
  const chatState = useChatState();

  return (
    <div className="absolute top-4 right-4 z-10 font-chat">
      <AnimatePresence mode="wait">
        {minimized ? (
          <ChatFab onExpand={() => setMinimized(false)} />
        ) : (
          <ChatWindow
            {...chatState}
            onMinimize={() => setMinimized(true)}
          />
        )}
      </AnimatePresence>
    </div>
  );
}
