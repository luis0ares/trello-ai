export interface TypedResponse<T> extends Response {
  json: () => Promise<T>;
}

export interface TaskType {
  id: string;
  title: string;
  description?: string;
  position: number;
}

export interface BoardType {
  id: string;
  title: string;
  position: number;
  tasks: TaskType[];
}

export interface AppData {
  boards: BoardType[];
}
