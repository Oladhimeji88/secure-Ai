import { AssetsTable } from "@/components/assets/assets-table";
import { api } from "@/lib/api";

export default async function AssetsPage() {
  let items: any[] = [];
  try {
    const res = await api.assets();
    items = res.items || [];
  } catch {
    items = [];
  }

  return (
    <div className="space-y-4">
      <h2 className="text-xl font-semibold">Assets</h2>
      <AssetsTable assets={items} />
    </div>
  );
}
