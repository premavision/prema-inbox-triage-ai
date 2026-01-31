import { Icons } from './Icons'
import './HeroSection.css'

export function HeroSection() {
  const openYoutubeDemo = () => {
    window.open('https://youtu.be/OHVMQciu70U', '_blank', 'noopener,noreferrer')
  }

  return (
    <section className="hero-section">
      <div className="hero-content">
        <div className="hero-badge">
          <Icons.Mail />
          <span>AI-Powered Lead Response</span>
        </div>

        <h1 className="hero-title">
          Never Miss a Sales Lead <br />
          <span className="hero-highlight">Buried in Your Inbox</span>
        </h1>

        <p className="hero-description">
          Your sales team loses 23% of inbound leads because they're buried in support tickets,
          spam, and internal emails. By the time you find them, they've gone cold.
        </p>

        <div className="hero-features">
          <div className="feature-item">
            <div className="feature-icon feature-icon-lead">
              <Icons.Star />
            </div>
            <div className="feature-text">
              <h3>Instant Lead Detection</h3>
              <p>AI identifies sales opportunities in real-time and prioritizes them</p>
            </div>
          </div>

          <div className="feature-item">
            <div className="feature-icon feature-icon-support">
              <Icons.Tool />
            </div>
            <div className="feature-text">
              <h3>Smart Categorization</h3>
              <p>Automatically sorts Support Requests, Leads, and Internal emails</p>
            </div>
          </div>

          <div className="feature-item">
            <div className="feature-icon feature-icon-ai">
              <Icons.Sparkles />
            </div>
            <div className="feature-text">
              <h3>AI-Drafted Replies</h3>
              <p>Personalized responses ready in &lt;2 minutes. Edit and send.</p>
            </div>
          </div>
        </div>

        <div className="hero-cta">
          <button onClick={openYoutubeDemo} className="btn btn-hero">
            <Icons.PlayCircle />
            Watch Demo on YouTube
          </button>
          <p className="hero-cta-note">
            No signup required • See it in action in 30 seconds
          </p>
        </div>
      </div>
    </section>
  )
}
