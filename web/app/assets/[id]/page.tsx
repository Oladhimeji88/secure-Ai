import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Table, TBody, TD, TH, THead, TR } from "@/components/ui/table";
import { api } from "@/lib/api";

export default async function AssetDetailPage({ params }: { params: { id: string } }) {
  const data = await api.asset(params.id);
  return (
    <div className="space-y-6">
      <Card>
        <CardHeader><CardTitle>{data.asset.name}</CardTitle></CardHeader>
        <CardContent>
          <div className="grid gap-2 text-sm md:grid-cols-2">
            <div>Type: {data.asset.type}</div>
            <div>Owner: {data.asset.owner}</div>
            <div>Criticality: {data.asset.criticality}</div>
            <div>Internet Exposed: {data.asset.internet_exposed ? "Yes" : "No"}</div>
          </div>
        </CardContent>
      </Card>
      <Card>
        <CardHeader><CardTitle>Findings</CardTitle></CardHeader>
        <CardContent>
          <Table>
            <THead><TR><TH>Category</TH><TH>CVE</TH><TH>Created</TH></TR></THead>
            <TBody>{data.findings.map((f: any) => <TR key={f.id}><TD>{f.category}</TD><TD>{f.cve || "-"}</TD><TD>{new Date(f.created_at).toLocaleString()}</TD></TR>)}</TBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  );
}
