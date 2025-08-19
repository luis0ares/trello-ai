import { Button } from "@/components/ui/button";
import { Kanban } from "lucide-react";

export function Navbar() {
  return (
    <header className="sticky top-0 z-50 w-full border-b bg-slate-200/95 shadow-xl dark:bg-slate-800/95 backdrop-blur text-slate-800 dark:text-slate-200">
      <div className="flex h-16 items-center justify-between mx-auto px-5">
        <div className="flex items-center gap-2">
          <Kanban className="h-12 w-12" />
          <span className="text-3xl font-bold">Trello AI</span>
        </div>

        <div className="flex items-center gap-4">
          <Button size="lg">Log in</Button>
        </div>
      </div>
    </header>
  );
}
