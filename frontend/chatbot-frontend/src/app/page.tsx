'use client';

import { Chat } from '@/components/Chat';

export default function Home() {
  return (
    <div className="flex flex-col h-screen">
      <header className="bg-blue-600 text-white p-4 shadow-md">
        <div className="max-w-4xl mx-auto flex justify-between items-center">
          <h1 className="text-2xl font-bold">RAG Chatbot</h1>
          <span className="text-sm bg-blue-700 px-3 py-1 rounded-full">
            Powered by LlamaIndex
          </span>
        </div>
      </header>
      
      <main className="flex-1 overflow-hidden">
        <div className="h-full max-w-4xl mx-auto">
          <Chat />
        </div>
      </main>
      
      <footer className="bg-gray-100 border-t border-gray-200 p-4">
        <div className="max-w-4xl mx-auto text-center text-gray-500 text-sm">
          &copy; {new Date().getFullYear()} RAG Chatbot Demo | 
          Connected to FastAPI backend
        </div>
      </footer>
    </div>
  );
}
