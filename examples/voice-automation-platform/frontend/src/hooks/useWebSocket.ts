/**
 * React hook for WebSocket connection
 */

import { useEffect, useState, useCallback } from "react";
import { getWebSocketClient, WebSocketMessage } from "@/lib/websocket";

export function useWebSocket() {
  const [isConnected, setIsConnected] = useState(false);
  const [lastMessage, setLastMessage] = useState<WebSocketMessage | null>(null);

  useEffect(() => {
    const client = getWebSocketClient();

    // Connect
    client.connect().then(() => {
      setIsConnected(true);
    }).catch((error) => {
      console.error("WebSocket connection failed:", error);
      setIsConnected(false);
    });

    // Listen to all messages
    const handleMessage = (message: WebSocketMessage) => {
      setLastMessage(message);
    };

    client.on("*", handleMessage);

    // Cleanup
    return () => {
      client.off("*", handleMessage);
    };
  }, []);

  const subscribe = useCallback((events: string[]) => {
    const client = getWebSocketClient();
    client.subscribe(events);
  }, []);

  const send = useCallback((message: Record<string, any>) => {
    const client = getWebSocketClient();
    client.send(message);
  }, []);

  return {
    isConnected,
    lastMessage,
    subscribe,
    send,
  };
}

/**
 * Hook to listen for specific WebSocket events
 */
export function useWebSocketEvent(
  event: string,
  handler: (data: any) => void
) {
  useEffect(() => {
    const client = getWebSocketClient();

    const wrappedHandler = (message: WebSocketMessage) => {
      handler(message.data);
    };

    client.on(event, wrappedHandler);

    return () => {
      client.off(event, wrappedHandler);
    };
  }, [event, handler]);
}

