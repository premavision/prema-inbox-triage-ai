// Modern JavaScript for UI interactivity

document.addEventListener('DOMContentLoaded', function() {
  // Initialize all interactive features
  initToggleDetails();
  initFormLoadingStates();
  initSmoothScrolling();
  initEmailCardAnimations();
  initSyncButton();
  initResetButton();
  initTestErrorButton();
  initErrorAlert();
});

/**
 * Toggle email details visibility
 */
function initToggleDetails() {
  const toggleButtons = document.querySelectorAll('.toggle-details');
  
  toggleButtons.forEach(button => {
    button.addEventListener('click', function() {
      const emailId = this.getAttribute('data-email-id');
      const detailsElement = document.getElementById(`details-${emailId}`);
      
      if (detailsElement) {
        const isHidden = detailsElement.style.display === 'none' || 
                        detailsElement.style.display === '';
        
        if (isHidden) {
          detailsElement.style.display = 'block';
          this.innerHTML = '<span class="btn-icon">👁️</span> Hide Details';
          // Smooth scroll to details if needed
          setTimeout(() => {
            detailsElement.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
          }, 100);
        } else {
          detailsElement.style.display = 'none';
          this.innerHTML = '<span class="btn-icon">📋</span> View Details';
        }
      }
    });
  });
}

/**
 * Add loading states to forms and handle AJAX submissions
 */
function initFormLoadingStates() {
  const forms = document.querySelectorAll('form');
  
  forms.forEach(form => {
    // Skip forms that are already handled (sync, reset)
    if (form.id === 'sync-form' || form.id === 'reset-form') {
      return;
    }
    
    form.addEventListener('submit', async function(e) {
      const submitButton = form.querySelector('button[type="submit"]');
      const formAction = form.getAttribute('action');
      
      // Handle retriage and send forms with AJAX
      if (formAction && (formAction.includes('/retriage') || formAction.includes('/send'))) {
        e.preventDefault();
        
        if (submitButton) {
          const originalText = submitButton.innerHTML;
          submitButton.disabled = true;
          submitButton.classList.add('loading');
          submitButton.innerHTML = '<span class="btn-icon">⏳</span> Processing...';
          
          try {
            const formData = new FormData(form);
            const response = await fetch(formAction, {
              method: 'POST',
              body: formData,
              headers: {
                'Accept': 'application/json',
              },
            });
            
            const data = await response.json();
            
            if (data.success || response.ok) {
              showToast('Operation completed successfully', 'success');
              // Reload emails to show updated state
              await loadAndUpdateEmails();
            } else {
              showError(data.error || 'Operation failed');
            }
          } catch (error) {
            showError('Network error: ' + error.message);
          } finally {
            if (submitButton) {
              submitButton.disabled = false;
              submitButton.classList.remove('loading');
              submitButton.innerHTML = originalText;
            }
          }
        }
        return;
      }
      
      // For other forms, just show loading state
      if (submitButton) {
        // Disable button and show loading state
        submitButton.disabled = true;
        submitButton.classList.add('loading');
        
        const originalText = submitButton.innerHTML;
        submitButton.innerHTML = '<span class="btn-icon">⏳</span> Processing...';
        
        // Re-enable after 10 seconds as a fallback (in case of errors)
        setTimeout(() => {
          submitButton.disabled = false;
          submitButton.classList.remove('loading');
          submitButton.innerHTML = originalText;
        }, 10000);
      }
    });
  });
}

/**
 * Smooth scrolling for anchor links
 */
function initSmoothScrolling() {
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      const href = this.getAttribute('href');
      if (href !== '#' && href.length > 1) {
        e.preventDefault();
        const target = document.querySelector(href);
        if (target) {
          target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      }
    });
  });
}

/**
 * Add entrance animations to email cards
 */
function initEmailCardAnimations() {
  const emailCards = document.querySelectorAll('.email-card');
  
  // Use Intersection Observer for fade-in animations
  const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
  };
  
  const observer = new IntersectionObserver(function(entries) {
    entries.forEach((entry, index) => {
      if (entry.isIntersecting) {
        setTimeout(() => {
          entry.target.style.opacity = '1';
          entry.target.style.transform = 'translateY(0)';
        }, index * 50); // Stagger animation
        observer.unobserve(entry.target);
      }
    });
  }, observerOptions);
  
  emailCards.forEach(card => {
    // Set initial state
    card.style.opacity = '0';
    card.style.transform = 'translateY(20px)';
    card.style.transition = 'opacity 0.5s ease-out, transform 0.5s ease-out';
    
    observer.observe(card);
  });
}

