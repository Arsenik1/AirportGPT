"use client";

import dynamic from "next/dynamic";

const ClientThemeProvider = dynamic(
  () => import("./ClientThemeProvider"),
  { ssr: false }
);

export default function ClientThemeProviderWrapper({
  children,
}: {
  children: React.ReactNode;
}) {
  return <ClientThemeProvider>{children}</ClientThemeProvider>;
}