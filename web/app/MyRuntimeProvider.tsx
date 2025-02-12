"use client";
 
import type { ReactNode } from "react";
import {
  AssistantRuntimeProvider,
  useLocalRuntime,
  type ChatModelAdapter,
} from "@assistant-ui/react";

// Function to generate random thread ID
const generateThreadId = () => {
  return 'thread-' + Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);
};

const thread_id = generateThreadId();

const LLMAdapter: ChatModelAdapter = {
  async run({ messages, abortSignal, context }) {
    console.log("messages", messages, context);
    // TODO replace with your own API

    const lastMessage = messages[messages.length - 1];
    const lastMessageContent = lastMessage.content[0];
    const lastMessageText = lastMessageContent.type === 'text' 
      ? lastMessageContent.text 
      : '';

    const result = await fetch("http://localhost:8000/query", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      // forward the messages in the chat to the API
      body: JSON.stringify({
        message: lastMessageText,
        thread_id: thread_id
      }),
      // if the user hits the "cancel" button or escape keyboard key, cancel the request
      signal: abortSignal,
    });
 
    const data = await result.json();
    console.log("data", data);
    return {
      content: [
        {
          type: "text",
          text: data.response,
        },
      ],
    };
  },
};

const StreamingLLMAdapter: ChatModelAdapter = {
    async *run({ messages, abortSignal}) {
      const lastMessage = messages[messages.length - 1];
      const lastMessageContent = lastMessage.content[0];
      const lastMessageText = lastMessageContent.type === 'text' 
        ? lastMessageContent.text 
        : '';
  
      const response = await fetch("http://localhost:8000/query-stream", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Accept": "text/event-stream",
        },
        body: JSON.stringify({
          message: lastMessageText,
          thread_id: thread_id
        }),
        signal: abortSignal,
      });

      const reader = response.body?.getReader();
      if (!reader) {
        throw new Error("No reader available");
      }

      const decoder = new TextDecoder();
      let buffer = '';
      let accumulatedContent = '';
      let lastYieldTime = Date.now();
      const YIELD_INTERVAL = 300;

      try {
        while (true) {
          const { done, value } = await reader.read();
          if (done) {
            if (accumulatedContent) {
              yield {
                content: [
                  {
                    type: "text",
                    text: accumulatedContent,
                  },
                ],
              };
            }
            break;
          }

          buffer += decoder.decode(value);
          const lines = buffer.split('\n');
          buffer = '';
          
          let currentEvent = '';
          let currentData = '';
          
          for (const line of lines) {
            if (line.trim() === '') {
              // End of event
              if (currentEvent === 'message' && currentData) {
                try {
                  const parsed = JSON.parse(currentData);
                  if (parsed.content) {
                    accumulatedContent += parsed.content;
                    
                    const currentTime = Date.now();
                    const timeSinceLastYield = currentTime - lastYieldTime;

                    if (timeSinceLastYield >= YIELD_INTERVAL || 
                        parsed.content.includes('.') ||
                        parsed.content.includes('!') ||
                        parsed.content.includes('?') ||
                        parsed.content.includes('\n')
                    ) {
                      yield {
                        content: [
                          {
                            type: "text",
                            text: accumulatedContent,
                          },
                        ],
                      };
                      lastYieldTime = currentTime;
                    }
                  }
                } catch (e) {
                  console.error('Error parsing JSON:', e);
                }
              } else if (currentEvent === 'error') {
                console.error('Server error:', currentData);
              }
              currentEvent = '';
              currentData = '';
              continue;
            }

            if (line.startsWith('event: ')) {
              currentEvent = line.slice(7);
            } else if (line.startsWith('data: ')) {
              currentData = line.slice(6);
            }
          }

          // Add a small delay to prevent overwhelming React
          await new Promise(resolve => setTimeout(resolve, 10));
        }
      } finally {
        reader.releaseLock();
      }
    },
  };
 
export function MyRuntimeProvider({
  children,
}: Readonly<{
  children: ReactNode;
}>) {
  const runtime = useLocalRuntime(StreamingLLMAdapter);
 
  return (
    <AssistantRuntimeProvider runtime={runtime}>
      {children}
    </AssistantRuntimeProvider>
  );
}