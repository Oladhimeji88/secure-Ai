import Link from "next/link";
import { Alert } from "@/lib/types";
import { Badge } from "@/components/ui/badge";
import { Table, TBody, TD, TH, THead, TR } from "@/components/ui/table";

const severityClasses: Record<string, string> = {
  low: "bg-zinc-700/30 text-zinc-200",
  med: "bg-amber-600/25 text-amber-200",
  high: "bg-orange-600/25 text-orange-200",
  critical: "bg-red-600/25 text-red-200",
};

export function AlertTable({ alerts }: { alerts: Alert[] }) {
  return (
    <Table>
      <THead>
        <TR>
          <TH>Created</TH>
          <TH>Module</TH>
          <TH>Severity</TH>
          <TH>Score</TH>
          <TH>Status</TH>
          <TH>View</TH>
        </TR>
      </THead>
      <TBody>
        {alerts.map((a) => (
          <TR key={a.id}>
            <TD>{new Date(a.created_at).toLocaleString()}</TD>
            <TD>{a.module}</TD>
            <TD><Badge className={severityClasses[a.severity]}>{a.severity}</Badge></TD>
            <TD>{a.score}</TD>
            <TD>{a.status}</TD>
            <TD><Link className="text-emerald-300 hover:underline" href={`/alerts/${a.id}`}>Open</Link></TD>
          </TR>
        ))}
      </TBody>
    </Table>
  );
}
