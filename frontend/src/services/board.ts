import { TypedResponse } from "@/types";

async function createBoard(
  name: string,
  position: number
): Promise<TypedResponse<{ id: string; name: string; position: number }>> {
  return await fetch(`${process.env.NEXT_PUBLIC_BASE_URL}/boards`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ name, position }),
  });
}

type BoardsWithTasks = {
  id: string;
  name: string;
  position: number;
  tasks: { id: string; title: string; description: string; position: number }[];
};

async function getBoards(): Promise<TypedResponse<BoardsWithTasks[]>> {
  return await fetch(`${process.env.NEXT_PUBLIC_BASE_URL}/boards`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  });
}

async function deleteBoard(id: string): Promise<TypedResponse<null>> {
  return await fetch(`${process.env.NEXT_PUBLIC_BASE_URL}/boards/${id}`, {
    method: "DELETE",
    headers: {
      "Content-Type": "application/json",
    },
  });
}

async function updateBoard(
  id: string,
  name: string,
  position: number
): Promise<TypedResponse<{ id: string; name: string }>> {
  return await fetch(`${process.env.NEXT_PUBLIC_BASE_URL}/boards/${id}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ name, position }),
  });
}

export const BoardService = {
  createBoard,
  getBoards,
  deleteBoard,
  updateBoard,
};
