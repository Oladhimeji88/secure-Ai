export function Topbar() {
  return (
    <header className="flex h-14 items-center justify-between border-b border-border bg-card px-6">
      <h1 className="text-sm font-medium text-zinc-300">Defensive Operations Console</h1>
      <span className="rounded-full bg-emerald-500/20 px-3 py-1 text-xs font-medium text-emerald-300">Secure Mode</span>
    </header>
  );
}
