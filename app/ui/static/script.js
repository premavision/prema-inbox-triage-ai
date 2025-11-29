// Modern JavaScript for UI interactivity

document.addEventListener('DOMContentLoaded', function() {
  // Initialize all interactive features
  initToggleDetails();
  initFormLoadingStates();
  initSmoothScrolling();
  initEmailCardAnimations();
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
 * Add loading states to forms
 */
function initFormLoadingStates() {
  const forms = document.querySelectorAll('form');
  
  forms.forEach(form => {
    form.addEventListener('submit', function(e) {
      const submitButton = form.querySelector('button[type="submit"]');
      
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
 * Utility function to show toast notifications (can be enhanced later)
 */
function showToast(message, type = 'info') {
  // Simple console log for now, can be enhanced with a toast library
  console.log(`[${type.toUpperCase()}] ${message}`);
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

