"use client";

import { useEffect, useState } from "react";

export default function MobileWarning() {
  const [isMobileWarningVisible, setMobileWarningVisible] = useState(false);

  useEffect(() => {
    const checkScreenWidth = () => {
      setMobileWarningVisible(window.innerWidth < 1000);
    };

    checkScreenWidth();

    window.addEventListener("resize", checkScreenWidth);
    return () => {
      window.removeEventListener("resize", checkScreenWidth);
    };
  }, []);

  if (!isMobileWarningVisible) return null;

  return (
    <div className="fixed top-0 left-0 w-full h-full bg-black bg-opacity-70 flex justify-center items-center z-50">
      <div className="bg-white p-6 rounded-lg text-center text-lg">
        <p>
          Te rugăm să folosești aplicația pe un PC pentru o experiență mai bună.
        </p>
        <button
          onClick={() => setMobileWarningVisible(false)}
          className=" button mt-10 "
        >
          Continuă
        </button>
      </div>
    </div>
  );
}
