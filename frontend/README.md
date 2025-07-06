# RAG Chatbot Frontend

A modern, responsive frontend for the LlamaIndex RAG chatbot built with Next.js and Tailwind CSS.

## Features

- Clean, responsive UI for chatting with the RAG system
- Real-time message display
- Elegant styling with Tailwind CSS
- TypeScript for type safety

## Getting Started

### Prerequisites

- Node.js (v18 or higher)
- npm or yarn

### Installation

1. Navigate to the frontend directory:
   ```
   cd frontend/chatbot-frontend
   ```

2. Install dependencies:
   ```
   npm install
   ```
   or
   ```
   yarn
   ```

### Development

To run the development server:

```
npm run dev
```
or
```
yarn dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser to see the application.

### Production Build

To build for production:

```
npm run build
```
or
```
yarn build
```

To start the production build:

```
npm start
```
or
```
yarn start
```

## Backend Connection

The frontend is configured to connect to the FastAPI backend at `http://localhost:8000`. Make sure the backend is running before interacting with the chat.
