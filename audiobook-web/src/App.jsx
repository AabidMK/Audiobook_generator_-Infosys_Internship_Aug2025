import { useState } from "react";
import { API_URL, ingest, askRag } from "./api";
import "./styles.css";

function Uploader({ onDone }) {
  const [file, setFile] = useState(null);
  const [title, setTitle] = useState("");
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState("");

  const submit = async (e) => {
    e.preventDefault();
    if (!file) return;
    setBusy(true); setErr("");
    try {
      const item = await ingest(file, title);
      onDone(item);                 // <- sets current upload in parent
      setFile(null); setTitle("");
    } catch (e) {
      setErr(String(e));
    } finally {
      setBusy(false);
    }
  };

  return (
    <form className="card" onSubmit={submit}>
      <h3>Upload → Gemini rewrite → MP3 → Index</h3>
      <div className="row" style={{marginBottom:8}}>
        <input className="file" type="file" accept=".pdf,.docx,.txt,.md"
               onChange={e=>setFile(e.target.files?.[0]||null)} />
        <input className="input" type="text" placeholder="Title (optional)"
               value={title} onChange={e=>setTitle(e.target.value)} />
        <button className="btn" disabled={!file || busy}>
          {busy ? <><span className="spinner" /> Processing</> : "Start pipeline"}
        </button>
      </div>
      {err && <div className="error">Error: {err}</div>}
      <div className="hr" />
      <small style={{color:"var(--muted)"}}>
        Files are rewritten with Gemini and converted to an MP3 automatically.
      </small>
    </form>
  );
}

function Player({ item }) {
  if (!item) return (
    <div className="card">
      <h3>Preview</h3>
      <div style={{color:"var(--muted)"}}>Upload a document to generate an audiobook and see it here.</div>
    </div>
  );
  return (
    <div className="card">
      <h3 style={{marginBottom:6}}>{item.title}</h3>
      <audio className="audio" controls src={`${API_URL}/audiobooks/${item.id}/stream`} />
      <div style={{marginTop:10}}>
        <a className="link" href={`${API_URL}/audiobooks/${item.id}/download`}>Download MP3</a>
      </div>
    </div>
  );
}

function Chat({ current }) {
  const [q, setQ] = useState("");
  const [busy, setBusy] = useState(false);
  const [ans, setAns] = useState("");
  const [cits, setCits] = useState([]);

  const ask = async (e) => {
    e.preventDefault();
    if (!current?.id || !q.trim()) return;
    setBusy(true); setAns(""); setCits([]);
    try {
      const r = await askRag(q, current.id);  // <- strictly scope to current file
      setAns(r.answer);
      setCits(r.citations || []);
    } catch (e) {
      setAns(String(e));
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="card" style={{marginTop:18}}>
      <h3>RAG Q&A</h3>
      {!current ? (
        <div className="answer" style={{color:"var(--muted)"}}>
          Upload a document first. Questions will be answered using only the latest upload.
        </div>
      ) : (
        <>
          <div style={{margin:"0 0 8px", color:"var(--muted)"}}>
            Using: <strong>{current.title}</strong>
          </div>
          <form className="row" onSubmit={ask} style={{marginBottom:10}}>
            <input className="input" style={{flex:1}} placeholder="Ask about your document..."
                   value={q} onChange={e=>setQ(e.target.value)} />
            <button className="btn" disabled={busy || !current?.id}>
              {busy ? <><span className="spinner" /> Asking</> : "Ask"}
            </button>
          </form>
          {ans && (<>
            <div className="answer">{ans}</div>
            {cits.length>0 && (
              <ul className="citations">
                {cits.map((c,i)=>
                  <li key={i}>{c.file_path} (chunk {c.chunk_id}) — dist {c.distance}, sim {c.similarity}</li>
                )}
              </ul>
            )}
          </>)}
        </>
      )}
    </div>
  );
}

export default function App() {
  const [current, setCurrent] = useState(null); // no auto-pick of old uploads

  return (
    <div className="page">
      <h1 className="title">Audiobook Pipeline</h1>
      <div className="grid">
        <Uploader onDone={(item)=>setCurrent(item)} />
        <Player item={current} />
      </div>
      <Chat current={current} />
    </div>
  );
}
