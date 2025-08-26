"use client";

import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import {
  Sheet,
  SheetContent,
  SheetDescription,
  SheetFooter,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from "@/components/ui/sheet";
import { Textarea } from "@/components/ui/textarea";
import { Send, MessageSquareMore } from "lucide-react";
import { useEffect, useRef, useState } from "react";
import Markdown from "react-markdown";
import useWebSocket, { ReadyState } from "react-use-websocket";

interface Message {
  id: string | number;
  content: string;
  sender: "user" | "ai";
  timestamp: Date;
}

export type GeneratedTasks = {
  title: string;
  description: string;
  created_by: "AI";
};

type WSJsonMessage =
  | {
      type: "final";
      data: GeneratedTasks[];
    }
  | {
      type: "reply";
      data: string;
    }
  | {
      type: "error";
      details: string;
    };

function getWebSocketURL() {
  return `${process.env.NEXT_PUBLIC_BASE_URL}/ws/tasks`
    .replaceAll("https://", "wss://")
    .replaceAll("http://", "ws://");
}

export function ChatSheet({
  onTasksGenerated,
}: {
  onTasksGenerated: (tasks: GeneratedTasks[]) => void;
}) {
  const scrollAreaRef = useRef<HTMLDivElement>(null);
  const [newMessage, setNewMessage] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);

  useEffect(() => {
    function scrollToBottom() {
      if (scrollAreaRef.current) {
        const scrollContainer = scrollAreaRef.current.querySelector(
          "[data-radix-scroll-area-viewport]"
        );
        if (scrollContainer) {
          scrollContainer.scrollTop = scrollContainer.scrollHeight;
        }
      }
    }
    // Auto-scroll to bottom when new messages arrive
    scrollToBottom();
  }, [messages]);

  const { sendMessage, lastJsonMessage, readyState } =
    useWebSocket<WSJsonMessage | null>(getWebSocketURL(), {
      share: false,
      shouldReconnect: () => true,
      onOpen: () => {
        setMessages([]);
      },
    });

  useEffect(() => {
    function handleNewMessage() {
      if (!lastJsonMessage) return;

      if (lastJsonMessage.type === "reply") {
        const message: Message = {
          id: Date.now().toString(),
          content: lastJsonMessage.data,
          sender: "ai",
          timestamp: new Date(),
        };
        setMessages((prev) => [...prev, message]);
      } else if (lastJsonMessage.type === "final") {
        onTasksGenerated(lastJsonMessage.data);
      } else if (lastJsonMessage.type === "error") {
        console.error(lastJsonMessage.details);
      }
    }
    handleNewMessage();
  }, [lastJsonMessage]);

  function handleSendMessage(e: React.FormEvent) {
    e.preventDefault();

    if (!newMessage.trim()) return;

    const message: Message = {
      id: Date.now().toString(),
      content: newMessage,
      sender: "user",
      timestamp: new Date(),
    };
    sendMessage(newMessage);

    setMessages((prev) => [...prev, message]);
    setNewMessage("");
  }

  if (readyState !== ReadyState.OPEN) return <></>;

  return (
    <Sheet>
      <SheetTrigger>
        <div className="fixed bottom-24 right-6 z-50 ">
          <div className="bg-slate-900 hover:bg-slate-900/80 rounded-full h-14 w-14 flex items-center justify-center text-white p-0">
            <MessageSquareMore className="w-8 h-8" />
          </div>
        </div>
      </SheetTrigger>

      <SheetContent className="w-full sm:w-[640px] sm:max-w-full border-b bg-slate-200/95 shadow-xl dark:bg-slate-800/95 backdrop-blur text-slate-800 dark:text-slate-200">
        <SheetHeader>
          <SheetTitle className="text-2xl font-semibold border-b pb-4 border-slate-950 dark:border-slate-50 pl-6">
            Auto create tasks with AI
          </SheetTitle>
          <SheetDescription></SheetDescription>
        </SheetHeader>

        <ScrollArea className="flex-1 h-0" ref={scrollAreaRef}>
          <div className="space-y-4 px-6">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`flex gap-3 ${
                  message.sender === "user"
                    ? "justify-end flex-row-reverse"
                    : "justify-start"
                }`}
              >
                <div
                  className={`max-w-[85%] rounded-lg px-3 py-2 shadow-md ${
                    message.sender === "ai"
                      ? "bg-primary dark:bg-slate-700 text-accent dark:text-accent-foreground"
                      : "bg-muted dark:bg-slate-300 text-accent-foreground dark:text-accent"
                  }`}
                >
                  <article
                    className={`prose ${
                      message.sender === "ai" && "prose-slate prose-invert"
                    }`}
                  >
                    <Markdown
                      components={{
                        h1: "h2",
                        h2: "h3",
                      }}
                    >
                      {message.content.trim()}
                    </Markdown>
                  </article>
                  <div className="text-xs opacity-70 mt-1 text-end">
                    {formatTime(message.timestamp)}
                  </div>
                </div>

                <Avatar className="h-12 w-12">
                  {message.sender === "ai" ? (
                    <AvatarImage src="https://github.com/openai.png" />
                  ) : (
                    <AvatarImage src="https://github.com/guest.png" />
                  )}
                  <AvatarFallback>CN</AvatarFallback>
                </Avatar>
              </div>
            ))}
          </div>
        </ScrollArea>

        <SheetFooter>
          <form
            onSubmit={handleSendMessage}
            className="flex gap-2 items-end border-t pt-2 border-slate-950 dark:border-slate-50"
          >
            <Textarea
              value={newMessage}
              rows={5}
              onChange={(e) => setNewMessage(e.target.value)}
              placeholder="Type your message..."
              className="max-h-40 resize-none border-slate-950 dark:border-slate-50 bg-transparent shadow-xl"
              onKeyDown={(e) => {
                if (e.key === "Enter" && !e.shiftKey) {
                  e.preventDefault();
                  handleSendMessage(e);
                }
              }}
            />
            <Button type="submit" size="icon" className="">
              <Send className="h-6 w-6" />
            </Button>
          </form>
        </SheetFooter>
      </SheetContent>
    </Sheet>
  );
}

function formatTime(date: Date) {
  return date.toLocaleDateString([], { hour: "2-digit", minute: "2-digit" });
}
