import { AlertDetail } from "@/components/alerts/alert-detail";
import { api } from "@/lib/api";

export default async function AlertDetailPage({ params }: { params: { id: string } }) {
  const alert = await api.alert(params.id);
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-semibold">Alert Detail</h2>
      <AlertDetail alert={alert} />
    </div>
  );
}
