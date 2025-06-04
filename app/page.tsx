'use client';

import { useState, useEffect } from 'react';
import { ArrowPathIcon } from '@heroicons/react/24/outline';
import { PullRequest, RawPullRequestData } from './types/github';
import PullRequestComponent from './components/PullRequest';

export default function Home() {
  const [pullRequests, setPullRequests] = useState<PullRequest[]>([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  const fetchPRs = async () => {
    try {
      const response = await fetch('/api/pull-requests');
      const data = await response.json();
      
      // Transform the data to match our type definition
      const transformedData: PullRequest[] = (data as RawPullRequestData[]).map((pr) => ({
        ...pr,
        owner: pr.repository.full_name.split('/')[0],
        repo: pr.repository.name,
        url: pr.html_url
      }));
      
      setPullRequests(transformedData);
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
          <PullRequestComponent key={pr.id} pr={pr} onUpdate={fetchPRs} />
        ))}

        {pullRequests.length === 0 && (
          <p className="text-center text-gray-500 dark:text-gray-400 py-8">No pull requests found.</p>
        )}
      </div>
    </main>
  );
}
