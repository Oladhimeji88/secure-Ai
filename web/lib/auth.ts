export function getTokenFromCookie(cookieHeader: string | null): string | null {
  if (!cookieHeader) return null;
  const token = cookieHeader
    .split(";")
    .map((v) => v.trim())
    .find((v) => v.startsWith("aegis_token="));
  return token ? token.split("=")[1] : null;
}
