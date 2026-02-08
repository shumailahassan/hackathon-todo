import { TokenManager } from './token-manager';

export interface DataItem {
  id: string;
  title: string;
  content: string;
  user_id: string;
  created_at: string;
  updated_at: string;
  is_public: boolean;
}

export interface CreateDataRequest {
  title: string;
  content: string;
}

export interface UpdateDataRequest {
  title?: string;
  content?: string;
  is_public?: boolean;
}

class DataService {
  private API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || '/api';

  /**
   * Get all data items for the authenticated user
   */
  async getAll(): Promise<DataItem[]> {
    const token = TokenManager.getAccessToken();
    if (!token) {
      throw new Error('Authentication required');
    }

    const response = await fetch(`${this.API_BASE_URL}/data`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      if (response.status === 401) {
        throw new Error('Unauthorized: Please log in again');
      }
      throw new Error('Failed to fetch data items');
    }

    return response.json();
  }

  /**
   * Get a specific data item by ID
   */
  async getById(id: string): Promise<DataItem> {
    const token = TokenManager.getAccessToken();
    if (!token) {
      throw new Error('Authentication required');
    }

    const response = await fetch(`${this.API_BASE_URL}/data/${id}`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      if (response.status === 401) {
        throw new Error('Unauthorized: Please log in again');
      } else if (response.status === 404) {
        throw new Error('Data item not found');
      }
      throw new Error('Failed to fetch data item');
    }

    return response.json();
  }

  /**
   * Create a new data item
   */
  async create(data: CreateDataRequest): Promise<DataItem> {
    const token = TokenManager.getAccessToken();
    if (!token) {
      throw new Error('Authentication required');
    }

    const response = await fetch(`${this.API_BASE_URL}/data`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      if (response.status === 401) {
        throw new Error('Unauthorized: Please log in again');
      }
      const error = await response.json();
      throw new Error(error.detail || 'Failed to create data item');
    }

    return response.json();
  }

  /**
   * Update an existing data item
   */
  async update(id: string, data: UpdateDataRequest): Promise<DataItem> {
    const token = TokenManager.getAccessToken();
    if (!token) {
      throw new Error('Authentication required');
    }

    const response = await fetch(`${this.API_BASE_URL}/data/${id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      if (response.status === 401) {
        throw new Error('Unauthorized: Please log in again');
      } else if (response.status === 404) {
        throw new Error('Data item not found');
      }
      const error = await response.json();
      throw new Error(error.detail || 'Failed to update data item');
    }

    return response.json();
  }

  /**
   * Delete a data item by ID
   */
  async delete(id: string): Promise<void> {
    const token = TokenManager.getAccessToken();
    if (!token) {
      throw new Error('Authentication required');
    }

    const response = await fetch(`${this.API_BASE_URL}/data/${id}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      if (response.status === 401) {
        throw new Error('Unauthorized: Please log in again');
      } else if (response.status === 404) {
        throw new Error('Data item not found');
      }
      throw new Error('Failed to delete data item');
    }
  }
}

export default new DataService();