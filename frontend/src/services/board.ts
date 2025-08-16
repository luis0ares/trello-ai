import { TypedResponse } from "@/types";

async function createBoard(
  name: string
): Promise<TypedResponse<{ id: string; name: string }>> {
  return await fetch(`${process.env.NEXT_PUBLIC_BASE_URL}/boards`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ name }),
  });
}

async function getBoards(): Promise<
  TypedResponse<{ id: string; name: string }[]>
> {
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

export const BoardService = {
  createBoard,
  getBoards,
  deleteBoard,
};
