import React, { useState, useEffect } from 'react';
import './App.css';
import { Button } from './components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './components/ui/card';
import { Progress } from './components/ui/progress';
import { Alert, AlertDescription } from './components/ui/alert';
import { Badge } from './components/ui/badge';
import { Trash2, Download, Upload, BookOpen, Volume2, FileText } from 'lucide-react';
import QABox from "./components/ui/QABox";

const BACKEND_URL = "http://localhost:8000"; // Make sure this matches your FastAPI port

function App() {
  const [jobs, setJobs] = useState([]);
  const [isUploading, setIsUploading] = useState(false);
  const [dragActive, setDragActive] = useState(false);

  const fetchJobs = async () => {
    try {
      const response = await fetch(`${BACKEND_URL}/api/jobs`);
      if (response.ok) {
        const data = await response.json();
        setJobs(data);
      }
    } catch (error) {
      console.error('Failed to fetch jobs:', error);
    }
  };

  useEffect(() => {
    fetchJobs();
    const interval = setInterval(fetchJobs, 2000); // Poll every 2 seconds
    return () => clearInterval(interval);
  }, []);

  const handleFileUpload = async (file) => {
    if (!file) return;

    const allowedTypes = ['.pdf', '.docx', '.txt'];
    const fileExtension = '.' + file.name.split('.').pop().toLowerCase();

    if (!allowedTypes.includes(fileExtension)) {
      alert('Please upload a PDF, DOCX, or TXT file');
      return;
    }

    setIsUploading(true);

    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await fetch(`${BACKEND_URL}/api/upload`, {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        await fetchJobs();
      } else {
        const error = await response.json();
        alert(`Upload failed: ${error.detail}`);
      }
    } catch (error) {
      console.error('Upload error:', error);
      alert('Upload failed. Please try again.');
    } finally {
      setIsUploading(false);
    }
  };

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileUpload(e.dataTransfer.files[0]);
    }
  };

  const handleDownload = async (jobId, audioFile) => {
    try {
      const response = await fetch(`${BACKEND_URL}/api/download/${jobId}/${audioFile}`);
      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = audioFile;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
      } else {
        alert('Download failed');
      }
    } catch (error) {
      console.error('Download error:', error);
      alert('Download failed');
    }
  };

  const handleDelete = async (jobId) => {
    if (window.confirm('Are you sure you want to delete this audiobook?')) {
      try {
        const response = await fetch(`${BACKEND_URL}/api/jobs/${jobId}`, {
          method: 'DELETE',
        });
        if (response.ok) {
          await fetchJobs();
        }
      } catch (error) {
        console.error('Delete error:', error);
      }
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'completed': return 'bg-emerald-500';
      case 'error': return 'bg-red-500';
      case 'processing': 
      case 'rewriting': 
      case 'generating_audio': return 'bg-blue-500';
      default: return 'bg-gray-500';
    }
  };

  const getStatusText = (status) => {
    switch (status) {
      case 'uploaded': return 'Queued';
      case 'processing': return 'Processing';
      case 'rewriting': return 'AI Rewriting';
      case 'generating_audio': return 'Generating Audio';
      case 'completed': return 'Complete';
      case 'error': return 'Error';
      default: return status;
    }
  };

  const formatDuration = (createdAt, completedAt) => {
    if (!completedAt) return '';
    const duration = Math.round((new Date(completedAt) - new Date(createdAt)) / 1000);
    return `${duration}s`;
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-purple-50">
      {/* Header */}
      <div className="bg-white/80 backdrop-blur-md border-b border-indigo-100 sticky top-0 z-10">
        <div className="max-w-6xl mx-auto px-6 py-4">
          <div className="flex items-center space-x-3">
            <div className="flex items-center justify-center w-12 h-12 rounded-2xl bg-gradient-to-r from-indigo-500 to-purple-600">
              <BookOpen className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-2xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">
                AI Audiobook Generator
              </h1>
              <p className="text-sm text-gray-600">Transform your documents into engaging audiobooks</p>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-6xl mx-auto px-6 py-8">
        {/* Upload Section */}
        <Card className="mb-8 border-0 shadow-xl bg-white/70 backdrop-blur-sm">
          <CardHeader className="text-center pb-4">
            <CardTitle className="text-xl text-gray-800">Upload Your Document</CardTitle>
            <CardDescription>
              Support for PDF, DOCX, and TXT files. AI will rewrite your content for optimal audiobook narration.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div
              className={`relative border-2 border-dashed rounded-2xl p-12 text-center transition-all duration-200 ${
                dragActive 
                  ? 'border-indigo-400 bg-indigo-50/50' 
                  : 'border-gray-300 hover:border-indigo-300 hover:bg-indigo-50/30'
              }`}
              onDragEnter={handleDrag}
              onDragLeave={handleDrag}
              onDragOver={handleDrag}
              onDrop={handleDrop}
            >
              <input
                type="file"
                accept=".pdf,.docx,.txt"
                onChange={(e) => handleFileUpload(e.target.files[0])}
                className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                disabled={isUploading}
              />
              
              <div className="space-y-4">
                <div className="flex justify-center">
                  <div className="p-4 rounded-full bg-gradient-to-r from-indigo-100 to-purple-100">
                    <Upload className="w-8 h-8 text-indigo-600" />
                  </div>
                </div>
                
                <div>
                  <p className="text-lg font-medium text-gray-700 mb-2">
                    {isUploading ? 'Uploading...' : 'Drop your file here or click to browse'}
                  </p>
                  <p className="text-sm text-gray-500">
                    PDF, DOCX, TXT files up to 50MB
                  </p>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Jobs List */}
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-semibold text-gray-800 flex items-center">
              <Volume2 className="w-5 h-5 mr-2 text-indigo-600" />
              Your Audiobooks
            </h2>
            <Badge variant="secondary" className="text-sm">
              {jobs.length} {jobs.length === 1 ? 'book' : 'books'}
            </Badge>
          </div>

          {jobs.length === 0 ? (
            <Card className="border-0 shadow-lg bg-white/70 backdrop-blur-sm">
              <CardContent className="py-16 text-center">
                <div className="flex justify-center mb-4">
                  <div className="p-4 rounded-full bg-gray-100">
                    <FileText className="w-8 h-8 text-gray-400" />
                  </div>
                </div>
                <p className="text-gray-500 text-lg">No audiobooks yet</p>
                <p className="text-gray-400 text-sm mt-1">Upload a document to get started</p>
              </CardContent>
            </Card>
          ) : (
            <div className="grid gap-4">
              {jobs.map((job) => (
                <Card key={job.id} className="border-0 shadow-lg bg-white/70 backdrop-blur-sm hover:shadow-xl transition-all duration-200">
                  <CardContent className="p-6">
                    <div className="flex items-center justify-between">
                      <div className="flex-1">
                        <div className="flex items-center space-x-3 mb-3">
                          <div className="flex items-center justify-center w-8 h-8 rounded-lg bg-gradient-to-r from-indigo-100 to-purple-100">
                            <FileText className="w-4 h-4 text-indigo-600" />
                          </div>
                          <div>
                            <h3 className="font-medium text-gray-800 truncate max-w-md">
                              {job.filename}
                            </h3>
                            <div className="flex items-center space-x-3 mt-1">
                              <Badge className={`${getStatusColor(job.status)} text-white text-xs px-2 py-1`}>
                                {getStatusText(job.status)}
                              </Badge>
                              <span className="text-xs text-gray-500">
                                {new Date(job.created_at).toLocaleString()}
                              </span>
                              {job.completed_at && (
                                <span className="text-xs text-green-600 font-medium">
                                  ✓ {formatDuration(job.created_at, job.completed_at)}
                                </span>
                              )}
                            </div>
                          </div>
                        </div>

                        {(job.status === 'processing' || job.status === 'rewriting' || job.status === 'generating_audio') && (
                          <div className="mb-3">
                            <div className="flex justify-between text-sm text-gray-600 mb-1">
                              <span>{getStatusText(job.status)}</span>
                              <span>{job.progress}%</span>
                            </div>
                            <Progress value={job.progress} className="h-2" />
                          </div>
                        )}

                        {job.status === 'error' && job.error_message && (
                          <Alert className="mt-3 border-red-200 bg-red-50">
                            <AlertDescription className="text-red-700 text-sm">
                              {job.error_message}
                            </AlertDescription>
                          </Alert>
                        )}
                      </div>

                      <div className="flex items-center space-x-2 ml-4">
                        {job.status === 'completed' && job.audio_files && (
                          <Button
                            onClick={() => handleDownload(job.id, job.audio_files[0])}
                            size="sm"
                            className="bg-emerald-500 hover:bg-emerald-600 text-white px-4 py-2 rounded-lg transition-colors"
                          >
                            <Download className="w-4 h-4 mr-1" />
                            Download Audio
                          </Button>
                        )}
                        
                        <Button
                          onClick={() => handleDelete(job.id)}
                          size="sm"
                          variant="outline"
                          className="text-red-600 border-red-200 hover:bg-red-50 px-3 py-2 rounded-lg transition-colors"
                        >
                          <Trash2 className="w-4 h-4" />
                        </Button>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Footer */}
      <div className="mt-16 py-8 border-t border-indigo-100 bg-white/50 backdrop-blur-sm">
        <div className="max-w-6xl mx-auto px-6 text-center">
          <p className="text-gray-600 text-sm">
            Powered by AI • Transform any document into an engaging audiobook experience
          </p>
        </div>
      </div>
      {/* Q&A Box */ }
      <QABox />
    </div>
  );
}

export default App;
