export interface User {
    login: string;
}

export interface Repository {
    name: string;
    full_name: string;
}

// Raw API response interface
export interface RawPullRequestData {
    id: number;
    number: number;
    title: string;
    html_url: string;
    user: User;
    repository: Repository;
    hasTests?: boolean;
}

export interface PullRequest {
    id: number;
    number: number;
    title: string;
    html_url: string;
    url: string;  // For the component's href
    user: User;
    repository: Repository;
    hasTests?: boolean;  // Optional to match backend model
    owner: string;  // Derived from repository.full_name
    repo: string;   // Derived from repository.name
}

export interface RequestTestsPayload {
    owner: string;
    repo: string;
    prNumber: number;
    comment?: string;  // Optional for initial request, required for posting
} 