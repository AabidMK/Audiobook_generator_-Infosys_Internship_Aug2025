import React, { useEffect, useState } from "react";

export default function UploadBox() {
  const [file, setFile] = useState(null);
  const [jobs, setJobs] = useState([]);

  // fetch jobs from backend
  async function fetchJobs() {
    try {
      const res = await fetch("http://localhost:8000/api/jobs");
      const data = await res.json();
      setJobs(data);
    } catch (err) {
      console.error("Error fetching jobs:", err);
    }
  }

  useEffect(() => {
    fetchJobs();
    const interval = setInterval(fetchJobs, 3000);
    return () => clearInterval(interval);
  }, []);

  // handle file upload
  async function handleUpload() {
    if (!file) return;
    const fd = new FormData();
    fd.append("file", file);

    try {
      await fetch("http://localhost:8000/api/upload", {
        method: "POST",
        body: fd,
      });
      setFile(null);
      setTimeout(fetchJobs, 2000);
    } catch (err) {
      alert("Upload failed");
    }
  }

  // delete job
  async function deleteJob(jobId) {
    try {
      await fetch(`http://localhost:8000/api/jobs/${jobId}`, { method: "DELETE" });
      fetchJobs();
    } catch (err) {
      console.error("Error deleting job:", err);
    }
  }

  return (
    <div className="upload-box">
      <h2>Upload Your Document</h2>
      <input
        type="file"
        onChange={(e) => setFile(e.target.files[0])}
        accept=".pdf,.docx,.txt"
      />
      <button onClick={handleUpload}>Upload</button>

      <h3>Your Audiobooks</h3>
      <ul>
        {jobs.map((job) => (
          <li key={job.id}>
            <strong>{job.filename}</strong> — {job.status}
            {job.status === "completed" && job.audio_files && job.audio_files.length > 0 && (
              <>
                {" "}
                <a
                  href={`http://localhost:8000/api/download/${job.id}/${job.audio_files[0]}`}
                  download
                >
                  Download Audio
                </a>
              </>
            )}
            {job.status === "error" && <span>  {job.error_message}</span>}
            <button onClick={() => deleteJob(job.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
}
