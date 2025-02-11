'use client'
import { Thread } from "@/components/assistant-ui/thread";
import { useChatRuntime } from "@assistant-ui/react-ai-sdk";
import { AssistantRuntimeProvider } from "@assistant-ui/react";
import RootLayout from "./layout";

// export default function Home() {
//   const runtime = useChatRuntime({ api: "/api/chat" });

//   return (
//     <AssistantRuntimeProvider runtime={runtime}>
//       <main className="h-dvh">
//         <Thread />
//       </main>
//     </AssistantRuntimeProvider>
//   );
// }


export default function Home() {

  return (
    <main className="h-dvh">
    <Thread />
  </main>
  );
}
