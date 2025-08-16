import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Card } from "@/components/ui/card";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Plus, X } from "lucide-react";
import { TaskType, BoardType } from "@/types";

interface TaskFormProps {
  onAddTask: (boardId: string, task: TaskType) => void;
  boards: BoardType[];
}

export const TaskForm = ({ onAddTask, boards }: TaskFormProps) => {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [boardId, setBoardId] = useState("");
  const [isExpanded, setIsExpanded] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (title.trim() && boardId) {
      const now = new Date();
      onAddTask(boardId, {
        id: now.toISOString(),
        title: title.trim() ?? "",
        description: description.trim() ?? "",
      });
      setTitle("");
      setDescription("");
      setBoardId("");
      setIsExpanded(false);
    }
  };

  const resetForm = () => {
    setTitle("");
    setDescription("");
    setBoardId("");
    setIsExpanded(false);
  };

  if (!isExpanded) {
    return (
      <div className="fixed bottom-6 right-6 z-50 ">
        <button
          onClick={() => setIsExpanded(true)}
          className="bg-slate-900 hover:bg-slate-900/80 rounded-full h-14 w-14 flex items-center justify-center text-white p-0"
        >
          <Plus className="w-8 h-8" />
        </button>
      </div>
    );
  }

  return (
    <div className="fixed bottom-6 right-6 z-50">
      <Card className="w-[480px] p-4 bg-card shadow-xl border animate-slide-up">
        <div className="flex items-center justify-between">
          <h3 className="font-semibold">Add New Task</h3>
          <Button variant="ghost" onClick={resetForm} className="h-8 w-8 p-0">
            <X className="w-4 h-4" />
          </Button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-3">
          <div>
            <Label htmlFor="task-title" className="text-sm font-medium">
              Title *
            </Label>
            <Input
              id="task-title"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="Enter task title..."
              className="mt-1"
              autoFocus
            />
          </div>

          <div>
            <Label htmlFor="task-description" className="text-sm font-medium">
              Description
            </Label>
            <Textarea
              id="task-description"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Enter task description..."
              className="mt-1 resize-none h-24"
              rows={3}
            />
          </div>

          <div>
            <Label className="text-sm font-medium">Board *</Label>
            <Select value={boardId} onValueChange={setBoardId}>
              <SelectTrigger className="mt-1 w-full">
                <SelectValue placeholder="Select a board..." />
              </SelectTrigger>
              <SelectContent>
                {boards.map((board) => (
                  <SelectItem key={board.id} value={board.id}>
                    {board.title}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          <div className="flex gap-2 pt-2">
            <Button
              type="submit"
              className="flex-1 bg-slate-900 hover:bg-slate-900/90"
              disabled={!title.trim() || !boardId}
            >
              Add Task
            </Button>
            <Button type="button" variant="outline" onClick={resetForm}>
              Cancel
            </Button>
          </div>
        </form>
      </Card>
    </div>
  );
};
