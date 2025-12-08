import React, { useState, useEffect } from 'react';
import type { Email } from '../types/email';
import { emailService } from '../services/api';
import { useToast } from '../context/ToastContext';

interface EmailCardProps {
    email: Email;
    onUpdate: () => void;
}

export const EmailCard: React.FC<EmailCardProps> = ({ email, onUpdate }) => {
    const [expanded, setExpanded] = useState(false);
    const [replyBody, setReplyBody] = useState(email.suggested_reply || '');
    const [loading, setLoading] = useState(false);
    const { success: showSuccess, error: showError } = useToast();

    useEffect(() => {
        setReplyBody(email.suggested_reply || '');
    }, [email.suggested_reply]);

    // Helpers from original script.js
    const getCategoryIcon = (category: string) => {
        const iconMap: Record<string, string> = {
            'SALES_LEAD': '💼',
            'SUPPORT_REQUEST': '🛟',
            'INTERNAL': '🏢',
            'OTHER': '📧'
        };
        return iconMap[category] || '📧';
    };

    const formatCategory = (category: string) => {
        const categoryMap: Record<string, string> = {
            'SALES_LEAD': 'Sales Lead',
            'SUPPORT_REQUEST': 'Support Request',
            'INTERNAL': 'Internal',
            'OTHER': 'Other'
        };
        return categoryMap[category] || category.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase());
    };

    const getStatusIcon = (status: string) => {
        const iconMap: Record<string, string> = {
            'pending': '⏳',
            'reply_generated': '✏️',
            'reply_sent': '✅',
            'no_reply_needed': '🚫'
        };
        return iconMap[status] || '❓';
    };

    const formatStatus = (status: string) => {
        const statusMap: Record<string, string> = {
            'pending': 'Pending',
            'reply_generated': 'Reply Drafted',
            'reply_sent': 'Reply Sent',
            'no_reply_needed': 'No Reply Needed'
        };
        return statusMap[status] || status.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase());
    };

    const formatDate = (dateString: string) => {
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', {
            month: 'short',
            day: 'numeric',
            year: 'numeric',
            hour: 'numeric',
            minute: '2-digit'
        });
    };

    const handleRetriage = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        try {
            await emailService.retriage(email.id);
            onUpdate();
        } catch (error) {
            console.error('Failed to retriage:', error);
            showError('Failed to classify & reply');
        } finally {
            setLoading(false);
        }
    };

    const handleGenerateReply = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        try {
            await emailService.generateReply(email.id);
            onUpdate();
        } catch (error) {
            console.error('Failed to generate reply:', error);
            showError('Failed to generate reply');
        } finally {
            setLoading(false);
        }
    };

    const handleSendReply = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        try {
            await emailService.sendReply(email.id, replyBody);
            showSuccess('Reply sent successfully!');
            onUpdate();
        } catch (error) {
            console.error('Failed to send reply:', error);
            showError('Failed to send reply');
        } finally {
            setLoading(false);
        }
    };

    const isReplySent = email.processing_status === 'reply_sent';

    return (
        <div className="email-card">
            <div className="email-card-header">
                <div className="email-meta">
                    <div className="email-sender">
                        <span className="sender-avatar">
                            {email.sender ? email.sender[0].toUpperCase() : '?'}
                        </span>
                        <div className="sender-info">
                            <strong className="sender-name">{email.sender || 'Unknown'}</strong>
                            <span className="email-date">{formatDate(email.received_at)}</span>
                        </div>
                    </div>
                </div>
                <div className="email-badges">
                    <span className={`badge badge-status badge-status-${(email.processing_status || 'pending').toLowerCase().replace(/_/g, '-')}`}>
                        <span className="badge-icon">{getStatusIcon(email.processing_status || 'pending')}</span>
                        <span className="badge-text">{formatStatus(email.processing_status || 'pending')}</span>
                    </span>
                    {email.lead_flag && <span className="badge badge-lead">⭐ Lead</span>}
                    {email.category && (
                        <span className={`badge badge-category badge-${email.category.toLowerCase().replace('_', '-')}`}>
                            <span className="badge-icon">{getCategoryIcon(email.category)}</span>
                            <span className="badge-text">{formatCategory(email.category)}</span>
                        </span>
                    )}
                    {email.priority && (
                        <span className={`badge badge-priority badge-${email.priority.toLowerCase()}`}>
                            {email.priority}
                        </span>
                    )}
                </div>
            </div>

            <div className="email-card-body">
                <h3 className="email-subject">{email.subject || '(No Subject)'}</h3>
                {email.snippet && <p className="email-snippet">{email.snippet}</p>}
            </div>

            <div className="email-card-footer">
                {!email.category ? (
                    <form className="inline-form" onSubmit={handleRetriage}>
                        <button type="submit" className="btn btn-secondary btn-sm" disabled={loading}>
                            <span className="btn-icon">🤖</span>
                            {loading ? 'Processing...' : 'Classify & Reply'}
                        </button>
                    </form>
                ) : (
                    <button 
                        type="button" 
                        className="btn btn-outline btn-sm toggle-details"
                        onClick={() => setExpanded(!expanded)}
                    >
                        <span className="btn-icon">{expanded ? '👁️' : '📋'}</span>
                        {expanded ? 'Hide Details' : 'View Details'}
                    </button>
                )}
            </div>

            {expanded && email.category && (
                <div className="email-details" style={{ display: 'block' }}>
                    <div className="details-content">
                        <div className="detail-section">
                            <h4>Email Content</h4>
                            <div className="email-body-preview">{email.body}</div>
                        </div>

                        {email.suggested_reply ? (
                            <div className="detail-section">
                                <h4>{isReplySent ? 'Sent Reply' : 'Suggested Reply'}</h4>
                                <form className="reply-form" onSubmit={handleSendReply}>
                                    <textarea 
                                        rows={8}
                                        className={`reply-textarea ${isReplySent ? 'reply-sent' : ''}`}
                                        placeholder="Edit the suggested reply before sending..."
                                        value={replyBody}
                                        onChange={(e) => setReplyBody(e.target.value)}
                                        disabled={isReplySent}
                                    />
                                    <div className="form-actions">
                                        <button 
                                            type="submit" 
                                            className={`btn ${isReplySent ? 'btn-secondary' : 'btn-success'}`}
                                            disabled={loading || isReplySent}
                                        >
                                            <span className="btn-icon">{isReplySent ? '✅' : '✉️'}</span>
                                            {loading ? 'Sending...' : (isReplySent ? 'Reply Sent' : 'Send Reply')}
                                        </button>
                                    </div>
                                </form>
                            </div>
                        ) : (
                            <div className="detail-section">
                                <div className="empty-state">
                                    <p>No reply generated yet.</p>
                                    <form className="inline-form generate-reply-form" onSubmit={handleGenerateReply}>
                                        <button type="submit" className="btn btn-secondary btn-sm" disabled={loading}>
                                            <span className="btn-icon">✏️</span>
                                            {loading ? 'Generating...' : 'Generate Reply'}
                                        </button>
                                    </form>
                                </div>
                            </div>
                        )}
                    </div>
                </div>
            )}
        </div>
    );
};
