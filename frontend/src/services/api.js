const BACKEND_URL = 'http://localhost:8000';

export async function analyzeStock(company) {
  const response = await fetch(
    `${BACKEND_URL}/analyze?company=${encodeURIComponent(company)}`
  );
  if (!response.ok) {
    throw new Error(`Analysis failed: ${response.status}`);
  }
  return response.json();
}

export async function askAI({ question, company, context }) {
  const response = await fetch(`${BACKEND_URL}/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question, company, context }),
  });
  if (!response.ok) {
    throw new Error(`Chat failed: ${response.status}`);
  }
  const data = await response.json();
  return data.answer;
}