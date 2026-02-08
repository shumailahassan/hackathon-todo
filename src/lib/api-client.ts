// frontend/src/lib/api-client.ts
export const apiClient = {
  login: async ({ email, password }: { email: string; password: string }) => {
    await new Promise((r) => setTimeout(r, 800)); // simulate delay
    if (email === 'test@example.com' && password === '123456') {
      return {
        data: {
          user: {
            id: '1',
            email,
            first_name: 'John',
            last_name: 'Doe',
            is_active: true,
            is_verified: true,
            created_at: new Date().toISOString(),
            updated_at: new Date().toISOString(),
          },
        },
      };
    } else {
      return { error: 'Invalid credentials' };
    }
  },

  register: async (userData: any) => {
    await new Promise((r) => setTimeout(r, 800)); // simulate delay
    if (userData.email !== 'test@example.com') {
      return { data: { user: { ...userData, id: '2', is_active: true, is_verified: true, created_at: new Date().toISOString(), updated_at: new Date().toISOString() } } };
    } else {
      return { error: 'Email already exists' };
    }
  },

  logout: async () => {
    await new Promise((r) => setTimeout(r, 500));
    return { success: true };
  },
};
