import { KpiCard } from "@/components/kpi-card";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { AlertTrend } from "@/components/charts/alert-trend";
import { ModuleBreakdown } from "@/components/charts/module-breakdown";
import { api } from "@/lib/api";

export default async function OverviewPage() {
  let data = { kpis: { total_alerts: 0, high_severity: 0, assets_at_risk: 0, open_remediations: 0 }, trend: [], module_breakdown: [] };
  try {
    data = await api.overview();
  } catch {
    // keep empty dashboard state
  }

  return (
    <div className="space-y-6">
      <div className="grid gap-4 md:grid-cols-4">
        <KpiCard label="Total Alerts" value={data.kpis.total_alerts} />
        <KpiCard label="High Severity" value={data.kpis.high_severity} />
        <KpiCard label="Assets at Risk" value={data.kpis.assets_at_risk} />
        <KpiCard label="Open Remediations" value={data.kpis.open_remediations} />
      </div>
      <div className="grid gap-6 md:grid-cols-2">
        <Card>
          <CardHeader><CardTitle>Alert Trend (7 days)</CardTitle></CardHeader>
          <CardContent><AlertTrend data={data.trend} /></CardContent>
        </Card>
        <Card>
          <CardHeader><CardTitle>Module Breakdown</CardTitle></CardHeader>
          <CardContent><ModuleBreakdown data={data.module_breakdown} /></CardContent>
        </Card>
      </div>
    </div>
  );
}
