"use client";

import { Navbar } from "@/components/layout/navbar";
import { BoardList } from "@/components/board/board-list";
import { TaskForm } from "@/app/(public)/task-form";
import { BoardService } from "@/services/board";
import { TaskService } from "@/services/task";
import { BoardType, TaskType } from "@/types";
import { DragDropContext, DropResult } from "@hello-pangea/dnd";
import { useQuery } from "@tanstack/react-query";
import { useEffect, useState } from "react";
import { toast } from "sonner";
import { ChatSheet, GeneratedTasks } from "./chat-sheet";

async function getBoards(): Promise<BoardType[]> {
  const res = await BoardService.getBoards();
  if (!res.ok) return [];

  const json = await res.json();
  return json.map((board) => {
    return {
      id: board.id,
      title: board.name,
      position: board.position,
      tasks: board.tasks.map((task) => {
        return {
          id: task.id,
          title: task.title,
          description: task.description,
          position: task.position,
        };
      }),
    } as BoardType;
  });
}

export default function Home() {
  const { data, isLoading } = useQuery({
    queryKey: ["boards"],
    queryFn: getBoards,
    initialData: [],
  });

  return (
    <>
      <main className="flex min-h-screen flex-col items-center">
        <Navbar />

        {isLoading ? <></> : <TaskBoards boardData={data} />}
      </main>
    </>
  );
}

