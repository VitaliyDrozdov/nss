import { ColorModeContext, useTheme } from "./hooks/useTheme";
import { CssBaseline, ThemeProvider } from "@mui/material";
import { Routes, Route, Navigate, useLocation, Outlet } from "react-router-dom";
import { useAuth } from "./hooks/useAuth";

import SignIn from "./pages/SignIn/SignIn";
import SignUp from "./pages/SignUp/SignUp";
import Test from "./pages/Test/Test"; // IN PROGRESS
import Profile from "./pages/Profile/Profile";

import Topbar from "./components/Topbar";
import Sidebar from "./components/Sidebar";

function App() {
  const [theme, colorMode] = useTheme();

  const location = useLocation();
  const showSidebarOn = ["/test", "/profile", "/history"];
  const showTopbarOn = ["/test", "/profile"];

  return (
    <ColorModeContext.Provider value={colorMode}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <div className="app">
          {showSidebarOn.includes(location.pathname) && <Sidebar />}
          <main className="content">
            {showTopbarOn.includes(location.pathname) && <Topbar />}
            <Routes>
              {/* unprotected routes */}

              <Route path="/signin" element={<SignIn />} />
              <Route path="/signup" element={<SignUp />} />

              {/* protected routes */}
              <Route element={<ProtectedRoutes />}>
              <Route path="/" element={<SignIn />} /> {/* IN PROGRESS */}
              <Route path="/test" element={<Test />} /> {/* IN PROGRESS */}

              <Route path="/profile" element={<Profile />} />
               
              </Route>
            </Routes>
          </main>
        </div>
      </ThemeProvider>
    </ColorModeContext.Provider>
  );
}

const ProtectedRoutes = () => {
  const { isLoggedIn } = useAuth();
  return isLoggedIn ? <Outlet /> : <Navigate to="/signin" replace />;
};

export default App;