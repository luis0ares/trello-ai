import { TypedResponse } from "@/types";

async function createTask(
  boardId: string,
  title: string,
  position: number,
  description?: string
): Promise<
  TypedResponse<{
    id: string;
    board_id: string;
    title: string;
    position: number;
    description?: string;
  }>
> {
  return await fetch(`${process.env.NEXT_PUBLIC_BASE_URL}/tasks`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ title, description, position, board_id: boardId }),
  });
}

async function deleteTask(id: string): Promise<TypedResponse<null>> {
  return await fetch(`${process.env.NEXT_PUBLIC_BASE_URL}/tasks/${id}`, {
    method: "DELETE",
    headers: {
      "Content-Type": "application/json",
    },
  });
}

async function updateTask(
  id: string,
  boardId: string,
  title: string,
  position: number,
  description?: string
): Promise<
  TypedResponse<{
    id: string;
    board_id: string;
    title: string;
    position: number;
    description?: string;
  }>
> {
  return await fetch(`${process.env.NEXT_PUBLIC_BASE_URL}/tasks/${id}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ title, description, position, board_id: boardId }),
  });
}

export const TaskService = {
  createTask,
  deleteTask,
  updateTask,
};
