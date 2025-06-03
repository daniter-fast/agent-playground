import { Fragment } from 'react'
import { Dialog, Transition } from '@headlessui/react'
import { CheckCircleIcon, XCircleIcon } from '@heroicons/react/24/outline'

interface RequestTestsModalProps {
  isOpen: boolean;
  onClose: () => void;
  status: 'loading' | 'error' | 'success';
  comment?: string;
  error?: string;
}

export default function RequestTestsModal({
  isOpen,
  onClose,
  status,
  comment,
  error
}: RequestTestsModalProps) {
  return (
    <Transition.Root show={isOpen} as={Fragment}>
      <Dialog as="div" className="relative z-10" onClose={onClose}>
        <Transition.Child
          as={Fragment}
          enter="ease-out duration-300"
          enterFrom="opacity-0"
          enterTo="opacity-100"
          leave="ease-in duration-200"
          leaveFrom="opacity-100"
          leaveTo="opacity-0"
        >
          <div className="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" />
        </Transition.Child>

        <div className="fixed inset-0 z-10 w-screen overflow-y-auto">
          <div className="flex min-h-full items-end justify-center p-4 text-center sm:items-center sm:p-0">
            <Transition.Child
              as={Fragment}
              enter="ease-out duration-300"
              enterFrom="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
              enterTo="opacity-100 translate-y-0 sm:scale-100"
              leave="ease-in duration-200"
              leaveFrom="opacity-100 translate-y-0 sm:scale-100"
              leaveTo="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
            >
              <Dialog.Panel className="relative transform overflow-hidden rounded-lg bg-white dark:bg-gray-800 px-4 pb-4 pt-5 text-left shadow-xl transition-all sm:my-8 sm:w-full sm:max-w-lg sm:p-6">
                <div>
                  {status === 'loading' && (
                    <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-blue-100 dark:bg-blue-900">
                      <div className="h-8 w-8 animate-spin rounded-full border-4 border-solid border-current border-r-transparent align-[-0.125em] motion-reduce:animate-[spin_1.5s_linear_infinite]" />
                    </div>
                  )}
                  {status === 'success' && (
                    <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-green-100 dark:bg-green-900">
                      <CheckCircleIcon className="h-8 w-8 text-green-600 dark:text-green-400" />
                    </div>
                  )}
                  {status === 'error' && (
                    <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-red-100 dark:bg-red-900">
                      <XCircleIcon className="h-8 w-8 text-red-600 dark:text-red-400" />
                    </div>
                  )}

                  <div className="mt-3 text-center sm:mt-5">
                    <Dialog.Title as="h3" className="text-lg font-semibold leading-6 text-gray-900 dark:text-white">
                      {status === 'loading' && 'Requesting Tests...'}
                      {status === 'success' && 'Comment Posted Successfully'}
                      {status === 'error' && 'Error Requesting Tests'}
                    </Dialog.Title>
                    <div className="mt-2">
                      {status === 'loading' && (
                        <p className="text-sm text-gray-500 dark:text-gray-400">
                          Analyzing code and generating test recommendations...
                        </p>
                      )}
                      {status === 'success' && comment && (
                        <div className="mt-4 rounded-md bg-gray-50 dark:bg-gray-700 p-4">
                          <pre className="text-sm text-gray-700 dark:text-gray-300 whitespace-pre-wrap">
                            {comment}
                          </pre>
                        </div>
                      )}
                      {status === 'error' && error && (
                        <p className="text-sm text-red-500 dark:text-red-400">
                          {error}
                        </p>
                      )}
                    </div>
                  </div>
                </div>

                <div className="mt-5 sm:mt-6">
                  <button
                    type="button"
                    className="inline-flex w-full justify-center rounded-md bg-blue-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-blue-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-600"
                    onClick={onClose}
                  >
                    {status === 'loading' ? 'Please wait...' : 'Close'}
                  </button>
                </div>
              </Dialog.Panel>
            </Transition.Child>
          </div>
        </div>
      </Dialog>
    </Transition.Root>
  )
} 