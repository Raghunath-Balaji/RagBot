import React from 'react';

const Chatbot = () => {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
      <div className="p-8 bg-white rounded-lg shadow-xl">
        <h1 className="text-3xl font-bold text-blue-600 mb-4">
          Tailwind Test: Chatbot Component
        </h1>
        <p className="text-gray-700">
          If you see a <span className="text-red-500 font-bold">blue heading</span> and a card with a shadow, Tailwind is working!
        </p>
        <div className="mt-6 p-4 bg-green-100 border-l-4 border-green-500 text-green-700">
          Backend Proxy Test: Check if /api routes work here.
        </div>
      </div>
    </div>
  );
};

export default Chatbot;
