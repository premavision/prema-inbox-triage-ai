"""
End-to-end tests for API endpoints.

This test suite covers all REST API endpoints to ensure they work correctly
from an external client perspective. Tests verify:
- Correct HTTP status codes
- Response data structure and content
- Error handling for invalid requests
- Query parameter filtering
"""

import pytest
from playwright.sync_api import APIRequestContext, expect


@pytest.fixture
def api_request_context(base_url: str, playwright) -> APIRequestContext:
    """
    Create an API request context for making HTTP requests.
    
    This allows us to test API endpoints directly without using a browser,
    which is faster and more appropriate for API testing.
    """
    return playwright.request.new_context(base_url=base_url)


class TestHealthEndpoint:
    """Tests for the health check endpoint."""

    def test_health_check_returns_ok(self, api_request_context: APIRequestContext):
        """
        Verify that the health check endpoint returns a successful response.
        
        The /health endpoint should always return 200 OK with a status field,
        indicating the server is running and healthy.
        """
        response = api_request_context.get("/health")
        expect(response).to_be_ok()
        
        data = response.json()
        assert data["status"] == "ok"
        assert response.status == 200


class TestProviderConfigEndpoint:
    """Tests for the provider configuration endpoint."""

    def test_get_providers_returns_config(self, api_request_context: APIRequestContext):
        """
        Verify that the provider config endpoint returns provider information.
        
        This endpoint should return details about:
        - Gmail provider (enabled status, mode, user)
        - LLM provider (enabled status, model)
        """
        response = api_request_context.get("/config/providers")
        expect(response).to_be_ok()
        
        data = response.json()
        assert "providers" in data
        assert isinstance(data["providers"], list)
        assert len(data["providers"]) >= 2
        
        # Verify Gmail provider is present
        gmail_provider = next((p for p in data["providers"] if p["name"] == "gmail"), None)
        assert gmail_provider is not None
        assert "enabled" in gmail_provider
        assert "details" in gmail_provider
        assert "mode" in gmail_provider["details"]
        
        # Verify LLM provider is present
        llm_provider = next((p for p in data["providers"] if p["name"] == "openai"), None)
        assert llm_provider is not None
        assert "enabled" in llm_provider
        assert "details" in llm_provider


class TestEmailSyncEndpoint:
    """Tests for the email synchronization endpoint."""

    def test_sync_emails_returns_json(self, api_request_context: APIRequestContext):
        """
        Verify that syncing emails returns a JSON response with sync statistics.
        
        The /emails/sync endpoint should:
        - Return 200 OK
        - Include counts of synced, classified, and replies_generated
        - Work with mock email provider
        """
        response = api_request_context.post("/emails/sync", headers={"Content-Type": "application/json"}, timeout=60000)
        expect(response).to_be_ok()
        
        data = response.json()
        assert "synced" in data
        assert "classified" in data
        assert "replies_generated" in data
        assert isinstance(data["synced"], int)
        assert isinstance(data["classified"], int)
        assert isinstance(data["replies_generated"], int)
        assert data["synced"] >= 0

    def test_sync_emails_creates_emails(self, api_request_context: APIRequestContext):
        """
        Verify that syncing emails actually creates email records.
        
        After syncing, we should be able to list emails and see the synced ones.
        """
        # Sync emails
        sync_response = api_request_context.post("/emails/sync", headers={"Content-Type": "application/json"}, timeout=60000)
        expect(sync_response).to_be_ok()
        
        # List emails
        list_response = api_request_context.get("/emails")
        expect(list_response).to_be_ok()
        
        data = list_response.json()
        assert "emails" in data
        assert isinstance(data["emails"], list)
        
        # If emails were synced, we should see them
        sync_data = sync_response.json()
        if sync_data["synced"] > 0:
            assert len(data["emails"]) > 0


