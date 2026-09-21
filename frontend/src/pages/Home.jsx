import { Link } from "react-router-dom";
import { Button, Container, Typography, Box, Card, CardContent } from "@mui/material";
import DarkModeIcon from "@mui/icons-material/DarkMode";
import LightModeIcon from "@mui/icons-material/LightMode";

function Home({ mode, toggleTheme }) {
  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-900">
      <Container maxWidth="lg">
        <Box className="flex min-h-screen items-center justify-center py-10">
          <Card className="w-full max-w-4xl">
            <CardContent className="p-8 md:p-12">
              <div className="mb-6 flex justify-end">
                <Button
                  variant="outlined"
                  onClick={toggleTheme}
                  startIcon={mode === "light" ? <DarkModeIcon /> : <LightModeIcon />}
                >
                  {mode === "light" ? "Dark Mode" : "Light Mode"}
                </Button>
              </div>

              <Typography variant="h2" className="mb-4 text-center">
                RAG Document Assistant
              </Typography>

              <Typography
                variant="h6"
                color="text.secondary"
                className="mx-auto mb-8 max-w-2xl text-center"
              >
                Upload your documents, create isolated chat sessions, and ask
                AI questions from only your own uploaded files.
              </Typography>

              <div className="flex flex-col justify-center gap-4 sm:flex-row">
                <Button
                  component={Link}
                  to="/login"
                  variant="contained"
                  size="large"
                >
                  Login
                </Button>

                <Button
                  component={Link}
                  to="/register"
                  variant="outlined"
                  size="large"
                >
                  Create Account
                </Button>
              </div>

              <div className="mt-10 grid gap-4 md:grid-cols-3">
                <div className="rounded-2xl bg-slate-100 p-5">
                  <h3 className="mb-2 text-lg font-bold text-slate-900">
                    Secure Auth
                  </h3>
                  <p className="text-sm text-slate-600">
                    JWT access and refresh token based authentication.
                  </p>
                </div>

                <div className="rounded-2xl bg-slate-100 p-5">
                  <h3 className="mb-2 text-lg font-bold text-slate-900">
                    Session Isolation
                  </h3>
                  <p className="text-sm text-slate-600">
                    Each chat only uses documents uploaded inside that chat.
                  </p>
                </div>

                <div className="rounded-2xl bg-slate-100 p-5">
                  <h3 className="mb-2 text-lg font-bold text-slate-900">
                    RAG Pipeline
                  </h3>
                  <p className="text-sm text-slate-600">
                    LangChain, ChromaDB, embeddings, and LLM-powered answers.
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
        </Box>
      </Container>
    </div>
  );
}

export default Home;