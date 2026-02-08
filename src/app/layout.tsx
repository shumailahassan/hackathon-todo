import React from 'react';
import { Providers } from '../lib/providers';
import './globals.css';

export const metadata = {
  title: 'Todo Web Application',
  description: 'A full-stack todo web application with authentication and data management',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <Providers>
          {children}
        </Providers>
      </body>
    </html>
  );
}