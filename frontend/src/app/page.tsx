import { Navbar } from "@/components/layout/navbar";

export default function Home() {
  return (
    <div className="min-h-screen transition-colors duration-300 bg-gradient-to-br from-blue-50 to-indigo-100">
      <Navbar />

      <div className="pt-24 px-6 pb-6 h-screen overflow-hidden">
        <div className="h-full overflow-x-auto overflow-y-hidden max-w-7xl mx-auto">
          boards here
        </div>
      </div>
    </div>
  );
}
