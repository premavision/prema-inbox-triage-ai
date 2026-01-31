import { Icons } from './Icons'
import './EnhancedFooter.css'

export function EnhancedFooter() {
  const handleRequestDemo = () => {
    const params = new URLSearchParams({
      budget: '< $5k (Audit/Small Fix)',
      brief: 'Interested in Prema Inbox Triage AI - AI-powered lead detection and email classification system',
      source: 'Prema Inbox Triage Demo'
    })
    window.open(`https://premavision.net/contact?${params.toString()}`, '_blank')
  }

  return (
    <footer className="enhanced-footer">
      <div className="footer-content">
        <div className="footer-cta">
          <h3>Ready to Try with Your Inbox?</h3>
          <p>Get instant lead detection and AI-powered responses for your business</p>
          <div className="footer-actions">
            <button
              onClick={handleRequestDemo}
              className="btn btn-footer-primary"
            >
              <Icons.Mail />
              Request Demo
            </button>
            <a
              href="https://github.com/premavision/prema-inbox-triage-ai"
              target="_blank"
              rel="noopener noreferrer"
              className="btn btn-footer-secondary"
            >
              <Icons.ExternalLink />
              View on GitHub
            </a>
          </div>
        </div>

        <div className="footer-info">
          <div className="footer-section">
            <h4>Product Demos</h4>
            <ul>
              <li>
                <div className="product-link-group">
                  <a 
                    href="https://prema-inbox-triage-ai.vercel.app/" 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="product-name"
                  >
                    Lead Response
                  </a>
                  <div className="product-actions">
                    <a href="https://youtu.be/OHVMQciu70U" target="_blank" rel="noopener noreferrer" title="Watch Video">
                      <Icons.PlayCircle />
                    </a>
                    <a href="https://prema-inbox-triage-ai.onrender.com/docs" target="_blank" rel="noopener noreferrer" title="API Docs">
                      <Icons.FileText />
                    </a>
                    <a href="https://github.com/premavision/prema-inbox-triage-ai" target="_blank" rel="noopener noreferrer" title="View Source">
                      <Icons.GitHub />
                    </a>
                  </div>
                </div>
              </li>
              <li>
                <div className="product-link-group">
                  <a 
                    href="https://prema-linkedin-outreach.vercel.app" 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="product-name"
                  >
                    Sales Copilot
                  </a>
                  <div className="product-actions">
                    <a href="https://youtu.be/-iKLSFOZntY" target="_blank" rel="noopener noreferrer" title="Watch Video">
                      <Icons.PlayCircle />
                    </a>
                    <a href="https://prema-linkedin-outreach.onrender.com/docs" target="_blank" rel="noopener noreferrer" title="API Docs">
                      <Icons.FileText />
                    </a>
                    <a href="https://github.com/premavision/prema-linkedin-outreach" target="_blank" rel="noopener noreferrer" title="View Source">
                      <Icons.GitHub />
                    </a>
                  </div>
                </div>
              </li>
              <li>
                <div className="product-link-group">
                  <a 
                    href="https://prema-sales-call-summarizer.streamlit.app" 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="product-name"
                  >
                    CRM Intelligence
                  </a>
                  <div className="product-actions">
                    <a href="https://youtu.be/i-79cnPB1Vk" target="_blank" rel="noopener noreferrer" title="Watch Video">
                      <Icons.PlayCircle />
                    </a>
                    <a href="https://prema-sales-call-summarizer.onrender.com/docs" target="_blank" rel="noopener noreferrer" title="API Docs">
                      <Icons.FileText />
                    </a>
                    <a href="https://github.com/premavision/prema-sales-call-summarizer" target="_blank" rel="noopener noreferrer" title="View Source">
                      <Icons.GitHub />
                    </a>
                  </div>
                </div>
              </li>
            </ul>
          </div>

          <div className="footer-section">
            <h4>Pricing</h4>
            <ul>
              <li className="text-only">From $2,200/month</li>
              <li className="text-only">One-time ownership option</li>
              <li className="text-only">Custom integrations</li>
            </ul>
          </div>

          <div className="footer-section">
            <h4>Support</h4>
            <ul>
              <li>
                <a href="mailto:denys@premavision.net">
                  denys@premavision.net
                </a>
              </li>
              <li className="text-only">2-3 weeks integration</li>
              <li className="text-only">Your data, your cloud</li>
            </ul>
          </div>
        </div>

        <div className="footer-bottom">
          <p>&copy; 2024 Prema Inbox Triage AI. All rights reserved.</p>
          <div className="footer-badges">
            <span className="badge">Powered by GPT-4</span>
            <span className="badge">No Data Stored</span>
            <span className="badge">Self-Hosted</span>
          </div>
        </div>
      </div>
    </footer>
  )
}
