"use client";

import { Navbar } from "@/components/layout/navbar";
import { BoardList } from "@/components/ui/board-list";
import { TaskForm } from "@/components/ui/task-form";
import { BoardService } from "@/services/board";
import { BoardType, TaskType } from "@/types";
import { DragDropContext, DropResult } from "@hello-pangea/dnd";
import { useQuery } from "@tanstack/react-query";
import { useEffect, useState } from "react";

async function getBoards(): Promise<BoardType[]> {
  const res = await BoardService.getBoards();
  if (!res.ok) return [];

  const json = await res.json();
  return json.map((board) => {
    return { id: board.id, title: board.name, tasks: [] } as BoardType;
  });
}

export default function Home() {
  const { data, isLoading } = useQuery({
    queryKey: ["boards"],
    queryFn: getBoards,
    initialData: [],
  });

  console.log(data);

  return (
    <>
      <main className="flex min-h-screen flex-col items-center">
        <Navbar />

        {isLoading ? <></> : <TaskBoards boardData={data} />}
      </main>
    </>
  );
}

function TaskBoards({ boardData }: { boardData: BoardType[] }) {
  const [data, setData] = useState<BoardType[]>([]);

  useEffect(() => {
    setData(boardData);
  }, [boardData]);

  function onDragEnd(result: DropResult) {
    const { destination, source, type } = result;
    if (!destination) return;

    // Moving boards
    if (type === "board") {
      const newBoards = [...data];
      const [moved] = newBoards.splice(source.index, 1);
      newBoards.splice(destination.index, 0, moved);
      setData([...newBoards]);
      return;
    }

    // Moving tasks
    const sourceBoardIndex = data.findIndex((b) => b.id === source.droppableId);
    const destBoardIndex = data.findIndex(
      (b) => b.id === destination.droppableId
    );

    const sourceBoard = data[sourceBoardIndex];
    const destBoard = data[destBoardIndex];

    const sourceTasks = [...sourceBoard.tasks];
    const [movedTask] = sourceTasks.splice(source.index, 1);

    if (sourceBoard === destBoard) {
      sourceTasks.splice(destination.index, 0, movedTask);
      const newBoards = [...data];
      newBoards[sourceBoardIndex] = { ...sourceBoard, tasks: sourceTasks };
      setData([...newBoards]);
    } else {
      const destTasks = [...destBoard.tasks];
      destTasks.splice(destination.index, 0, movedTask);

      const newBoards = [...data];
      newBoards[sourceBoardIndex] = { ...sourceBoard, tasks: sourceTasks };
      newBoards[destBoardIndex] = { ...destBoard, tasks: destTasks };
      setData([...newBoards]);
    }
  }

  function onAddTask(boardId: string, task: TaskType) {
    const newData = data.map((board) => {
      if (board.id === boardId) board.tasks.push(task);
      return board;
    });
    setData([...newData]);
  }

  function onAddBoard(board: BoardType) {
    const newData = [...data, board];
    setData(newData);
  }

  return (
    <>
      <DragDropContext onDragEnd={onDragEnd}>
        <BoardList boards={data} onAddBoard={onAddBoard} />
      </DragDropContext>
      <TaskForm onAddTask={onAddTask} boards={data} />
    </>
  );
}
