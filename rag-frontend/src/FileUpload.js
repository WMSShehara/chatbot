import React from 'react'

function FileUpload ({ onFileUploaded }) {
  const handleFileChange = async event => {
    const file = event.target.files[0]
    if (!file) return

    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await fetch('http://127.0.0.1:8000/upload-file/', {
        method: 'POST',
        body: formData
      })

      if (!response.ok) {
        throw new Error('Failed to upload the file.')
      }

      const data = await response.json()
      console.log('upload response', data)
      onFileUploaded(data.file_name)
    } catch (error) {
      console.error(error)
      alert('File upload failed. Please try again.')
    }
  }

  return (
    <div>
      <input type='file' onChange={handleFileChange} />
    </div>
  )
}

export default FileUpload