/**
 * Utility function to show toast notifications
 */
function showToast(message, type = 'info') {
  // Create toast container if it doesn't exist
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    container.className = 'toast-container';
    document.body.appendChild(container);
  }
  
  // Create toast element
  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.innerHTML = `
    <span class="toast-icon">${type === 'success' ? '✅' : type === 'error' ? '❌' : 'ℹ️'}</span>
    <span class="toast-message">${escapeHtml(message)}</span>
  `;
  
  container.appendChild(toast);
  
  // Auto-remove after 5 seconds
  setTimeout(() => {
    toast.style.animation = 'slideInRight 0.25s ease-in-out reverse';
    setTimeout(() => {
      if (toast.parentElement) {
        toast.remove();
      }
    }, 250);
  }, 5000);
}

/**
 * Handle form errors gracefully
 */
function handleFormError(form, errorMessage) {
  const submitButton = form.querySelector('button[type="submit"]');
  if (submitButton) {
    submitButton.disabled = false;
    submitButton.classList.remove('loading');
    showToast(errorMessage, 'error');
  }
}

/**
 * Format dates in a more readable way
 */
function formatDate(dateString) {
  const date = new Date(dateString);
  const now = new Date();
  const diffInSeconds = Math.floor((now - date) / 1000);
  
  if (diffInSeconds < 60) {
    return 'Just now';
  } else if (diffInSeconds < 3600) {
    const minutes = Math.floor(diffInSeconds / 60);
    return `${minutes} minute${minutes !== 1 ? 's' : ''} ago`;
  } else if (diffInSeconds < 86400) {
    const hours = Math.floor(diffInSeconds / 3600);
    return `${hours} hour${hours !== 1 ? 's' : ''} ago`;
  } else {
    return date.toLocaleDateString('en-US', { 
      month: 'short', 
      day: 'numeric', 
      year: date.getFullYear() !== now.getFullYear() ? 'numeric' : undefined
    });
  }
}

// Apply relative date formatting to all date elements
document.addEventListener('DOMContentLoaded', function() {
  const dateElements = document.querySelectorAll('.email-date');
  dateElements.forEach(element => {
    const dateText = element.textContent.trim();
    if (dateText && dateText !== 'Unknown date') {
      try {
        const formatted = formatDate(dateText);
        if (formatted) {
          element.textContent = formatted;
        }
      } catch (e) {
        // Keep original date if parsing fails
      }
    }
  });
});

/**
 * Initialize sync button with AJAX
 */
function initSyncButton() {
  const syncForm = document.getElementById('sync-form');
  if (!syncForm) return;
  
  syncForm.addEventListener('submit', async function(e) {
    e.preventDefault();
    const syncBtn = document.getElementById('sync-btn');
    const originalText = syncBtn.innerHTML;
    
    // Disable button and show loading
    syncBtn.disabled = true;
    syncBtn.classList.add('loading');
    syncBtn.innerHTML = '<span class="btn-icon">⏳</span> Syncing...';
    
    // Hide any existing error alerts
    const errorAlert = document.getElementById('error-alert');
    if (errorAlert) {
      errorAlert.remove();
    }
    
    try {
      const response = await fetch('/emails/sync', {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
        },
      });
      
      const data = await response.json();
      
      if (data.success) {
        // Show success message with details
        const message = `Synced ${data.synced} email(s)${data.classified > 0 ? `, classified ${data.classified}` : ''}${data.replies_generated > 0 ? `, generated ${data.replies_generated} replies` : ''}`;
        showToast(message, 'success');
        
        // Update button to show success with badge
        syncBtn.innerHTML = `
          <span class="btn-icon">✅</span>
          <span class="btn-text">Synced!</span>
          ${data.synced > 0 ? `<span class="btn-badge" style="display: inline-flex;">+${data.synced}</span>` : ''}
        `;
        syncBtn.classList.add('success-state');
        
        // Load updated emails immediately without delay
        loadAndUpdateEmails(data.synced).then(() => {
          // Restore button after emails are loaded
          syncBtn.disabled = false;
          syncBtn.classList.remove('loading', 'success-state');
          syncBtn.innerHTML = originalText;
        });
        return;
      } else {
        // Show error
        showError(data.error || 'Failed to sync emails');
        syncBtn.disabled = false;
        syncBtn.classList.remove('loading');
        syncBtn.innerHTML = originalText;
      }
    } catch (error) {
      showError('Network error: ' + error.message);
      syncBtn.disabled = false;
      syncBtn.classList.remove('loading');
      syncBtn.innerHTML = originalText;
    }
  });
}

