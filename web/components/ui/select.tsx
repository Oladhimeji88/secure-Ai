import * as React from "react";
import { cn } from "@/lib/utils";

export function Select(props: React.SelectHTMLAttributes<HTMLSelectElement>) {
  return <select {...props} className={cn("h-9 rounded-md border border-border bg-muted px-3 text-sm text-foreground outline-none focus:border-emerald-500", props.className)} />;
}
