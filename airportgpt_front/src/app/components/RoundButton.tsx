import React from 'react';
import { motion, HTMLMotionProps } from 'framer-motion';

interface RoundButtonProps extends HTMLMotionProps<"button"> {
  children: React.ReactNode;
}

export default function RoundButton({ children, ...props }: RoundButtonProps) {
  return (
    <motion.button
      {...props}
    //   whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.95 }}
      transition={{ duration: 0.2, ease: "easeInOut" }}
      className={`bg-primary text-primary-foreground rounded-full px-4 py-2 transition-all disabled:opacity-50 hover:bg-primary/75 ${props.className || ''}`}
    >
      {children}
    </motion.button>
  );
}
