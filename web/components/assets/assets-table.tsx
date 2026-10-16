import Link from "next/link";
import { Badge } from "@/components/ui/badge";
import { Table, TBody, TD, TH, THead, TR } from "@/components/ui/table";

const critClass: Record<string, string> = {
  low: "bg-zinc-700/30 text-zinc-200",
  med: "bg-amber-600/25 text-amber-200",
  high: "bg-red-600/25 text-red-200",
};

export function AssetsTable({ assets }: { assets: any[] }) {
  return (
    <Table>
      <THead><TR><TH>Name</TH><TH>Type</TH><TH>Owner</TH><TH>Criticality</TH><TH>Internet Exposed</TH><TH>Details</TH></TR></THead>
      <TBody>
        {assets.map((a) => (
          <TR key={a.id}>
            <TD>{a.name}</TD><TD>{a.type}</TD><TD>{a.owner}</TD>
            <TD><Badge className={critClass[a.criticality]}>{a.criticality}</Badge></TD>
            <TD>{a.internet_exposed ? "Yes" : "No"}</TD>
            <TD><Link href={`/assets/${a.id}`} className="text-emerald-300 hover:underline">Open</Link></TD>
          </TR>
        ))}
      </TBody>
    </Table>
  );
}
