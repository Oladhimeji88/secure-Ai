import { JsonViewer } from "@/components/common/json-viewer";
import { Button } from "@/components/ui/button";

export function AlertDetail({ alert }: { alert: any }) {
  return (
    <div className="space-y-6">
      <section className="grid gap-4 md:grid-cols-2">
        <div>
          <h3 className="mb-2 text-sm font-semibold">Reasons</h3>
          <ul className="list-disc space-y-1 pl-5 text-sm text-zinc-300">
            {alert.reasons.map((r: string) => <li key={r}>{r}</li>)}
          </ul>
        </div>
        <div>
          <h3 className="mb-2 text-sm font-semibold">Recommended Actions</h3>
          <ul className="list-disc space-y-1 pl-5 text-sm text-zinc-300">
            {alert.recommended_actions.map((r: string) => <li key={r}>{r}</li>)}
          </ul>
        </div>
      </section>
      <section>
        <h3 className="mb-2 text-sm font-semibold">Evidence JSON</h3>
        <JsonViewer data={alert.evidence} />
      </section>
      <section>
        <h3 className="mb-2 text-sm font-semibold">Timeline</h3>
        <div className="rounded-md border border-border bg-card p-3 text-sm text-zinc-300">{new Date(alert.created_at).toLocaleString()} - Alert created</div>
      </section>
      <Button>Mark as triaged</Button>
    </div>
  );
}
