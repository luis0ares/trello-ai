"use client";

import { DraggableProvidedDragHandleProps, Droppable } from "@hello-pangea/dnd";
import { EllipsisVertical, Trash2 } from "lucide-react";
import { Task } from "./task";
import { BoardType } from "@/types";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "./dropdown-menu";
import { BoardService } from "@/services/board";
import { toast } from "sonner";

export function Board({
  board,
  dragHandleProps,
}: {
  board: BoardType;
  dragHandleProps: DraggableProvidedDragHandleProps | null;
}) {
  async function handleDelete(id: string) {
    const res = await BoardService.deleteBoard(id);
    if (res.ok) {
      toast.success("Board deleted successfully");
    } else {
      toast.error("Failed to delete board");
    }
  }

  return (
    <div className="bg-slate-200 dark:bg-slate-800 rounded-lg flex flex-col h-full w-80 mx-2 shadow-sm">
      <div
        {...dragHandleProps}
        className="bg-slate-800 dark:bg-slate-900 text-slate-200 p-3 rounded-t-lg cursor-grab active:cursor-grabbing flex items-center justify-between"
      >
        <h3 className="font-semibold text-xl flex items-center gap-2">
          {board.title}
          <span className="ml-2 px-2 py-1 text-xs bg-white/20 rounded-full">
            {board.tasks.length}
          </span>
        </h3>

        <DropdownMenu>
          <DropdownMenuTrigger>
            <EllipsisVertical className="w-4 h-4 opacity-60" />
          </DropdownMenuTrigger>
          <DropdownMenuContent>
            <DropdownMenuItem onClick={() => handleDelete(board.id)}>
              <Trash2 className="text-red-600" /> Delete
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </div>

      <Droppable droppableId={board.id} type="task">
        {(provided) => (
          <div
            ref={provided.innerRef}
            {...provided.droppableProps}
            className="flex flex-col flex-1 p-3"
          >
            {board.tasks.map((task, index) => (
              <Task key={task.id} task={task} index={index} />
            ))}
            {provided.placeholder}
          </div>
        )}
      </Droppable>
    </div>
  );
}
