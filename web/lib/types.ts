export type Severity = "low" | "med" | "high" | "critical";
export type Status = "open" | "triaged" | "closed";

export interface Alert {
  id: string;
  created_at: string;
  module: string;
  severity: Severity;
  score: number;
  status: Status;
  reasons: string[];
  recommended_actions: string[];
  evidence: Record<string, unknown>;
  related_asset_id?: string | null;
}
