// API service for communicating with the FastAPI backend

/**
 * Send a query to the RAG backend
 * @param query User's query text
 * @returns The response from the RAG system
 */
export async function sendQuery(query: string): Promise<{ response: string }> {
  try {
    const response = await fetch('http://localhost:8000/query', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ query }),
    });
    
    if (!response.ok) {
      throw new Error(`Error: ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error querying the RAG system:', error);
    throw error;
  }
}
