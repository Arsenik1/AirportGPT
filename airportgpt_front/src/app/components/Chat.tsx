import React, { useState, useRef, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { ToastProvider } from '@/components/ui/toast';
import { LoadingSpinner } from './LoadingSpinner';
import ClearContextButton from './ClearContextButton';
import ChatBox from './ChatBox';
import { sendChatMessage } from '@/api/chat';
import TopToast from './TopToast';
import { motion } from 'framer-motion';
import RoundButton from './RoundButton';

interface Message {
  id: string;
  sender: 'user' | 'bot' | 'system';
  text: string;
}

export default function Chat() {
  const [message, setMessage] = useState('');
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);
  const [toast, setToast] = useState({
    open: false,
    message: '',
    variant: 'success' as 'success' | 'error'
  });
  const [isInputFocused, setIsInputFocused] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const sendMessage = async () => {
    if (!message.trim()) return;
    const userMsg: Message = { id: Date.now().toString(), sender: 'user', text: message.trim() };
    setMessages((prev) => [...prev, userMsg]);
    setMessage('');
    setLoading(true);

    // Add a temporary bot message for loading state
    const loadingMsg: Message = { id: (Date.now() + 1).toString(), sender: 'bot', text: '' };
    setMessages((prev) => [...prev, loadingMsg]);

    try {
      const data = await sendChatMessage(userMsg.text);
      setMessages((prev) => prev.filter((msg) => msg.id !== loadingMsg.id));
      setMessages((prev) => [
        ...prev,
        { id: (Date.now() + 2).toString(), sender: 'bot', text: data.reply || 'No response generated' }
      ]);
    } catch (error) {
      setMessages((prev) => prev.filter((msg) => msg.id !== loadingMsg.id));
      setMessages((prev) => [
        ...prev,
        { id: (Date.now() + 2).toString(), sender: 'bot', text: 'Error connecting to server.' }
      ]);
    }
    setLoading(false);
  };

  const handleClear = () => setMessages([]);
  const handleToastClose = () => setToast({ ...toast, open: false });
  const showNotification = (msg: string, variant: 'success' | 'error') =>
    setToast({ open: true, message: msg, variant });

  return (
    <ToastProvider>
      <div
        className="fixed inset-0 bg-background text-foreground flex flex-col border border-border"
        style={{ perspective: '1000px' }}
      >
        {/* Sleek Animated Header with 3D effect */}
        <motion.header
          className="flex items-center justify-between bg-primary p-4 shadow-2xl rounded-lg transform"
          style={{ perspective: '800px' }}
          initial={{ y: -50, opacity: 0, rotateX: -10 }}
          animate={{ y: 0, opacity: 1, rotateX: 0 }}
          transition={{ type: 'spring', stiffness: 100, damping: 20 }}
        >
          <motion.div
            className="flex items-center"
            whileHover={{ scale: 1.05 }}
            transition={{ type: 'spring', stiffness: 300, damping: 20 }}
          >
            <ClearContextButton onClear={handleClear} onNotify={showNotification} />
          </motion.div>
          <motion.h1
            className="text-primary-foreground text-xl font-bold"
            initial={{ scale: 0.8, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ delay: 0.2, duration: 0.5 }}
          >
            AirportGPT Chat Interface
          </motion.h1>
          <motion.div className="w-8" />
        </motion.header>

        {/* Chat Box */}
        <ChatBox messages={messages} messagesEndRef={messagesEndRef} />

        {/* Unified Input Area with 3D floating effect */}
        <motion.div
          className="p-4 bg-card"
          style={{
            perspective: '800px',
            background: 'linear-gradient(to top, rgb(0, 0, 0), transparent)',  // updated gradient background
            pointerEvents: 'none' // disable pointer events on the outer container
          }}
          initial={{ opacity: 0, y: 20, scale: 0.98, rotateX: -5 }}
          animate={{ opacity: 1, y: 0, scale: 1, rotateX: 0 }}
          transition={{ duration: 0.5 }}
        >
          <div className="flex justify-center">
            <motion.div
              className="flex items-center gap-2 rounded-full border border-border shadow-2xl bg-muted p-1 w-full max-w-3xl transition-all focus-within:ring-2 focus-within:ring-primary focus-within:border-primary transform"
              style={{ pointerEvents: 'auto' }} // added pointer events to enable hover
              animate={isInputFocused ? { translateY: -3, scale: 1.02, rotateX: 3 } : {}}
              whileHover={!isInputFocused ? { translateY: -3, scale: 1.02, rotateX: 3 } : {}}
              transition={{ duration: 0.2 }}
            >
              <Input
                placeholder="Type your message..."
                value={message}
                onFocus={() => setIsInputFocused(true)}
                onBlur={() => setIsInputFocused(false)}
                onChange={(e) => setMessage(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
                className="flex-1 bg-transparent text-muted-foreground outline-none px-4 py-2 focus:ring-0 focus-visible:ring-0"
              />
              <RoundButton onClick={sendMessage} disabled={loading}>
                Send
              </RoundButton>
            </motion.div>
          </div>
        </motion.div>
      </div>

      <TopToast
        open={toast.open}
        message={toast.message}
        variant={toast.variant}
        onOpenChange={handleToastClose}
      />
    </ToastProvider>
  );
}
