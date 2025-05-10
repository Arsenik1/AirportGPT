import React from 'react';
import { Toast, ToastViewport } from '@/components/ui/toast';
import '../styles/toast-animation.css'; // Import the new animation styles

interface TopToastProps {
  open: boolean;
  message: string;
  variant: 'success' | 'error';
  onOpenChange: (open: boolean) => void;
}

export default function TopToast({ open, message, variant, onOpenChange }: TopToastProps) {
  return (
    <ToastViewport className="fixed top-0 right-0 m-4 z-50" style={{ top: 0 }}>
      {open && (
        <Toast
          open={open}
          onOpenChange={onOpenChange}
          variant={variant === 'success' ? 'default' : 'destructive'}
          className="animate-slide-down" // Apply the slide-down animation
        >
          {message}
        </Toast>
      )}
    </ToastViewport>
  );
}
