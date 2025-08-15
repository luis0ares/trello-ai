import { DraggableProvidedDragHandleProps, Droppable } from "@hello-pangea/dnd";
import { GripVertical } from "lucide-react";
import { Task } from "./task";
import { BoardType } from "@/types";

export function Board({
  board,
  dragHandleProps,
}: {
  board: BoardType;
  dragHandleProps: DraggableProvidedDragHandleProps | null;
}) {
  return (
    <div className="bg-gray-100 rounded-lg flex flex-col h-full w-80 mx-2">
      <div
        {...dragHandleProps}
        className="bg-slate-800 text-slate-200 p-3 rounded-t-lg cursor-grab active:cursor-grabbing flex items-center justify-between"
      >
        <h3 className="font-semibold text-sm flex items-center gap-2">
          {board.title}
          <span className="ml-2 px-2 py-1 text-xs bg-white/20 rounded-full">
            {board.tasks.length}
          </span>
        </h3>
        <GripVertical className="w-4 h-4 opacity-60" />
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
