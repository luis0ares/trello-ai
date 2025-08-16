"use client";

import { Navbar } from "@/components/layout/navbar";
import { BoardList } from "@/components/ui/board-list";
import { TaskForm } from "@/components/ui/task-form";
import { BoardType, TaskType } from "@/types";
import { DragDropContext, DropResult } from "@hello-pangea/dnd";
import { useState } from "react";

const initialData: BoardType[] = [
  {
    id: "board-1",
    title: "Pending",
    tasks: [
      { id: "task-1", title: "Learn React", description: "Learn React" },
      {
        id: "task-2",
        title: "Read about @hello-pangea/dnd",
        description: "Learn React",
      },
    ],
  },
  {
    id: "board-2",
    title: "Doing",
    tasks: [
      { id: "task-3", title: "Build Trello clone", description: "Learn React" },
    ],
  },
  {
    id: "board-3",
    title: "Done",
    tasks: [
      { id: "task-4", title: "Drink coffee", description: "Learn React" },
    ],
  },
];

export default function Home() {
  const [data, setData] = useState<BoardType[]>(initialData);

  function onDragEnd(result: DropResult) {
    const { destination, source, type } = result;
    if (!destination) return;

    // Moving boards
    if (type === "board") {
      const newBoards = Array.from(data);
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

    const sourceTasks = Array.from(sourceBoard.tasks);
    const [movedTask] = sourceTasks.splice(source.index, 1);

    if (sourceBoard === destBoard) {
      sourceTasks.splice(destination.index, 0, movedTask);
      const newBoards = [...data];
      newBoards[sourceBoardIndex] = { ...sourceBoard, tasks: sourceTasks };
      setData([...newBoards]);
    } else {
      const destTasks = Array.from(destBoard.tasks);
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
      <main className="flex min-h-screen flex-col items-center">
        <Navbar />

        <DragDropContext onDragEnd={onDragEnd}>
          <BoardList boards={data} onAddBoard={onAddBoard} />
        </DragDropContext>
        <TaskForm onAddTask={onAddTask} boards={data} />
      </main>
    </>
  );
}
