import { useEffect, useState } from 'react'
import './App.css'
import type { Email } from './types/email'
import { emailService } from './services/api'
import { EmailCard } from './components/EmailCard'

function App() {
  const [emails, setEmails] = useState<Email[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [syncing, setSyncing] = useState(false)

  const fetchEmails = async () => {
    setLoading(true)
    setError(null)
    try {
      const data = await emailService.getAll()
      setEmails(data)
    } catch (err: any) {
      setError(err.message || 'Failed to fetch emails')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchEmails()
  }, [])

  const handleSync = async (e: React.FormEvent) => {
    e.preventDefault()
    setSyncing(true)
    setError(null)
    try {
      const result = await emailService.sync()
      if (result.success) {
        alert(`Synced ${result.synced} emails!`)
        await fetchEmails()
      } else {
        setError(result.error || 'Sync failed')
      }
    } catch (err: any) {
      setError(err.message || 'Sync failed')
    } finally {
      setSyncing(false)
    }
  }

  const handleReset = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!confirm('Are you sure you want to reset all emails? This cannot be undone.')) return
    
    setLoading(true)
    try {
      const result = await emailService.reset()
      if (result.success) {
        alert(`Deleted ${result.deleted} emails.`)
        await fetchEmails()
      } else {
        setError(result.error || 'Reset failed')
      }
    } catch (err: any) {
      setError(err.message || 'Reset failed')
    } finally {
      setLoading(false)
    }
  }

  const handleTestError = async () => {
    try {
      await emailService.simulateError()
    } catch (err: any) {
      setError('Simulated error occurred: ' + err.message)
    }
  }

  return (
    <>
      <header className="main-header">
        <div className="header-content">
          <div className="logo">
            <span className="logo-icon">📧</span>
            <span>Prema Inbox Triage</span>
          </div>
          <p className="tagline">AI-powered email classification and response drafting</p>
        </div>
      </header>

      <main className="main-content">
        <div className="dashboard-container">
          <section className="controls-section">
            <div className="controls-card">
              <h2>Email Management</h2>
              
              {error && (
                <div className="alert alert-error" id="error-alert">
                  <span className="alert-icon">⚠️</span>
                  <span className="alert-message">{error}</span>
                  <button className="alert-close" onClick={() => setError(null)}>×</button>
                </div>
              )}

              <div className="controls-actions">
                <form className="sync-form" onSubmit={handleSync}>
                  <button type="submit" className="btn btn-primary btn-sync" id="sync-btn" disabled={syncing}>
                    <span className="btn-icon">{syncing ? '⏳' : '🔄'}</span>
                    <span className="btn-text">{syncing ? 'Syncing...' : 'Sync Latest Emails'}</span>
                  </button>
                </form>
                
                <form className="reset-form" onSubmit={handleReset}>
                  <button type="submit" className="btn btn-secondary btn-reset" id="reset-btn" disabled={loading}>
                    <span className="btn-icon">🗑️</span>
                    <span className="btn-text">Reset Data</span>
                  </button>
                </form>
                
                <button type="button" className="btn btn-outline btn-test-error" onClick={handleTestError}>
                  <span className="btn-icon">🧪</span>
                  <span className="btn-text">Test Error</span>
                </button>
              </div>
            </div>
          </section>

          <section className="emails-section">
            <div className="section-header">
              <h2>Inbox</h2>
              <span className="email-count">
                {emails.length} email{emails.length !== 1 ? 's' : ''}
              </span>
            </div>

            {emails.length > 0 ? (
              <div className="emails-grid">
                {emails.map(email => (
                  <EmailCard 
                    key={email.id} 
                    email={email} 
                    onUpdate={fetchEmails}
                  />
                ))}
              </div>
            ) : (
              <div className="empty-inbox">
                <div className="empty-state-large">
                  <span className="empty-icon">📭</span>
                  <h3>No emails yet</h3>
                  <p>Click "Sync Latest Emails" to fetch emails from your inbox.</p>
                </div>
              </div>
            )}
          </section>
        </div>
      </main>

      <footer className="main-footer">
        <p>&copy; 2024 Prema Inbox Triage AI. All rights reserved.</p>
      </footer>
    </>
  )
}

export default App
