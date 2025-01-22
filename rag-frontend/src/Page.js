import React, { useState } from 'react'
import axios from 'axios'

const Page = () => {
  const [query, setQuery] = useState('')
  const [answer, setAnswer] = useState('')
  const [context, setContext] = useState('')

  const handleSubmit = async e => {
    e.preventDefault()
    try {
      const response = await axios.post('http://localhost:5000/query', {
        query
      })
      setAnswer(response.data.answer)
      setContext(response.data.context)
    } catch (error) {
      console.error('Error fetching the answer:', error)
    }
  }

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <label htmlFor='query'>Enter Your Query:</label>
        <input
          type='text'
          id='query'
          value={query}
          onChange={e => setQuery(e.target.value)}
        />
        <button type='submit'>Submit</button>
      </form>
      {answer && (
        <div>
          <h3>Answer:</h3>
          <p>{answer}</p>
          <h3>Context:</h3>
          <p>{context}</p>
        </div>
      )}
    </div>
  )
}

export default Page
