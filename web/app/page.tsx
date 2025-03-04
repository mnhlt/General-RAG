'use client'
import { Thread } from "@/components/assistant-ui/thread";
import { FileUpload } from "@/components/ui/FileUpload";

export default function Home() {
  return (
    <main className="h-dvh">
      <div className="flex w-full h-full">
        <div className="flex-1">
          <Thread />
        </div>
        <div className="w-80 border-l p-4 bg-gray-50">
          <FileUpload />
        </div>
      </div>
    </main>
  );
}
