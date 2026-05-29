import { Link } from "react-router-dom";
import { MessageSquare, Settings } from "lucide-react";

export function Header() {
  return (
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
  );
}
