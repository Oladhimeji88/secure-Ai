import { RemediationTable } from "@/components/remediation/remediation-table";
import { api } from "@/lib/api";

export default async function RemediationPage() {
  let items: any[] = [];
  try {
    const data = await api.remediation();
    items = data.items || [];
  } catch {
    items = [];
  }

  return (
    <div className="space-y-4">
      <h2 className="text-xl font-semibold">Ranked Remediation Plan</h2>
      <RemediationTable items={items} />
    </div>
  );
}
