import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '../../lib/auth-context';
import { useForm } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import * as yup from 'yup';

// Define the validation schema for forgot password
const forgotPasswordSchema = yup.object().shape({
  email: yup.string().email('Invalid email').required('Email is required'),
});

// Define the validation schema for reset password
const resetPasswordSchema = yup.object().shape({
  token: yup.string().required('Reset token is required'),
  newPassword: yup
    .string()
    .min(8, 'Password must be at least 8 characters')
    .matches(/[A-Z]/, 'Password must contain at least one uppercase letter')
    .matches(/[a-z]/, 'Password must contain at least one lowercase letter')
    .matches(/[0-9]/, 'Password must contain at least one number')
    .matches(/[^A-Za-z0-9]/, 'Password must contain at least one special character')
    .required('New password is required'),
  confirmPassword: yup
    .string()
    .oneOf([yup.ref('newPassword')], 'Passwords must match')
    .required('Confirm password is required'),
});

interface ForgotPasswordFormData {
  email: string;
}

interface ResetPasswordFormData {
  token: string;
  newPassword: string;
  confirmPassword: string;
}

interface PasswordResetFormProps {
  mode: 'forgot' | 'reset'; // 'forgot' for requesting reset, 'reset' for resetting with token
}

const PasswordResetForm: React.FC<PasswordResetFormProps> = ({ mode = 'forgot' }) => {
  const { forgotPassword, resetPassword, isLoading } = useAuth();
  const router = useRouter();
  const [successMessage, setSuccessMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [step, setStep] = useState<'request' | 'reset'>(
    mode === 'reset' ? 'reset' : 'request'
  );

  // Initialize form based on mode
  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
    watch,
  } = useForm<ForgotPasswordFormData | ResetPasswordFormData>({
    resolver: yupResolver(
      mode === 'forgot' ? forgotPasswordSchema : resetPasswordSchema
    ),
  });

  const onSubmit = async (data: any) => {
    setError(null);
    setSuccessMessage(null);

    if (mode === 'forgot') {
      // Handle forgot password request
      const { success, error } = await forgotPassword(data.email);

      if (success) {
        setSuccessMessage(
          'Password reset instructions have been sent to your email.'
        );
        reset(); // Clear the form
      } else {
        setError(error || 'Failed to send password reset instructions. Please try again.');
      }
    } else {
      // Handle password reset
      const { success, error } = await resetPassword(data.token, data.newPassword);

      if (success) {
        setSuccessMessage('Your password has been reset successfully. You can now log in with your new password.');
        setTimeout(() => {
          router.push('/login'); // Redirect to login after success
        }, 3000);
        reset(); // Clear the form
      } else {
        setError(error || 'Failed to reset password. Please check your token and try again.');
      }
    }
  };

  return (
    <div className="max-w-md w-full space-y-8">
      <div>
        <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
          {mode === 'forgot' ? 'Reset your password' : 'Enter reset details'}
        </h2>
        <p className="mt-2 text-center text-sm text-gray-600">
          {mode === 'forgot'
            ? 'Enter your email address and we\'ll send you a link to reset your password.'
            : 'Enter your reset token and new password.'}
        </p>
      </div>
      <form className="mt-8 space-y-6" onSubmit={handleSubmit(onSubmit)}>
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
            <span className="block sm:inline">{error}</span>
          </div>
        )}

        {successMessage && (
          <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded relative" role="alert">
            <span className="block sm:inline">{successMessage}</span>
          </div>
        )}

        <input type="hidden" name="remember" defaultValue="true" />
        <div className="rounded-md shadow-sm -space-y-px">
          {mode === 'reset' && (
            <div>
              <label htmlFor="token" className="sr-only">
                Reset Token
              </label>
              <input
                id="token"
                {...register('token')}
                className={`appearance-none rounded-none relative block w-full px-3 py-2 border ${
                  errors.token ? 'border-red-300' : 'border-gray-300'
                } placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm`}
                placeholder="Reset Token"
              />
              {errors.token && (
                <p className="mt-1 text-sm text-red-600">{errors.token.message}</p>
              )}
            </div>
          )}

          {mode === 'forgot' ? (
            <div>
              <label htmlFor="email-address" className="sr-only">
                Email address
              </label>
              <input
                id="email-address"
                {...register('email')}
                className={`appearance-none rounded-none relative block w-full px-3 py-2 border ${
                  errors.email ? 'border-red-300' : 'border-gray-300'
                } placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm`}
                placeholder="Email address"
              />
              {errors.email && (
                <p className="mt-1 text-sm text-red-600">{errors.email.message}</p>
              )}
            </div>
          ) : (
            <>
              <div>
                <label htmlFor="newPassword" className="sr-only">
                  New Password
                </label>
                <input
                  id="newPassword"
                  type="password"
                  {...register('newPassword')}
                  className={`appearance-none rounded-none relative block w-full px-3 py-2 border ${
                    errors.newPassword ? 'border-red-300' : 'border-gray-300'
                  } placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm`}
                  placeholder="New Password"
                />
                {errors.newPassword && (
                  <p className="mt-1 text-sm text-red-600">{errors.newPassword.message}</p>
                )}
              </div>
              <div>
                <label htmlFor="confirmPassword" className="sr-only">
                  Confirm New Password
                </label>
                <input
                  id="confirmPassword"
                  type="password"
                  {...register('confirmPassword')}
                  className={`appearance-none rounded-none relative block w-full px-3 py-2 border ${
                    errors.confirmPassword ? 'border-red-300' : 'border-gray-300'
                  } placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm`}
                  placeholder="Confirm New Password"
                />
                {errors.confirmPassword && (
                  <p className="mt-1 text-sm text-red-600">{errors.confirmPassword.message}</p>
                )}
              </div>
            </>
          )}
        </div>

        <div>
          <button
            type="submit"
            disabled={isLoading}
            className={`group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white ${
              isLoading ? 'bg-gray-400' : 'bg-indigo-600 hover:bg-indigo-700'
            } focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500`}
          >
            {isLoading
              ? (mode === 'forgot' ? 'Sending reset instructions...' : 'Resetting password...')
              : (mode === 'forgot' ? 'Send Reset Instructions' : 'Reset Password')}
          </button>
        </div>
      </form>
    </div>
  );
};

export default PasswordResetForm;