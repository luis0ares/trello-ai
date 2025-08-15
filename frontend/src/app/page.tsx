import { Navbar } from "@/components/layout/navbar";
import { BoardList } from "@/components/ui/board-list";
import { Board } from "@/types";

const boards: Board[] = [
  { id: "1", name: "Pending", position: 0 },
  { id: "2", name: "Doing", position: 1 },
  { id: "3", name: "Done", position: 2 },
];

export default function Home() {
  return (
    <div className="min-h-screen transition-colors duration-300 bg-gradient-to-br from-blue-50 to-indigo-100">
      <Navbar />

      <div className="max-w-7xl mx-auto pt-24 px-6 pb-6 h-screen overflow-hidden">
        <BoardList boards={boards} tasks={[]} />
      </div>
    </div>
  );
}
