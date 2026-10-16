import Link from "next/link";
import { Shield, LayoutDashboard, Bell, Server, Wrench, Bot, Settings } from "lucide-react";

const links = [
  { href: "/overview", label: "Overview", icon: LayoutDashboard },
  { href: "/alerts", label: "Alerts", icon: Bell },
  { href: "/assets", label: "Assets", icon: Server },
  { href: "/remediation", label: "Remediation", icon: Wrench },
  { href: "/agent-gateway", label: "Agent Gateway", icon: Bot },
  { href: "/settings", label: "Settings", icon: Settings },
];

export function Sidebar() {
  return (
    <aside className="w-64 border-r border-border bg-card p-4">
      <div className="mb-6 flex items-center gap-2 text-foreground">
        <Shield className="h-5 w-5 text-emerald-500" />
        <span className="text-lg font-semibold">Secure AI</span>
      </div>
      <nav className="space-y-1">
        {links.map((item) => (
          <Link key={item.href} href={item.href} className="flex items-center gap-2 rounded-md px-3 py-2 text-sm text-zinc-400 hover:bg-muted hover:text-foreground">
            <item.icon className="h-4 w-4" />
            {item.label}
          </Link>
        ))}
      </nav>
    </aside>
  );
}
