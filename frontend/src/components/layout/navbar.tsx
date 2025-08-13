"use client";

import { Button } from "@/components/ui/button";
import { Moon } from "lucide-react";

export function Navbar() {
  return (
    <nav className="fixed top-0 left-0 right-0 shadow-md z-50 border-b transition-colors duration-300 bg-white border-gray-200">
      <div className="max-w-7xl mx-auto px-6 py-4">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold transition-colors duration-300 text-gray-800">
              Trello AI
            </h1>
            <p className="text-sm transition-colors duration-300 text-gray-600">
              Organize your tasks and stay productive.
            </p>
          </div>
          <div className="flex items-center gap-4">
            <Button variant="ghost" size="sm">
              <Moon className="h-4 w-4" />
            </Button>
          </div>
        </div>
      </div>
    </nav>
  );
}
