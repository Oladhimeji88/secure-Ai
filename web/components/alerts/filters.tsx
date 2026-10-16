"use client";

import { useState } from "react";
import { Input } from "@/components/ui/input";
import { Select } from "@/components/ui/select";

export function AlertFilters({ onChange }: { onChange: (q: string) => void }) {
  const [module, setModule] = useState("");
  const [severity, setSeverity] = useState("");
  const [status, setStatus] = useState("");
  const [minScore, setMinScore] = useState("");
  const [maxScore, setMaxScore] = useState("");

  function apply() {
    const qs = new URLSearchParams();
    if (module) qs.set("module", module);
    if (severity) qs.set("severity", severity);
    if (status) qs.set("status", status);
    if (minScore) qs.set("min_score", minScore);
    if (maxScore) qs.set("max_score", maxScore);
    onChange(`?${qs.toString()}`);
  }

  return (
    <div className="grid grid-cols-1 gap-3 md:grid-cols-5">
      <Input placeholder="Module" value={module} onChange={(e) => setModule(e.target.value)} />
      <Select value={severity} onChange={(e) => setSeverity(e.target.value)}>
        <option value="">Severity</option>
        <option value="low">Low</option>
        <option value="med">Med</option>
        <option value="high">High</option>
        <option value="critical">Critical</option>
      </Select>
      <Select value={status} onChange={(e) => setStatus(e.target.value)}>
        <option value="">Status</option>
        <option value="open">Open</option>
        <option value="triaged">Triaged</option>
        <option value="closed">Closed</option>
      </Select>
      <Input placeholder="Min Score" value={minScore} onChange={(e) => setMinScore(e.target.value)} />
      <Input placeholder="Max Score" value={maxScore} onChange={(e) => setMaxScore(e.target.value)} onBlur={apply} />
    </div>
  );
}
