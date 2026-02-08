import { ReactNode } from 'react';
import AuthNavigation from '@/components/auth/AuthNavigation';

export default function AuthLayout({
  children,
}: {
  children: ReactNode;
}) {
  return (
    <div className="relative min-h-screen flex items-center justify-center overflow-hidden">
      {/* Animated background blobs */}
      <div className="absolute -top-24 -left-24 w-96 h-96 bg-indigo-300 rounded-full blur-3xl opacity-30 animate-blob"></div>
      <div className="absolute top-1/2 -right-24 w-96 h-96 bg-purple-300 rounded-full blur-3xl opacity-30 animate-blob animation-delay-2000"></div>
      <div className="absolute -bottom-24 left-1/3 w-96 h-96 bg-indigo-200 rounded-full blur-3xl opacity-30 animate-blob animation-delay-4000"></div>

      {/* Content container with higher z-index */}
      <div className="relative z-10 max-w-md w-full">
        <div className="text-center mb-8">
          <div className="mx-auto h-12 w-12 rounded-full bg-indigo-600 flex items-center justify-center">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
            </svg>
          </div>
          <h1 className="mt-4 text-3xl font-bold text-gray-900">TodoApp</h1>
          <p className="mt-2 text-gray-600">Manage your tasks efficiently</p>
        </div>
        <div className="bg-white/85 backdrop-blur-sm py-8 px-6 shadow rounded-lg sm:px-10">
          <AuthNavigation />
          {children}
        </div>
      </div>
    </div>
  );
}