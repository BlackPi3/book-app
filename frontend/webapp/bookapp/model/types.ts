export interface IBook {
    id?: number;
    title: string;
    author: string;
    created_on?: string;
    created_by: string;
}

export interface IBookCreate {
    title: string;
    author: string;
    created_by: string;
}

export interface IBookUpdate {
    title?: string;
    author?: string;
}

export interface IBookResponse {
    id: number;
    title: string;
    author: string;
    created_on: string;
    created_by: string;
}

export interface IApiResponse<T> {
    data?: T;
    error?: string;
    message?: string;
}

export interface IBookSearchParams {
    title?: string;
    author?: string;
    created_by?: string;
}
