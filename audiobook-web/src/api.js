export const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

export async function ingest(file, title) {
  const fd = new FormData();
  fd.append("file", file);
  if (title) fd.append("title", title);
  const res = await fetch(`${API_URL}/pipeline/ingest`, { method: "POST", body: fd });
  if (!res.ok) throw new Error(await res.text());
  return res.json(); // { id, title, play_url, download_url }
}

// Ask strictly about the CURRENT upload (audiobook_id is required by the UI)
export async function askRag(question, audiobook_id) {
  const res = await fetch(`${API_URL}/rag/ask`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question, audiobook_id }),
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}
