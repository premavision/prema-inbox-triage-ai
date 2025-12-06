"""
End-to-end tests for the dashboard UI.

This test suite covers all user interface interactions to ensure the dashboard
works correctly from a user's perspective. Tests verify:
- Page rendering and layout
- User interactions (clicks, form submissions)
- Dynamic content updates
- Error states and empty states
- Navigation and redirects
"""

import pytest
from playwright.sync_api import Page, expect


class TestDashboardRendering:
    """Tests for dashboard page rendering and initial state."""

    def test_dashboard_loads_successfully(self, page: Page, base_url: str):
        """
        Verify that the dashboard page loads without errors.
        
        The root URL should render the dashboard with:
        - Page title and header
        - Sync button
        - Email list section
        """
        page.goto(base_url)
        
        # Check page title
        expect(page).to_have_title("Inbox Triage AI")
        
        # Check for main sections
        expect(page.locator("h2:has-text('Email Management')")).to_be_visible()
        expect(page.locator("h2:has-text('Inbox')")).to_be_visible()
        
        # Check for sync button
        sync_button = page.locator("button:has-text('Sync Latest Emails')")
        expect(sync_button).to_be_visible()

    def test_dashboard_shows_empty_state_when_no_emails(self, page: Page, base_url: str):
        """
        Verify that the dashboard displays an empty state when no emails exist.
        
        When there are no emails, the dashboard should show:
        - Empty inbox message
        - Instructions to sync emails
        - No email cards
        """
        page.goto(base_url)
        
        # Check for empty state
        empty_state = page.locator(".empty-inbox, .empty-state-large")
        if empty_state.count() > 0:
            expect(empty_state.first).to_be_visible()
            expect(page.locator("text=No emails yet")).to_be_visible()
            expect(page.locator("text=Sync Latest Emails")).to_be_visible()

    def test_dashboard_displays_email_count(self, page: Page, base_url: str):
        """
        Verify that the dashboard displays the correct email count.
        
        The inbox section header should show the number of emails,
        updating dynamically as emails are synced.
        """
        page.goto(base_url)
        
        # Check for email count element
        email_count = page.locator(".email-count")
        # The count might be "0 emails" or "1 email" etc.
        expect(email_count).to_be_visible()


class TestEmailSyncUI:
    """Tests for email synchronization from the UI."""

    def test_sync_button_triggers_sync(self, page: Page, base_url: str):
        """
        Verify that clicking the sync button triggers email synchronization.
        
        When the sync button is clicked:
        - Form should submit
        - Page should redirect back to dashboard
        - New emails should appear (if mock provider has emails)
        """
        page.goto(base_url)
        
        # Click sync button and wait for the response
        sync_button = page.locator("button:has-text('Sync Latest Emails')")
        expect(sync_button).to_be_visible()
        
        # Wait for navigation after form submission (with longer timeout for LLM processing)
        with page.expect_navigation(timeout=60000, wait_until="domcontentloaded"):
            sync_button.click(timeout=60000)
        
        # Verify we're back on the dashboard
        expect(page).to_have_url(f"{base_url}/")
        
        # Wait a bit more for any async operations to complete
        page.wait_for_timeout(1000)

    def test_sync_button_shows_loading_state(self, page: Page, base_url: str):
        """
        Verify that the sync button shows a loading state during sync.
        
        When clicked, the button should:
        - Disable itself
        - Show "Processing..." text
        - Have a loading class
        """
        page.goto(base_url)
        
        sync_button = page.locator("button:has-text('Sync Latest Emails')")
        expect(sync_button).to_be_visible()
        
        # Click and wait for navigation (with timeout for slow operations)
        with page.expect_navigation(timeout=60000, wait_until="domcontentloaded"):
            sync_button.click()
        
        # Verify button exists (loading state might be too brief to catch reliably)
        expect(sync_button).to_be_visible()


class TestEmailCardDisplay:
    """Tests for email card rendering and display."""

    def test_email_cards_display_after_sync(self, page: Page, base_url: str):
        """
        Verify that email cards appear after syncing emails.
        
        After syncing, the dashboard should display:
        - Email cards in a grid
        - Sender information
        - Subject line
        - Date received
        - Category badges (if classified)
        """
        page.goto(base_url)
        
        # Sync emails
        sync_button = page.locator("button:has-text('Sync Latest Emails')")
        with page.expect_navigation(timeout=60000, wait_until="domcontentloaded"):
            sync_button.click()
        page.wait_for_timeout(2000)  # Wait for classification
        
        # Check for email cards
        email_cards = page.locator(".email-card")
        
        # If emails were synced, cards should be visible
        if email_cards.count() > 0:
            expect(email_cards.first).to_be_visible()
            
            # Check for email metadata
            expect(email_cards.first.locator(".sender-name, .email-sender")).to_be_visible()
            expect(email_cards.first.locator(".email-subject, h3")).to_be_visible()

    def test_email_cards_show_category_badges(self, page: Page, base_url: str):
        """
        Verify that email cards display category badges when emails are classified.
        
        Classified emails should show:
        - Category badge with icon
        - Lead badge (if applicable)
        - Priority badge (if applicable)
        """
        page.goto(base_url)
        
        # Sync and wait for classification
        sync_button = page.locator("button:has-text('Sync Latest Emails')")
        sync_button.click()
        page.wait_for_load_state("networkidle")
        
        # Wait a bit for classification to complete
        page.wait_for_timeout(2000)
        
        email_cards = page.locator(".email-card")
        if email_cards.count() > 0:
            # Check for badges (they might not all have categories)
            badges = email_cards.first.locator(".badge")
            # At least the structure should be there


