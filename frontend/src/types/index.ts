export interface TypedResponse<T> extends Response {
  json: () => Promise<T>;
}

export interface TaskType {
  id: string;
  title: string;
  description?: string;
}

export interface BoardType {
  id: string;
  title: string;
  tasks: TaskType[];
}

export interface AppData {
  boards: BoardType[];
}
