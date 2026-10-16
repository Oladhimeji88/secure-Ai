import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Table, TBody, TD, TH, THead, TR } from "@/components/ui/table";
import { api } from "@/lib/api";

export default async function SettingsPage() {
  const [users, thresholds] = await Promise.all([
    api.users().catch(() => ({ items: [] })),
    api.thresholds().catch(() => ({ phishing_threshold: 65, step_up_threshold: 70, anomaly_threshold: 60 })),
  ]);

  return (
    <div className="grid gap-6 md:grid-cols-2">
      <Card>
        <CardHeader><CardTitle>RBAC Users</CardTitle></CardHeader>
        <CardContent>
          <Table>
            <THead><TR><TH>Email</TH><TH>Name</TH><TH>Role</TH></TR></THead>
            <TBody>{users.items.map((u: any) => <TR key={u.id}><TD>{u.email}</TD><TD>{u.full_name}</TD><TD>{u.role}</TD></TR>)}</TBody>
          </Table>
        </CardContent>
      </Card>
      <Card>
        <CardHeader><CardTitle>System Thresholds</CardTitle></CardHeader>
        <CardContent>
          <div className="space-y-2 text-sm">
            <div>Phishing Score Threshold: {thresholds.phishing_threshold}</div>
            <div>Step-up Verification Threshold: {thresholds.step_up_threshold}</div>
            <div>Anomaly Threshold: {thresholds.anomaly_threshold}</div>
            <div>Gateway Risk Threshold: {thresholds.gateway_risk_threshold}</div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