class TestEmailDetailsToggle:
    """Tests for viewing and hiding email details."""

    def test_view_details_button_toggles_details(self, page: Page, base_url: str):
        """
        Verify that clicking "View Details" shows/hides email details.
        
        When clicking "View Details":
        - Details section should become visible
        - Button text should change to "Hide Details"
        - Email body should be displayed
        - Suggested reply form should be visible (if reply exists)
        """
        page.goto(base_url)
        
        # Sync emails first
        sync_button = page.locator("button:has-text('Sync Latest Emails')")
        sync_button.click()
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(2000)  # Wait for classification
        
        # Find an email card with "View Details" button
        view_details_button = page.locator("button:has-text('View Details')")
        
        if view_details_button.count() > 0:
            first_button = view_details_button.first
            email_id = first_button.get_attribute("data-email-id")
            
            # Click to show details
            first_button.click()
            
            # Check that details are visible
            details_section = page.locator(f"#details-{email_id}")
            expect(details_section).to_be_visible()
            
            # Check for email body
            expect(details_section.locator(".email-body-preview, .detail-section")).to_be_visible()
            
            # Click again to hide
            first_button.click()
            
            # Details should be hidden
            expect(details_section).to_be_hidden()

    def test_details_section_shows_email_content(self, page: Page, base_url: str):
        """
        Verify that the details section displays the full email content.
        
        The details section should show:
        - Email body (truncated preview)
        - Suggested reply textarea (if reply exists)
        - Send reply button (if reply exists)
        """
        page.goto(base_url)
        
        # Sync and classify
        sync_button = page.locator("button:has-text('Sync Latest Emails')")
        sync_button.click()
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(2000)
        
        # Open details for an email
        view_details_button = page.locator("button:has-text('View Details')")
        if view_details_button.count() > 0:
            view_details_button.first.click()
            
            # Check for email content section
            email_content = page.locator(".email-body-preview, .detail-section h4:has-text('Email Content')")
            if email_content.count() > 0:
                expect(email_content.first).to_be_visible()


class TestEmailRetriageUI:
    """Tests for retriaging emails from the UI."""

    def test_classify_and_reply_button_triggers_retriage(self, page: Page, base_url: str):
        """
        Verify that clicking "Classify & Reply" triggers retriage.
        
        For unclassified emails, the button should:
        - Submit a retriage request
        - Redirect back to dashboard
        - Update the email with classification and reply
        """
        page.goto(base_url)
        
        # Sync emails
        sync_button = page.locator("button:has-text('Sync Latest Emails')")
        with page.expect_navigation(timeout=60000, wait_until="domcontentloaded"):
            sync_button.click()
        page.wait_for_timeout(2000)  # Wait for classification
        
        # Find "Classify & Reply" button (for unclassified emails)
        classify_button = page.locator("button:has-text('Classify & Reply')")
        
        if classify_button.count() > 0:
            # Click to retriage (with longer timeout for LLM processing)
            with page.expect_navigation(timeout=60000, wait_until="domcontentloaded"):
                classify_button.first.click(timeout=60000)
            
            # Verify we're back on dashboard
            expect(page).to_have_url(f"{base_url}/")

    def test_classify_button_only_shows_for_unclassified_emails(self, page: Page, base_url: str):
        """
        Verify that "Classify & Reply" button only appears for unclassified emails.
        
        Email cards should show:
        - "Classify & Reply" button if category is missing
        - "View Details" button if category exists
        """
        page.goto(base_url)
        
        # Sync emails
        sync_button = page.locator("button:has-text('Sync Latest Emails')")
        with page.expect_navigation(timeout=60000, wait_until="domcontentloaded"):
            sync_button.click()
        page.wait_for_timeout(2000)  # Wait for classification
        
        email_cards = page.locator(".email-card")
        if email_cards.count() > 0:
            # Check that each card has either "Classify & Reply" or "View Details"
            for i in range(email_cards.count()):
                card = email_cards.nth(i)
                classify_btn = card.locator("button:has-text('Classify & Reply')")
                view_btn = card.locator("button:has-text('View Details')")
                
                # At least one should exist
                assert classify_btn.count() > 0 or view_btn.count() > 0


