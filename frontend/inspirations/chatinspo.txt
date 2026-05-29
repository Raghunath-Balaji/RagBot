import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import ChatbotScreen from './screens/chatbot';
import AdminScreen from './screens/admin';
import { MessageSquare, Settings } from 'lucide-react';

function Layout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex flex-col h-screen bg-gray-50">
      <nav className="bg-white border-b border-gray-200 px-4 py-3 flex justify-between items-center">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
            <MessageSquare className="text-white w-5 h-5" />
          </div>
          <span className="font-bold text-xl text-gray-800">RAGbot</span>
        </div>
        <div className="flex gap-4">
          <Link 
            to="/" 
            className="flex items-center gap-2 px-3 py-2 rounded-md hover:bg-gray-100 text-gray-700 transition-colors"
          >
            <MessageSquare className="w-4 h-4" />
            <span>Chat</span>
          </Link>
          <Link 
            to="/admin" 
            className="flex items-center gap-2 px-3 py-2 rounded-md hover:bg-gray-100 text-gray-700 transition-colors"
          >
            <Settings className="w-4 h-4" />
            <span>Admin</span>
          </Link>
        </div>
      </nav>
      <main className="flex-1 overflow-hidden">
        {children}
      </main>
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
