import { SignupRequest, SigninRequest } from '../types/auth';

/**
 * Validates email format using standard regex
 */
export function validateEmail(email: string): boolean {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

/**
 * Validates password strength
 * Requirements: minimum 8 characters, at least one uppercase, lowercase, number, and special character
 */
export function validatePassword(password: string): boolean {
  if (password.length < 8) {
    return false;
  }

  // At least one uppercase letter
  const hasUpperCase = /[A-Z]/.test(password);
  // At least one lowercase letter
  const hasLowerCase = /[a-z]/.test(password);
  // At least one digit
  const hasDigit = /\d/.test(password);
  // At least one special character
  const hasSpecialChar = /[!@#$%^&*(),.?":{}|<>]/.test(password);

  return hasUpperCase && hasLowerCase && hasDigit && hasSpecialChar;
}

/**
 * Validates signup request data
 */
export function validateSignupRequest(data: SignupRequest): { isValid: boolean; errors: string[] } {
  const errors: string[] = [];

  if (!data.email) {
    errors.push('Email is required');
  } else if (!validateEmail(data.email)) {
    errors.push('Invalid email format');
  }

  if (!data.password) {
    errors.push('Password is required');
  } else if (!validatePassword(data.password)) {
    errors.push('Password must be at least 8 characters with uppercase, lowercase, number, and special character');
  }

  return {
    isValid: errors.length === 0,
    errors
  };
}

/**
 * Validates signin request data
 */
export function validateSigninRequest(data: SigninRequest): { isValid: boolean; errors: string[] } {
  const errors: string[] = [];

  if (!data.email) {
    errors.push('Email is required');
  } else if (!validateEmail(data.email)) {
    errors.push('Invalid email format');
  }

  if (!data.password) {
    errors.push('Password is required');
  }

  return {
    isValid: errors.length === 0,
    errors
  };
}