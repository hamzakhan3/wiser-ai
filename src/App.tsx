import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Index from "./pages/Index";
import NotFound from "./pages/NotFound";
import ChatPage from "./pages/ChatPage";
import SettingsPage from "./pages/SettingsPage";
import PostgreSQLSetupPage from "./pages/PostgreSQLSetupPage";
import MachineHealthPage from "./pages/MachineHealthPage";
import InspectionPage from "./pages/InspectionPage";
import MaintenanceSchedulePage from "./pages/MaintenanceSchedulePage";
import WisdomPage from "./pages/WisdomPage";
import ComingSoonPage from "./pages/ComingSoonPage";

const queryClient = new QueryClient();

const App = () => (
  <QueryClientProvider client={queryClient}>
    <TooltipProvider>
      <Toaster />
      <Sonner />
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<WisdomPage />} />
          <Route path="/index" element={<Index />} />
          <Route path="/chat" element={<ChatPage />} />
          <Route path="/settings" element={<SettingsPage />} />
          <Route path="/postgresql-setup" element={<PostgreSQLSetupPage />} />
          <Route path="/machine-health" element={<MachineHealthPage />} />
          <Route path="/inspection" element={<InspectionPage />} />
          <Route path="/maintenance-schedule" element={<MaintenanceSchedulePage />} />
          <Route path="/wisdom" element={<WisdomPage />} />
          <Route path="/coming-soon" element={<ComingSoonPage />} />
          {/* ADD ALL CUSTOM ROUTES ABOVE THE CATCH-ALL "*" ROUTE */}
          <Route path="*" element={<ComingSoonPage />} />
        </Routes>
      </BrowserRouter>
    </TooltipProvider>
  </QueryClientProvider>
);

export default App;