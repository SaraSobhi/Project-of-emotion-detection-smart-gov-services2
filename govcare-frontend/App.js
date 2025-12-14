import { BrowserRouter, Routes, Route } from "react-router-dom";

import HomePage from "./pages/HomePage";
import LoginPage from "./pages/LoginPage";
import DashboardPage from "./pages/DashboardPage";
import CitizenPage from "./pages/CitizenPage";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* الصفحة الرئيسية */}
        <Route path="/" element={<HomePage />} />

        {/* لوجن الموظف */}
        <Route path="/login" element={<LoginPage />} />

        {/* داشبورد الموظف */}
        <Route path="/dashboard" element={<DashboardPage />} />

        {/* صفحة المواطن */}
        <Route path="/citizen" element={<CitizenPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
