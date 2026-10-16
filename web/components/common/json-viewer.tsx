export function JsonViewer({ data }: { data: unknown }) {
  return <pre className="max-h-80 overflow-auto rounded-md bg-zinc-950 p-4 text-xs text-zinc-100">{JSON.stringify(data, null, 2)}</pre>;
}
