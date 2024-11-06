"use client";

import { useState } from "react";
import IssuePopup from "@/components/IssuePopup";

export default function ReportBanner() {
  const [isVisible, setIsVisible] = useState(true);
  const [isPopupVisible, setIsPopupVisible] = useState(false);

  const handleDismiss = () => {
    setIsVisible(false);
  };

  const openPopup = () => {
    setIsPopupVisible(true);
  };

  const closePopup = () => {
    setIsPopupVisible(false);
  };

  return (
    <>
      {isVisible && (
        <div
          id="sticky-banner"
          tabIndex={-1}
          className="flex justify-between w-full p-2 border-b border-gray-200 bg-gray-200 "
        >
          <div className="flex items-center mx-auto">
            <p className="flex items-center text-sm font-normal text-gray-500">
              <span className="inline-flex p-1 me-3 bg-gray-200 rounded-full w-7 h-7 items-center justify-center flex-shrink-0">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 448 512"
                  className="w-4 h-4 text-gray-500"
                  aria-hidden="true"
                  fill="currentColor"
                >
                  <path d="M64 32C64 14.3 49.7 0 32 0S0 14.3 0 32L0 64 0 368 0 480c0 17.7 14.3 32 32 32s32-14.3 32-32l0-128 64.3-16.1c41.1-10.3 84.6-5.5 122.5 13.4c44.2 22.1 95.5 24.8 141.7 7.4l34.7-13c12.5-4.7 20.8-16.6 20.8-30l0-247.7c0-23-24.2-38-44.8-27.7l-9.6 4.8c-46.3 23.2-100.8 23.2-147.1 0c-35.1-17.6-75.4-22-113.5-12.5L64 48l0-16z" />
                </svg>
              </span>
              <span>
                Ai găsit o eroare?
                <button
                  onClick={openPopup}
                  className="ml-4 inline-flex items-center px-2 py-1 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-300"
                >
                  Raportează
                </button>
              </span>
            </p>
          </div>
          <div className="flex items-center">
            <button
              onClick={handleDismiss}
              type="button"
              className="flex-shrink-0 inline-flex justify-center w-7 h-7 items-center text-gray-400 hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm p-1.5"
            >
              <svg
                className="w-4 h-4"
                aria-hidden="true"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 14 14"
              >
                <path
                  stroke="currentColor"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6"
                />
              </svg>
            </button>
          </div>
        </div>
      )}
      {!isVisible && (
        <div
          className=" absolute top-1 left-1 p-2 bg-gray-700 text-white rounded-full cursor-pointer"
          onClick={openPopup}
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 448 512"
            className="w-3 h-3"
            aria-hidden="true"
            fill="#fff"
          >
            <path d="M64 32C64 14.3 49.7 0 32 0S0 14.3 0 32L0 64 0 368 0 480c0 17.7 14.3 32 32 32s32-14.3 32-32l0-128 64.3-16.1c41.1-10.3 84.6-5.5 122.5 13.4c44.2 22.1 95.5 24.8 141.7 7.4l34.7-13c12.5-4.7 20.8-16.6 20.8-30l0-247.7c0-23-24.2-38-44.8-27.7l-9.6 4.8c-46.3 23.2-100.8 23.2-147.1 0c-35.1-17.6-75.4-22-113.5-12.5L64 48l0-16z" />
          </svg>
        </div>
      )}
      {isPopupVisible && <IssuePopup onClose={closePopup} />}
    </>
  );
}
