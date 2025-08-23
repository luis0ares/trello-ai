"use client";

import { DraggableProvidedDragHandleProps, Droppable } from "@hello-pangea/dnd";
import { EllipsisVertical, Trash2 } from "lucide-react";
import { BoardType } from "@/types";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "../ui/dropdown-menu";

export function Board({
  board,
  onDeleteBoard,
  onDeleteTask,
  dragHandleProps,
}: {
  board: BoardType;
  onDeleteBoard: (id: string) => Promise<boolean>;
  onDeleteTask: (id: string) => Promise<boolean>;
  dragHandleProps: DraggableProvidedDragHandleProps | null;
}) {
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
            <DropdownMenuItem onClick={() => onDeleteBoard(board.id)}>
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
              <Task
                key={task.id}
                task={task}
                index={index}
                onDeleteTask={onDeleteTask}
              />
            ))}
            {provided.placeholder}
          </div>
        )}
      </Droppable>
    </div>
  );
}

import { TaskType } from "@/types";
import { Draggable } from "@hello-pangea/dnd";

export function Task({
  task,
  index,
  onDeleteTask,
}: {
  task: TaskType;
  index: number;
  onDeleteTask: (id: string) => Promise<boolean>;
}) {
  return (
    <Draggable draggableId={task.id} index={index}>
      {(provided) => (
        <div
          ref={provided.innerRef}
          {...provided.draggableProps}
          {...provided.dragHandleProps}
          className="bg-white p-2 rounded shadow-sm mb-2 border border-gray-200 "
          style={provided.draggableProps.style}
        >
          <div className="flex w-full justify-between gap-3">
            <h4 className="text-lg font-bold text-gray-800 line-clamp-2">
              {task.title}
            </h4>
            <DropdownMenu>
              <DropdownMenuTrigger>
                <EllipsisVertical className="w-4 h-4 opacity-60" />
              </DropdownMenuTrigger>
              <DropdownMenuContent>
                <DropdownMenuItem onClick={() => onDeleteTask(task.id)}>
                  <Trash2 className="text-red-600" /> Delete
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          </div>
          <p className="m-1 line-clamp-6">{task.description}</p>
        </div>
      )}
    </Draggable>
  );
}
