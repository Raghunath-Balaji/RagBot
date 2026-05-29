import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import ChatbotScreen from "./components/pages/chatbot";
import AdminScreen from "./components/pages/admin";
import { Header } from "./components/layout/Header";

function Layout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex flex-col h-screen bg-gray-50">
      {/* //calls the header and then the children */}
      <Header />
      <main className="flex-1 overflow-hidden">{children}</main>
    </div>
  );
}

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<ChatbotScreen />} />
          <Route path="/admin" element={<AdminScreen />} />
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;
