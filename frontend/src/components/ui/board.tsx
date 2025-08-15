"use client"

import { Draggable } from '@hello-pangea/dnd';
import { Card } from '@/components/ui/card';
import { Board as BoardType } from '@/types';
import { GripVertical } from 'lucide-react';

interface BoardProps {
  board: BoardType;
  tasks: any[];
  index: number;
}

export const Board = ({ board, tasks, index }: BoardProps) => {
  return (
    <Draggable draggableId={board.id} index={index}>
      {(provided, snapshot) => (
        <Card 
          ref={provided.innerRef}
          {...provided.draggableProps}
          className={`
            flex-shrink-0 w-[280px] bg-gradient-board shadow-sm py-0
            transition-all duration-200 bg-white
            ${snapshot.isDragging ? 'rotate-1 shadow-lg scale-105' : ''}
          `}
        >
          <div 
            {...provided.dragHandleProps}
            className="bg-slate-800 text-slate-200 p-3 border-b bg-board-header text-board-header-foreground rounded-t-lg cursor-grab active:cursor-grabbing flex items-center justify-between"
          >
            <h3 className="font-semibold text-sm flex items-center gap-2">
              {board.name}
              <span className="ml-2 px-2 py-1 text-xs bg-white/20 rounded-full">
                {tasks.length}
              </span>
            </h3>
            <GripVertical className="w-4 h-4 opacity-60" />
          </div>
          <div className="p-3 max-h-[calc(100vh-200px)] overflow-y-auto">
            List tasks here
          </div>
        </Card>
      )}
    </Draggable>
  );
};