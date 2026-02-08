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

export interface UserDataList {
  data: DataItem[];
}