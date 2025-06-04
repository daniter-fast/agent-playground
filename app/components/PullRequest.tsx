import { useState } from 'react';
import { PullRequest } from '../types/github';

interface Props {
  pr: PullRequest;
  onUpdate: () => void;
}

export default function PullRequestComponent({ pr, onUpdate }: Props) {
  const [loading, setLoading] = useState(false);
  const [showConfirm, setShowConfirm] = useState(false);
  const [previewComment, setPreviewComment] = useState('');
  const [error, setError] = useState('');

  const handleRequestTests = async () => {
    try {
      setLoading(true);
      setError('');
      
      const response = await fetch('/api/request-tests', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          owner: pr.owner,
          repo: pr.repo,
          prNumber: pr.number,
        }),
      });

      const data = await response.json();
      
      if (!response.ok) {
        throw new Error(data.detail || 'Failed to request tests');
      }

      setPreviewComment(data.comment);
      setShowConfirm(true);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  const handleConfirm = async () => {
    try {
      setLoading(true);
      setError('');
      
      const response = await fetch('/api/post-comment', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          owner: pr.owner,
          repo: pr.repo,
          prNumber: pr.number,
          comment: previewComment,
        }),
      });

      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.detail || 'Failed to post comment');
      }

      // Clear the preview and close the modal
      setShowConfirm(false);
      setPreviewComment('');
      
      // Show success message
      setError(''); // Clear any previous errors
      alert('Comment posted successfully! Check the PR on GitHub.');
      
      // Refresh the PR list
      onUpdate();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="border rounded-lg p-4 mb-4 bg-white dark:bg-gray-800">
      <h3 className="text-lg font-semibold mb-2">
        <a href={pr.html_url} target="_blank" rel="noopener noreferrer" className="text-blue-600 dark:text-blue-400 hover:underline">
          {pr.title}
        </a>
      </h3>
      <p className="text-gray-600 dark:text-gray-400 mb-4">
        #{pr.number} opened by {pr.user.login} in {pr.repository.full_name}
      </p>
      
      {error && (
        <p className="text-red-600 dark:text-red-400 mb-4">{error}</p>
      )}

      <button
        onClick={handleRequestTests}
        disabled={loading || showConfirm}
        className={`px-4 py-2 rounded ${
          loading || showConfirm
            ? 'bg-gray-400 cursor-not-allowed'
            : 'bg-blue-600 hover:bg-blue-700'
        } text-white`}
      >
        {loading ? 'Loading...' : 'Request Tests'}
      </button>

      {showConfirm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4">
          <div className="bg-white dark:bg-gray-800 rounded-lg p-6 max-w-2xl w-full">
            <h3 className="text-xl font-semibold mb-4">Preview Comment</h3>
            <div className="bg-gray-100 dark:bg-gray-700 p-4 rounded mb-4 whitespace-pre-wrap">
              {previewComment}
            </div>
            <div className="flex justify-end space-x-4">
              <button
                onClick={() => setShowConfirm(false)}
                className="px-4 py-2 rounded bg-gray-500 hover:bg-gray-600 text-white"
              >
                Cancel
              </button>
              <button
                onClick={handleConfirm}
                disabled={loading}
                className="px-4 py-2 rounded bg-blue-600 hover:bg-blue-700 text-white"
              >
                {loading ? 'Posting...' : 'Post Comment'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
} 