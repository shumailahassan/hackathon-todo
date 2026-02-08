'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';

export default function AuthNavigation() {
  const pathname = usePathname();

  const isActive = (path: string) => pathname === path;

  return (
    <div className="flex space-x-4 mb-6">
      <Link
        href="/login"
        className={`px-3 py-2 rounded-md text-sm font-medium ${
          isActive('/login')
            ? 'bg-indigo-100 text-indigo-700'
            : 'text-gray-700 hover:bg-gray-100 hover:text-gray-900'
        }`}
      >
        Sign In
      </Link>
      <Link
        href="/register"
        className={`px-3 py-2 rounded-md text-sm font-medium ${
          isActive('/register')
            ? 'bg-indigo-100 text-indigo-700'
            : 'text-gray-700 hover:bg-gray-100 hover:text-gray-900'
        }`}
      >
        Sign Up
      </Link>
    </div>
  );
}