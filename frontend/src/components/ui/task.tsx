import { TaskType } from "@/types";
import { Draggable } from "@hello-pangea/dnd";

export function Task({ task, index }: { task: TaskType; index: number }) {
  return (
    <Draggable draggableId={task.id} index={index}>
      {(provided) => (
        <div
          ref={provided.innerRef}
          {...provided.draggableProps}
          {...provided.dragHandleProps}
          className="bg-white p-2 rounded shadow-sm mb-2 border border-gray-200"
          style={provided.draggableProps.style}
        >
          {task.content}
        </div>
      )}
    </Draggable>
  );
}
