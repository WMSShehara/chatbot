import React, { useState } from 'react'
import FileUpload from './FileUpload'

function Page () {
  const [query, setQuery] = useState('')
  const [fileName, setFileName] = useState('')
  const [answer, setAnswer] = useState('')

  const handleQuery = async () => {
    if (!fileName) {
      alert('Please upload a file first!')
      return
    }

    const formData = new URLSearchParams()
    formData.append('query', query)
    formData.append('file_name', fileName)

    try {
      const response = await fetch('http://127.0.0.1:8000/ask-question/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: formData
      })

      if (!response.ok) {
        throw new Error('Failed to get answer from the server.')
      }

      const data = await response.json()
      setAnswer(data.answer || 'No answer found.')
    } catch (error) {
      console.error(error)
      setAnswer('Error fetching answer. Please try again.')
    }
  }

  return (
    <div>
      <h1>Ask a Question</h1>
      <FileUpload
        onFileUploaded={fileName => {
          console.log('File uploaded:', fileName)
          setFileName(fileName)
        }}
      />
      <p>Uploaded file: {fileName || 'No file uploaded yet'}</p>

      <input
        type='text'
        placeholder='Enter query'
        value={query}
        onChange={e => setQuery(e.target.value)}
      />
      <button onClick={handleQuery}>Submit</button>
      <p>Answer: {answer}</p>
    </div>
  )
}

export default Page
