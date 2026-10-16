import { Table, TBody, TD, TH, THead, TR } from "@/components/ui/table";

export function GatewayLogTable({ items }: { items: any[] }) {
  return (
    <Table>
      <THead><TR><TH>Time</TH><TH>Tool</TH><TH>Decision</TH><TH>Reasons</TH></TR></THead>
      <TBody>
        {items.map((r) => (
          <TR key={r.id}>
            <TD>{new Date(r.created_at).toLocaleString()}</TD>
            <TD>{r.tool_name}</TD>
            <TD>{r.decision}</TD>
            <TD>{(r.reasons || []).join(", ")}</TD>
          </TR>
        ))}
      </TBody>
    </Table>
  );
}
