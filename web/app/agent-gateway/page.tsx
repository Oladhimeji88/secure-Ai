import { GatewayLogTable } from "@/components/gateway/gateway-log-table";
import { PolicyForm } from "@/components/settings/policy-form";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { api } from "@/lib/api";

export default async function AgentGatewayPage() {
  const [logs, policy] = await Promise.all([
    api.gatewayLogs().catch(() => ({ items: [] })),
    api.gatewayPolicy().catch(() => ({ gateway_risk_threshold: 50, allow_tools: [] })),
  ]);

  return (
    <div className="grid gap-6 md:grid-cols-3">
      <Card className="md:col-span-2">
        <CardHeader><CardTitle>Gateway Logs</CardTitle></CardHeader>
        <CardContent><GatewayLogTable items={logs.items || []} /></CardContent>
      </Card>
      <PolicyForm policy={policy} />
    </div>
  );
}
