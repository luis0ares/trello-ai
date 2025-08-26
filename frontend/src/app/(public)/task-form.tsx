import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Plus } from "lucide-react";
import { BoardType } from "@/types";
import z from "zod";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";

interface TaskFormProps {
  onAddTask: (
    boardId: string,
    title: string,
    description?: string
  ) => Promise<void>;
  boards: BoardType[];
}

const taskFormSchema = z.object({
  title: z.string().min(3, {
    message: "Task title must be at least 3 characters.",
  }),
  description: z.string().optional(),
  boardId: z.string().min(1, {
    message: "You must select a board to create a task.",
  }),
});
type taskFormType = z.infer<typeof taskFormSchema>;

export function TaskForm({ onAddTask, boards }: TaskFormProps) {
  const [isExpanded, setIsExpanded] = useState(false);

  const form = useForm<taskFormType>({
    resolver: zodResolver(taskFormSchema),
    defaultValues: {
      title: "",
      description: "",
      boardId: "",
    },
  });

  async function onSubmit(formData: taskFormType) {
    await onAddTask(formData.boardId, formData.title, formData.description);
    closeAndReset()
  }

  function closeAndReset() {
    form.reset();
    setIsExpanded(false);
  }

  return (
    <>
      <div className="fixed bottom-6 right-6">
        <button
          onClick={() => setIsExpanded(true)}
          className="bg-slate-900 hover:bg-slate-900/80 rounded-full h-14 w-14 flex items-center justify-center text-white p-0"
        >
          <Plus className="w-8 h-8" />
        </button>
      </div>

      <Dialog open={isExpanded} onOpenChange={(open) => setIsExpanded(open)}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Create new task</DialogTitle>
            <DialogDescription></DialogDescription>
          </DialogHeader>

          <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-3">
              <FormField
                control={form.control}
                name="title"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Title</FormLabel>
                    <FormControl>
                      <Input placeholder="Task title" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="description"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Description</FormLabel>
                    <FormControl>
                      <Textarea placeholder="Task description" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="boardId"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Board</FormLabel>
                    <Select
                      onValueChange={field.onChange}
                      defaultValue={field.value}
                    >
                      <FormControl className="w-full">
                        <SelectTrigger>
                          <SelectValue placeholder="Select a board..." />
                        </SelectTrigger>
                      </FormControl>
                      <SelectContent className="z-70">
                        {boards.map((board) => (
                          <SelectItem key={board.id} value={board.id}>
                            {board.title}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <div className="flex gap-2 pt-2">
                <Button type="submit" className="flex-1">
                  Add Task
                </Button>
                <Button type="button" variant="outline" onClick={closeAndReset}>
                  Cancel
                </Button>
              </div>
            </form>
          </Form>
        </DialogContent>
      </Dialog>
    </>
  );
}
