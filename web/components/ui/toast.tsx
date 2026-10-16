export function Toast({ message }: { message: string }) {
  return <div className="rounded-md bg-zinc-900 px-3 py-2 text-xs text-white">{message}</div>;
}
