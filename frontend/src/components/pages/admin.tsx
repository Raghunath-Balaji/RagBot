import React, { useState, useEffect, useRef } from "react";
import {
  Upload,
  FileText,
  CheckCircle,
  Clock,
  AlertCircle,
  Trash2,
} from "lucide-react";
import { AdminTableSkeleton } from "../ui/AdminTableSkeleton";

interface Document {
  id: number;
  filename: string;
  upload_date: string;
  status: "pending" | "processed" | "error" | "processing";
}

const AdminScreen = () => {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [isUploading, setIsUploading] = useState(false);
  const [isInitialLoading, setIsInitialLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const fetchDocuments = async (showLoading = false) => {
    if (showLoading) setIsInitialLoading(true);
    try {
      const response = await fetch("/api/admin/");
      if (response.ok) {
        const data = await response.json();
        setDocuments(data);
      }
    } catch (err) {
      console.error("Failed to fetch documents:", err);
    } finally {
      if (showLoading) setIsInitialLoading(false);
    }
  };

  useEffect(() => {
    fetchDocuments(true);
    // Poll for status updates every 5 seconds if there are pending docs
    const interval = setInterval(() => {
      fetchDocuments(false);
    }, 5000);
    return () => clearInterval(interval);
  }, []);

  const handleFileUpload = async (
    event: React.ChangeEvent<HTMLInputElement>,
  ) => {
    const file = event.target.files?.[0];
    if (!file) return;

    if (!file.name.endsWith(".pdf")) {
      setError("Only PDF files are supported.");
      return;
    }

    setIsUploading(true);
    setError(null);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("/api/admin/upload", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Upload failed");
      }

      await fetchDocuments(false);
      if (fileInputRef.current) fileInputRef.current.value = "";
    } catch (err) {
      console.log(err);
      setError("Failed to upload document.");
    } finally {
      setIsUploading(false);
    }
  };

  const handleDelete = async (id: number) => {
    if (
      !window.confirm(
        "Are you sure you want to delete this document? All associated data will be removed.",
      )
    )
      return;

    try {
      const response = await fetch(`/api/admin/delete/${id}`, {
        method: "DELETE",
      });

      if (!response.ok) {
        throw new Error("Deletion failed");
      }

      await fetchDocuments(false);
    } catch (err) {
      setError("Failed to delete document.");
    }
  };

  return (
    <div className="max-w-5xl mx-auto p-6">
      <div className="mb-8 flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">
            Document Management
          </h1>
          <p className="text-gray-600">
            Upload PDFs to train your chatbot context.
          </p>
        </div>

        <div>
          <input
            type="file"
            accept=".pdf"
            onChange={handleFileUpload}
            className="hidden"
            ref={fileInputRef}
          />
          <button
            onClick={() => fileInputRef.current?.click()}
            disabled={isUploading}
            className={`flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors ${
              isUploading ? "opacity-50 cursor-not-allowed" : ""
            }`}
          >
            <Upload className="w-4 h-4" />
            {isUploading ? "Uploading..." : "Upload PDF"}
          </button>
        </div>
      </div>

      {error && (
        <div className="mb-6 p-4 bg-red-50 border-l-4 border-red-500 text-red-700 flex items-center gap-3">
          <AlertCircle className="w-5 h-5" />
          <span>{error}</span>
        </div>
      )}

      {isInitialLoading ? (
        <AdminTableSkeleton />
      ) : (
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
          <table className="w-full text-left">
            <thead className="bg-gray-50 border-b border-gray-200 text-gray-600 uppercase text-xs font-semibold">
              <tr>
                <th className="px-6 py-4">Document Name</th>
                <th className="px-6 py-4">Upload Date</th>
                <th className="px-6 py-4">Status</th>
                <th className="px-6 py-4 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {documents.length === 0 ? (
                <tr>
                  <td
                    colSpan={4}
                    className="px-6 py-12 text-center text-gray-500"
                  >
                    No documents uploaded yet.
                  </td>
                </tr>
              ) : (
                documents.map((doc) => (
                  <tr
                    key={doc.id}
                    className="hover:bg-gray-50 transition-colors"
                  >
                    <td className="px-6 py-4 flex items-center gap-3">
                      <FileText className="w-5 h-5 text-blue-500" />
                      <span className="font-medium text-gray-900">
                        {doc.filename}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-gray-600">
                      {new Date(doc.upload_date).toLocaleDateString()}
                    </td>
                    <td className="px-6 py-4">
                      <div className="flex items-center gap-2">
                        {doc.status === "processed" && (
                          <>
                            <CheckCircle className="w-4 h-4 text-green-500" />
                            <span className="text-green-700 text-sm font-medium">
                              Processed
                            </span>
                          </>
                        )}
                        {doc.status === "processing" && (
                          <>
                            <Clock className="w-4 h-4 text-yellow-500 animate-pulse" />
                            <span className="text-yellow-700 text-sm font-medium">
                              Processing...
                            </span>
                          </>
                        )}
                        {doc.status === "error" && (
                          <>
                            <AlertCircle className="w-4 h-4 text-red-500" />
                            <span className="text-red-700 text-sm font-medium">
                              Error
                            </span>
                          </>
                        )}
                        {doc.status === "pending" && (
                          <>
                            <Clock className="w-4 h-4 text-gray-400" />
                            <span className="text-gray-500 text-sm font-medium">
                              Pending
                            </span>
                          </>
                        )}
                      </div>
                    </td>
                    <td className="px-6 py-4 text-right">
                      <button
                        onClick={() => handleDelete(doc.id)}
                        className="text-gray-400 hover:text-red-600 transition-colors"
                      >
                        <Trash2 className="w-5 h-5" />
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default AdminScreen;
