import React from 'react';
import { Button } from '@/components/ui/button';
import { clearChatContext } from '@/api/chat';

interface ClearContextButtonProps {
  onClear: () => void;
  onNotify: (message: string, severity: 'success' | 'error') => void;
}

export default function ClearContextButton({ onClear, onNotify }: ClearContextButtonProps) {
  const handleClick = async () => {
    try {
      const result = await clearChatContext();
      if (result.cleared) {
        onClear();
        onNotify('Context cleared successfully.', 'success');
      } else {
        console.error('Backend did not clear the context.');
        onNotify('Backend did not clear the context.', 'error');
      }
    } catch (error) {
      console.error('Failed to clear context', error);
      onNotify('Failed to clear context.', 'error');
    }
  };

  return (
    <Button
      onClick={handleClick}
      className="bg-destructive text-destructive-foreground hover:bg-destructive/90 focus:ring-2 focus:ring-offset-2 focus:ring-destructive rounded-full"
    >
      Clear Context
    </Button>
  );
}
