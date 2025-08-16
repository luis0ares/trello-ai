import React, { useState } from "react";
import {
  DragDropContext,
  Droppable,
  Draggable,
  DropResult,
  DraggableProvidedDragHandleProps
} from "@hello-pangea/dnd";

// ================== Types ==================
interface TaskType {
  id: string;
  content: string;
}

interface BoardType {
  id: string;
  title: string;
  tasks: TaskType[];
}

interface AppData {
  boards: BoardType[];
}

// ================== Initial Data ==================
const initialData: AppData = {
  boards: [
    {
      id: "board-1",
      title: "Pending",
      tasks: [
        { id: "task-1", content: "Learn React" },
        { id: "task-2", content: "Read about @hello-pangea/dnd" }
      ]
    },
    {
      id: "board-2",
      title: "Doing",
      tasks: [{ id: "task-3", content: "Build Trello clone" }]
    },
    {
      id: "board-3",
      title: "Done",
      tasks: [{ id: "task-4", content: "Drink coffee" }]
    }
  ]
};

// ================== Task Component ==================
function Task({ task, index }: { task: TaskType; index: number }) {
  return (
    <Draggable draggableId={task.id} index={index}>
      {(provided) => (
        <div
          ref={provided.innerRef}
          {...provided.draggableProps}
          {...provided.dragHandleProps}
          style={{
            background: "#fff",
            padding: "8px",
            borderRadius: "4px",
            marginBottom: "8px",
            boxShadow: "0 1px 2px rgba(0,0,0,0.1)",
            ...provided.draggableProps.style
          }}
        >
          {task.content}
        </div>
      )}
    </Draggable>
  );
}

// ================== Board Component ==================
function Board({
  board,
  dragHandleProps
}: {
  board: BoardType;
  dragHandleProps: DraggableProvidedDragHandleProps | null;
}) {
  return (
    <div
      style={{
        background: "#f4f4f4",
        padding: "10px",
        borderRadius: "8px",
        width: "250px",
        display: "flex",
        flexDirection: "column"
      }}
    >
      <h3 {...dragHandleProps} style={{ cursor: "grab", marginBottom: "10px" }}>
        {board.title}
      </h3>

      <Droppable droppableId={board.id} type="task">
        {(provided) => (
          <div
            style={{ minHeight: "50px" }}
            ref={provided.innerRef}
            {...provided.droppableProps}
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

// ================== BoardList Component ==================
function BoardList({ boards }: { boards: BoardType[] }) {
  return (
    <Droppable droppableId="all-boards" direction="horizontal" type="board">
      {(provided) => (
        <div
          style={{ display: "flex", gap: "20px" }}
          ref={provided.innerRef}
          {...provided.droppableProps}
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

// ================== Main App ==================
export default function App() {
  const [data, setData] = useState<AppData>(initialData);

  const onDragEnd = (result: DropResult) => {
    const { destination, source, type } = result;
    if (!destination) return;

    // Moving boards
    if (type === "board") {
      const newBoards = [...data.boards];
      const [moved] = newBoards.splice(source.index, 1);
      newBoards.splice(destination.index, 0, moved);
      setData({ boards: newBoards });
      return;
    }

    // Moving tasks
    const sourceBoardIndex = data.boards.findIndex(
      (b) => b.id === source.droppableId
    );
    const destBoardIndex = data.boards.findIndex(
      (b) => b.id === destination.droppableId
    );

    const sourceBoard = data.boards[sourceBoardIndex];
    const destBoard = data.boards[destBoardIndex];

    const sourceTasks = [...sourceBoard.tasks];
    const [movedTask] = sourceTasks.splice(source.index, 1);

    if (sourceBoard === destBoard) {
      sourceTasks.splice(destination.index, 0, movedTask);
      const newBoards = [...data.boards];
      newBoards[sourceBoardIndex] = { ...sourceBoard, tasks: sourceTasks };
      setData({ boards: newBoards });
    } else {
      const destTasks = [...destBoard.tasks];
      destTasks.splice(destination.index, 0, movedTask);

      const newBoards = [...data.boards];
      newBoards[sourceBoardIndex] = { ...sourceBoard, tasks: sourceTasks };
      newBoards[destBoardIndex] = { ...destBoard, tasks: destTasks };
      setData({ boards: newBoards });
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h2>Trello-like App</h2>
      <DragDropContext onDragEnd={onDragEnd}>
        <BoardList boards={data.boards} />
      </DragDropContext>
    </div>
  );
}
