import { useMemo } from 'react'
import type { Email } from '../types/email'
import { Icons } from './Icons'
import './SummaryDashboard.css'

interface SummaryDashboardProps {
  emails: Email[]
}

export function SummaryDashboard({ emails }: SummaryDashboardProps) {
  const stats = useMemo(() => {
    const leads = emails.filter(e => e.category === 'SALES_LEAD')
    const support = emails.filter(e => e.category === 'SUPPORT_REQUEST')
    const internal = emails.filter(e => e.category === 'INTERNAL')

    const replied = emails.filter(e => e.suggested_reply && e.suggested_reply.length > 0).length

    return {
      total: emails.length,
      leads: leads.length,
      support: support.length,
      internal: internal.length,
      replied,
      replyRate: emails.length > 0 ? Math.round((replied / emails.length) * 100) : 0
    }
  }, [emails])

  if (emails.length === 0) {
    return null
  }

  return (
    <div className="summary-dashboard">
      <div className="summary-header">
        <div className="summary-title">
          <Icons.TrendingUp />
          <h3>Inbox Summary</h3>
        </div>
        <div className="summary-subtitle">
          Last sync: {stats.total} email{stats.total !== 1 ? 's' : ''} processed
        </div>
      </div>

      <div className="summary-stats">
        <div className="stat-card stat-leads">
          <div className="stat-icon">
            <Icons.Star />
          </div>
          <div className="stat-content">
            <div className="stat-value">{stats.leads}</div>
            <div className="stat-label">Sales Leads</div>
            <div className="stat-percentage">
              {stats.total > 0 ? Math.round((stats.leads / stats.total) * 100) : 0}% of total
            </div>
          </div>
        </div>

        <div className="stat-card stat-support">
          <div className="stat-icon">
            <Icons.LifeBuoy />
          </div>
          <div className="stat-content">
            <div className="stat-value">{stats.support}</div>
            <div className="stat-label">Support Requests</div>
            <div className="stat-percentage">
              {stats.total > 0 ? Math.round((stats.support / stats.total) * 100) : 0}% of total
            </div>
          </div>
        </div>

        <div className="stat-card stat-internal">
          <div className="stat-icon">
            <Icons.Building />
          </div>
          <div className="stat-content">
            <div className="stat-value">{stats.internal}</div>
            <div className="stat-label">Internal</div>
            <div className="stat-percentage">
              {stats.total > 0 ? Math.round((stats.internal / stats.total) * 100) : 0}% of total
            </div>
          </div>
        </div>

        <div className="stat-card stat-performance">
          <div className="stat-icon">
            <Icons.Zap />
          </div>
          <div className="stat-content">
            <div className="stat-value">{stats.replied}/{stats.total}</div>
            <div className="stat-label">AI Replies Ready</div>
            <div className="stat-percentage">
              {stats.replyRate}% response rate
            </div>
          </div>
        </div>
      </div>

      {stats.leads > 0 && (
        <div className="summary-alert">
          <Icons.Alert />
          <div className="alert-content">
            <strong>{stats.leads} sales lead{stats.leads !== 1 ? 's' : ''} detected!</strong>
            <span>Review and respond within 2 minutes to maximize conversion.</span>
          </div>
        </div>
      )}
    </div>
  )
}