/**
 * Initialize reset button with AJAX
 */
function initResetButton() {
  const resetForm = document.getElementById('reset-form');
  if (!resetForm) return;
  
  resetForm.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    if (!confirm('Are you sure you want to reset all emails? This cannot be undone.')) {
      return;
    }
    
    const resetBtn = document.getElementById('reset-btn');
    const originalText = resetBtn.innerHTML;
    
    // Disable button and show loading
    resetBtn.disabled = true;
    resetBtn.classList.add('loading');
    resetBtn.innerHTML = '<span class="btn-icon">⏳</span> Resetting...';
    
    try {
      const response = await fetch('/emails/reset', {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
        },
      });
      
      const data = await response.json();
      
      if (data.success) {
        showToast(`Reset complete. Deleted ${data.deleted} email(s).`, 'success');
        // Update emails list without page reload
        await loadAndUpdateEmails();
        // Restore button
        setTimeout(() => {
          resetBtn.disabled = false;
          resetBtn.classList.remove('loading');
          resetBtn.innerHTML = originalText;
        }, 500);
      } else {
        showError(data.error || 'Failed to reset emails');
        resetBtn.disabled = false;
        resetBtn.classList.remove('loading');
        resetBtn.innerHTML = originalText;
      }
    } catch (error) {
      showError('Network error: ' + error.message);
      resetBtn.disabled = false;
      resetBtn.classList.remove('loading');
      resetBtn.innerHTML = originalText;
    }
  });
}

/**
 * Initialize test error button
 */
function initTestErrorButton() {
  const testErrorBtn = document.getElementById('test-error-btn');
  if (!testErrorBtn) return;
  
  testErrorBtn.addEventListener('click', async function() {
    const syncBtn = document.getElementById('sync-btn');
    const originalText = syncBtn.innerHTML;
    
    // Disable button and show loading
    syncBtn.disabled = true;
    syncBtn.classList.add('loading');
    syncBtn.innerHTML = '<span class="btn-icon">⏳</span> Testing Error...';
    
    // Hide any existing error alerts
    const errorAlert = document.getElementById('error-alert');
    if (errorAlert) {
      errorAlert.remove();
    }
    
    try {
      const response = await fetch('/emails/sync?simulate_error=true', {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
        },
      });
      
      const data = await response.json();
      
      if (!data.success) {
        // Show error
        showError(data.error || 'Simulated error occurred');
      } else {
        showError('Error simulation did not work as expected');
      }
      
      syncBtn.disabled = false;
      syncBtn.classList.remove('loading');
      syncBtn.innerHTML = originalText;
    } catch (error) {
      showError('Network error: ' + error.message);
      syncBtn.disabled = false;
      syncBtn.classList.remove('loading');
      syncBtn.innerHTML = originalText;
    }
  });
}

/**
 * Show error message in alert
 */
function showError(message) {
  // Remove existing error alert
  const existingAlert = document.getElementById('error-alert');
  if (existingAlert) {
    existingAlert.remove();
  }
  
  // Create new error alert
  const controlsCard = document.querySelector('.controls-card');
  if (controlsCard) {
    const alert = document.createElement('div');
    alert.className = 'alert alert-error';
    alert.id = 'error-alert';
    alert.innerHTML = `
      <span class="alert-icon">⚠️</span>
      <span class="alert-message">${escapeHtml(message)}</span>
      <button class="alert-close" onclick="this.parentElement.remove()">×</button>
    `;
    
    // Insert after h2
    const h2 = controlsCard.querySelector('h2');
    if (h2 && h2.nextSibling) {
      controlsCard.insertBefore(alert, h2.nextSibling);
    } else {
      controlsCard.appendChild(alert);
    }
    
    // Scroll to alert
    alert.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }
  
  showToast(message, 'error');
}

/**
 * Initialize error alert auto-dismiss
 */
function initErrorAlert() {
  const errorAlert = document.getElementById('error-alert');
  if (errorAlert) {
    // Auto-dismiss after 10 seconds
    setTimeout(() => {
      if (errorAlert.parentElement) {
        errorAlert.remove();
      }
    }, 10000);
  }
}

/**
 * Escape HTML to prevent XSS
 */
function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

/**
 * Show status indicator in controls section
 */
