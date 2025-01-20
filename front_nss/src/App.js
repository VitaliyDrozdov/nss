import { ColorModeContext, useTheme } from "./hooks/useTheme";
import { CssBaseline, ThemeProvider } from "@mui/material";
import { Routes, Route, Navigate, useLocation, Outlet } from "react-router-dom";
import { useAuth } from "./hooks/useAuth";
import { PermifyProvider } from "@permify/react-role";

import QuoteOsago from "./pages/QuoteOsago/QuoteOsago";
import Profile from "./pages/Profile/Profile";
import QualityControl from "./pages/Quality/QualityControl";
import ModelMonitoring from "./pages/ModelMonitoring/ModelMonitoring";
import ModelCatalog from "./pages/ModelCatalog/ModelCatalog";
import DataMart from "./pages/DWH/DataMart";
import IncidentList from "./pages/Observability/IncidentList";
import ListQuality from "./pages/Quality/QualityHistory";
import SignIn from "./pages/UM/SignIn/SignIn";
import AccountManagement from "./pages/UM/SignUp/SignUp";

import Topbar from "./components/Topbar";
import Sidebar from "./components/Sidebar";

function App() {
  const [theme, colorMode] = useTheme();

  const location = useLocation();
  const showSidebarOn = [
    "/quoteOsago",
    "/profile", 
    "/history", 
    "/qualityControl", 
    "/createReport",
    "/modelCatalog",
    "/dataMart",
    "/manageRoles",
    "/manageUsers",
    "/incidentList",
    "/qualityHistory"

  ];
  const showTopbarOn = [
    "/quoteOsago",
    "/profile",
    "/qualityControl",
    "/createReport",
    "/modelCatalog",
    "/dataMart",
    "/manageRoles",
    "/manageUsers",
    "/incidentList",
    "/qualityHistory"
  ];

  return (
    <PermifyProvider>
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
                <Route path="/manageUsers" element={<AccountManagement />} />

                {/* protected routes */}
                <Route element={<ProtectedRoutes />}>
                <Route path="/" element={<SignIn />} />
                <Route path="/quoteOsago" element={<QuoteOsago />} /> {/* IN PROGRESS */}

                <Route path="/profile" element={<Profile />} />

                <Route path="/qualityControl" element={<QualityControl />} />
                <Route path="/qualityHistory" element={<ListQuality />} />

                <Route path="/createReport" element={<ModelMonitoring />} />

                <Route path="/modelCatalog" element={<ModelCatalog />} />

                <Route path="/dataMart" element={<DataMart />} />
                <Route path="/incidentList" element={<IncidentList />} />
                
                </Route>
              </Routes>
            </main>
          </div>
        </ThemeProvider>
      </ColorModeContext.Provider>
    </PermifyProvider>
  );
}

const ProtectedRoutes = () => {
  const { isLoggedIn } = useAuth();
  return isLoggedIn ? <Outlet /> : <Navigate to="/signin" replace />;
};

export default App;