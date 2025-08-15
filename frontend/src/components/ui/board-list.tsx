"use client"

import { DragDropContext, Droppable } from "@hello-pangea/dnd";
import { Board } from "./board";
import { Board as BoardType } from "@/types";

interface BoardListProps {
  boards: BoardType[];
  tasks: any[];
}

export const BoardList = ({ boards, tasks }: BoardListProps) => {
  const sortedBoards = [...boards].sort((a, b) => a.position - b.position);

  const handleDragEnd = (result: any) => {
    console.log(result);
  };

  return (
    <DragDropContext onDragEnd={handleDragEnd}>
      <Droppable droppableId="board-list" type="BOARD" direction="horizontal">
        {(provided, snapshot) => (
          <div
            ref={provided.innerRef}
            {...provided.droppableProps}
            className={`
              flex gap-4 py-2 overflow-x-auto overflow-y-hidden min-h-full
              ${snapshot.isDraggingOver ? "bg-accent/20" : ""}
            `}
          >
            {sortedBoards.map((board, index) => {
              const boardTasks = tasks
                .filter((task) => task.boardId === board.id)
                .sort((a, b) => a.position - b.position);

              return (
                <Board
                  key={board.id}
                  board={board}
                  tasks={boardTasks}
                  index={index}
                />
              );
            })}
            {provided.placeholder}
          </div>
        )}
      </Droppable>
    </DragDropContext>
  );
};