function showStatusIndicator(type, message) {
  const statusDiv = document.getElementById('controls-status');
  if (!statusDiv) return;
  
  const statusIcon = statusDiv.querySelector('.status-icon');
  const statusMessage = statusDiv.querySelector('.status-message');
  
  const icons = {
    success: '✅',
    error: '❌',
    loading: '⏳',
    info: 'ℹ️'
  };
  
  if (statusIcon) statusIcon.textContent = icons[type] || icons.info;
  if (statusMessage) statusMessage.textContent = message;
  
  statusDiv.style.display = 'block';
  statusDiv.className = `controls-status status-${type}`;
}

/**
 * Hide status indicator
 */
function hideStatusIndicator() {
  const statusDiv = document.getElementById('controls-status');
  if (statusDiv) {
    statusDiv.style.display = 'none';
  }
}

/**
 * Load emails from API and update the DOM
 */
async function loadAndUpdateEmails() {
  try {
    const response = await fetch('/emails', {
      method: 'GET',
      headers: {
        'Accept': 'application/json',
      },
    });
    
    const data = await response.json();
    if (data.emails) {
      updateEmailsList(data.emails);
    }
  } catch (error) {
    console.error('Failed to load emails:', error);
    showError('Failed to load updated emails: ' + error.message);
  }
}

/**
 * Update the emails list in the DOM
 */
function updateEmailsList(emails, newEmailsCount = 0) {
  const emailsSection = document.querySelector('.emails-section');
  if (!emailsSection) return;
  
  const emailsGrid = emailsSection.querySelector('.emails-grid');
  const emptyInbox = emailsSection.querySelector('.empty-inbox');
  const sectionHeader = emailsSection.querySelector('.section-header');
  
  // Update email count with animation
  if (sectionHeader) {
    const emailCount = sectionHeader.querySelector('.email-count');
    if (emailCount) {
      emailCount.style.transition = 'transform 0.3s ease-out';
      emailCount.style.transform = 'scale(1.2)';
      setTimeout(() => {
        emailCount.textContent = `${emails.length} email${emails.length !== 1 ? 's' : ''}`;
        emailCount.style.transform = 'scale(1)';
      }, 150);
    }
  }
  
  if (emails.length === 0) {
    // Show empty state
    if (emailsGrid) emailsGrid.remove();
    if (!emptyInbox) {
      const emptyDiv = document.createElement('div');
      emptyDiv.className = 'empty-inbox';
      emptyDiv.innerHTML = `
        <div class="empty-state-large">
          <span class="empty-icon">📭</span>
          <h3>No emails yet</h3>
          <p>Click "Sync Latest Emails" to fetch emails from your inbox.</p>
        </div>
      `;
      emailsSection.appendChild(emptyDiv);
    }
    return;
  }
  
  // Remove empty state if exists
  if (emptyInbox) emptyInbox.remove();
  
  // Create or update emails grid
  let grid = emailsGrid;
  if (!grid) {
    grid = document.createElement('div');
    grid.className = 'emails-grid';
    emailsSection.appendChild(grid);
  }
  
  // Get existing email IDs to identify new ones
  const existingIds = new Set(Array.from(grid.querySelectorAll('.email-card')).map(card => 
    parseInt(card.getAttribute('data-email-id'))
  ));
  
  // Clear and render all emails immediately
  grid.innerHTML = '';
  
  // Render emails with animation
  emails.forEach((email, index) => {
    const emailCard = createEmailCard(email);
    const isNew = !existingIds.has(email.id) && newEmailsCount > 0;
    if (isNew) {
      emailCard.classList.add('new-email');
      // Stagger animation for new emails
      emailCard.style.animationDelay = `${index * 0.03}s`;
    }
    grid.appendChild(emailCard);
  });
  
  // Re-initialize interactive features for new cards
  initToggleDetails();
  initEmailCardAnimations();
}

/**
 * Create an email card element from email data
 */
