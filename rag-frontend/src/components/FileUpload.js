import React, { useState } from 'react'
import { Button, Spinner } from 'react-bootstrap'
import { FiUpload } from 'react-icons/fi'

function FileUpload ({ setCurrentFile }) {
  const [isUploading, setIsUploading] = useState(false)
  const [uploadedFileName, setUploadedFileName] = useState('')

  const handleFileChange = async event => {
    const file = event.target.files[0]
    if (!file) return

    if (file.type !== 'application/pdf') {
      alert('Please upload a PDF file')
      return
    }

    setIsUploading(true)
    try {
      const formData = new FormData()
      formData.append('file', file)

      const response = await fetch('http://localhost:8000/upload-file/', {
        method: 'POST',
        body: formData
      })

      if (!response.ok) throw new Error('Upload failed')

      setCurrentFile(file)
      setUploadedFileName(file.name)
    } catch (error) {
      alert('Failed to upload file')
      console.error(error)
    } finally {
      setIsUploading(false)
    }
  }

  return (
    <div className='text-center'>
      <label className='btn btn-outline-secondary'>
        <FiUpload className='me-2' />
        {isUploading ? (
          <>
            <Spinner animation='border' size='sm' className='me-2' />
            File is processing...
          </>
        ) : (
          'Upload PDF'
        )}
        <input
          type='file'
          accept='.pdf'
          onChange={handleFileChange}
          className='d-none'
          disabled={isUploading}
        />
      </label>
      {uploadedFileName && !isUploading && (
        <div className='mt-2 text-success'>
          Uploaded File: {uploadedFileName}
        </div>
      )}
    </div>
  )
}

export default FileUpload
