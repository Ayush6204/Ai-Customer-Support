import AppRoutes from "./routes/AppRoutes";

function App({ mode, toggleTheme }) {
  return <AppRoutes mode={mode} toggleTheme={toggleTheme} />;
}

export default App;