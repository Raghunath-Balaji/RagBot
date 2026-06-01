import React, { Suspense, lazy } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { Header } from "./components/layout/Header";
import { GlobalSkeleton } from "./components/ui/GlobalSkeleton";
import { ErrorBoundary } from "./components/ui/ErrorBoundary";

// Lazy load page components
const ChatbotScreen = lazy(() => import("./components/pages/chatbot"));
const AdminScreen = lazy(() => import("./components/pages/admin"));

function Layout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex flex-col h-screen bg-gray-50">
      <Header />
      <main className="flex-1 overflow-hidden">{children}</main>
    </div>
  );
}

function App() {
  return (
    <ErrorBoundary>
      <Router>
        <Layout>
          <Suspense fallback={<GlobalSkeleton />}>
            <Routes>
              <Route path="/" element={<ChatbotScreen />} />
              <Route path="/admin" element={<AdminScreen />} />
            </Routes>
          </Suspense>
        </Layout>
      </Router>
    </ErrorBoundary>
  );
}

export default App;