interface DropResultExtended extends DropResult {
  type: "board" | "task";
}
function TaskBoards({ boardData }: { boardData: BoardType[] }) {
  const [data, setData] = useState<BoardType[]>([]);

  useEffect(() => {
    setData(boardData);
  }, [boardData]);

  function handleDragEnd(result: DropResult) {
    const { destination, source, type } = result as DropResultExtended;
    if (!destination) return;

    // Moving boards
    if (type === "board") {
      const newBoards = [...data];
      const [moved] = newBoards.splice(source.index, 1);
      newBoards.splice(destination.index, 0, moved);
      setData([...newBoards]);
      // Update positions of boards
      newBoards.forEach((board, index) => {
        BoardService.updateBoard(board.id, board.title, index);
      });
      return;
    }

    // Moving tasks
    const sourceBoardIndex = data.findIndex(
      (board) => board.id === source.droppableId
    );
    const destBoardIndex = data.findIndex(
      (board) => board.id === destination.droppableId
    );

    const sourceBoard = data[sourceBoardIndex];
    const destBoard = data[destBoardIndex];

    const sourceTasks = [...sourceBoard.tasks];
    const [movedTask] = sourceTasks.splice(source.index, 1);

    if (sourceBoard === destBoard) {
      console.log("moving tasks within the same board");
      sourceTasks.splice(destination.index, 0, movedTask);
      const newBoards = [...data];
      newBoards[sourceBoardIndex] = { ...sourceBoard, tasks: sourceTasks };
      setData([...newBoards]);

      sourceTasks.forEach((task, index) => {
        TaskService.updateTask(
          task.id,
          destBoard.id,
          task.title,
          index,
          task.description
        );
      });
    } else {
      console.log("moving tasks between boards");
      const destTasks = [...destBoard.tasks];
      destTasks.splice(destination.index, 0, movedTask);

      const newBoards = [...data];
      newBoards[sourceBoardIndex] = { ...sourceBoard, tasks: sourceTasks };
      newBoards[destBoardIndex] = { ...destBoard, tasks: destTasks };
      setData([...newBoards]);

      destTasks.forEach((task, index) => {
        TaskService.updateTask(
          task.id,
          destBoard.id,
          task.title,
          index,
          task.description
        );
      });
    }
  }

  async function handleAddTask(
    boardId: string,
    title: string,
    description?: string
  ) {
    const board = data.find((board) => board.id === boardId);
    if (!board) return;

    const res = await TaskService.createTask(
      boardId,
      title,
      board.tasks.length,
      description
    );
    if (!res.ok) return;
    const newTask = await res.json();

    toast.success("Task created successfully", {
      duration: 2000,
    });

    const newData = data.map((board) => {
      if (board.id === boardId)
        board.tasks.push({
          id: newTask.id,
          title: newTask.title,
          description: newTask.description,
          position: board.tasks.length,
        } as TaskType);
      return board;
    });
    setData([...newData]);
  }

  async function handleEditTask(boardId: string, task: TaskType) {
    const res = await TaskService.updateTask(
      task.id,
      boardId,
      task.title,
      task.position,
      task.description
    );
    if (!res.ok) {
      toast.error("Error while updating task", {
        duration: 2000,
      });
      return;
    }

    toast.success("Task updated successfully", {
      duration: 2000,
    });

    const newData = data.map((board) => {
      if (board.id === boardId)
        board.tasks = board.tasks.map((boardTask) => {
          if (boardTask.id === boardTask.id) {
            return {
              ...boardTask,
              title: task.title,
              description: task.description,
            };
          }
          return boardTask;
        });
      return board;
    });
    setData([...newData]);
  }

  async function handleAddBoard(name: string) {
    const res = await BoardService.createBoard(name.trim(), data.length);
    if (res.status !== 201) return false;

    const board = await res.json();

    const newData = [
      ...data,
      {
        id: board.id,
        title: board.name,
        position: board.position,
        tasks: [],
      } as BoardType,
    ];
    setData(newData);

    toast.success("Board created successfully", {
      duration: 2000,
      action: {
        label: "Undo",
        onClick: () => BoardService.deleteBoard(board.id),
      },
    });
    return true;
  }

  async function handleTasksGenerated(tasks: GeneratedTasks[]) {
    async function createGeneratedTasks(board: BoardType): Promise<TaskType[]> {
      const createdTasks: TaskType[] = [];
      let position = board.tasks.length;

      for (const task of tasks) {
        const res = await TaskService.createTask(
          board.id,
          task.title,
          position,
          task.description
        );
        if (!res.ok) continue;
        const newTask = await res.json();

        createdTasks.push({
          id: newTask.id,
          title: newTask.title,
          description: newTask.description,
          position,
        } as TaskType);
        position++;
      }
      return createdTasks;
    }

    // Get the 'AI generated' board to create generated tasks
    const existingBoard = data.find((board) => board.title === "AI Generated");
    if (existingBoard) {
      const newTasks = await createGeneratedTasks(existingBoard);

      const newData = data.map((board) => {
        if (board.id === existingBoard.id) {
          return {
            ...board,
            tasks: [...board.tasks, ...newTasks],
          };
        }
        return board;
      });
      setData(newData);
      return;
    }

    // Otherwise, create a new board and add generated tasks to it
    const res = await BoardService.createBoard("AI Generated", data.length);
    if (res.status !== 201) return;
    const newBoard = await res.json();

    const createdBoard = {
      id: newBoard.id,
      title: newBoard.name,
      position: newBoard.position,
      tasks: [],
    } as BoardType;
    createdBoard.tasks = await createGeneratedTasks(createdBoard);
    setData([...data, createdBoard]);
  }

  async function handleDeleteBoard(id: string) {
    const res = await BoardService.deleteBoard(id);
    if (res.ok) {
      toast.success("Board deleted successfully");
      const newData = data.filter((board) => board.id !== id);
      setData(newData);
      return true;
    }
    toast.error("Failed to delete board");
    return false;
  }

  async function handleDeleteTask(id: string) {
    const res = await TaskService.deleteTask(id);
    if (res.ok) {
      toast.success("Task deleted successfully");
      const newData = data.map((board) => {
        return {
          ...board,
          tasks: board.tasks.filter((task) => task.id !== id),
        };
      });
      setData(newData);
      return true;
    }
    toast.error("Failed to delete task");
    return false;
  }

  return (
    <>
      <DragDropContext onDragEnd={handleDragEnd}>
        <BoardList
          boards={data}
          onAddBoard={handleAddBoard}
          onDeleteTask={handleDeleteTask}
          onEditTask={handleEditTask}
          onDeleteBoard={handleDeleteBoard}
        />
      </DragDropContext>
      <TaskForm onAddTask={handleAddTask} boards={data} />
      <ChatSheet onTasksGenerated={handleTasksGenerated} />
    </>
  );
}
