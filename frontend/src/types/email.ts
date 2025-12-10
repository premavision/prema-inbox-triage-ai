export interface Email {
    id: number;
    provider_id: string;
    thread_id?: string | null;
    sender: string;
    recipients: string;
    cc?: string | null;
    subject: string;
    snippet?: string | null;
    body: string;
    received_at: string; // ISO date string
    processing_status: string;
    lead_flag: boolean;
    category?: string | null;
    priority?: string | null;
    extracted_entities?: Record<string, any> | null;
    suggested_reply?: string | null;
    reply_generated_at?: string | null;
}

export interface EmailListResponse {
    emails: Email[];
}

export interface SyncResponse {
    success: boolean;
    synced: number;
    classified?: number;
    replies_generated?: number;
    error?: string;
}

export interface ResetResponse {
    success: boolean;
    deleted: number;
    error?: string;
}

