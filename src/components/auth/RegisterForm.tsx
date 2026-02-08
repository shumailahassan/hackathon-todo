'use client';
import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '../../lib/auth-context';
import { useForm } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import * as yup from 'yup';

// Validation schema
const registerSchema = yup.object().shape({
  first_name: yup.string().required('First name is required'),
  last_name: yup.string().required('Last name is required'),
  email: yup.string().email('Invalid email').required('Email is required'),
  password: yup.string().min(6, 'Password must be at least 6 characters').required('Password is required'),
  confirmPassword: yup
    .string()
    .oneOf([yup.ref('password')], 'Passwords must match')
    .required('Confirm password is required'),
});

interface RegisterFormData {
  first_name: string;
  last_name: string;
  email: string;
  password: string;
  confirmPassword: string;
}

export default function RegisterForm() {
  const { register: registerUser, isLoading } = useAuth();
  const router = useRouter();
  const [error, setError] = useState<string | null>(null);

  const { register, handleSubmit, formState: { errors }, reset } = useForm<RegisterFormData>({
    resolver: yupResolver(registerSchema),
  });

  const onSubmit = async (data: RegisterFormData) => {
    setError(null);

    const { success, error } = await registerUser({
      email: data.email,
      password: data.password,
      first_name: data.first_name,
      last_name: data.last_name,
    });

    if (success) {
      router.push('/dashboard');
      reset();
    } else {
      setError(error || 'Registration failed.');
    }
  };

  return (
    <div className="w-full">
      <div className="card">
        <h2 className="text-3xl font-bold mb-2 highlight">Create Account</h2>
        <p className="text-gray-600 dark:text-gray-300 mb-6">Join us today to get started</p>

        {error && <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-2 rounded mb-4">{error}</div>}

        <form className="space-y-4" onSubmit={handleSubmit(onSubmit)}>
          <div className="flex gap-4">
            <div className="flex-1">
              <label className="block mb-1 text-sm text-gray-700 dark:text-gray-300">First Name</label>
              <input {...register('first_name')} placeholder="John" className="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 bg-white/85"/>
              {errors.first_name && <p className="text-red-600 text-sm mt-1">{errors.first_name.message}</p>}
            </div>
            <div className="flex-1">
              <label className="block mb-1 text-sm text-gray-700 dark:text-gray-300">Last Name</label>
              <input {...register('last_name')} placeholder="Doe" className="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 bg-white/85"/>
              {errors.last_name && <p className="text-red-600 text-sm mt-1">{errors.last_name.message}</p>}
            </div>
          </div>

          <div>
            <label className="block mb-1 text-sm text-gray-700 dark:text-gray-300">Email</label>
            <input {...register('email')} placeholder="you@example.com" className="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 bg-white/85" type="email"/>
            {errors.email && <p className="text-red-600 text-sm mt-1">{errors.email.message}</p>}
          </div>

          <div>
            <label className="block mb-1 text-sm text-gray-700 dark:text-gray-300">Password</label>
            <input type="password" {...register('password')} placeholder="••••••••" className="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 bg-white/85"/>
            {errors.password && <p className="text-red-600 text-sm mt-1">{errors.password.message}</p>}
          </div>

          <div>
            <label className="block mb-1 text-sm text-gray-700 dark:text-gray-300">Confirm Password</label>
            <input type="password" {...register('confirmPassword')} placeholder="••••••••" className="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 bg-white/85"/>
            {errors.confirmPassword && <p className="text-red-600 text-sm mt-1">{errors.confirmPassword.message}</p>}
          </div>

          <button
            type="submit"
            disabled={isLoading}
            className="w-full py-2 rounded-md font-medium shadow focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 dark:focus:ring-purple-500 bg-gradient-to-r from-indigo-500 to-purple-600 text-white transition-all duration-300 hover:transform hover:-translate-y-0.5 hover:shadow-lg disabled:opacity-70 disabled:cursor-not-allowed"
          >
            {isLoading ? 'Signing up...' : 'Sign up'}
          </button>
        </form>

        <p className="text-center text-gray-600 dark:text-gray-300 mt-6">
          Already have an account? <a href="/login" className="highlight hover:underline">Sign in</a>
        </p>
      </div>
    </div>
  );
}
