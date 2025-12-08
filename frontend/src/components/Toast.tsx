import React, { useEffect } from 'react';
import { Icons } from './Icons';

export type ToastType = 'success' | 'error' | 'info';

export interface ToastProps {
  id: string;
  message: string;
  type: ToastType;
  onClose: (id: string) => void;
  duration?: number;
}

export const Toast = ({ id, message, type, onClose, duration = 3000 }: ToastProps) => {
  useEffect(() => {
    const timer = setTimeout(() => {
      onClose(id);
    }, duration);

    return () => clearTimeout(timer);
  }, [id, duration, onClose]);

  const getIcon = () => {
    switch (type) {
      case 'success': return <Icons.Check />;
      case 'error': return <Icons.Alert />;
      case 'info': return <Icons.LifeBuoy />; // Using LifeBuoy as info icon or maybe Alert
      default: return <Icons.LifeBuoy />;
    }
  };

  return (
    <div className={`toast toast-${type}`}>
      <span className="toast-icon">{getIcon()}</span>
      <span className="toast-message">{message}</span>
      <button className="alert-close" onClick={() => onClose(id)}>&times;</button>
    </div>
  );
};
