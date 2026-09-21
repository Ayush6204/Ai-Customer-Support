import { createTheme } from "@mui/material/styles";

export const getAppTheme = (mode = "light") =>
  createTheme({
    palette: {
      mode,
      primary: {
        main: "#4f46e5",
        light: "#818cf8",
        dark: "#3730a3",
        contrastText: "#ffffff",
      },
      secondary: {
        main: "#06b6d4",
        light: "#67e8f9",
        dark: "#0e7490",
      },
      background: {
        default: mode === "light" ? "#f8fafc" : "#0f172a",
        paper: mode === "light" ? "#ffffff" : "#1e293b",
      },
      text: {
        primary: mode === "light" ? "#0f172a" : "#f8fafc",
        secondary: mode === "light" ? "#475569" : "#cbd5e1",
      },
      divider: mode === "light" ? "#e2e8f0" : "#334155",
    },

    typography: {
      fontFamily: ["Inter", "Roboto", "Arial", "sans-serif"].join(","),
      h1: {
        fontWeight: 800,
        letterSpacing: "-0.04em",
      },
      h2: {
        fontWeight: 800,
        letterSpacing: "-0.03em",
      },
      h3: {
        fontWeight: 700,
      },
      h4: {
        fontWeight: 700,
      },
      h5: {
        fontWeight: 700,
      },
      h6: {
        fontWeight: 700,
      },
      button: {
        textTransform: "none",
        fontWeight: 600,
      },
    },

    shape: {
      borderRadius: 14,
    },

    components: {
      MuiButton: {
        styleOverrides: {
          root: {
            borderRadius: "12px",
            padding: "10px 18px",
            boxShadow: "none",
          },
          containedPrimary: {
            background: "linear-gradient(135deg, #4f46e5, #06b6d4)",
            color: "#ffffff",
            "&:hover": {
              boxShadow: "0 10px 24px rgba(79, 70, 229, 0.35)",
            },
          },
        },
      },

      MuiCard: {
        styleOverrides: {
          root: {
            borderRadius: "20px",
            boxShadow: mode === "light"
              ? "0 12px 35px rgba(15, 23, 42, 0.08)"
              : "0 12px 35px rgba(0, 0, 0, 0.35)",
          },
        },
      },

      MuiTextField: {
        styleOverrides: {
          root: {
            "& .MuiOutlinedInput-root": {
              borderRadius: "12px",
            },
          },
        },
      },

      MuiPaper: {
        styleOverrides: {
          root: {
            backgroundImage: "none",
          },
        },
      },
    },
  });