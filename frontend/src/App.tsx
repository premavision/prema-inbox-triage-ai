import { useEffect, useState } from 'react'
import './App.css'
import type { Email } from './types/email'
import { emailService } from './services/api'
import { EmailCard } from './components/EmailCard'
import { useToast } from './context/ToastContext'
import { Icons } from './components/Icons'

function App() {
  const [emails, setEmails] = useState<Email[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [syncing, setSyncing] = useState(false)
  const { success: showSuccess, error: showError } = useToast()

  const fetchEmails = async () => {
    setLoading(true)
    setError(null)
    try {
      const data = await emailService.getAll()
      setEmails(data)
    } catch (err: any) {
      setError(err.message || 'Failed to fetch emails')
      showError(err.message || 'Failed to fetch emails')
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
        showSuccess(`Synced ${result.synced} emails!`)
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
        showSuccess(`Deleted ${result.deleted} emails.`)
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
      const msg = 'Simulated error occurred: ' + err.message
      setError(msg)
      showError(msg)
    }
  }

  return (
    <>
      <header className="main-header">
        <div className="header-content">
          <div className="logo">
            <span className="logo-icon"><Icons.Mail /></span>
            <span>Prema Inbox Triage</span>
          </div>
          <p className="tagline">AI-powered email classification</p>
        </div>
      </header>

      <main className="main-content">
        <div className="dashboard-container">
          <section className="controls-section">
            <div className="controls-card">
              <div className="controls-header">
                <h2>Email Management</h2>
                <div className="controls-actions">
                  <form className="sync-form" onSubmit={handleSync}>
                    <button type="submit" className="btn btn-primary" disabled={syncing}>
                      <Icons.Refresh className={syncing ? 'spin' : ''} />
                      {syncing ? 'Syncing...' : 'Sync Latest Emails'}
                    </button>
                  </form>
                  
                  <form className="reset-form" onSubmit={handleReset}>
                    <button type="submit" className="btn btn-secondary" disabled={loading}>
                      <Icons.Trash />
                      Reset Data
                    </button>
                  </form>
                  
                  <button type="button" className="btn btn-outline" onClick={handleTestError}>
                    <Icons.Beaker />
                    Test Error
                  </button>
                </div>
              </div>
              
              {error && (
                <div className="alert alert-error">
                  <Icons.Alert />
                  <span className="alert-message">{error}</span>
                  <button className="alert-close" onClick={() => setError(null)}>&times;</button>
                </div>
              )}
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
                  <span className="empty-icon"><Icons.Inbox /></span>
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