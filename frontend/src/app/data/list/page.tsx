import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';

export default function DataListPage() {
  const router = useRouter();
  const [dataItems, setDataItems] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check authentication and fetch user data
    const fetchData = async () => {
      try {
        const accessToken = localStorage.getItem('accessToken');
        if (!accessToken) {
          router.push('/login');
          return;
        }

        const response = await fetch('/api/data', {
          headers: {
            'Authorization': Bearer ${accessToken},
          },
        });

        if (!response.ok) {
          router.push('/login');
          return;
        }

        const data = await response.json();
        setDataItems(data);
      } catch (err) {
        console.error('Error fetching data:', err);
        router.push('/login');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return <div className="flex justify-center items-center h-screen">Loading...</div>;
  }

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
                onClick={() => {
                  localStorage.removeItem('accessToken');
                  localStorage.removeItem('refreshToken');
                  router.push('/login');
                }}
                className="ml-4 px-3 py-2 rounded-md text-sm font-medium text-gray-900 hover:text-gray-900 hover:bg-gray-100"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </nav>

      <main className="py-6">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="pb-5 border-b border-gray-200">
            <h1 className="text-2xl font-semibold text-gray-900">Your Data</h1>
          </div>
          
          <div className="mt-6">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-lg font-medium text-gray-900">All Records</h2>
              <button
                onClick={() => router.push('/data/create')}
                className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
              >
                Create New
              </button>
            </div>
            
            {dataItems.length === 0 ? (
              <div className="bg-white shadow overflow-hidden sm:rounded-md">
                <ul className="divide-y divide-gray-200">
                  <li>
                    <div className="px-4 py-4 sm:px-6">
                      <div className="flex items-center justify-between">
                        <p className="text-sm font-medium text-indigo-600 truncate">No data records yet</p>
                      </div>
                      <div className="mt-2 sm:flex sm:justify-between">
                        <div className="sm:flex">
                          <p className="flex items-center text-sm text-gray-500">
                            Create your first data record to get started
                          </p>
                        </div>
                      </div>
                    </div>
                  </li>
                </ul>
              </div>
            ) : (
              <div className="bg-white shadow overflow-hidden sm:rounded-md">
                <ul className="divide-y divide-gray-200">
                  {dataItems.map((item) => (
                    <li key={item.id}>
                      <a href={`/data/${item.id}`} className="block hover:bg-gray-50">
                        <div className="px-4 py-4 sm:px-6">
                          <div className="flex items-center justify-between">
                            <p className="text-sm font-medium text-indigo-600 truncate">
                              {item.title}
                            </p>
                            <div className="ml-2 flex flex-shrink-0">
                              <p className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                                Active
                              </p>
                            </div>
                          </div>
                          <div className="mt-2 sm:flex sm:justify-between">
                            <div className="sm:flex">
                              <p className="flex items-center text-sm text-gray-500">
                                {item.content.substring(0, 100)}...
                              </p>
                            </div>
                            <div className="mt-2 flex items-center text-sm text-gray-500 sm:mt-0">
                              <p>{new Date(item.created_at).toLocaleDateString()}</p>
                            </div>
                          </div>
                        </div>
                      </a>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}
