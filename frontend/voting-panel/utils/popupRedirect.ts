import { AppRouterInstance } from "next/dist/shared/lib/app-router-context.shared-runtime";
import { Router } from "next/router";

export function handlePopupRedirect(
  showPopup: boolean,
  setRedirectCountdown: React.Dispatch<React.SetStateAction<number>>,
  router: AppRouterInstance 
) {
  if (showPopup) {
    const countdownInterval = setInterval(() => {
      setRedirectCountdown((prev) => prev - 1);
    }, 1000);

    const redirectTimeout = setTimeout(() => {
      router.push("https://www.google.com");
    }, 5000);

    return () => {
      clearInterval(countdownInterval);
      clearTimeout(redirectTimeout);
    };
  }
}
