import React from 'react'
import { Button } from 'react-bootstrap'
import { FiUpload } from 'react-icons/fi'

function FileUpload ({ setCurrentFile }) {
  const handleFileChange = async event => {
    const file = event.target.files[0]
    if (!file) return

    if (file.type !== 'application/pdf') {
      alert('Please upload a PDF file')
      return
    }

    try {
      const formData = new FormData()
      formData.append('file', file)

      const response = await fetch('http://localhost:8000/upload-file/', {
        method: 'POST',
        body: formData
      })

      if (!response.ok) throw new Error('Upload failed')

      setCurrentFile(file)
      alert('File uploaded successfully!')
    } catch (error) {
      alert('Failed to upload file')
      console.error(error)
    }
  }

  return (
    <div className='text-center'>
      <label className='btn btn-outline-secondary'>
        <FiUpload className='me-2' />
        Upload PDF
        <input
          type='file'
          accept='.pdf'
          onChange={handleFileChange}
          className='d-none'
        />
      </label>
    </div>
  )
}

export default FileUpload
