import * as React from "react";
import { cn } from "@/lib/utils";

export function Input(props: React.InputHTMLAttributes<HTMLInputElement>) {
  return <input {...props} className={cn("h-9 w-full rounded-md border border-border bg-muted px-3 text-sm text-foreground outline-none focus:border-emerald-500", props.className)} />;
}
