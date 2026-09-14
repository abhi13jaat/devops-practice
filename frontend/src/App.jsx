import { useEffect, useState } from 'react'
import './App.css'

const API = '/api/tasks'

function App() {
  const [tasks, setTasks] = useState([])
  const [title, setTitle] = useState('')
  const [error, setError] = useState(null)

  async function loadTasks() {
    try {
      const res = await fetch(API)
      if (!res.ok) throw new Error(`HTTP ${res.status}`)
      setTasks(await res.json())
    } catch (e) {
      setError(e.message)
    }
  }

  async function createTask(e) {
    e.preventDefault()
    if (!title.trim()) return
    try {
      const res = await fetch(API, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title, description: '' }),
      })
      if (!res.ok) throw new Error(`HTTP ${res.status}`)
      setTitle('')
      loadTasks()
    } catch (e) {
      setError(e.message)
    }
  }

  useEffect(() => {
    loadTasks()
  }, [])

  return (
    <div className="app">
      <h1>DevOps Task Manager</h1>

      <form onSubmit={createTask}>
        <input
          type="text"
          placeholder="New task title..."
          value={title}
          onChange={(e) => setTitle(e.target.value)}
        />
        <button type="submit">Add</button>
      </form>

      {error && <p className="error">Error: {error}</p>}

      <ul>
        {tasks.map((t) => (
          <li key={t.id}>
            <strong>#{t.id}</strong> — {t.title}
          </li>
        ))}
      </ul>

      {tasks.length === 0 && !error && (
        <p className="empty">No tasks yet. Add one above.</p>
      )}
    </div>
  )
}

export default App