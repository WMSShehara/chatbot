import React from 'react'

function MessageList ({ messages }) {
  return (
    <div className='d-flex flex-column gap-3'>
      {messages.map((message, index) => (
        <div
          key={index}
          className={`p-3 rounded ${
            message.sender === 'user'
              ? 'bg-primary text-white ms-auto'
              : 'bg-light'
          }`}
          style={{ maxWidth: '70%' }}
        >
          {message.text}
        </div>
      ))}
    </div>
  )
}

export default MessageList
