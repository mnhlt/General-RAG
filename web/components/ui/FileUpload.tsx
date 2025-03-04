'use client'

import { useState } from 'react'

export function FileUpload() {
  const [file, setFile] = useState<File | null>(null)
  const [uploading, setUploading] = useState(false)
  const [message, setMessage] = useState<string>('')

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0]
    if (selectedFile && selectedFile.type === 'text/plain') {
      setFile(selectedFile)
      setMessage('')
    } else {
      setFile(null)
      setMessage('Please select a valid text file')
    }
  }

  const handleUpload = async () => {
    if (!file) {
      setMessage('Please select a file first')
      return
    }

    try {
      setUploading(true)
      const formData = new FormData()
      formData.append('file', file)

      const response = await fetch('http://localhost:8000/update', {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        throw new Error('Upload failed')
      }

      setMessage('File uploaded successfully!')
      setFile(null)
    } catch (error) {
      setMessage('Error uploading file. Please try again.')
    } finally {
      setUploading(false)
    }
  }

  return (
    <div className="p-4 border rounded-lg shadow-sm">
      <h2 className="text-lg font-semibold mb-4">Upload Document</h2>
      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Select a text file
          </label>
          <input
            type="file"
            accept=".txt"
            onChange={handleFileChange}
            className="block w-full text-sm text-gray-500
              file:mr-4 file:py-2 file:px-4
              file:rounded-md file:border-0
              file:text-sm file:font-semibold
              file:bg-blue-50 file:text-blue-700
              hover:file:bg-blue-100"
          />
        </div>
        
        <button
          onClick={handleUpload}
          disabled={!file || uploading}
          className={`w-full py-2 px-4 rounded-md text-white font-medium
            ${!file || uploading 
              ? 'bg-gray-400 cursor-not-allowed'
              : 'bg-blue-600 hover:bg-blue-700'
            }`}
        >
          {uploading ? 'Uploading...' : 'Upload'}
        </button>

        {message && (
          <p className={`text-sm ${
            message.includes('successfully') 
              ? 'text-green-600' 
              : 'text-red-600'
          }`}>
            {message}
          </p>
        )}
      </div>
    </div>
  )
} 