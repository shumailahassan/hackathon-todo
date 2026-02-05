import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import { TokenManager } from '../lib/token-manager';

interface ProtectedRouteProps {
  children: React.ReactNode;
}

export default function ProtectedRoute({ children }: ProtectedRouteProps) {
  const router = useRouter();
  const [isAuthorized, setIsAuthorized] = useState<boolean | null>(null);

  useEffect(() => {
    const checkAuth = async () => {
      if (!TokenManager.hasAccessToken()) {
        // No token, redirect to login
        router.push('/login');
        setIsAuthorized(false);
        return;
      }

      if (TokenManager.isAccessTokenExpired()) {
        // Token is expired, redirect to login
        // In a real app, you might try to refresh the token here
        TokenManager.removeTokens();
        router.push('/login');
        setIsAuthorized(false);
        return;
      }

      // Token is valid
      setIsAuthorized(true);
    };

    checkAuth();
  }, [router]);

  if (isAuthorized === null) {
    // Loading state while checking authentication
    return (
      <div className="flex justify-center items-center h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-500"></div>
      </div>
    );
  }

  if (isAuthorized === false) {
    // Redirect is happening, show a message or nothing
    return null;
  }

  // User is authenticated, render children
  return <>{children}</>;
}