import React from 'react'
import ChatInterface from './components/ChatInterface'
import 'bootstrap/dist/css/bootstrap.min.css'

function App () {
  return (
    <div className='min-vh-100 bg-light'>
      <div className='container py-4'>
        <ChatInterface />
      </div>
    </div>
  )
}

export default App
