import React, { useState, useCallback } from 'react';
import { motion } from 'framer-motion';
import { Upload, FileText, X } from 'lucide-react';

const FileUploadZone = ({ onFileSelect, acceptedTypes, maxSize = 10 * 1024 * 1024 }) => {
  const [isDragOver, setIsDragOver] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);

  const handleDragOver = useCallback((e) => {
    e.preventDefault();
    setIsDragOver(true);
  }, []);

  const handleDragLeave = useCallback((e) => {
    e.preventDefault();
    setIsDragOver(false);
  }, []);

  const handleDrop = useCallback((e) => {
    e.preventDefault();
    setIsDragOver(false);
    
    const files = Array.from(e.dataTransfer.files);
    if (files.length > 0) {
      handleFileSelection(files[0]);
    }
  }, []);

  const handleFileSelection = (file) => {
    if (file.size > maxSize) {
      alert('File size too large. Please select a file under 10MB.');
      return;
    }

    setSelectedFile(file);
    onFileSelect(file);
  };

  const handleFileInput = (e) => {
    const file = e.target.files[0];
    if (file) {
      handleFileSelection(file);
    }
  };

  const removeFile = () => {
    setSelectedFile(null);
    onFileSelect(null);
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="w-full"
    >
      <div
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        className={`border-2 border-dashed rounded-xl p-8 text-center transition-all duration-300 ${
          isDragOver
            ? 'border-blue-400 bg-blue-50'
            : selectedFile
            ? 'border-green-400 bg-green-50'
            : 'border-gray-300 hover:border-blue-400 hover:bg-gray-50'
        }`}
      >
        <input
          type="file"
          onChange={handleFileInput}
          accept={acceptedTypes}
          className="hidden"
          id="file-upload"
        />

        {selectedFile ? (
          <motion.div
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            className="flex items-center justify-center space-x-4"
          >
            <FileText className="w-8 h-8 text-green-600" />
            <div className="flex-1 text-left">
              <p className="font-medium text-gray-900">{selectedFile.name}</p>
              <p className="text-sm text-gray-600">
                {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
              </p>
            </div>
            <button
              onClick={removeFile}
              className="p-1 hover:bg-red-100 rounded-full transition-colors"
            >
              <X className="w-5 h-5 text-red-500" />
            </button>
          </motion.div>
        ) : (
          <label htmlFor="file-upload" className="cursor-pointer">
            <Upload className="w-12 h-12 text-gray-400 mx-auto mb-4" />
            <p className="text-lg font-medium text-gray-700 mb-2">
              {isDragOver ? 'Drop your file here' : 'Upload Document'}
            </p>
            <p className="text-gray-500">
              Drag and drop or click to select
            </p>
            <p className="text-sm text-gray-400 mt-2">
              Supports PDF, DOCX, PPTX, and images (max 10MB)
            </p>
          </label>
        )}
      </div>
    </motion.div>
  );
};

export default FileUploadZone;