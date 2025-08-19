import { Draggable, Droppable } from "@hello-pangea/dnd";
import { Board } from "./board";
import { BoardType } from "@/types";
import { BoardForm } from "./board-form";

export function BoardList({
  onAddBoard,
  onDeleteBoard,
  onDeleteTask,
  boards,
}: {
  onAddBoard: (name: string) => Promise<boolean>;
  onDeleteBoard: (id: string) => Promise<boolean>;
  onDeleteTask: (id: string) => Promise<boolean>;
  boards: BoardType[];
}) {
  return (
    <Droppable droppableId="all-boards" direction="horizontal" type="board">
      {(provided) => (
        <div
          ref={provided.innerRef}
          {...provided.droppableProps}
          className="flex flex-1 w-full overflow-x-auto p-5"
        >
          {boards.map((board, index) => (
            <Draggable draggableId={board.id} index={index} key={board.id}>
              {(provided) => (
                <div ref={provided.innerRef} {...provided.draggableProps}>
                  <Board
                    board={board}
                    onDeleteBoard={onDeleteBoard}
                    onDeleteTask={onDeleteTask}
                    dragHandleProps={provided.dragHandleProps}
                  />
                </div>
              )}
            </Draggable>
          ))}
          {provided.placeholder}
          <BoardForm onAddBoard={onAddBoard}  />
        </div>
      )}
    </Droppable>
  );
}
