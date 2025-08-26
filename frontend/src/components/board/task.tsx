"use client";

import { EllipsisVertical, PencilLine, Trash2 } from "lucide-react";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "../ui/dropdown-menu";
import { TaskType } from "@/types";
import { Draggable } from "@hello-pangea/dnd";
import { TaskEdit } from "./task-edit-dialog";
import { useState } from "react";

export function Task({
  task,
  index,
  onDeleteTask,
  onEditTask,
}: {
  task: TaskType;
  index: number;
  onDeleteTask: (id: string) => Promise<boolean>;
  onEditTask: (task: TaskType) => void;
}) {
  const [editDialog, setEditDialog] = useState<boolean>(false);

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

                <DropdownMenuItem onClick={() => setEditDialog(true)}>
                  <PencilLine className="text-amber-600" /> Edit task
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          </div>
          <p className="m-1 line-clamp-6">{task.description}</p>
          <TaskEdit
            task={task}
            onTaskUpdate={(task: TaskType) => onEditTask(task)}
            dialogOpen={editDialog}
            handleOpenChange={(open: boolean) => setEditDialog(open)}
          />
        </div>
      )}
    </Draggable>
  );
}
