import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card } from "@/components/ui/card";
import { Plus } from "lucide-react";

interface BoardFormProps {
  onAddBoard: (name: string) => Promise<boolean>;
}

export function BoardForm({ onAddBoard }: BoardFormProps) {
  const [name, setName] = useState("");
  const [isExpanded, setIsExpanded] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!name.trim()) return;
    const result = await onAddBoard(name);
    if (result) {
      setName("");
      setIsExpanded(false);
    }
  }

  if (!isExpanded) {
    return (
      <div className="flex-shrink-0 mx-2">
        <Button
          onClick={() => setIsExpanded(true)}
          variant="outline"
          className="h-[52px] min-w-[320px] border-dashed border-2 border-slate-800 dark:border-slate-200 bg-slate-200 dark:bg-slate-900 hover:bg-slate-800 dark:hover:bg-slate-200 text-slate-800 dark:text-slate-200 hover:text-slate-200 dark:hover:text-slate-800"
        >
          <Plus className="w-4 h-4 mr-2" />
          Add another board
        </Button>
      </div>
    );
  }

  return (
    <Card className="min-w-[320px] p-4 shadow-sm bg-slate-100 mx-2">
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="space-y-2">
          <Label htmlFor="board-name" className="text-xl font-medium">
            Board Name
          </Label>
          <Input
            id="board-name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="Enter board name..."
            className="mt-1 bg-white"
            autoFocus
          />
        </div>
        <div className="flex gap-2">
          <Button
            type="submit"
            className="flex-1 bg-slate-900 hover:bg-slate-900/90"
          >
            Add Board
          </Button>

          <Button
            type="button"
            variant="outline"
            onClick={() => {
              setIsExpanded(false);
              setName("");
            }}
          >
            Cancel
          </Button>
        </div>
      </form>
    </Card>
  );
}
