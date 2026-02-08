'use client';

import { useEffect, useState } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { useAuth } from '../../../lib/auth-context';
import authService from '../../../lib/auth-service';

export default function DataDetailPage({ params }: { params: { id: string } }) {
  const router = useRouter();
  const { id } = params;
  const { isAuthenticated, isLoading, logout } = useAuth();
  const [dataItem, setDataItem] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!isLoading && isAuthenticated) {
      // Fetch the specific data item
      const fetchData = async () => {
        if (!id) return;

        try {
          const response = await authService.makeAuthenticatedRequest(`/data/${id}`, {
            method: 'GET',
          });

          const item = await response.json();
          setDataItem(item);
        } catch (err) {
          console.error('Error fetching data:', err);
          // If unauthorized, redirect to login
          if (err.message.includes('Session expired')) {
            router.push('/login');
          }
        } finally {
          setLoading(false);
        }
      };

      fetchData();
    }
  }, [id, isAuthenticated, isLoading]);

  if (loading || isLoading) {
    return <div className="flex justify-center items-center h-screen">Loading...</div>;
  }

  if (!dataItem) {
    return <div className="flex justify-center items-center h-screen">Data not found</div>;
  }

  const handleDelete = async () => {
    if (!window.confirm('Are you sure you want to delete this item?')) return;

    try {
      const response = await authService.makeAuthenticatedRequest(`/data/${id}`, {
        method: 'DELETE',
      });

      if (response.ok) {
        router.push('/data/list');
      } else {
        alert('Failed to delete item');
      }
    } catch (err) {
      console.error('Error deleting data:', err);
      alert('An error occurred while deleting the item');
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-semibold text-gray-900">Todo Dashboard</h1>
            </div>
            <div className="flex items-center">
              <button
                onClick={async () => {
                  await logout(); // Use the auth context logout
                  router.push('/login');
                }}
                className="ml-4 px-3 py-2 rounded-md text-sm font-medium text-gray-700 hover:text-gray-900 hover:bg-gray-100"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </nav>

      <main className="py-6">
        <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="pb-5 border-b border-gray-200 flex justify-between items-center">
            <h1 className="text-2xl font-semibold text-gray-900">{dataItem.title}</h1>
            <div className="flex space-x-2">
              <button
                onClick={() => router.push(`/data/${id}/edit`)}
                className="inline-flex items-center px-3 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
              >
                Edit
              </button>
              <button
                onClick={handleDelete}
                className="inline-flex items-center px-3 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
              >
                Delete
              </button>
            </div>
          </div>

          <div className="mt-6 bg-white shadow overflow-hidden sm:rounded-lg">
            <div className="px-4 py-5 sm:p-6">
              <div className="mb-4">
                <h2 className="text-lg font-medium text-gray-900">Content</h2>
                <div className="mt-2 text-gray-700 whitespace-pre-wrap">
                  {dataItem.content}
                </div>
              </div>

              <div className="border-t border-gray-200 pt-4 mt-6">
                <dl className="grid grid-cols-1 gap-x-4 gap-y-8 sm:grid-cols-2">
                  <div className="sm:col-span-1">
                    <dt className="text-sm font-medium text-gray-500">Created</dt>
                    <dd className="mt-1 text-sm text-gray-900">
                      {new Date(dataItem.created_at).toLocaleString()}
                    </dd>
                  </div>
                  <div className="sm:col-span-1">
                    <dt className="text-sm font-medium text-gray-500">Last Updated</dt>
                    <dd className="mt-1 text-sm text-gray-900">
                      {new Date(dataItem.updated_at).toLocaleString()}
                    </dd>
                  </div>
                </dl>
              </div>
            </div>
          </div>

          <div className="mt-4 flex justify-start">
            <button
              onClick={() => router.push('/data/list')}
              className="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              Back to List
            </button>
          </div>
        </div>
      </main>
    </div>
  );
}
