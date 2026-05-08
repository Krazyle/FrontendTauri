import { useEffect, useRef } from 'react';
import { mount, unmount } from 'svelte';
// @ts-expect-error - Svelte component imported in React
import HeaderSvelte from './Header.svelte';

export default function Header() {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!ref.current) return;
    const app = mount(HeaderSvelte, { target: ref.current });
    return () => unmount(app);
  }, []);
import { Button } from "./Button";
import { MousePointer2, Hand, Square, Circle, Pencil } from "lucide-react";

interface HeaderProps {
  onNavigate: (view: "main" | "projects") => void;
}

export default function Header({ onNavigate }: HeaderProps) {
  return (
    <header className="flex items-center justify-between p-3 bg-white border-b border-gray-100">
      <button
        type="button"
        className="text-2xl font-bold text-black px-4 text-left cursor-pointer"
        onClick={() => onNavigate("projects")}
      >
        Geon
      </button>

  return <div ref={ref} />;
}
      