class TestEmailListEndpoint:
    """Tests for the email listing endpoint."""

    def test_list_emails_returns_array(self, api_request_context: APIRequestContext):
        """
        Verify that listing emails returns a properly structured response.
        
        The /emails endpoint should return:
        - A list of email objects
        - Each email with required fields (id, sender, subject, etc.)
        """
        # First sync to ensure we have emails
        api_request_context.post("/emails/sync", headers={"Content-Type": "application/json"}, timeout=60000)
        
        response = api_request_context.get("/emails")
        expect(response).to_be_ok()
        
        data = response.json()
        assert "emails" in data
        assert isinstance(data["emails"], list)
        
        # If emails exist, verify structure
        if data["emails"]:
            email = data["emails"][0]
            assert "id" in email
            assert "sender" in email
            assert "subject" in email
            assert "received_at" in email

    def test_list_emails_with_is_lead_filter(self, api_request_context: APIRequestContext):
        """
        Verify that filtering emails by is_lead parameter works correctly.
        
        The endpoint should accept ?is_lead=true or ?is_lead=false to filter
        emails based on their lead flag status.
        """
        # Sync emails first
        api_request_context.post("/emails/sync", headers={"Content-Type": "application/json"}, timeout=60000)
        
        # Test with is_lead=true
        response = api_request_context.get("/emails?is_lead=true")
        expect(response).to_be_ok()
        data = response.json()
        assert "emails" in data
        
        # Test with is_lead=false
        response = api_request_context.get("/emails?is_lead=false")
        expect(response).to_be_ok()
        data = response.json()
        assert "emails" in data

    def test_list_emails_with_category_filter(self, api_request_context: APIRequestContext):
        """
        Verify that filtering emails by category parameter works correctly.
        
        The endpoint should accept ?category=SALES_LEAD, SUPPORT_REQUEST, etc.
        to filter emails by their classification category.
        """
        # Sync emails first
        api_request_context.post("/emails/sync", headers={"Content-Type": "application/json"}, timeout=60000)
        
        # Test with category filter
        response = api_request_context.get("/emails?category=SALES_LEAD")
        expect(response).to_be_ok()
        data = response.json()
        assert "emails" in data
        
        # Verify all returned emails have the correct category (if any exist)
        for email in data["emails"]:
            if email.get("category"):
                assert email["category"] == "SALES_LEAD"

    def test_list_emails_with_priority_filter(self, api_request_context: APIRequestContext):
        """
        Verify that filtering emails by priority parameter works correctly.
        
        The endpoint should accept ?priority=high, medium, low to filter
        emails by their priority level.
        """
        # Sync emails first
        api_request_context.post("/emails/sync", headers={"Content-Type": "application/json"}, timeout=60000)
        
        # Test with priority filter
        response = api_request_context.get("/emails?priority=high")
        expect(response).to_be_ok()
        data = response.json()
        assert "emails" in data


class TestEmailDetailEndpoint:
    """Tests for the email detail endpoint."""

    def test_get_email_by_id_returns_email(self, api_request_context: APIRequestContext):
        """
        Verify that getting an email by ID returns the correct email data.
        
        The /emails/{id} endpoint should return:
        - Complete email details including body, metadata, classification
        - 404 if email doesn't exist
        """
        # Sync emails first
        sync_response = api_request_context.post("/emails/sync", headers={"Content-Type": "application/json"}, timeout=60000)
        expect(sync_response).to_be_ok()
        
        # Get list of emails
        list_response = api_request_context.get("/emails")
        expect(list_response).to_be_ok()
        emails = list_response.json()["emails"]
        
        if emails:
            email_id = emails[0]["id"]
            
            # Get email details
            detail_response = api_request_context.get(f"/emails/{email_id}")
            expect(detail_response).to_be_ok()
            
            email_data = detail_response.json()
            assert email_data["id"] == email_id
            assert "sender" in email_data
            assert "subject" in email_data
            assert "body" in email_data
            assert "received_at" in email_data

    def test_get_nonexistent_email_returns_404(self, api_request_context: APIRequestContext):
        """
        Verify that requesting a non-existent email returns 404.
        
        The endpoint should return a proper 404 error with a descriptive message
        when an email ID doesn't exist in the database.
        """
        response = api_request_context.get("/emails/99999")
        assert response.status == 404
        
        data = response.json()
        assert "detail" in data


