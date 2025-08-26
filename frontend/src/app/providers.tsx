"use client";

import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { ThemeProvider, useTheme } from "next-themes";
import { Toaster } from "sonner";

type AvailableTheme = "light" | "dark" | "system";

export function Providers({ children }: { children: React.ReactNode }) {
  const queryClient = new QueryClient();

  return (
    <ThemeProvider
      attribute="class"
      defaultTheme="system"
      enableSystem
      disableTransitionOnChange
      themes={["light", "dark", "system"]}
    >
      <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
      <ToasterProvider />
    </ThemeProvider>
  );
}


function ToasterProvider() {
  const { theme } = useTheme();

  return (
    <Toaster richColors position="top-center" theme={theme as AvailableTheme} />
  );
}
