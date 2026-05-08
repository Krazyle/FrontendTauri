export function TypingIndicator() {
  return (
    <div className="flex w-full max-w-[95%]">
      <div className="px-1 py-2">
        <div className="flex items-center gap-1.5">
          <span className="typing-dot" />
          <span className="typing-dot" />
          <span className="typing-dot" />
        </div>
      </div>
    </div>
  );
}