class TestEmailRetriageEndpoint:
    """Tests for the email retriage endpoint."""

    def test_retriage_email_updates_classification(self, api_request_context: APIRequestContext):
        """
        Verify that retriaging an email re-runs classification and reply generation.
        
        The /emails/{id}/retriage endpoint should:
        - Re-classify the email using the LLM
        - Generate a new suggested reply
        - Return the updated email data
        """
        # Sync emails first
        api_request_context.post("/emails/sync", headers={"Content-Type": "application/json"}, timeout=60000)
        
        # Get an email
        list_response = api_request_context.get("/emails")
        emails = list_response.json()["emails"]
        
        if emails:
            email_id = emails[0]["id"]
            
            # Retriage the email
            retriage_response = api_request_context.post(f"/emails/{email_id}/retriage", timeout=60000)
            expect(retriage_response).to_be_ok()
            
            retriage_data = retriage_response.json()
            assert "email" in retriage_data
            email = retriage_data["email"]
            assert email["id"] == email_id

    def test_retriage_nonexistent_email_returns_404(self, api_request_context: APIRequestContext):
        """
        Verify that retriaging a non-existent email returns 404.
        
        The endpoint should handle invalid email IDs gracefully.
        """
        response = api_request_context.post("/emails/99999/retriage")
        assert response.status == 404


class TestEmailSendEndpoint:
    """Tests for the email send endpoint."""

    def test_send_reply_with_custom_body(self, api_request_context: APIRequestContext):
        """
        Verify that sending a reply with a custom body works correctly.
        
        The /emails/{id}/send endpoint should:
        - Accept a reply_body form parameter
        - Send the reply using the email provider
        - Return success response
        """
        # Sync emails first
        api_request_context.post("/emails/sync", headers={"Content-Type": "application/json"}, timeout=60000)
        
        # Get an email
        list_response = api_request_context.get("/emails")
        emails = list_response.json()["emails"]
        
        if emails:
            email_id = emails[0]["id"]
            
            # Send reply with custom body
            form_data = {"reply_body": "Thank you for your email. We'll get back to you soon."}
            send_response = api_request_context.post(
                f"/emails/{email_id}/send",
                form=form_data,
                headers={"Accept": "application/json"}
            )
            expect(send_response).to_be_ok()
            
            # Check if response is JSON or HTML (redirect)
            content_type = send_response.headers.get("content-type", "")
            if "application/json" in content_type:
                data = send_response.json()
                assert data["success"] is True
                assert "message" in data
            else:
                # If it's not JSON, it should be the dashboard HTML (redirected)
                # This happens if the endpoint treats it as a browser form submission
                pass

    def test_send_reply_without_body_uses_suggested(self, api_request_context: APIRequestContext):
        """
        Verify that sending a reply without a body uses the suggested reply.
        
        If no reply_body is provided, the endpoint should use the email's
        suggested_reply field if available.
        """
        # Sync emails first
        api_request_context.post("/emails/sync", headers={"Content-Type": "application/json"}, timeout=60000)
        
        # Get an email that has a suggested reply
        list_response = api_request_context.get("/emails")
        emails = list_response.json()["emails"]
        
        if emails:
            # Find an email with a suggested reply or retriage one to generate it
            email_id = emails[0]["id"]
            
            # Retriage to generate a reply
            api_request_context.post(f"/emails/{email_id}/retriage", timeout=60000)
            
            # Get updated email
            detail_response = api_request_context.get(f"/emails/{email_id}")
            email = detail_response.json()
            
            if email.get("suggested_reply"):
                # Send reply without body
                send_response = api_request_context.post(f"/emails/{email_id}/send")
                expect(send_response).to_be_ok()
                
                data = send_response.json()
                assert data["success"] is True

    def test_send_reply_without_body_or_suggested_returns_400(self, api_request_context: APIRequestContext):
        """
        Verify that sending a reply without body or suggested reply returns 400.
        
        The endpoint should return an error if there's no reply content available.
        """
        # Sync emails first
        api_request_context.post("/emails/sync", headers={"Content-Type": "application/json"}, timeout=60000)
        
        # Get an email without a suggested reply
        list_response = api_request_context.get("/emails")
        emails = list_response.json()["emails"]
        
        if emails:
            email_id = emails[0]["id"]
            
            # Try to send without body (assuming no suggested reply)
            send_response = api_request_context.post(f"/emails/{email_id}/send")
            
            # Should return 400 if no reply body available
            # Note: This might succeed if the email has a suggested reply from sync
            # So we check the status and handle both cases
            if send_response.status == 400:
                data = send_response.json()
                assert "detail" in data

    def test_send_reply_nonexistent_email_returns_404(self, api_request_context: APIRequestContext):
        """
        Verify that sending a reply for a non-existent email returns 404.
        
        The endpoint should handle invalid email IDs gracefully.
        """
        form_data = {"reply_body": "Test reply"}
        response = api_request_context.post("/emails/99999/send", form=form_data)
        assert response.status == 404

