'use client';

import { useState, useEffect } from 'react';
import { ArrowPathIcon, ExclamationCircleIcon } from '@heroicons/react/24/outline';
import RequestTestsModal from './components/RequestTestsModal';

interface PullRequest {
  id: number;
  title: string;
  number: number;
  html_url: string;
  user: {
    login: string;
  };
  hasTests: boolean;
  repository: {
    name: string;
    full_name: string;
  };
}

interface ModalState {
  isOpen: boolean;
  status: 'loading' | 'error' | 'success';
  comment?: string;
  error?: string;
}

export default function Home() {
  const [pullRequests, setPullRequests] = useState<PullRequest[]>([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [mounted, setMounted] = useState(false);
  const [modalState, setModalState] = useState<ModalState>({
    isOpen: false,
    status: 'loading'
  });

  useEffect(() => {
    setMounted(true);
  }, []);

  const fetchPRs = async () => {
    try {
      const response = await fetch('/api/pull-requests');
      const data = await response.json();
      setPullRequests(data);
    } catch (error) {
      console.error('Error fetching PRs:', error);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  const handleRefresh = () => {
    setRefreshing(true);
    fetchPRs();
  };

  const handleRequestTests = async (pr: PullRequest) => {
    setModalState({
      isOpen: true,
      status: 'loading'
    });

    try {
      const response = await fetch('/api/request-tests', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          owner: pr.repository.full_name.split('/')[0],
          repo: pr.repository.name,
          prNumber: pr.number,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'Failed to request tests');
      }

      setModalState({
        isOpen: true,
        status: 'success',
        comment: data.comment
      });

      // Refresh the PR list to update the status
      fetchPRs();
    } catch (error) {
      console.error('Error requesting tests:', error);
      setModalState({
        isOpen: true,
        status: 'error',
        error: error instanceof Error ? error.message : 'An unknown error occurred'
      });
    }
  };

  const handleCloseModal = () => {
    setModalState(prev => ({ ...prev, isOpen: false }));
  };

  useEffect(() => {
    fetchPRs();
  }, []);

  // Prevent hydration issues by not rendering until mounted
  if (!mounted) {
    return null;
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <main className="container mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Pull Requests</h1>
        <button
          onClick={handleRefresh}
          className="flex items-center gap-2 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors disabled:opacity-50"
          disabled={refreshing}
        >
          <ArrowPathIcon className={`h-5 w-5 ${refreshing ? 'animate-spin' : ''}`} />
          Refresh
        </button>
      </div>

      <div className="grid gap-4">
        {pullRequests.map((pr) => (
          <div
            key={pr.id}
            className="border rounded-lg p-4 bg-white dark:bg-gray-800 shadow hover:shadow-md transition-shadow"
          >
            <div className="flex justify-between items-start">
              <div>
                <a
                  href={pr.html_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-xl font-semibold text-blue-600 dark:text-blue-400 hover:underline"
                >
                  {pr.title}
                </a>
                <p className="text-gray-600 dark:text-gray-400">
                  #{pr.number} by {pr.user.login} in {pr.repository.full_name}
                </p>
              </div>
              {!pr.hasTests && (
                <button
                  onClick={() => handleRequestTests(pr)}
                  className="flex items-center gap-2 px-3 py-1 bg-yellow-100 dark:bg-yellow-900 text-yellow-800 dark:text-yellow-200 rounded-full hover:bg-yellow-200 dark:hover:bg-yellow-800 transition-colors"
                >
                  <ExclamationCircleIcon className="h-5 w-5" />
                  Request Tests
                </button>
              )}
            </div>
          </div>
        ))}

        {pullRequests.length === 0 && (
          <p className="text-center text-gray-500 dark:text-gray-400 py-8">No pull requests found.</p>
        )}
      </div>

      <RequestTestsModal
        isOpen={modalState.isOpen}
        onClose={handleCloseModal}
        status={modalState.status}
        comment={modalState.comment}
        error={modalState.error}
      />
    </main>
  );
}
