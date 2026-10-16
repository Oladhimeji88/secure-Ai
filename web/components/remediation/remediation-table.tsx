import { Table, TBody, TD, TH, THead, TR } from "@/components/ui/table";

export function RemediationTable({ items }: { items: any[] }) {
  return (
    <Table>
      <THead><TR><TH>CVE</TH><TH>Asset</TH><TH>Priority Score</TH><TH>SLA</TH><TH>Patch Available</TH></TR></THead>
      <TBody>
        {items.map((i) => (
          <TR key={`${i.cve}-${i.asset}`}>
            <TD>{i.cve ?? "N/A"}</TD>
            <TD>{i.asset}</TD>
            <TD>{i.priority_score}</TD>
            <TD>{i.sla_suggestion}</TD>
            <TD>{i.patch_available ? "Yes" : "No"}</TD>
          </TR>
        ))}
      </TBody>
    </Table>
  );
}
