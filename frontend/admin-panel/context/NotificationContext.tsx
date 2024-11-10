import React, { createContext, useContext, useState, ReactNode } from "react";
import SuccessToast from "@/components/SuccessToast";
import ErrorToast from "@/components/ErrorToast";

interface Notification {
  type: "success" | "error";
  message: string;
}

interface NotificationContextType {
  notify: (message: string, type: "success" | "error") => void;
}

const NotificationContext = createContext<NotificationContextType | undefined>(
  undefined
);

export const NotificationProvider: React.FC<{ children: ReactNode }> = ({
  children,
}) => {
  const [notification, setNotification] = useState<Notification | null>(null);

  const notify = (message: string, type: "success" | "error") => {
    setNotification({ message, type });
    setTimeout(() => setNotification(null), 2000);
  };

  return (
    <NotificationContext.Provider value={{ notify }}>
      {children}
      {notification?.type === "success" && (
        <SuccessToast
          message={notification.message}
          onClose={() => setNotification(null)}
        />
      )}
      {notification?.type === "error" && (
        <ErrorToast
          message={notification.message}
          onClose={() => setNotification(null)}
        />
      )}
    </NotificationContext.Provider>
  );
};

export const useNotification = () => {
  const context = useContext(NotificationContext);
  if (!context) {
    throw new Error(
      "useNotification must be used within a NotificationProvider"
    );
  }
  return context;
};
