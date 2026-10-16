"use client";

import { useEffect, useState } from "react";
import { AlertFilters } from "@/components/alerts/filters";
import { AlertTable } from "@/components/alerts/alert-table";
import { EmptyState } from "@/components/common/empty-state";
import { TableSkeleton } from "@/components/common/skeletons";
import { api } from "@/lib/api";
import { Alert } from "@/lib/types";

export default function AlertsPage() {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(true);
  const [alerts, setAlerts] = useState<Alert[]>([]);

  useEffect(() => {
    setLoading(true);
    api.alerts(query)
      .then((res) => setAlerts(res.items || []))
      .catch(() => setAlerts([]))
      .finally(() => setLoading(false));
  }, [query]);

  return (
    <div className="space-y-4">
      <AlertFilters onChange={setQuery} />
      {loading ? <TableSkeleton /> : alerts.length ? <AlertTable alerts={alerts} /> : <EmptyState title="No alerts" description="Try adjusting filters or ingesting sample data." />}
    </div>
  );
}
