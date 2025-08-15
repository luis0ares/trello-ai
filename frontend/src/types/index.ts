export interface TaskType {
  id: string;
  content: string;
}

export interface BoardType {
  id: string;
  title: string;
  tasks: TaskType[];
}

export interface AppData {
  boards: BoardType[];
}