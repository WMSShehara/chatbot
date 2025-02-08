import React, { useState } from 'react'
import { FiSend } from 'react-icons/fi'
import { Form, Button, Spinner } from 'react-bootstrap'
import FileUpload from './FileUpload'
import MessageList from './MessageList'

function ChatInterface () {
  const [messages, setMessages] = useState([])
  const [query, setQuery] = useState('')
  const [currentFile, setCurrentFile] = useState(null)
  const [isLoading, setIsLoading] = useState(false)

  const handleSendMessage = async () => {
    if (!query.trim()) return
    if (!currentFile) {
      alert('Please upload a PDF file first')
      return
    }

    setIsLoading(true)
    setMessages(prev => [...prev, { text: query, sender: 'user' }])

    try {
      const formData = new FormData()
      formData.append('query', query)
      formData.append('file_name', currentFile.name)

      const response = await fetch('http://localhost:8000/ask-question/', {
        method: 'POST',
        body: formData
      })

      const data = await response.json()
      setMessages(prev => [...prev, { text: data.answer, sender: 'bot' }])
    } catch (error) {
      alert('Failed to get response')
    } finally {
      setIsLoading(false)
      setQuery('')
    }
  }

  return (
    <div className='d-flex flex-column gap-4'>
      <h1 className='text-center mb-4'>PDF Chat Assistant</h1>

      <FileUpload setCurrentFile={setCurrentFile} />

      <div
        className='bg-white rounded p-3 shadow-sm'
        style={{ height: '60vh', overflowY: 'auto' }}
      >
        <MessageList messages={messages} />
      </div>

      <div className='d-flex gap-2'>
        <Form.Control
          value={query}
          onChange={e => setQuery(e.target.value)}
          placeholder='Ask a question...'
          onKeyPress={e => e.key === 'Enter' && handleSendMessage()}
        />
        <Button
          variant='primary'
          onClick={handleSendMessage}
          disabled={isLoading}
        >
          {isLoading ? (
            <Spinner animation='border' size='sm' />
          ) : (
            <>
              <FiSend className='me-2' />
              Send
            </>
          )}
        </Button>
      </div>
    </div>
  )
}

export default ChatInterface
