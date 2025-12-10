import axios from 'axios';
import type { Email, EmailListResponse, SyncResponse, ResetResponse } from '../types/email';

// Create axios instance with default config
const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
    headers: {
        'Content-Type': 'application/json',
    },
});

export const emailService = {
    getAll: async (): Promise<Email[]> => {
        const response = await api.get<EmailListResponse>('/emails');
        return response.data.emails;
    },

    sync: async (): Promise<SyncResponse> => {
        const response = await api.post<SyncResponse>('/emails/sync');
        return response.data;
    },

    reset: async (): Promise<ResetResponse> => {
        const response = await api.post<ResetResponse>('/emails/reset');
        return response.data;
    },

    retriage: async (id: number): Promise<void> => {
        await api.post(`/emails/${id}/retriage`);
    },

    generateReply: async (id: number): Promise<void> => {
        await api.post(`/emails/${id}/generate-reply`);
    },

    sendReply: async (id: number, body: string): Promise<void> => {
        const formData = new FormData();
        formData.append('reply_body', body);
        // Note: The backend expects form data for this endpoint based on previous HTML form
        await api.post(`/emails/${id}/send`, formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });
    },

    simulateError: async (): Promise<void> => {
        await api.post('/emails/sync?simulate_error=true');
    }
};
