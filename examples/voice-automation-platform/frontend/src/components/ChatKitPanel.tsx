"use client";

/**
 * ChatKit Panel Component
 * 
 * Official ChatKit integration following OpenAI patterns.
 * Features:
 * - Session management with client secrets
 * - File attachments support
 * - Client-side tools handling
 * - Theme configuration
 * - Error handling and recovery
 */

import { useCallback, useEffect, useRef, useState } from "react";
import { ChatKit, useChatKit } from "@openai/chatkit-react";

// Configuration
const CREATE_SESSION_ENDPOINT = "/api/chatkit/session";
const WORKFLOW_ID = process.env.NEXT_PUBLIC_CHATKIT_WORKFLOW_ID || "";

// Types
export type ColorScheme = "light" | "dark";

export type ClientToolInvocation = {
  name: string;
  params: Record<string, unknown>;
};

export type ChatKitPanelProps = {
  theme: ColorScheme;
  onClientTool?: (invocation: ClientToolInvocation) => Promise<Record<string, unknown>>;
  onResponseEnd?: () => void;
  onResponseStart?: () => void;
  onThemeChange?: (scheme: ColorScheme) => void;
  className?: string;
};

type ErrorState = {
  script: string | null;
  session: string | null;
  integration: string | null;
  retryable: boolean;
};

const isBrowser = typeof window !== "undefined";
const isDev = process.env.NODE_ENV !== "production";

const createInitialErrors = (): ErrorState => ({
  script: null,
  session: null,
  integration: null,
  retryable: false,
});

