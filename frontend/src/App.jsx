import React, { useState, useEffect } from "react";
import axios from "axios";
import "./reflection.css"; // reflections + ripple

// ✅ Axios defaults — ensures all requests use backend base URL + token automatically
axios.defaults.baseURL = "http://127.0.0.1:8000"; // adjust if backend runs elsewhere
axios.interceptors.request.use((config) => {
  const token = localStorage.getItem("auth_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

function App() {
  const [file, setFile] = useState(null);
  const [filename, setFilename] = useState(null);
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [qaHistory, setQaHistory] = useState([]);
  const [langs, setLangs] = useState({});
  const [selectedLang, setSelectedLang] = useState("en");
  const [audioUrl, setAudioUrl] = useState(null);
  const [dragOver, setDragOver] = useState(false);

  // login states
  const [showLogin, setShowLogin] = useState(true);
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  useEffect(() => {
    if (isLoggedIn) {
      fetchLangs();
      fetchHistory();
    }
  }, [isLoggedIn]);

  // 🗣️ Get languages
  const fetchLangs = async () => {
    try {
      const res = await axios.get("/api/langs");
      setLangs(res.data.langs || {});
    } catch (e) {
      console.error("Error fetching langs:", e);
    }
  };

  // 🧠 Get Q&A history
  const fetchHistory = async () => {
    try {
      const res = await axios.get("/api/qa-history");
      setQaHistory(res.data.qa_pairs || []);
    } catch (e) {
      console.error("Error fetching history:", e);
    }
  };

  // 🔐 LOGIN FUNCTION
  const handleLogin = async () => {
    if (!username || !password) {
      alert("Please enter username & password");
      return;
    }

    try {
      const res = await axios.post("/api/login", { username, password });
      const { token } = res.data;

      if (token) {
        localStorage.setItem("auth_token", token);
        setIsLoggedIn(true);
        setShowLogin(false);
        fetchLangs();
        fetchHistory();
      } else {
        alert("Invalid credentials");
      }
    } catch (err) {
      alert("Login failed. Check your credentials.");
      console.error(err);
    }
  };

  // 📄 Upload document
  const uploadFile = async () => {
    if (!file) return alert("Pick a file first!");
    const fd = new FormData();
    fd.append("file", file);

    try {
      const res = await axios.post("/api/upload", fd, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setFilename(file.name);
      fetchHistory();
      alert("✅ File uploaded successfully!");
    } catch (e) {
      console.error("Upload failed:", e);
      alert("Upload failed — check backend logs.");
    }
  };

  // ❓ Ask question
  const askQuestion = async () => {
    if (!question) return alert("Enter a question");

    try {
      const res = await axios.post("/api/answer", { question });
      setAnswer(res.data.answer);
      fetchHistory();
    } catch (e) {
      console.error("Ask failed:", e);
      alert("Failed to get answer");
    }
  };

  // 🎧 Generate Audio
  const generateAudio = async () => {
    try {
      const res = await axios.post(
        "/api/audiobook",
        { lang_code: selectedLang },
        { responseType: "blob" }
      );
      const blob = new Blob([res.data], { type: "audio/mpeg" });
      const url = window.URL.createObjectURL(blob);
      setAudioUrl(url);
      alert("🎧 Audio generated successfully!");
    } catch (error) {
      console.error("Audio generation failed:", error);
      alert("Audio generation failed — check backend logs.");
    }
  };

  // Logout
  const handleLogout = () => {
    localStorage.removeItem("auth_token");
    setIsLoggedIn(false);
    setShowLogin(true);
    setQaHistory([]);
    setAudioUrl(null);
    setAnswer("");
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#0f0c29] via-[#302b63] to-[#24243e] text-white">
      {/* Navbar */}
      <nav className="flex justify-between items-center px-8 py-4">
        <h1 className="text-xl font-bold text-pink-400">AssistifyAI</h1>
        <div className="flex items-center space-x-4">
          {!isLoggedIn ? (
            <button
              onClick={() => setShowLogin(true)}
              className="ripple-btn relative px-5 py-2 rounded-lg border border-pink-400 text-pink-300 font-medium transition-all duration-300 hover:bg-pink-500 hover:text-white hover:shadow-[0_0_20px_rgba(236,72,153,0.7)]"
            >
              Login
            </button>
          ) : (
            <button
              onClick={handleLogout}
              className="ripple-btn px-5 py-2 bg-red-500 rounded-lg font-medium"
            >
              Logout
            </button>
          )}
        </div>
      </nav>

      {/* Hero Section */}
      <section className="text-center py-16">
        <h2 className="text-4xl md:text-5xl font-bold">
          Transform Documents with <span className="text-pink-400">AI Assistant</span>
        </h2>
        <p className="mt-4 text-lg text-gray-300">
          Upload any document to get instant answers via advanced RAG technology <br />
          or convert it into a high-quality audiobook
        </p>
      </section>

      {/* Main Content */}
      {isLoggedIn ? (
        <div className="max-w-5xl mx-auto px-4 grid gap-12">
          {/* Upload Box */}
          <div
            className="reflection-card bg-[#10172a] p-6 rounded-2xl shadow-lg transform transition-all duration-300 hover:scale-105"
            onDragOver={(e) => {
              e.preventDefault();
              setDragOver(true);
            }}
            onDragLeave={() => setDragOver(false)}
            onDrop={(e) => {
              e.preventDefault();
              setDragOver(false);
              if (e.dataTransfer.files.length > 0) {
                setFile(e.dataTransfer.files[0]);
              }
            }}
          >
            <h3 className="text-lg font-semibold mb-2">📄 Upload Document</h3>
            <div
              className={`border-2 border-dashed rounded-lg p-6 text-center cursor-pointer ${
                dragOver ? "border-pink-400 bg-pink-400/10" : "border-gray-600 bg-[#1e293b]"
              }`}
              onClick={() => document.getElementById("fileInput").click()}
            >
              {file ? (
                <p className="text-green-300">{file.name}</p>
              ) : (
                <p className="text-gray-300">Drag & Drop here or Click to Select</p>
              )}
            </div>
            <input
              id="fileInput"
              type="file"
              className="hidden"
              onChange={(e) => setFile(e.target.files[0])}
            />
            <button
              onClick={uploadFile}
              className="ripple-btn mt-4 w-full py-2 bg-gradient-to-r from-purple-500 to-pink-500 rounded-lg transform hover:scale-95 transition-all"
            >
              Upload
            </button>
            {filename && <p className="mt-2 text-sm text-gray-400">Uploaded: {filename}</p>}
          </div>

          {/* Ask + Audio */}
          <div className="grid md:grid-cols-2 gap-12">
            {/* Ask */}
            <div className="reflection-card bg-[#10172a] p-6 rounded-2xl shadow-lg transform transition-all duration-300 hover:scale-105">
              <h3 className="text-lg font-semibold mb-2">💬 Ask Questions By RAG Model</h3>
              <input
                type="text"
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                placeholder="e.g. What is this document about?"
                className="w-full border border-gray-600 rounded-lg p-2 bg-[#1e293b] text-gray-200"
              />
              <button
                onClick={askQuestion}
                className="ripple-btn mt-4 w-full py-2 bg-gradient-to-r from-purple-500 to-pink-500 rounded-lg transform hover:scale-95 transition-all"
              >
                Get Answer
              </button>
              {answer && (
                <p className="mt-4 text-gray-300">
                  <b>Answer:</b> {answer}
                </p>
              )}
            </div>

            {/* Audio */}
            <div className="reflection-card bg-[#10172a] p-6 rounded-2xl shadow-lg transform transition-all duration-300 hover:scale-105">
              <h3 className="text-lg font-semibold mb-2">🎧 Generate Audiobook</h3>
              <select
                value={selectedLang}
                onChange={(e) => setSelectedLang(e.target.value)}
                className="w-full border border-gray-600 rounded-lg p-2 bg-[#1e293b] text-gray-200"
              >
                {Object.entries(langs).map(([code, name]) => (
                  <option key={code} value={code}>
                    {name} ({code})
                  </option>
                ))}
              </select>
              <button
                onClick={generateAudio}
                className="ripple-btn mt-4 w-full py-2 bg-gradient-to-r from-purple-500 to-pink-500 rounded-lg transform hover:scale-95 transition-all"
              >
                Generate Audio
              </button>
              {audioUrl && (
                <div className="mt-4">
                  <audio controls src={audioUrl} className="w-full" />
                </div>
              )}
            </div>
          </div>

          {/* Q&A History */}
          <div className="reflection-card bg-[#10172a] p-6 rounded-2xl shadow-lg transform transition-all duration-300 hover:scale-105">
            <h3 className="text-lg font-semibold mb-4">📜 Q&A History</h3>
            {qaHistory.length === 0 && <p className="text-gray-400">No Q&A yet</p>}
            <div className="space-y-3">
              {qaHistory.map(([q, a], idx) => (
                <div key={idx} className="p-3 rounded-lg bg-[#1e293b]">
                  <p className="text-purple-300"><b>Q:</b> {q}</p>
                  <p className="text-pink-300 mt-1"><b>A:</b> {a}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      ) : (
        <p className="text-center text-gray-400 text-lg mt-12">🔒 Please log in to use AssistifyAI</p>
      )}

      {/* Login Modal */}
      {showLogin && (
        <div className="fixed inset-0 bg-black bg-opacity-70 flex items-center justify-center z-50 animate-fadeIn">
          <div className="bg-[#10172a] p-8 rounded-2xl shadow-2xl w-96 relative reflection-card">
            <h2 className="text-2xl font-bold text-center text-pink-400 mb-6">Login</h2>
            <input
              type="text"
              placeholder="Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="w-full mb-4 p-3 rounded-lg bg-[#1e293b] border border-gray-600 text-white"
            />
            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full mb-4 p-3 rounded-lg bg-[#1e293b] border border-gray-600 text-white"
            />
            <button
              onClick={handleLogin}
              className="ripple-btn w-full py-2 bg-gradient-to-r from-pink-500 to-purple-600 rounded-lg font-medium"
            >
              Login
            </button>
            <button
              onClick={() => setShowLogin(false)}
              className="absolute top-3 right-3 text-gray-400 hover:text-white"
            >
              ✕
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;


// import React, { useState, useEffect } from "react";
// import axios from "axios";
// import "./reflection.css"; // reflections + ripple

// // ✅ Axios instance with token injection
// const axiosAuth = axios.create();
// axiosAuth.interceptors.request.use((config) => {
//   const token = localStorage.getItem("auth_token");
//   if (token) config.headers["token"] = token;
//   return config;
// });

// function App() {
//   const [file, setFile] = useState(null);
//   const [filename, setFilename] = useState(null);
//   const [question, setQuestion] = useState("");
//   const [answer, setAnswer] = useState("");
//   const [qaHistory, setQaHistory] = useState([]);
//   const [langs, setLangs] = useState({});
//   const [selectedLang, setSelectedLang] = useState("en");
//   const [audioUrl, setAudioUrl] = useState(null);
//   const [dragOver, setDragOver] = useState(false);

//   // login states
//   const [showLogin, setShowLogin] = useState(true);
//   const [isLoggedIn, setIsLoggedIn] = useState(false);

//   const [username, setUsername] = useState("");
//   const [password, setPassword] = useState("");

//   // load langs & history after login
//   useEffect(() => {
//     if (isLoggedIn) {
//       fetchLangs();
//       fetchHistory();
//     }
//     // eslint-disable-next-line react-hooks/exhaustive-deps
//   }, [isLoggedIn]);

//   const fetchLangs = async () => {
//     try {
//       const res = await axios.get("/api/langs");
//       setLangs(res.data.langs || {});
//     } catch (e) {
//       console.error(e);
//     }
//   };

//   const fetchHistory = async () => {
//     try {
//       const res = await axiosAuth.get("/api/qa-history");
//       setQaHistory(res.data.qa_pairs || []);
//     } catch (e) {
//       console.error(e);
//     }
//   };

//   const uploadFile = async () => {
//     if (!file) return alert("Pick a file");
//     const fd = new FormData();
//     fd.append("file", file);
//     await axiosAuth.post("/api/upload", fd, {
//       headers: { "Content-Type": "multipart/form-data" },
//     });
//     setFilename(file.name);
//     fetchHistory();
//   };

//   const askQuestion = async () => {
//     if (!question) return alert("Enter a question");
//     const res = await axiosAuth.post("/api/answer", { question });
//     setAnswer(res.data.answer);
//     fetchHistory();
//   };

//   const generateAudio = async () => {
//     try {
//       const res = await axios.post(
//         "/api/audiobook",
//         { lang_code: selectedLang },
//         {
//           responseType: "blob", // 👈 important: receive binary
//         }
//       );

//       // Create a blob and URL
//       const blob = new Blob([res.data], { type: "audio/mpeg" });
//       const url = window.URL.createObjectURL(blob);
//       setAudioUrl(url);

//       // Optional: auto-play when ready
//       const audio = new Audio(url);
//       audio.play();
//     } catch (error) {
//       console.error("Audio generation failed:", error);
//       alert("Failed to generate audiobook.");
//     }
//   };


//   // login handler
//   const handleLogin = async () => {
//     if (!username || !password) {
//       alert("Please enter username & password");
//       return;
//     }
//     try {
//       const res = await axios.post("/api/login", { username, password });
//       if (res.data.token) {
//         localStorage.setItem("auth_token", res.data.token);
//         setIsLoggedIn(true);
//         setShowLogin(false);
//       }
//     } catch {
//       alert("Invalid credentials");
//     }
//   };

//   return (
//     <div className="min-h-screen bg-gradient-to-br from-[#0f0c29] via-[#302b63] to-[#24243e] text-white">
//       {/* Navbar */}
//       <nav className="flex justify-between items-center px-8 py-4">
//         <h1 className="text-xl font-bold text-pink-400">AssistifyAI</h1>
//         <div className="flex items-center space-x-4">
//           {!isLoggedIn ? (
//             <button
//               onClick={() => setShowLogin(true)}
//               className="ripple-btn relative px-5 py-2 rounded-lg border border-pink-400 text-pink-300 font-medium transition-all duration-300 hover:bg-pink-500 hover:text-white hover:shadow-[0_0_20px_rgba(236,72,153,0.7)]"
//             >
//               Login
//             </button>
//           ) : (
//             <button
//               onClick={() => {
//                 localStorage.removeItem("auth_token");
//                 setIsLoggedIn(false);
//                 setShowLogin(true);
//               }}
//               className="ripple-btn px-5 py-2 bg-red-500 rounded-lg font-medium"
//             >
//               Logout
//             </button>
//           )}

//           <button className="ripple-btn px-5 py-2 bg-gradient-to-r from-pink-500 to-purple-600 rounded-lg font-medium shadow-md transform hover:scale-95 transition-all">
//             Get Started
//           </button>
//         </div>
//       </nav>

//       {/* Hero Section */}
//       <section className="text-center py-16">
//         <h2 className="text-4xl md:text-5xl font-bold">
//           Transform Documents with <span className="text-pink-400">AI Assistant</span>
//         </h2>
//         <p className="mt-4 text-lg text-gray-300">
//           Upload any document to get instant answers via advanced RAG technology <br />
//           or convert it into a high-quality audiobook
//         </p>
//       </section>

//       {/* Main Content (locked until login) */}
//       {isLoggedIn ? (
//         <div className="max-w-5xl mx-auto px-4 grid gap-12">
//           {/* Upload Box */}
//           <div
//             className="reflection-card bg-[#10172a] p-6 rounded-2xl shadow-lg transform transition-all duration-300 hover:scale-105"
//             onDragOver={(e) => {
//               e.preventDefault();
//               setDragOver(true);
//             }}
//             onDragLeave={() => setDragOver(false)}
//             onDrop={(e) => {
//               e.preventDefault();
//               setDragOver(false);
//               if (e.dataTransfer.files.length > 0) {
//                 setFile(e.dataTransfer.files[0]);
//               }
//             }}
//           >
//             <h3 className="text-lg font-semibold mb-2">📄 Upload Document</h3>
//             <div
//               className={`border-2 border-dashed rounded-lg p-6 text-center cursor-pointer ${dragOver
//                   ? "border-pink-400 bg-pink-400/10"
//                   : "border-gray-600 bg-[#1e293b]"
//                 }`}
//               onClick={() => document.getElementById("fileInput").click()}
//             >
//               {file ? (
//                 <p className="text-green-300">{file.name}</p>
//               ) : (
//                 <p className="text-gray-300">Drag & Drop here or Click to Select</p>
//               )}
//             </div>
//             <input
//               id="fileInput"
//               type="file"
//               className="hidden"
//               onChange={(e) => setFile(e.target.files[0])}
//             />
//             <button
//               onClick={uploadFile}
//               className="ripple-btn mt-4 w-full py-2 bg-gradient-to-r from-purple-500 to-pink-500 rounded-lg transform hover:scale-95 transition-all"
//             >
//               Upload
//             </button>
//             {filename && (
//               <p className="mt-2 text-sm text-gray-400">Uploaded: {filename}</p>
//             )}
//           </div>

//           {/* Ask + Audio */}
//           <div className="grid md:grid-cols-2 gap-12">
//             <div className="reflection-card bg-[#10172a] p-6 rounded-2xl shadow-lg transform transition-all duration-300 hover:scale-105">
//               <h3 className="text-lg font-semibold mb-2">💬 Ask Questions</h3>
//               <input
//                 type="text"
//                 value={question}
//                 onChange={(e) => setQuestion(e.target.value)}
//                 placeholder="e.g. What is this document about?"
//                 className="w-full border border-gray-600 rounded-lg p-2 bg-[#1e293b] text-gray-200"
//               />
//               <button
//                 onClick={askQuestion}
//                 className="ripple-btn mt-4 w-full py-2 bg-gradient-to-r from-purple-500 to-pink-500 rounded-lg transform hover:scale-95 transition-all"
//               >
//                 Get Answer
//               </button>
//               {answer && (
//                 <p className="mt-4 text-gray-300">
//                   <b>Answer:</b> {answer}
//                 </p>
//               )}
//             </div>

//             <div className="reflection-card bg-[#10172a] p-6 rounded-2xl shadow-lg transform transition-all duration-300 hover:scale-105">
//               <h3 className="text-lg font-semibold mb-2">🎧 Generate Audiobook</h3>
//               <select
//                 value={selectedLang}
//                 onChange={(e) => setSelectedLang(e.target.value)}
//                 className="w-full border border-gray-600 rounded-lg p-2 bg-[#1e293b] text-gray-200"
//               >
//                 {Object.entries(langs).map(([code, name]) => (
//                   <option key={code} value={code}>
//                     {name} ({code})
//                   </option>
//                 ))}
//               </select>
//               <button
//                 onClick={generateAudio}
//                 className="ripple-btn mt-4 w-full py-2 bg-gradient-to-r from-purple-500 to-pink-500 rounded-lg transform hover:scale-95 transition-all"
//               >
//                 Generate Audio
//               </button>
//               {audioUrl && (
//                 <div className="mt-4">
//                   <audio controls src={audioUrl} className="w-full" />
//                 </div>
//               )}
//             </div>
//           </div>

//           {/* Q&A History */}
//           <div className="reflection-card bg-[#10172a] p-6 rounded-2xl shadow-lg transform transition-all duration-300 hover:scale-105">
//             <h3 className="text-lg font-semibold mb-4">📜 Q&A History</h3>
//             {qaHistory.length === 0 && <p className="text-gray-400">No Q&A yet</p>}
//             <div className="space-y-3">
//               {qaHistory.map(([q, a], idx) => (
//                 <div key={idx} className="p-3 rounded-lg bg-[#1e293b]">
//                   <p className="text-purple-300">
//                     <b>Q:</b> {q}
//                   </p>
//                   <p className="text-pink-300 mt-1">
//                     <b>A:</b> {a}
//                   </p>
//                 </div>
//               ))}
//             </div>
//           </div>
//         </div>
//       ) : (
//         <p className="text-center text-gray-400 text-lg mt-12">
//           🔒 Please log in to use AssistifyAI
//         </p>
//       )}

//       {/* Login Modal */}
//       {showLogin && (
//         <div className="fixed inset-0 bg-black bg-opacity-70 flex items-center justify-center z-50 animate-fadeIn">
//           <div className="bg-[#10172a] p-8 rounded-2xl shadow-2xl w-96 relative reflection-card">
//             <h2 className="text-2xl font-bold text-center text-pink-400 mb-6">
//               Login
//             </h2>
//             <input
//               type="text"
//               placeholder="Username"
//               value={username}
//               onChange={(e) => setUsername(e.target.value)}
//               className="w-full mb-4 p-3 rounded-lg bg-[#1e293b] border border-gray-600 text-white"
//             />
//             <input
//               type="password"
//               placeholder="Password"
//               value={password}
//               onChange={(e) => setPassword(e.target.value)}
//               className="w-full mb-4 p-3 rounded-lg bg-[#1e293b] border border-gray-600 text-white"
//             />
//             <button
//               onClick={handleLogin}
//               className="ripple-btn w-full py-2 bg-gradient-to-r from-pink-500 to-purple-600 rounded-lg font-medium"
//             >
//               Login
//             </button>
//             <button
//               onClick={() => setShowLogin(false)}
//               className="absolute top-3 right-3 text-gray-400 hover:text-white"
//             >
//               ✕
//             </button>
//           </div>
//         </div>
//       )}
//     </div>
//   );
// }

// export default App;


// import React, { useState, useEffect } from "react";
// import axios from "axios";
// import "./reflection.css"; // reflections + ripple

// function App() {
//   const [file, setFile] = useState(null);
//   const [filename, setFilename] = useState(null);
//   const [question, setQuestion] = useState("");
//   const [answer, setAnswer] = useState("");
//   const [qaHistory, setQaHistory] = useState([]);
//   const [langs, setLangs] = useState({});
//   const [selectedLang, setSelectedLang] = useState("en");
//   const [audioUrl, setAudioUrl] = useState(null);
//   const [dragOver, setDragOver] = useState(false);

//   // login states
//   const [showLogin, setShowLogin] = useState(true); // 👈 force login modal on start
//   const [isLoggedIn, setIsLoggedIn] = useState(false);

//   // dummy login creds (can replace with backend auth)
//   const [username, setUsername] = useState("");
//   const [password, setPassword] = useState("");

//   useEffect(() => {
//     if (isLoggedIn) {
//       fetchLangs();
//       fetchHistory();
//     }
//   }, [isLoggedIn]);

//   const fetchLangs = async () => {
//     try {
//       const res = await axios.get("/api/langs");
//       setLangs(res.data.langs || {});
//     } catch (e) {
//       console.error(e);
//     }
//   };

//   const fetchHistory = async () => {
//     try {
//       const res = await axios.get("/api/qa-history");
//       setQaHistory(res.data.qa_pairs || []);
//     } catch (e) {
//       console.error(e);
//     }
//   };

//   const uploadFile = async () => {
//     if (!file) return alert("Pick a file");
//     const fd = new FormData();
//     fd.append("file", file);
//     await axios.post("/api/upload", fd, { headers: { "Content-Type": "multipart/form-data" } });
//     setFilename(file.name);
//     fetchHistory();
//   };

//   const askQuestion = async () => {
//     if (!question) return alert("Enter a question");
//     const res = await axios.post("/api/answer", { question });
//     setAnswer(res.data.answer);
//     fetchHistory();
//   };

//   const generateAudio = async () => {
//     const res = await axios.post("/api/audiobook", { lang_code: selectedLang }, { responseType: "blob" });
//     const blob = new Blob([res.data], { type: "audio/mpeg" });
//     setAudioUrl(URL.createObjectURL(blob));
//   };

//   // handle login
//   const handleLogin = () => {
//     if (!username || !password) {
//       alert("Please enter username & password");
//       return;
//     }
//     // 👉 replace with API call to your backend login
//     if (username === "admin" && password === "1234") {
//       setIsLoggedIn(true);
//       setShowLogin(false);
//     } else {
//       alert("Invalid credentials");
//     }
//   };

//   return (
//     <div className="min-h-screen bg-gradient-to-br from-[#0f0c29] via-[#302b63] to-[#24243e] text-white">
//       {/* Navbar */}
//       <nav className="flex justify-between items-center px-8 py-4">
//         <h1 className="text-xl font-bold text-pink-400">AssistifyAI</h1>
//         <div className="flex items-center space-x-4">
//           {!isLoggedIn ? (
//             <button
//               onClick={() => setShowLogin(true)}
//               className="ripple-btn relative px-5 py-2 rounded-lg border border-pink-400 text-pink-300 font-medium transition-all duration-300 hover:bg-pink-500 hover:text-white hover:shadow-[0_0_20px_rgba(236,72,153,0.7)]"
//             >
//               Login
//             </button>
//           ) : (
//             <button
//               onClick={() => {
//                 setIsLoggedIn(false);
//                 setShowLogin(true);
//               }}
//               className="ripple-btn px-5 py-2 bg-red-500 rounded-lg font-medium"
//             >
//               Logout
//             </button>
//           )}

//           <button className="ripple-btn px-5 py-2 bg-gradient-to-r from-pink-500 to-purple-600 rounded-lg font-medium shadow-md transform hover:scale-95 transition-all">
//             Get Started
//           </button>
//         </div>
//       </nav>

//       {/* Hero Section */}
//       <section className="text-center py-16">
//         <h2 className="text-4xl md:text-5xl font-bold">
//           Transform Documents with <span className="text-pink-400">AI Assistant</span>
//         </h2>
//         <p className="mt-4 text-lg text-gray-300">
//           Upload any document to get instant answers via advanced RAG technology <br />
//           or convert it into a high-quality audiobook
//         </p>
//       </section>

//       {/* Main Content (locked until login) */}
//       {isLoggedIn ? (
//         <div className="max-w-5xl mx-auto px-4 grid gap-12">
//           {/* Upload Box */}
//           <div
//             className="reflection-card bg-[#10172a] p-6 rounded-2xl shadow-lg transform transition-all duration-300 hover:scale-105"
//             onDragOver={(e) => {
//               e.preventDefault();
//               setDragOver(true);
//             }}
//             onDragLeave={() => setDragOver(false)}
//             onDrop={(e) => {
//               e.preventDefault();
//               setDragOver(false);
//               if (e.dataTransfer.files.length > 0) {
//                 setFile(e.dataTransfer.files[0]);
//               }
//             }}
//           >
//             <h3 className="text-lg font-semibold mb-2">📄 Upload Document</h3>
//             <div
//               className={`border-2 border-dashed rounded-lg p-6 text-center cursor-pointer ${
//                 dragOver ? "border-pink-400 bg-pink-400/10" : "border-gray-600 bg-[#1e293b]"
//               }`}
//               onClick={() => document.getElementById("fileInput").click()}
//             >
//               {file ? (
//                 <p className="text-green-300">{file.name}</p>
//               ) : (
//                 <p className="text-gray-300">Drag & Drop here or Click to Select</p>
//               )}
//             </div>
//             <input
//               id="fileInput"
//               type="file"
//               className="hidden"
//               onChange={(e) => setFile(e.target.files[0])}
//             />
//             <button
//               onClick={uploadFile}
//               className="ripple-btn mt-4 w-full py-2 bg-gradient-to-r from-purple-500 to-pink-500 rounded-lg transform hover:scale-95 transition-all"
//             >
//               Upload
//             </button>
//             {filename && <p className="mt-2 text-sm text-gray-400">Uploaded: {filename}</p>}
//           </div>

//           {/* Ask + Audio */}
//           <div className="grid md:grid-cols-2 gap-12">
//             <div className="reflection-card bg-[#10172a] p-6 rounded-2xl shadow-lg transform transition-all duration-300 hover:scale-105">
//               <h3 className="text-lg font-semibold mb-2">💬 Ask Questions</h3>
//               <input
//                 type="text"
//                 value={question}
//                 onChange={(e) => setQuestion(e.target.value)}
//                 placeholder="e.g. What is this document about?"
//                 className="w-full border border-gray-600 rounded-lg p-2 bg-[#1e293b] text-gray-200"
//               />
//               <button
//                 onClick={askQuestion}
//                 className="ripple-btn mt-4 w-full py-2 bg-gradient-to-r from-purple-500 to-pink-500 rounded-lg transform hover:scale-95 transition-all"
//               >
//                 Get Answer
//               </button>
//               {answer && (
//                 <p className="mt-4 text-gray-300">
//                   <b>Answer:</b> {answer}
//                 </p>
//               )}
//             </div>

//             <div className="reflection-card bg-[#10172a] p-6 rounded-2xl shadow-lg transform transition-all duration-300 hover:scale-105">
//               <h3 className="text-lg font-semibold mb-2">🎧 Generate Audiobook</h3>
//               <select
//                 value={selectedLang}
//                 onChange={(e) => setSelectedLang(e.target.value)}
//                 className="w-full border border-gray-600 rounded-lg p-2 bg-[#1e293b] text-gray-200"
//               >
//                 {Object.entries(langs).map(([code, name]) => (
//                   <option key={code} value={code}>
//                     {name} ({code})
//                   </option>
//                 ))}
//               </select>
//               <button
//                 onClick={generateAudio}
//                 className="ripple-btn mt-4 w-full py-2 bg-gradient-to-r from-purple-500 to-pink-500 rounded-lg transform hover:scale-95 transition-all"
//               >
//                 Generate Audio
//               </button>
//               {audioUrl && (
//                 <div className="mt-4">
//                   <audio controls src={audioUrl} className="w-full" />
//                 </div>
//               )}
//             </div>
//           </div>

//           {/* Q&A History */}
//           <div className="reflection-card bg-[#10172a] p-6 rounded-2xl shadow-lg transform transition-all duration-300 hover:scale-105">
//             <h3 className="text-lg font-semibold mb-4">📜 Q&A History</h3>
//             {qaHistory.length === 0 && <p className="text-gray-400">No Q&A yet</p>}
//             <div className="space-y-3">
//               {qaHistory.map(([q, a], idx) => (
//                 <div key={idx} className="p-3 rounded-lg bg-[#1e293b]">
//                   <p className="text-purple-300"><b>Q:</b> {q}</p>
//                   <p className="text-pink-300 mt-1"><b>A:</b> {a}</p>
//                 </div>
//               ))}
//             </div>
//           </div>
//         </div>
//       ) : (
//         <p className="text-center text-gray-400 text-lg mt-12">🔒 Please log in to use AssistifyAI</p>
//       )}

//       {/* Login Modal */}
//       {showLogin && (
//         <div className="fixed inset-0 bg-black bg-opacity-70 flex items-center justify-center z-50 animate-fadeIn">
//           <div className="bg-[#10172a] p-8 rounded-2xl shadow-2xl w-96 relative reflection-card">
//             <h2 className="text-2xl font-bold text-center text-pink-400 mb-6">Login</h2>
//             <input
//               type="text"
//               placeholder="Username"
//               value={username}
//               onChange={(e) => setUsername(e.target.value)}
//               className="w-full mb-4 p-3 rounded-lg bg-[#1e293b] border border-gray-600 text-white"
//             />
//             <input
//               type="password"
//               placeholder="Password"
//               value={password}
//               onChange={(e) => setPassword(e.target.value)}
//               className="w-full mb-4 p-3 rounded-lg bg-[#1e293b] border border-gray-600 text-white"
//             />
//             <button
//               onClick={handleLogin}
//               className="ripple-btn w-full py-2 bg-gradient-to-r from-pink-500 to-purple-600 rounded-lg font-medium"
//             >
//               Login
//             </button>
//             <button
//               onClick={() => setShowLogin(false)}
//               className="absolute top-3 right-3 text-gray-400 hover:text-white"
//             >
//               ✕
//             </button>
//           </div>
//         </div>
//       )}
//     </div>
//   );
// }

// export default App;



// import React, { useState, useEffect } from "react";
// import axios from "axios";
// import "./reflection.css"; // 👈 for reflection + ripple

// function App() {
//   const [file, setFile] = useState(null);
//   const [filename, setFilename] = useState(null);
//   const [question, setQuestion] = useState("");
//   const [answer, setAnswer] = useState("");
//   const [qaHistory, setQaHistory] = useState([]);
//   const [langs, setLangs] = useState({});
//   const [selectedLang, setSelectedLang] = useState("en");
//   const [audioUrl, setAudioUrl] = useState(null);
//   const [dragOver, setDragOver] = useState(false);

//   useEffect(() => {
//     fetchLangs();
//     fetchHistory();
//   }, []);

//   const fetchLangs = async () => {
//     try {
//       const res = await axios.get("/api/langs");
//       setLangs(res.data.langs || {});
//     } catch (e) {
//       console.error(e);
//     }
//   };

//   const fetchHistory = async () => {
//     try {
//       const res = await axios.get("/api/qa-history");
//       setQaHistory(res.data.qa_pairs || []);
//     } catch (e) {
//       console.error(e);
//     }
//   };

//   const uploadFile = async () => {
//     if (!file) return alert("Pick a file");
//     const fd = new FormData();
//     fd.append("file", file);
//     await axios.post("/api/upload", fd, { headers: { "Content-Type": "multipart/form-data" } });
//     setFilename(file.name);
//     fetchHistory();
//   };

//   const askQuestion = async () => {
//     if (!question) return alert("Enter a question");
//     const res = await axios.post("/api/answer", { question });
//     setAnswer(res.data.answer);
//     fetchHistory();
//   };

//   const generateAudio = async () => {
//     const res = await axios.post("/api/audiobook", { lang_code: selectedLang }, { responseType: "blob" });
//     const blob = new Blob([res.data], { type: "audio/mpeg" });
//     setAudioUrl(URL.createObjectURL(blob));
//   };

//   return (
//     <div className="min-h-screen bg-gradient-to-br from-[#0f0c29] via-[#302b63] to-[#24243e] text-white">

//       {/* Navbar */}
//       <nav className="flex justify-between items-center px-8 py-4">
//         <h1 className="text-xl font-bold text-pink-400">AssistifyAI</h1>
//         <div className="flex items-center space-x-4">
//           {/* Login Button */}
//           <button className="ripple-btn relative px-5 py-2 rounded-lg border border-pink-400 text-pink-300 font-medium transition-all duration-300 hover:bg-pink-500 hover:text-white hover:shadow-[0_0_20px_rgba(236,72,153,0.7)]">
//             Login
//           </button>

//           {/* Get Started Button */}
//           <button className="ripple-btn px-5 py-2 bg-gradient-to-r from-pink-500 to-purple-600 rounded-lg font-medium shadow-md transform hover:scale-95 transition-all">
//             Get Started
//           </button>
//         </div>
//       </nav>


//       {/* Hero Section */}
//       <section className="text-center py-16">
//         <h2 className="text-4xl md:text-5xl font-bold">
//           Transform Documents with <span className="text-pink-400">AI Assistant</span>
//         </h2>
//         <p className="mt-4 text-lg text-gray-300">
//           Upload any document to get instant answers via advanced RAG technology <br />
//           or convert it into a high-quality audiobook
//         </p>
//       </section>

//       {/* Main Content */}
//       <div className="max-w-5xl mx-auto px-4 grid gap-12">
//         {/* Upload Box */}
//         <div
//           className="reflection-card bg-[#10172a] p-6 rounded-2xl shadow-lg transform transition-all duration-300 hover:scale-105"
//           onDragOver={(e) => {
//             e.preventDefault();
//             setDragOver(true);
//           }}
//           onDragLeave={() => setDragOver(false)}
//           onDrop={(e) => {
//             e.preventDefault();
//             setDragOver(false);
//             if (e.dataTransfer.files.length > 0) {
//               setFile(e.dataTransfer.files[0]);
//             }
//           }}
//         >
//           <h3 className="text-lg font-semibold mb-2">📄 Upload Document</h3>
//           <div
//             className={`border-2 border-dashed rounded-lg p-6 text-center cursor-pointer ${dragOver ? "border-pink-400 bg-pink-400/10" : "border-gray-600 bg-[#1e293b]"
//               }`}
//             onClick={() => document.getElementById("fileInput").click()}
//           >
//             {file ? (
//               <p className="text-green-300">{file.name}</p>
//             ) : (
//               <p className="text-gray-300">Drag & Drop here or Click to Select</p>
//             )}
//           </div>
//           <input
//             id="fileInput"
//             type="file"
//             className="hidden"
//             onChange={(e) => setFile(e.target.files[0])}
//           />
//           <button
//             onClick={uploadFile}
//             className="ripple-btn mt-4 w-full py-2 bg-gradient-to-r from-purple-500 to-pink-500 rounded-lg transform hover:scale-95 transition-all"
//           >
//             Upload
//           </button>
//           {filename && <p className="mt-2 text-sm text-gray-400">Uploaded: {filename}</p>}
//         </div>

//         {/* Ask + Audio */}
//         <div className="grid md:grid-cols-2 gap-12">
//           <div className="reflection-card bg-[#10172a] p-6 rounded-2xl shadow-lg transform transition-all duration-300 hover:scale-105">
//             <h3 className="text-lg font-semibold mb-2">💬 Ask Questions</h3>
//             <input
//               type="text"
//               value={question}
//               onChange={(e) => setQuestion(e.target.value)}
//               placeholder="e.g. What is this document about?"
//               className="w-full border border-gray-600 rounded-lg p-2 bg-[#1e293b] text-gray-200"
//             />
//             <button
//               onClick={askQuestion}
//               className="ripple-btn mt-4 w-full py-2 bg-gradient-to-r from-purple-500 to-pink-500 rounded-lg transform hover:scale-95 transition-all"
//             >
//               Get Answer
//             </button>
//             {answer && (
//               <p className="mt-4 text-gray-300">
//                 <b>Answer:</b> {answer}
//               </p>
//             )}
//           </div>

//           <div className="reflection-card bg-[#10172a] p-6 rounded-2xl shadow-lg transform transition-all duration-300 hover:scale-105">
//             <h3 className="text-lg font-semibold mb-2">🎧 Generate Audiobook</h3>
//             <select
//               value={selectedLang}
//               onChange={(e) => setSelectedLang(e.target.value)}
//               className="w-full border border-gray-600 rounded-lg p-2 bg-[#1e293b] text-gray-200"
//             >
//               {Object.entries(langs).map(([code, name]) => (
//                 <option key={code} value={code}>
//                   {name} ({code})
//                 </option>
//               ))}
//             </select>
//             <button
//               onClick={generateAudio}
//               className="ripple-btn mt-4 w-full py-2 bg-gradient-to-r from-purple-500 to-pink-500 rounded-lg transform hover:scale-95 transition-all"
//             >
//               Generate Audio
//             </button>
//             {audioUrl && (
//               <div className="mt-4">
//                 <audio controls src={audioUrl} className="w-full" />
//               </div>
//             )}
//           </div>
//         </div>

//         {/* Q&A History */}
//         <div className="reflection-card bg-[#10172a] p-6 rounded-2xl shadow-lg transform transition-all duration-300 hover:scale-105">
//           <h3 className="text-lg font-semibold mb-4">📜 Q&A History</h3>
//           {qaHistory.length === 0 && <p className="text-gray-400">No Q&A yet</p>}
//           <div className="space-y-3">
//             {qaHistory.map(([q, a], idx) => (
//               <div key={idx} className="p-3 rounded-lg bg-[#1e293b]">
//                 <p className="text-purple-300"><b>Q:</b> {q}</p>
//                 <p className="text-pink-300 mt-1"><b>A:</b> {a}</p>
//               </div>
//             ))}
//           </div>
//         </div>
//       </div>
//     </div>
//   );
// }

// export default App;



// import React, { useState, useEffect } from "react";
// import axios from "axios";
// import "./reflection.css"; // 👈 custom CSS for reflection

// function App() {
//   const [file, setFile] = useState(null);
//   const [filename, setFilename] = useState(null);
//   const [question, setQuestion] = useState("");
//   const [answer, setAnswer] = useState("");
//   const [qaHistory, setQaHistory] = useState([]);
//   const [langs, setLangs] = useState({});
//   const [selectedLang, setSelectedLang] = useState("en");
//   const [audioUrl, setAudioUrl] = useState(null);
//   const [dragOver, setDragOver] = useState(false);

//   useEffect(() => {
//     fetchLangs();
//     fetchHistory();
//   }, []);

//   const fetchLangs = async () => {
//     try {
//       const res = await axios.get("/api/langs");
//       setLangs(res.data.langs || {});
//     } catch (e) {
//       console.error(e);
//     }
//   };

//   const fetchHistory = async () => {
//     try {
//       const res = await axios.get("/api/qa-history");
//       setQaHistory(res.data.qa_pairs || []);
//     } catch (e) {
//       console.error(e);
//     }
//   };

//   const uploadFile = async () => {
//     if (!file) return alert("Pick a file");
//     const fd = new FormData();
//     fd.append("file", file);
//     await axios.post("/api/upload", fd, { headers: { "Content-Type": "multipart/form-data" } });
//     setFilename(file.name);
//     fetchHistory();
//   };

//   const askQuestion = async () => {
//     if (!question) return alert("Enter a question");
//     const res = await axios.post("/api/answer", { question });
//     setAnswer(res.data.answer);
//     fetchHistory();
//   };

//   const generateAudio = async () => {
//     const res = await axios.post("/api/audiobook", { lang_code: selectedLang }, { responseType: "blob" });
//     const blob = new Blob([res.data], { type: "audio/mpeg" });
//     setAudioUrl(URL.createObjectURL(blob));
//   };

//   return (
//     <div className="min-h-screen bg-gradient-to-br from-[#0f0c29] via-[#302b63] to-[#24243e] text-white">
//       {/* Navbar */}
//       <nav className="flex justify-between items-center px-8 py-4">
//         <h1 className="text-xl font-bold text-pink-400">AssistifyAI</h1>
//         <div>
//           <button className="mr-4 hover:underline">Login</button>
//           <button className="px-4 py-2 bg-gradient-to-r from-pink-500 to-purple-600 rounded-lg transform hover:scale-95 transition-all">
//             Get Started
//           </button>
//         </div>
//       </nav>

//       {/* Hero Section */}
//       <section className="text-center py-16">
//         <h2 className="text-4xl md:text-5xl font-bold">
//           Transform Documents with <span className="text-pink-400">AI Assistant</span>
//         </h2>
//         <p className="mt-4 text-lg text-gray-300">
//           Upload any document to get instant answers via advanced RAG technology <br />
//           or convert it into a high-quality audiobook
//         </p>
//       </section>

//       {/* Main Content */}
//       <div className="max-w-5xl mx-auto px-4 grid gap-12">
//         {/* Upload Box */}
//         <div
//           className="reflection-card bg-[#10172a] p-6 rounded-2xl shadow-lg transform transition-all duration-300 hover:scale-105"
//           onDragOver={(e) => {
//             e.preventDefault();
//             setDragOver(true);
//           }}
//           onDragLeave={() => setDragOver(false)}
//           onDrop={(e) => {
//             e.preventDefault();
//             setDragOver(false);
//             if (e.dataTransfer.files.length > 0) {
//               setFile(e.dataTransfer.files[0]);
//             }
//           }}
//         >
//           <h3 className="text-lg font-semibold mb-2">📄 Upload Document</h3>
//           <div
//             className={`border-2 border-dashed rounded-lg p-6 text-center cursor-pointer ${
//               dragOver ? "border-pink-400 bg-pink-400/10" : "border-gray-600 bg-[#1e293b]"
//             }`}
//             onClick={() => document.getElementById("fileInput").click()}
//           >
//             {file ? (
//               <p className="text-green-300">{file.name}</p>
//             ) : (
//               <p className="text-gray-300">Drag & Drop here or Click to Select</p>
//             )}
//           </div>
//           <input
//             id="fileInput"
//             type="file"
//             className="hidden"
//             onChange={(e) => setFile(e.target.files[0])}
//           />
//           <button
//             onClick={uploadFile}
//             className="mt-4 w-full py-2 bg-gradient-to-r from-purple-500 to-pink-500 rounded-lg transform hover:scale-95 transition-all"
//           >
//             Upload
//           </button>
//           {filename && <p className="mt-2 text-sm text-gray-400">Uploaded: {filename}</p>}
//         </div>

//         {/* Ask + Audio */}
//         <div className="grid md:grid-cols-2 gap-12">
//           <div className="reflection-card bg-[#10172a] p-6 rounded-2xl shadow-lg transform transition-all duration-300 hover:scale-105">
//             <h3 className="text-lg font-semibold mb-2">💬 Ask Questions</h3>
//             <input
//               type="text"
//               value={question}
//               onChange={(e) => setQuestion(e.target.value)}
//               placeholder="e.g. What is this document about?"
//               className="w-full border border-gray-600 rounded-lg p-2 bg-[#1e293b] text-gray-200"
//             />
//             <button
//               onClick={askQuestion}
//               className="mt-4 w-full py-2 bg-gradient-to-r from-purple-500 to-pink-500 rounded-lg transform hover:scale-95 transition-all"
//             >
//               Get Answer
//             </button>
//             {answer && (
//               <p className="mt-4 text-gray-300">
//                 <b>Answer:</b> {answer}
//               </p>
//             )}
//           </div>

//           <div className="reflection-card bg-[#10172a] p-6 rounded-2xl shadow-lg transform transition-all duration-300 hover:scale-105">
//             <h3 className="text-lg font-semibold mb-2">🎧 Generate Audiobook</h3>
//             <select
//               value={selectedLang}
//               onChange={(e) => setSelectedLang(e.target.value)}
//               className="w-full border border-gray-600 rounded-lg p-2 bg-[#1e293b] text-gray-200"
//             >
//               {Object.entries(langs).map(([code, name]) => (
//                 <option key={code} value={code}>
//                   {name} ({code})
//                 </option>
//               ))}
//             </select>
//             <button
//               onClick={generateAudio}
//               className="mt-4 w-full py-2 bg-gradient-to-r from-purple-500 to-pink-500 rounded-lg transform hover:scale-95 transition-all"
//             >
//               Generate Audio
//             </button>
//             {audioUrl && (
//               <div className="mt-4">
//                 <audio controls src={audioUrl} className="w-full" />
//               </div>
//             )}
//           </div>
//         </div>

//         {/* Q&A History */}
//         <div className="reflection-card bg-[#10172a] p-6 rounded-2xl shadow-lg transform transition-all duration-300 hover:scale-105">
//           <h3 className="text-lg font-semibold mb-4">📜 Q&A History</h3>
//           {qaHistory.length === 0 && <p className="text-gray-400">No Q&A yet</p>}
//           <div className="space-y-3">
//             {qaHistory.map(([q, a], idx) => (
//               <div key={idx} className="p-3 rounded-lg bg-[#1e293b]">
//                 <p className="text-purple-300"><b>Q:</b> {q}</p>
//                 <p className="text-pink-300 mt-1"><b>A:</b> {a}</p>
//               </div>
//             ))}
//           </div>
//         </div>
//       </div>
//     </div>
//   );
// }

// export default App;



// import React, { useState, useEffect } from "react";
// import axios from "axios";

// function App() {
//   const [file, setFile] = useState(null);
//   const [filename, setFilename] = useState(null);
//   const [question, setQuestion] = useState("");
//   const [answer, setAnswer] = useState("");
//   const [qaHistory, setQaHistory] = useState([]);
//   const [langs, setLangs] = useState({});
//   const [selectedLang, setSelectedLang] = useState("en");
//   const [audioUrl, setAudioUrl] = useState(null);
//   const [dragOver, setDragOver] = useState(false);

//   useEffect(() => {
//     fetchLangs();
//     fetchHistory();
//   }, []);

//   const fetchLangs = async () => {
//     try {
//       const res = await axios.get("/api/langs");
//       setLangs(res.data.langs || {});
//     } catch (e) {
//       console.error(e);
//     }
//   };

//   const fetchHistory = async () => {
//     try {
//       const res = await axios.get("/api/qa-history");
//       setQaHistory(res.data.qa_pairs || []);
//     } catch (e) {
//       console.error(e);
//     }
//   };

//   const uploadFile = async () => {
//     if (!file) return alert("Pick a file");
//     const fd = new FormData();
//     fd.append("file", file);
//     await axios.post("/api/upload", fd, { headers: { "Content-Type": "multipart/form-data" } });
//     setFilename(file.name);
//     fetchHistory();
//   };

//   const askQuestion = async () => {
//     if (!question) return alert("Enter a question");
//     const res = await axios.post("/api/answer", { question });
//     setAnswer(res.data.answer);
//     fetchHistory();
//   };

//   const generateAudio = async () => {
//     const res = await axios.post("/api/audiobook", { lang_code: selectedLang }, { responseType: "blob" });
//     const blob = new Blob([res.data], { type: "audio/mpeg" });
//     setAudioUrl(URL.createObjectURL(blob));
//   };

//   return (
//     <div className="min-h-screen bg-gradient-to-br from-[#0f0c29] via-[#302b63] to-[#24243e] text-white transition-all duration-300 hover:shadow-[0_0_50px_rgba(255,255,255,0.2)]">
//       {/* Navbar */}
//       <nav className="flex justify-between items-center px-8 py-4">
//         <h1 className="text-xl font-bold text-pink-400">AssistifyAI</h1>
//         <div>
//           <button className="mr-4 hover:underline">Login</button>
//           <button className="px-4 py-2 bg-gradient-to-r from-pink-500 to-purple-600 rounded-lg transform hover:scale-95 transition-all">
//             Get Started
//           </button>
//         </div>
//       </nav>

//       {/* Hero Section */}
//       <section className="text-center py-16">
//         <h2 className="text-4xl md:text-5xl font-bold">
//           Transform Documents with <span className="text-pink-400">AI Assistant</span>
//         </h2>
//         <p className="mt-4 text-lg text-gray-300">
//           Upload any document to get instant answers via advanced RAG technology <br />
//           or convert it into a high-quality audiobook
//         </p>
//       </section>

//       {/* Main Content */}
//       <div className="max-w-5xl mx-auto px-4 grid gap-6">
//         {/* Upload Box with Drag and Drop */}
//         <div
//           className={`bg-[#10172a] p-6 rounded-2xl shadow-lg transform transition-all duration-300 hover:scale-105 hover:shadow-[0_0_30px_rgba(255,255,255,0.3)]`}
//           onDragOver={(e) => {
//             e.preventDefault();
//             setDragOver(true);
//           }}
//           onDragLeave={() => setDragOver(false)}
//           onDrop={(e) => {
//             e.preventDefault();
//             setDragOver(false);
//             if (e.dataTransfer.files.length > 0) {
//               setFile(e.dataTransfer.files[0]);
//             }
//           }}
//         >
//           <h3 className="text-lg font-semibold mb-2">📄 Upload Document</h3>
//           <div
//             className={`border-2 border-dashed rounded-lg p-6 text-center cursor-pointer ${
//               dragOver ? "border-pink-400 bg-pink-400/10" : "border-gray-600 bg-[#1e293b]"
//             }`}
//             onClick={() => document.getElementById("fileInput").click()}
//           >
//             {file ? (
//               <p className="text-green-300">{file.name}</p>
//             ) : (
//               <p className="text-gray-300">Drag & Drop here or Click to Select</p>
//             )}
//           </div>
//           <input
//             id="fileInput"
//             type="file"
//             className="hidden"
//             onChange={(e) => setFile(e.target.files[0])}
//           />
//           <button
//             onClick={uploadFile}
//             className="mt-4 w-full py-2 bg-gradient-to-r from-purple-500 to-pink-500 rounded-lg transform hover:scale-95 transition-all"
//           >
//             Upload
//           </button>
//           {filename && <p className="mt-2 text-sm text-gray-400">Uploaded: {filename}</p>}
//         </div>

//         {/* Ask + Audio */}
//         <div className="grid md:grid-cols-2 gap-6">
//           {/* Ask Questions */}
//           <div className="bg-[#10172a] p-6 rounded-2xl shadow-lg transform transition-all duration-300 hover:scale-105 hover:shadow-[0_0_30px_rgba(255,255,255,0.3)]">
//             <h3 className="text-lg font-semibold mb-2">💬 Ask Questions</h3>
//             <input
//               type="text"
//               value={question}
//               onChange={(e) => setQuestion(e.target.value)}
//               placeholder="e.g. What is this document about?"
//               className="w-full border border-gray-600 rounded-lg p-2 bg-[#1e293b] text-gray-200"
//             />
//             <button
//               onClick={askQuestion}
//               className="mt-4 w-full py-2 bg-gradient-to-r from-purple-500 to-pink-500 rounded-lg transform hover:scale-95 transition-all"
//             >
//               Get Answer
//             </button>
//             {answer && (
//               <p className="mt-4 text-gray-300">
//                 <b>Answer:</b> {answer}
//               </p>
//             )}
//           </div>

//           {/* Generate Audiobook */}
//           <div className="bg-[#10172a] p-6 rounded-2xl shadow-lg transform transition-all duration-300 hover:scale-105 hover:shadow-[0_0_30px_rgba(255,255,255,0.3)]">
//             <h3 className="text-lg font-semibold mb-2">🎧 Generate Audiobook</h3>
//             <select
//               value={selectedLang}
//               onChange={(e) => setSelectedLang(e.target.value)}
//               className="w-full border border-gray-600 rounded-lg p-2 bg-[#1e293b] text-gray-200"
//             >
//               {Object.entries(langs).map(([code, name]) => (
//                 <option key={code} value={code}>
//                   {name} ({code})
//                 </option>
//               ))}
//             </select>
//             <button
//               onClick={generateAudio}
//               className="mt-4 w-full py-2 bg-gradient-to-r from-purple-500 to-pink-500 rounded-lg transform hover:scale-95 transition-all"
//             >
//               Generate Audio
//             </button>
//             {audioUrl && (
//               <div className="mt-4">
//                 <audio controls src={audioUrl} className="w-full" />
//               </div>
//             )}
//           </div>
//         </div>

//         {/* Q&A History */}
//         <div className="bg-[#10172a] p-6 rounded-2xl shadow-lg transform transition-all duration-300 hover:scale-105 hover:shadow-[0_0_30px_rgba(255,255,255,0.3)]">
//           <h3 className="text-lg font-semibold mb-4">📜 Q&A History</h3>
//           {qaHistory.length === 0 && <p className="text-gray-400">No Q&A yet</p>}
//           <div className="space-y-3">
//             {qaHistory.map(([q, a], idx) => (
//               <div key={idx} className="p-3 rounded-lg bg-[#1e293b]">
//                 <p className="text-purple-300"><b>Q:</b> {q}</p>
//                 <p className="text-pink-300 mt-1"><b>A:</b> {a}</p>
//               </div>
//             ))}
//           </div>
//         </div>
//       </div>
//     </div>
//   );
// }

// export default App;



// import React, { useState, useEffect } from "react";
// import axios from "axios";

// function App() {
//   const [file, setFile] = useState(null);
//   const [filename, setFilename] = useState(null);
//   const [question, setQuestion] = useState("");
//   const [answer, setAnswer] = useState("");
//   const [qaHistory, setQaHistory] = useState([]);
//   const [langs, setLangs] = useState({});
//   const [selectedLang, setSelectedLang] = useState("en");
//   const [audioUrl, setAudioUrl] = useState(null);

//   useEffect(() => {
//     fetchLangs();
//     fetchHistory();
//   }, []);

//   const fetchLangs = async () => {
//     try {
//       const res = await axios.get("/api/langs");
//       setLangs(res.data.langs || {});
//     } catch (e) {
//       console.error(e);
//     }
//   };

//   const fetchHistory = async () => {
//     try {
//       const res = await axios.get("/api/qa-history");
//       setQaHistory(res.data.qa_pairs || []);
//     } catch (e) {
//       console.error(e);
//     }
//   };

//   const uploadFile = async () => {
//     if (!file) return alert("Pick a file");
//     const fd = new FormData();
//     fd.append("file", file);
//     await axios.post("/api/upload", fd, { headers: { "Content-Type": "multipart/form-data" } });
//     setFilename(file.name);
//     fetchHistory();
//   };

//   const askQuestion = async () => {
//     if (!question) return alert("Enter a question");
//     const res = await axios.post("/api/answer", { question });
//     setAnswer(res.data.answer);
//     fetchHistory();
//   };

//   const generateAudio = async () => {
//     const res = await axios.post("/api/audiobook", { lang_code: selectedLang }, { responseType: "blob" });
//     const blob = new Blob([res.data], { type: "audio/mpeg" });
//     setAudioUrl(URL.createObjectURL(blob));
//   };

//   return (
//     <div className="min-h-screen bg-gradient-to-br from-[#0f0c29] via-[#302b63] to-[#24243e] text-white">
//       {/* Navbar */}
//       <nav className="flex justify-between items-center px-8 py-4">
//         <h1 className="text-xl font-bold text-pink-400">AssistifyAI</h1>
//         <div>
//           <button className="mr-4 hover:underline">Login</button>
//           <button className="px-4 py-2 bg-gradient-to-r from-pink-500 to-purple-600 rounded-lg">
//             Get Started
//           </button>
//         </div>
//       </nav>

//       {/* Hero Section */}
//       <section className="text-center py-16">
//         <h2 className="text-4xl md:text-5xl font-bold">
//           Transform Documents with <span className="text-pink-400">AI Assistant</span>
//         </h2>
//         <p className="mt-4 text-lg text-gray-300">
//           Upload any document to get instant answers via advanced RAG technology <br />
//           or convert it into a high-quality audiobook
//         </p>
//       </section>

//       {/* Main Content */}
//       <div className="max-w-5xl mx-auto px-4 grid gap-6">
//         {/* Upload Box */}
//         <div className="bg-[#10172a] p-6 rounded-2xl shadow-lg">
//           <h3 className="text-lg font-semibold mb-2">📄 Upload Document</h3>
//           <input
//             type="file"
//             className="block w-full border border-gray-600 rounded-lg p-2 bg-[#1e293b] text-gray-200"
//             onChange={(e) => setFile(e.target.files[0])}
//           />
//           <button
//             onClick={uploadFile}
//             className="mt-4 w-full py-2 bg-gradient-to-r from-purple-500 to-pink-500 rounded-lg"
//           >
//             Upload
//           </button>
//           {filename && <p className="mt-2 text-sm text-gray-400">Uploaded: {filename}</p>}
//         </div>

//         {/* Ask + Audio */}
//         <div className="grid md:grid-cols-2 gap-6">
//           {/* Ask Questions */}
//           <div className="bg-[#10172a] p-6 rounded-2xl shadow-lg">
//             <h3 className="text-lg font-semibold mb-2">💬 Ask Questions</h3>
//             <input
//               type="text"
//               value={question}
//               onChange={(e) => setQuestion(e.target.value)}
//               placeholder="e.g. What is this document about?"
//               className="w-full border border-gray-600 rounded-lg p-2 bg-[#1e293b] text-gray-200"
//             />
//             <button
//               onClick={askQuestion}
//               className="mt-4 w-full py-2 bg-gradient-to-r from-purple-500 to-pink-500 rounded-lg"
//             >
//               Get Answer
//             </button>
//             {answer && (
//               <p className="mt-4 text-gray-300">
//                 <b>Answer:</b> {answer}
//               </p>
//             )}
//           </div>

//           {/* Generate Audiobook */}
//           <div className="bg-[#10172a] p-6 rounded-2xl shadow-lg">
//             <h3 className="text-lg font-semibold mb-2">🎧 Generate Audiobook</h3>
//             <select
//               value={selectedLang}
//               onChange={(e) => setSelectedLang(e.target.value)}
//               className="w-full border border-gray-600 rounded-lg p-2 bg-[#1e293b] text-gray-200"
//             >
//               {Object.entries(langs).map(([code, name]) => (
//                 <option key={code} value={code}>
//                   {name} ({code})
//                 </option>
//               ))}
//             </select>
//             <button
//               onClick={generateAudio}
//               className="mt-4 w-full py-2 bg-gradient-to-r from-purple-500 to-pink-500 rounded-lg"
//             >
//               Generate Audio
//             </button>
//             {audioUrl && (
//               <div className="mt-4">
//                 <audio controls src={audioUrl} className="w-full" />
//               </div>
//             )}
//           </div>
//         </div>

//         {/* Q&A History */}
//         <div className="bg-[#10172a] p-6 rounded-2xl shadow-lg">
//           <h3 className="text-lg font-semibold mb-4">📜 Q&A History</h3>
//           {qaHistory.length === 0 && <p className="text-gray-400">No Q&A yet</p>}
//           <div className="space-y-3">
//             {qaHistory.map(([q, a], idx) => (
//               <div key={idx} className="p-3 rounded-lg bg-[#1e293b]">
//                 <p className="text-purple-300"><b>Q:</b> {q}</p>
//                 <p className="text-pink-300 mt-1"><b>A:</b> {a}</p>
//               </div>
//             ))}
//           </div>
//         </div>
//       </div>
//     </div>
//   );
// }

// export default App;

// (No Q&A History)
// import React, { useState, useEffect } from "react";
// import axios from "axios";

// function App() {
//   const [file, setFile] = useState(null);
//   const [filename, setFilename] = useState(null);
//   const [question, setQuestion] = useState("");
//   const [answer, setAnswer] = useState("");
//   const [langs, setLangs] = useState({});
//   const [selectedLang, setSelectedLang] = useState("en");
//   const [audioUrl, setAudioUrl] = useState(null);

//   useEffect(() => {
//     fetchLangs();
//   }, []);

//   const fetchLangs = async () => {
//     try {
//       const res = await axios.get("/api/langs");
//       setLangs(res.data.langs || {});
//     } catch (e) {
//       console.error(e);
//     }
//   };

//   const uploadFile = async () => {
//     if (!file) return alert("Pick a file");
//     const fd = new FormData();
//     fd.append("file", file);
//     await axios.post("/api/upload", fd, { headers: { "Content-Type": "multipart/form-data" } });
//     setFilename(file.name);
//   };

//   const askQuestion = async () => {
//     if (!question) return alert("Enter a question");
//     const res = await axios.post("/api/answer", { question });
//     setAnswer(res.data.answer);
//   };

//   const generateAudio = async () => {
//     const res = await axios.post(
//       "/api/audiobook",
//       { lang_code: selectedLang },
//       { responseType: "blob" }
//     );
//     const blob = new Blob([res.data], { type: "audio/mpeg" });
//     setAudioUrl(URL.createObjectURL(blob));
//   };

//   return (
//     <div className="min-h-screen bg-gradient-to-br from-[#0f0c29] via-[#302b63] to-[#24243e] text-white">
//       {/* Navbar */}
//       <nav className="flex justify-between items-center px-8 py-4">
//         <h1 className="text-xl font-bold text-pink-400">AssistifyAI</h1>
//         <div>
//           <button className="mr-4 hover:underline">Login</button>
//           <button className="px-4 py-2 bg-gradient-to-r from-pink-500 to-purple-600 rounded-lg">
//             Get Started
//           </button>
//         </div>
//       </nav>

//       {/* Hero Section */}
//       <section className="text-center py-16">
//         <h2 className="text-4xl md:text-5xl font-bold">
//           Transform Documents with <span className="text-pink-400">AI Assistant</span>
//         </h2>
//         <p className="mt-4 text-lg text-gray-300">
//           Upload any document to get instant answers via advanced RAG technology <br />
//           or convert it into a high-quality audiobook
//         </p>
//       </section>

//       {/* Main Content */}
//       <div className="max-w-5xl mx-auto px-4 grid gap-6">
//         {/* Upload Document */}
//         <div className="bg-[#10172a] p-6 rounded-2xl shadow-lg">
//           <h3 className="text-lg font-semibold mb-2">📄 Upload Document</h3>
//           <input
//             type="file"
//             className="block w-full border border-gray-600 rounded-lg p-2 bg-[#1e293b] text-gray-200"
//             onChange={(e) => setFile(e.target.files[0])}
//           />
//           <button
//             onClick={uploadFile}
//             className="mt-4 w-full py-2 bg-gradient-to-r from-purple-500 to-pink-500 rounded-lg"
//           >
//             Upload
//           </button>
//           {filename && <p className="mt-2 text-sm text-gray-400">Uploaded: {filename}</p>}
//         </div>

//         {/* Ask Questions + Generate Audio side by side */}
//         <div className="grid md:grid-cols-2 gap-6">
//           {/* Ask Questions */}
//           <div className="bg-[#10172a] p-6 rounded-2xl shadow-lg">
//             <h3 className="text-lg font-semibold mb-2">💬 Ask Questions</h3>
//             <input
//               type="text"
//               value={question}
//               onChange={(e) => setQuestion(e.target.value)}
//               placeholder="e.g. What is this document about?"
//               className="w-full border border-gray-600 rounded-lg p-2 bg-[#1e293b] text-gray-200"
//             />
//             <button
//               onClick={askQuestion}
//               className="mt-4 w-full py-2 bg-gradient-to-r from-purple-500 to-pink-500 rounded-lg"
//             >
//               Get Answer
//             </button>

//             {/* Show Answer Here */}
//             {answer && (
//               <div className="mt-4 p-3 rounded-lg bg-[#1e293b]">
//                 <p className="text-gray-300">
//                   <b>Answer:</b> {answer}
//                 </p>
//               </div>
//             )}
//           </div>

//           {/* Generate Audiobook */}
//           <div className="bg-[#10172a] p-6 rounded-2xl shadow-lg">
//             <h3 className="text-lg font-semibold mb-2">🎧 Generate Audiobook</h3>
//             <select
//               value={selectedLang}
//               onChange={(e) => setSelectedLang(e.target.value)}
//               className="w-full border border-gray-600 rounded-lg p-2 bg-[#1e293b] text-gray-200"
//             >
//               {Object.entries(langs).map(([code, name]) => (
//                 <option key={code} value={code}>
//                   {name} ({code})
//                 </option>
//               ))}
//             </select>
//             <button
//               onClick={generateAudio}
//               className="mt-4 w-full py-2 bg-gradient-to-r from-purple-500 to-pink-500 rounded-lg"
//             >
//               Generate Audio
//             </button>
//             {audioUrl && (
//               <div className="mt-4">
//                 <audio controls src={audioUrl} className="w-full" />
//               </div>
//             )}
//           </div>
//         </div>
//       </div>
//     </div>
//   );
// }

// export default App;

