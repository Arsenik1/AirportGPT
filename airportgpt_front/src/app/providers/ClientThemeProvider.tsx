"use client";

// filepath: /c:/Users/salih/Desktop/cs-works/iGA_Intern/AirportGPT/airport-gpt-front/src/app/providers/ClientThemeProvider.tsx
import { ThemeProvider, createTheme, CssBaseline } from "@mui/material";
import React from "react";

const theme = createTheme({
  typography: {
    fontFamily: 'var(--font-geist-sans)',
    fontWeightLight: 300,
    fontWeightRegular: 400,
    fontWeightMedium: 500,
    fontWeightBold: 700,
  },
  palette: {
    mode: "dark",
    primary: {
      main: "#fff",
    },
    secondary: {
      main: "#fff",
    },
  },
});

export default function ClientThemeProvider({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      {children}
    </ThemeProvider>
  );
}