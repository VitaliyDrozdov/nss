import { ColorModeContext, useTheme } from "./hooks/useTheme";
import { CssBaseline, ThemeProvider } from "@mui/material";
import { Routes, Route, Navigate, useLocation, Outlet } from "react-router-dom";
import { useAuth } from "./hooks/useAuth";

import SignIn from "./pages/SignIn/SignIn";
import SignUp from "./pages/SignUp/SignUp";
import QuoteOsago from "./pages/QuoteOsago/QuoteOsago"; // IN PROGRESS
import Profile from "./pages/Profile/Profile";
import QualityControl from "./pages/Quality/QualityControl";
import ModelMonitoring from "./pages/ModelMonitoring/ModelMonitoring";
import ModelCatalog from "./pages/ModelCatalog/ModelCatalog";
import DataMart from "./pages/DWH/DataMart";

import Topbar from "./components/Topbar";
import Sidebar from "./components/Sidebar";

function App() {
  const [theme, colorMode] = useTheme();

  const location = useLocation();
  const showSidebarOn = ["/quoteOsago",
    "/profile", 
    "/history", 
    "/qualityControl", 
    "/modelMonitoring",
    "/modelCatalog",
    "/dataMart"

  ];
  const showTopbarOn = [
    "/quoteOsago",
    "/profile",
    "/qualityControl",
    "/modelMonitoring",
    "/modelCatalog",
    "/dataMart"
  ];

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
              <Route path="/" element={<SignIn />} />
              <Route path="/quoteOsago" element={<QuoteOsago />} /> {/* IN PROGRESS */}

              <Route path="/profile" element={<Profile />} />

              <Route path="/qualityControl" element={<QualityControl />} />

              <Route path="/modelMonitoring" element={<ModelMonitoring />} />

              <Route path="/modelCatalog" element={<ModelCatalog />} />

              <Route path="/dataMart" element={<DataMart />} />
               
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