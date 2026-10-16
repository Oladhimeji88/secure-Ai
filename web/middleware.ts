import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export function middleware(request: NextRequest) {
  const token = request.cookies.get("aegis_token")?.value;
  const protectedPaths = ["/overview", "/alerts", "/assets", "/remediation", "/agent-gateway", "/settings"];
  if (protectedPaths.some((path) => request.nextUrl.pathname.startsWith(path)) && !token) {
    return NextResponse.next();
  }
  return NextResponse.next();
}

export const config = {
  matcher: ["/overview/:path*", "/alerts/:path*", "/assets/:path*", "/remediation/:path*", "/agent-gateway/:path*", "/settings/:path*"],
};