export function ChatKitPanel({
  theme = "light",
  onClientTool,
  onResponseEnd,
  onResponseStart,
  onThemeChange,
  className = "h-[600px] w-full",
}: ChatKitPanelProps) {
  const [errors, setErrors] = useState<ErrorState>(createInitialErrors);
  const [isInitializingSession, setIsInitializingSession] = useState(true);
  const isMountedRef = useRef(true);
  const [scriptStatus, setScriptStatus] = useState<"pending" | "ready" | "error">(
    () => (isBrowser && window.customElements?.get("openai-chatkit") ? "ready" : "pending")
  );
  const [widgetInstanceKey, setWidgetInstanceKey] = useState(0);

  const setErrorState = useCallback((updates: Partial<ErrorState>) => {
    setErrors((current) => ({ ...current, ...updates }));
  }, []);

  useEffect(() => {
    return () => {
      isMountedRef.current = false;
    };
  }, []);

  // Monitor ChatKit script loading
  useEffect(() => {
    if (!isBrowser) return;

    let timeoutId: number | undefined;

    const handleLoaded = () => {
      if (!isMountedRef.current) return;
      setScriptStatus("ready");
      setErrorState({ script: null });
    };

    const handleError = (event: Event) => {
      console.error("Failed to load chatkit.js", event);
      if (!isMountedRef.current) return;
      setScriptStatus("error");
      const detail = (event as CustomEvent<unknown>)?.detail ?? "unknown error";
      setErrorState({ script: `Error: ${detail}`, retryable: false });
      setIsInitializingSession(false);
    };

    window.addEventListener("chatkit-script-loaded", handleLoaded);
    window.addEventListener("chatkit-script-error", handleError as EventListener);

    if (window.customElements?.get("openai-chatkit")) {
      handleLoaded();
    } else if (scriptStatus === "pending") {
      timeoutId = window.setTimeout(() => {
        if (!window.customElements?.get("openai-chatkit")) {
          handleError(
            new CustomEvent("chatkit-script-error", {
              detail: "ChatKit web component is unavailable. Verify script URL.",
            })
          );
        }
      }, 5000);
    }

    return () => {
      window.removeEventListener("chatkit-script-loaded", handleLoaded);
      window.removeEventListener("chatkit-script-error", handleError as EventListener);
      if (timeoutId) window.clearTimeout(timeoutId);
    };
  }, [scriptStatus, setErrorState]);

  // Validate workflow configuration
  const isWorkflowConfigured = Boolean(WORKFLOW_ID && !WORKFLOW_ID.startsWith("wf_replace"));

  useEffect(() => {
    if (!isWorkflowConfigured && isMountedRef.current) {
      setErrorState({
        session: "Set NEXT_PUBLIC_CHATKIT_WORKFLOW_ID in your .env.local file.",
        retryable: false,
      });
      setIsInitializingSession(false);
    }
  }, [isWorkflowConfigured, setErrorState]);

  const handleResetChat = useCallback(() => {
    if (isBrowser) {
      setScriptStatus(
        window.customElements?.get("openai-chatkit") ? "ready" : "pending"
      );
    }
    setIsInitializingSession(true);
    setErrors(createInitialErrors());
    setWidgetInstanceKey((prev) => prev + 1);
  }, []);

  /**
   * Get client secret from backend
   * Implements the official ChatKit session pattern
   */
  const getClientSecret = useCallback(
    async (currentSecret: string | null) => {
      if (isDev) {
        console.info("[ChatKitPanel] getClientSecret invoked", {
          currentSecretPresent: Boolean(currentSecret),
          workflowId: WORKFLOW_ID,
          endpoint: CREATE_SESSION_ENDPOINT,
        });
      }

      if (!isWorkflowConfigured) {
        const detail = "Set NEXT_PUBLIC_CHATKIT_WORKFLOW_ID in your .env.local file.";
        if (isMountedRef.current) {
          setErrorState({ session: detail, retryable: false });
          setIsInitializingSession(false);
        }
        throw new Error(detail);
      }

      if (isMountedRef.current) {
        if (!currentSecret) {
          setIsInitializingSession(true);
        }
        setErrorState({ session: null, integration: null, retryable: false });
      }

      try {
        const response = await fetch(CREATE_SESSION_ENDPOINT, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            workflow: { id: WORKFLOW_ID },
            chatkit_configuration: {
              file_upload: {
                enabled: true,
                max_size_mb: 10,
              },
            },
          }),
        });

        const raw = await response.text();

        if (isDev) {
          console.info("[ChatKitPanel] createSession response", {
            status: response.status,
            ok: response.ok,
            bodyPreview: raw.slice(0, 1600),
          });
        }

        let data: Record<string, unknown> = {};
        if (raw) {
          try {
            data = JSON.parse(raw) as Record<string, unknown>;
          } catch (parseError) {
            console.error("Failed to parse create-session response", parseError);
          }
        }

        if (!response.ok) {
          const detail = extractErrorDetail(data, response.statusText);
          console.error("Create session request failed", {
            status: response.status,
            body: data,
          });
          throw new Error(detail);
        }

        const clientSecret = data?.client_secret as string | undefined;
        if (!clientSecret) {
          throw new Error("Missing client secret in response");
        }

        if (isMountedRef.current) {
          setErrorState({ session: null, integration: null });
        }

        return clientSecret;
      } catch (error) {
        console.error("Failed to create ChatKit session", error);
        const detail =
          error instanceof Error
            ? error.message
            : "Unable to start ChatKit session.";
        if (isMountedRef.current) {
          setErrorState({ session: detail, retryable: false });
        }
        throw error instanceof Error ? error : new Error(detail);
      } finally {
        if (isMountedRef.current && !currentSecret) {
          setIsInitializingSession(false);
        }
      }
    },
    [isWorkflowConfigured, setErrorState]
  );

  /**
   * Handle client-side tool invocations
   * Official ChatKit pattern for client tools
   */
  const handleClientTool = useCallback(
    async (invocation: ClientToolInvocation) => {
      if (isDev) {
        console.debug("[ChatKitPanel] onClientTool", invocation);
      }

      // Built-in theme switching tool
      if (invocation.name === "switch_theme") {
        const requested = invocation.params.theme;
        if (requested === "light" || requested === "dark") {
          onThemeChange?.(requested);
          return { success: true };
        }
        return { success: false };
      }

      // Delegate to custom handler
      if (onClientTool) {
        try {
          return await onClientTool(invocation);
        } catch (error) {
          console.error("Client tool handler error", error);
          return { success: false, error: String(error) };
        }
      }

      return { success: false };
    },
    [onClientTool, onThemeChange]
  );

  // Initialize ChatKit with official hooks
  const chatkit = useChatKit({
    api: { getClientSecret },
    theme: {
      colorScheme: theme,
      // Add custom theme configuration here
      // See: https://chatkit.studio/playground
    },
    startScreen: {
      greeting: "👋 Welcome to Voice Automation Platform",
      prompts: [
        "Research the latest AI trends and create a report",
        "Review the code quality in this repository",
        "Help me automate a workflow",
      ],
    },
    composer: {
      placeholder: "Type or speak your command...",
      attachments: {
        enabled: true,
      },
    },
    threadItemActions: {
      feedback: true,
    },
    onClientTool: handleClientTool,
    onResponseEnd: () => {
      onResponseEnd?.();
    },
    onResponseStart: () => {
      setErrorState({ integration: null, retryable: false });
      onResponseStart?.();
    },
    onThreadChange: () => {
      // Handle thread change
      if (isDev) {
        console.debug("[ChatKitPanel] Thread changed");
      }
    },
    onError: ({ error }: { error: unknown }) => {
      console.error("ChatKit error", error);
    },
  });

  const activeError = errors.session ?? errors.integration;
  const blockingError = errors.script ?? activeError;

  if (isDev) {
    console.debug("[ChatKitPanel] render state", {
      isInitializingSession,
      hasControl: Boolean(chatkit.control),
      scriptStatus,
      hasError: Boolean(blockingError),
      workflowId: WORKFLOW_ID,
    });
  }

  return (
    <div className="relative flex flex-col overflow-hidden bg-white dark:bg-slate-900 rounded-lg shadow-sm">
      <ChatKit
        key={widgetInstanceKey}
        control={chatkit.control}
        className={
          blockingError || isInitializingSession
            ? "pointer-events-none opacity-0"
            : `block ${className}`
        }
      />
      {(blockingError || isInitializingSession) && (
        <div className="absolute inset-0 flex items-center justify-center bg-white/80 dark:bg-slate-900/80">
          {blockingError ? (
            <div className="text-center p-6 max-w-md">
              <div className="text-red-600 dark:text-red-400 mb-4">
                ⚠️ {blockingError}
              </div>
              {errors.retryable && (
                <button
                  onClick={handleResetChat}
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                >
                  Restart Chat
                </button>
              )}
            </div>
          ) : (
            <div className="text-center p-6">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
              <div className="text-gray-600 dark:text-gray-400">
                Loading assistant session...
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

function extractErrorDetail(
  payload: Record<string, unknown> | undefined,
  fallback: string
): string {
  if (!payload) return fallback;

  const error = payload.error;
  if (typeof error === "string") return error;

  if (
    error &&
    typeof error === "object" &&
    "message" in error &&
    typeof (error as { message?: unknown }).message === "string"
  ) {
    return (error as { message: string }).message;
  }

  const details = payload.details;
  if (typeof details === "string") return details;

  if (details && typeof details === "object" && "error" in details) {
    const nestedError = (details as { error?: unknown }).error;
    if (typeof nestedError === "string") return nestedError;
    if (
      nestedError &&
      typeof nestedError === "object" &&
      "message" in nestedError &&
      typeof (nestedError as { message?: unknown }).message === "string"
    ) {
      return (nestedError as { message: string }).message;
    }
  }

  if (typeof payload.message === "string") return payload.message;

  return fallback;
}

