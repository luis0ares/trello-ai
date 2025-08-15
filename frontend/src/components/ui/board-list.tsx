"use client";

import { Draggable, Droppable } from "@hello-pangea/dnd";
import { Board } from "./board";
import { BoardType } from "@/types";

// const BoardListOld = ({ boards, tasks }: any) => {
//   const sortedBoards = [...boards].sort((a, b) => a.position - b.position);

//   const handleDragEnd = (result: any) => {
//     console.log(result);
//   };

//   return (
//     <DragDropContext onDragEnd={handleDragEnd}>
//       <Droppable droppableId="board-list" type="BOARD" direction="horizontal">
//         {(provided, snapshot) => (
//           <div
//             ref={provided.innerRef}
//             {...provided.droppableProps}
//             className={`
//               flex gap-4 py-2 overflow-x-auto overflow-y-hidden min-h-full
//               ${snapshot.isDraggingOver ? "bg-accent/20" : ""}
//             `}
//           >
//             {sortedBoards.map((board, index) => {
//               const boardTasks = tasks
//                 .filter((task) => task.boardId === board.id)
//                 .sort((a, b) => a.position - b.position);

//               return (
//                 <Board
//                   key={board.id}
//                   board={board}
//                   tasks={boardTasks}
//                   index={index}
//                 />
//               );
//             })}
//             {provided.placeholder}
//           </div>
//         )}
//       </Droppable>
//     </DragDropContext>
//   );
// };

export function BoardList({ boards }: { boards: BoardType[] }) {
  return (
    <Droppable droppableId="all-boards" direction="horizontal" type="board">
      {(provided) => (
        <div
          ref={provided.innerRef}
          {...provided.droppableProps}
          className="flex flex-1 w-full container p-5"
        >
          {boards.map((board, index) => (
            <Draggable draggableId={board.id} index={index} key={board.id}>
              {(provided) => (
                <div ref={provided.innerRef} {...provided.draggableProps}>

                  <Board
                    board={board}
                    dragHandleProps={provided.dragHandleProps}
                  />
                </div>
              )}
            </Draggable>
          ))}
          {provided.placeholder}
        </div>
      )}
    </Droppable>
  );
}