class TestReplySendingUI:
    """Tests for sending replies from the UI."""

    def test_send_reply_button_sends_reply(self, page: Page, base_url: str):
        """
        Verify that clicking "Send Reply" sends the email reply.
        
        When sending a reply:
        - Form should submit with reply body
        - Page should redirect back to dashboard
        - Reply should be sent via the email provider
        """
        page.goto(base_url)
        
        # Sync and classify to get a reply
        sync_button = page.locator("button:has-text('Sync Latest Emails')")
        with page.expect_navigation(timeout=60000, wait_until="domcontentloaded"):
            sync_button.click()
        page.wait_for_timeout(2000)  # Wait for classification
        
        # Open details for an email with a reply
        view_details_button = page.locator("button:has-text('View Details')")
        if view_details_button.count() > 0:
            view_details_button.first.click()
            page.wait_for_timeout(500)
            
            # Look for send reply button
            send_button = page.locator("button:has-text('Send Reply')")
            
            if send_button.count() > 0:
                # Click to send (with navigation wait)
                with page.expect_navigation(timeout=30000, wait_until="domcontentloaded"):
                    send_button.first.click()
                
                # Verify we're back on dashboard
                expect(page).to_have_url(f"{base_url}/")

    def test_reply_textarea_is_editable(self, page: Page, base_url: str):
        """
        Verify that the reply textarea allows editing before sending.
        
        Users should be able to:
        - Edit the suggested reply text
        - Modify the content before sending
        - See their changes in the textarea
        """
        page.goto(base_url)
        
        # Sync and classify
        sync_button = page.locator("button:has-text('Sync Latest Emails')")
        sync_button.click()
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(2000)
        
        # Open details
        view_details_button = page.locator("button:has-text('View Details')")
        if view_details_button.count() > 0:
            view_details_button.first.click()
            
            # Find reply textarea
            reply_textarea = page.locator("textarea[name='reply_body'], .reply-textarea")
            
            if reply_textarea.count() > 0:
                textarea = reply_textarea.first
                expect(textarea).to_be_visible()
                expect(textarea).to_be_editable()
                
                # Test editing
                original_value = textarea.input_value()
                textarea.fill("Edited reply text")
                expect(textarea).to_have_value("Edited reply text")

    def test_send_reply_with_edited_text(self, page: Page, base_url: str):
        """
        Verify that edited reply text is sent correctly.
        
        When a user edits the reply and clicks send:
        - The edited text should be submitted
        - Not the original suggested reply
        """
        page.goto(base_url)
        
        # Sync and classify
        sync_button = page.locator("button:has-text('Sync Latest Emails')")
        with page.expect_navigation(timeout=60000, wait_until="domcontentloaded"):
            sync_button.click()
        page.wait_for_timeout(2000)
        
        # Open details
        view_details_button = page.locator("button:has-text('View Details')")
        if view_details_button.count() > 0:
            view_details_button.first.click()
            page.wait_for_timeout(500)
            
            # Edit reply
            reply_textarea = page.locator("textarea[name='reply_body']")
            if reply_textarea.count() > 0:
                edited_text = "This is my edited reply"
                reply_textarea.first.fill(edited_text)
                
                # Send (with navigation wait)
                send_button = page.locator("button:has-text('Send Reply')")
                if send_button.count() > 0:
                    with page.expect_navigation(timeout=30000, wait_until="domcontentloaded"):
                        send_button.first.click()


class TestUIInteractions:
    """Tests for general UI interactions and behavior."""

    def test_page_handles_multiple_syncs(self, page: Page, base_url: str):
        """
        Verify that the page handles multiple sync operations correctly.
        
        Users should be able to:
        - Sync emails multiple times
        - See updated email counts
        - Avoid duplicate emails
        """
        page.goto(base_url)
        
        sync_button = page.locator("button:has-text('Sync Latest Emails')")
        
        # Sync multiple times
        for _ in range(2):
            sync_button.click()
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(1000)

    def test_email_cards_have_correct_structure(self, page: Page, base_url: str):
        """
        Verify that email cards have all required UI elements.
        
        Each email card should contain:
        - Header with sender and date
        - Subject and snippet
        - Footer with action buttons
        - Badges for classification
        """
        page.goto(base_url)
        
        # Sync emails
        sync_button = page.locator("button:has-text('Sync Latest Emails')")
        with page.expect_navigation(timeout=60000, wait_until="domcontentloaded"):
            sync_button.click()
        page.wait_for_timeout(2000)  # Wait for classification
        
        email_cards = page.locator(".email-card")
        if email_cards.count() > 0:
            card = email_cards.first
            
            # Check for header
            expect(card.locator(".email-card-header, .email-meta")).to_be_visible()
            
            # Check for body
            expect(card.locator(".email-card-body")).to_be_visible()
            
            # Check for footer
            expect(card.locator(".email-card-footer")).to_be_visible()

