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

  return <div ref={ref} />;
}
