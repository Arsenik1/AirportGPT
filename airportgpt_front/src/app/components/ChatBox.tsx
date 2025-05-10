import React, { useState } from 'react';
import { Copy, Check } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { motion, AnimatePresence } from 'framer-motion';
import { LoadingSpinner } from './LoadingSpinner';
import './ChatBoxScrollbar.css'; // import custom scrollbar styles
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import rehypeRaw from 'rehype-raw';
import { Highlight, themes } from 'prism-react-renderer';
import type { Components } from 'react-markdown';

interface Message {
  id: string; // now using id as a key
  sender: 'user' | 'bot' | 'system';
  text: string;
}

interface ChatBoxProps {
  messages: Message[];
  messagesEndRef: React.RefObject<HTMLDivElement>;
}

export default function ChatBox({ messages, messagesEndRef }: ChatBoxProps) {
  // New state for copy button
  const [copiedMsgId, setCopiedMsgId] = useState<string | null>(null);

  const getAlignment = (sender: Message['sender']) => {
    if (sender === 'system') return 'justify-center';
    if (sender === 'user') return 'justify-end';
    return 'justify-start';
  };

  const getBgColor = (sender: Message['sender']) => {
    if (sender === 'user') return 'bg-primary';
    if (sender === 'bot') return 'bg-secondary';
    return 'bg-transparent';
  };

  const getTextColor = (sender: Message['sender']) => {
    if (sender === 'user') return 'text-primary-foreground';
    if (sender === 'bot') return 'text-secondary-foreground';
    return 'text-foreground';
  };

  const getCopyTheme = (_sender: Message['sender']) => {
    return 'text-foreground hover:bg-transparent';
  };

  // Adjusted variants: user messages slide in from right; bot messages slide in from left.
  const messageVariants = {
    user: {
      initial: { x: 100, opacity: 0 },
      animate: { x: 0, opacity: 1 },
      exit: { x: 100, opacity: 0 }
    },
    bot: {
      initial: { x: -100, opacity: 0 },
      animate: { x: 0, opacity: 1 },
      exit: { x: -100, opacity: 0 }
    },
    system: {
      initial: { scale: 0.8, opacity: 0 },
      animate: { scale: 1, opacity: 1 },
      exit: { scale: 0.8, opacity: 0 }
    }
  };

  return (
    <div className="flex-1 overflow-y-auto overflow-x-hidden p-4 chatbox-scroll" style={{ marginBottom: '-5rem', paddingBottom: '4rem' }}>
      <ul className="space-y-2">
      <AnimatePresence>
        {messages.map((msg) => (
        <motion.li
          key={msg.id}
          className={`w-full flex ${getAlignment(msg.sender)} px-2`}
          variants={messageVariants[msg.sender]}
          initial="initial"
          animate="animate"
          exit="exit"
          transition={{ duration: 0.25, ease: 'easeOut' }} // updated: faster animation
        >
          <motion.div
          className={`group relative p-2 rounded-3xl shadow max-w-[80%] ${getBgColor(msg.sender)} ${getTextColor(msg.sender)}`}
          whileHover={{ scale: 1.02 }}
          transition={{ type: 'spring', stiffness: 300, damping: 20 }}
          >
          {msg.sender === 'bot' && msg.text === '' ? (
            <div className="flex items-center space-x-2">
            <LoadingSpinner size={16} className="w-4 h-4" />
            <span>Loading...</span>
            </div>
          ) : (
            <motion.div
              className="markdown-content whitespace-pre-line"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.05, duration: 0.15 }}
            >
              <ReactMarkdown
                remarkPlugins={[remarkGfm]}
                components={{
                  code({ node, inline, className, children, ...props }: { node?: any; inline?: boolean; className?: string; children?: React.ReactNode; [prop: string]: any }) {
                    const match = /language-(\w+)/.exec(className || '');
                    return !inline && match ? (
                      <Highlight
                        theme={themes.nightOwl}
                        code={String(children).replace(/\n$/, '')}
                        language={match[1]}
                      >
                        {({className, style, tokens, getLineProps, getTokenProps}) => (
                          <pre className={className} style={{...style, padding: '1em', borderRadius: '0.5em', overflow: 'auto'}}>
                            {tokens.map((line, i) => (
                              <div key={i} {...getLineProps({line, key: i})}>
                                {line.map((token, key) => (
                                  <span key={key} {...getTokenProps({token, key})} />
                                ))}
                              </div>
                            ))}
                          </pre>
                        )}
                      </Highlight>
                    ) : (
                      <code className={className} {...props}>
                        {children}
                      </code>
                    );
                  },
                  a: ({node, ...props}) => (
                    <a 
                      {...props} 
                      target="_blank" 
                      rel="noopener noreferrer" 
                      className="text-blue-400 hover:underline"
                    />
                  ),
                  h1: ({node, ...props}) => (
                    <h1 {...props} className="text-xl font-bold my-2" />
                  ),
                  h2: ({node, ...props}) => (
                    <h2 {...props} className="text-lg font-bold my-2" />
                  ),
                  h3: ({node, ...props}) => (
                    <h3 {...props} className="text-md font-bold my-1" />
                  ),
                  ul: ({node, ...props}) => (
                    <ul {...props} className="list-disc ml-4 my-1" />
                  ),
                  ol: ({node, ...props}) => (
                    <ol {...props} className="list-decimal ml-4 my-1" />
                  ),
                  blockquote: ({node, ...props}) => (
                    <blockquote {...props} className="border-l-4 border-gray-400 pl-2 italic my-2" />
                  ),
                  p: ({node, ...props}) => (
                    <p {...props} className="my-1" />
                  ),
                }}
              >
                {msg.text}
              </ReactMarkdown>
            </motion.div>
          )}
          {(msg.sender === 'user' || (msg.sender === 'bot' && msg.text !== '')) && (
            <Button
            size="icon"
            variant="ghost"
            onClick={() => {
              navigator.clipboard.writeText(msg.text);
              setCopiedMsgId(msg.id);
              // Ensure tick remains for 1 second (1000 ms)
              setTimeout(() => setCopiedMsgId(null), 1500);
            }}
            className={`absolute opacity-0 transition-opacity duration-300 group-hover:opacity-100 ${
              msg.sender === 'user' ? 'right-1' : 'left-1'
            } ${getCopyTheme(msg.sender)}`}
            >
            <AnimatePresence mode="wait">
              {copiedMsgId === msg.id ? (
                <motion.span
                  key="check"
                  initial={{ scale: 0 }}
                  animate={{ scale: 1, transition: { duration: 0.1 } }} // updated: faster icon transition
                  exit={{ scale: 0, transition: { duration: 0.1 } }} // updated: faster icon transition
                >
                  <Check size={16} className="h-4 w-4" />
                </motion.span>
              ) : (
                <motion.span
                  key="copy"
                  initial={{ scale: 0 }}
                  animate={{ scale: 1, transition: { duration: 0.1 } }} // updated: faster icon transition
                  exit={{ scale: 0, transition: { duration: 0.1 } }} // updated: faster icon transition
                >
                  <Copy size={16} className="h-4 w-4" />
                </motion.span>
              )}
            </AnimatePresence>
            </Button>
          )}
          </motion.div>
        </motion.li>
        ))}
      </AnimatePresence>
      <div ref={messagesEndRef} />
      </ul>
    </div>
  );
}
