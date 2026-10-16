"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

export function PolicyForm({ policy }: { policy: any }) {
  const [threshold, setThreshold] = useState(String(policy.gateway_risk_threshold ?? 50));
  const [allowTools, setAllowTools] = useState((policy.allow_tools ?? []).join(","));

  return (
    <div className="space-y-3 rounded-xl border border-border bg-card p-4">
      <div>
        <label className="mb-1 block text-xs text-zinc-400">Gateway Risk Threshold</label>
        <Input value={threshold} onChange={(e) => setThreshold(e.target.value)} />
      </div>
      <div>
        <label className="mb-1 block text-xs text-zinc-400">Allowlisted Tools (comma-separated)</label>
        <Input value={allowTools} onChange={(e) => setAllowTools(e.target.value)} />
      </div>
      <Button type="button">Save Policy</Button>
    </div>
  );
}