function createEmailCard(email) {
  const card = document.createElement('div');
  card.className = 'email-card';
  card.setAttribute('data-email-id', email.id);
  
  // Format date
  const dateStr = email.received_at ? formatEmailDate(email.received_at) : 'Unknown date';
  
  // Format category
  const categoryLabel = formatCategory(email.category);
  const categoryIcon = getCategoryIcon(email.category);
  
  // Build badges HTML
  let badgesHtml = '';
  if (email.lead_flag) {
    badgesHtml += '<span class="badge badge-lead">⭐ Lead</span>';
  }
  if (email.category) {
    badgesHtml += `<span class="badge badge-category badge-${email.category.toLowerCase().replace('_', '-')}">
      <span class="badge-icon">${categoryIcon}</span>
      <span class="badge-text">${categoryLabel}</span>
    </span>`;
  }
  if (email.priority) {
    badgesHtml += `<span class="badge badge-priority badge-${email.priority.toLowerCase()}">${email.priority}</span>`;
  }
  
  // Build footer HTML
  let footerHtml = '';
  if (!email.category) {
    footerHtml = `
      <form method="post" action="/emails/${email.id}/retriage" class="inline-form">
        <button type="submit" class="btn btn-secondary btn-sm">
          <span class="btn-icon">🤖</span>
          Classify & Reply
        </button>
      </form>
    `;
  } else {
    footerHtml = `
      <button type="button" class="btn btn-outline btn-sm toggle-details" data-email-id="${email.id}">
        <span class="btn-icon">📋</span>
        View Details
      </button>
    `;
  }
  
  // Build details HTML
  const bodyPreview = email.body ? (email.body.length > 500 ? email.body.substring(0, 500) + '...' : email.body) : '';
  let detailsHtml = '';
  if (email.category) {
    detailsHtml = `
      <div class="email-details" id="details-${email.id}" style="display: none;">
        <div class="details-content">
          <div class="detail-section">
            <h4>Email Content</h4>
            <div class="email-body-preview">${escapeHtml(bodyPreview)}</div>
          </div>
          ${email.suggested_reply ? `
          <div class="detail-section">
            <h4>Suggested Reply</h4>
            <form method="post" action="/emails/${email.id}/send" class="reply-form">
              <textarea name="reply_body" rows="8" class="reply-textarea" placeholder="Edit the suggested reply before sending...">${escapeHtml(email.suggested_reply)}</textarea>
              <div class="form-actions">
                <button type="submit" class="btn btn-success">
                  <span class="btn-icon">✉️</span>
                  Send Reply
                </button>
              </div>
            </form>
          </div>
          ` : `
          <div class="detail-section">
            <div class="empty-state">
              <p>No reply generated yet. Click "Classify & Reply" to generate one.</p>
            </div>
          </div>
          `}
        </div>
      </div>
    `;
  }
  
  const senderInitial = email.sender ? email.sender[0].toUpperCase() : '?';
  
  card.innerHTML = `
    <div class="email-card-header">
      <div class="email-meta">
        <div class="email-sender">
          <span class="sender-avatar">${senderInitial}</span>
          <div class="sender-info">
            <strong class="sender-name">${escapeHtml(email.sender || 'Unknown')}</strong>
            <span class="email-date">${dateStr}</span>
          </div>
        </div>
      </div>
      <div class="email-badges">
        ${badgesHtml}
      </div>
    </div>
    <div class="email-card-body">
      <h3 class="email-subject">${escapeHtml(email.subject || '(No Subject)')}</h3>
      ${email.snippet ? `<p class="email-snippet">${escapeHtml(email.snippet)}</p>` : ''}
    </div>
    <div class="email-card-footer">
      ${footerHtml}
    </div>
    ${detailsHtml}
  `;
  
  return card;
}

/**
 * Format category for display
 */
function formatCategory(category) {
  const categoryMap = {
    'SALES_LEAD': 'Sales Lead',
    'SUPPORT_REQUEST': 'Support Request',
    'INTERNAL': 'Internal',
    'OTHER': 'Other'
  };
  if (!category) return '';
  return categoryMap[category] || category.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase());
}

/**
 * Get category icon
 */
function getCategoryIcon(category) {
  const iconMap = {
    'SALES_LEAD': '💼',
    'SUPPORT_REQUEST': '🛟',
    'INTERNAL': '🏢',
    'OTHER': '📧'
  };
  return iconMap[category] || '📧';
}

/**
 * Format email date
 */
function formatEmailDate(dateString) {
  const date = new Date(dateString);
  const now = new Date();
  const diffInSeconds = Math.floor((now - date) / 1000);
  
  if (diffInSeconds < 60) {
    return 'Just now';
  } else if (diffInSeconds < 3600) {
    const minutes = Math.floor(diffInSeconds / 60);
    return `${minutes} minute${minutes !== 1 ? 's' : ''} ago`;
  } else if (diffInSeconds < 86400) {
    const hours = Math.floor(diffInSeconds / 3600);
    return `${hours} hour${hours !== 1 ? 's' : ''} ago`;
  } else {
    return date.toLocaleDateString('en-US', { 
      month: 'short', 
      day: 'numeric', 
      year: date.getFullYear() !== now.getFullYear() ? 'numeric' : undefined
    });
  }
}




