'use client';

import React from 'react';
import Head from 'next/head';
import PasswordResetForm from '../components/auth/PasswordResetForm';
import Link from 'next/link';

interface ResetPasswordPageProps {
  token?: string; // Optional token for when this page is accessed via a reset link
}

const ResetPasswordPage: React.FC<ResetPasswordPageProps> = ({ token }) => {
  const mode = token ? 'reset' : 'forgot';

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <Head>
        <title>Reset Password | Authentication App</title>
        <meta name="description" content="Reset your password" />
      </Head>

      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <h1 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
          Authentication App
        </h1>
        <p className="mt-2 text-center text-sm text-gray-600">
          Remember your password?{' '}
          <Link href="/login" className="font-medium text-indigo-600 hover:text-indigo-500">
            Back to login
          </Link>
        </p>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <div className="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
          <PasswordResetForm mode={mode} />
        </div>
      </div>
    </div>
  );
};

export default ResetPasswordPage;