"use client";
import React, { useEffect, useRef, useState } from "react";
import { redirect, useRouter } from "next/navigation";
import StarRating from "@/components/StarRating";
import ProgrammeSelect from "@/components/ProgrammeSelect";
import SuccessPopup from "@/components/SuccessPopup";
import { handlePopupRedirect } from "@/utils/popupRedirect";
import { Programme } from "@/components/LocationTransit";

interface FormProps {
  latitude: number | null;
  longitude: number | null;
  programmes: Programme[];
  roomCode: string;
  timestamp: string;
}

const Form: React.FC<FormProps> = ({
  // latitude,
  // longitude,
  programmes,
  roomCode,
  timestamp,
}) => {
  const [selectedProgramme, setSelectedProgramme] = useState<string>("");
  const [showPopup, setShowPopup] = useState(false);
  const [redirectCountdown, setRedirectCountdown] = useState(5);
  const [ratingError, setRatingError] = useState<boolean>(false);
  const [timeLeft, setTimeLeft] = useState(7200);
  const [ratingClarityError, setRatingClarityError] = useState(false);
  const [ratingInteractivityError, setRatingInteractivityError] =
    useState(false);
  const [ratingRelevanceError, setRatingRelevanceError] = useState(false);
  const [ratingComprehensionError, setRatingComprehensionError] =
    useState(false);
  const router = useRouter();

  const startTime = useRef<number | null>(null);
  const latitude = 45.644123;
  const longitude = 25.595302;

  useEffect(() => {
    const calculateTimeLeftToEvenHour = () => {
      const now = new Date();
      const currentHour = now.getHours();
      const nextEvenHour =
        currentHour % 2 === 0 ? currentHour + 2 : currentHour + 1;

      const nextEvenTime = new Date(now);
      nextEvenTime.setHours(nextEvenHour, 0, 0, 0);

      const diffInMs = nextEvenTime.getTime() - now.getTime();
      return Math.floor(diffInMs / 1000);
    };

    const initialTimeLeft = calculateTimeLeftToEvenHour();
    setTimeLeft(initialTimeLeft);
    startTime.current = Date.now();

    const timerInterval = setInterval(() => {
      if (startTime.current) {
        const timeElapsed = Math.floor((Date.now() - startTime.current) / 1000);
        const newTimeLeft = initialTimeLeft - timeElapsed;

        if (newTimeLeft <= 0) {
          router.push("/sessionExpired");
          clearInterval(timerInterval);
          return;
        }
        setTimeLeft(newTimeLeft);
      }
    }, 1000);

    return () => clearInterval(timerInterval);
  }, [router]);

  const hours = Math.floor(timeLeft / 3600);
  const minutes = Math.floor((timeLeft % 3600) / 60);
  const seconds = timeLeft % 60;

  useEffect(() => {
    const cleanup = handlePopupRedirect(
      showPopup,
      setRedirectCountdown,
      router
    );
    return cleanup;
  }, [showPopup]);

  const handleProgrammeChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const selectedValue = e.target.value;
    setSelectedProgramme(selectedValue);
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    const form = e.currentTarget;
    const formData = new FormData(form);

    const ratingClarity = formData.get("rating_clarity");
    const ratingInteractivity = formData.get("rating_interactivity");
    const ratingRelevance = formData.get("rating_relevance");
    const ratingComprehension = formData.get("rating_comprehension");

    setRatingClarityError(!ratingClarity);
    setRatingInteractivityError(!ratingInteractivity);
    setRatingRelevanceError(!ratingRelevance);
    setRatingComprehensionError(!ratingComprehension);

    if (
      !ratingClarity ||
      !ratingInteractivity ||
      !ratingRelevance ||
      !ratingComprehension
    ) {
      setRatingError(true);
      return;
    } else {
      setRatingError(false);
    }

    const ratingData = {
      programme_id: parseInt(formData.get("programme-select") as string),
      rating_clarity: parseInt(ratingClarity as string),
      rating_interactivity: parseInt(ratingInteractivity as string),
      rating_relevance: parseInt(ratingRelevance as string),
      rating_comprehension: parseInt(ratingComprehension as string),
      timestamp: timestamp,
      room_code: roomCode,
      latitude: latitude,
      longitude: longitude,
    };
    try {
      const response = await fetch(`${process.env.API_URL}/ratings/`, {
        method: "POST",
        cache: "no-store",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(ratingData),
      });

      if (!response.ok) {
        throw new Error(`Error submitting ratings: ${response.statusText}`);
      }
      if (response.status === 201) {
        form.reset();
        setShowPopup(true);

        const comments = formData.get("comment");
        if (comments) {
          await submitComments(
            comments as string,
            ratingData.programme_id,
            roomCode,
            latitude,
            longitude
          );
        }
      } else {
        throw new Error(`Error submitting rating: ${response.statusText}`);
      }
    } catch (error) {
      redirect("/generalError");
    }
  };

  async function submitComments(
    comments: string,
    programme_id: number,
    roomCode: string,
    latitude: number,
    longitude: number
  ) {
    const commentData = {
      text: comments,
      timestamp: timestamp,
      room_code: roomCode,
      programme_id: programme_id,
      latitude: latitude,
      longitude: longitude,
    };

    try {
      const response = await fetch(`${process.env.API_URL}/comments`, {
        method: "POST",
        cache: "no-store",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(commentData),
      });

      if (!response.ok) {
        throw new Error(`Error submitting comments: ${response.statusText}`);
      }
    } catch (error) {
      redirect("/generalError");
    }
  }

  return (
    <div className="max-w-md w-full mx-auto">
      <p
        className={`text-center ${
          timeLeft <= 60 ? "text-red-500" : "text-black"
        }`}
      >
        {hours < 10 ? `0${hours}` : hours}:
        {minutes < 10 ? `0${minutes}` : minutes}:
        {seconds < 10 ? `0${seconds}` : seconds}
      </p>
      <form onSubmit={handleSubmit} className="w-full p-3 flex flex-col  ">
        <div className="flex flex-col gap-6 relative mb-10">
          <StarRating
            title="Cursul a fost ușor de înțeles"
            name="rating_clarity"
            isError={ratingClarityError}
          />
          <StarRating
            title="Cursul mi-a captat atenția și a fost implicativ"
            name="rating_interactivity"
            isError={ratingInteractivityError}
          />
          <StarRating
            title="Informațiile prezentate sunt utile și aplicabile"
            name="rating_relevance"
            isError={ratingRelevanceError}
          />
          <StarRating
            title="Am înțeles pe deplin conceptele prezentate"
            name="rating_comprehension"
            isError={ratingComprehensionError}
          />
          {ratingError && (
            <div className="rounded-lg bg-red-500 text-white px-1 absolute left-0 bottom-[-34px] font-semibold  text-sm ">
              <p className="flex justify-center items-center gap-1">
                <img
                  src="/svgs/exclamationMark.svg"
                  className="w-4 h-auto"
                  alt="Succes"
                />
                Toate evaluările trebuie completate.
              </p>
            </div>
          )}
        </div>
        <div className="mb-8">
          <label
            htmlFor="comment"
            className="block mb-2 text-base font-medium text-gray-900"
          >
            Lasă un comentariu (optional):
          </label>
          <textarea
            id="comment"
            name="comment"
            rows={4}
            maxLength={200}
            minLength={20}
            className="block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 resize-none"
            placeholder="Scrie părerea ta aici..."
          ></textarea>
        </div>

        <ProgrammeSelect
          programmes={programmes}
          selectedProgramme={selectedProgramme}
          handleProgrammeChange={handleProgrammeChange}
        />

        <button
          type="submit"
          className="bg-blue-700 mt-8 w-full hover:bg-blue-800 text-white text-base font-bold p-2 rounded transition-colors duration-300 whitespace-nowrap uppercase"
        >
          Trimite Evaluarea
        </button>
      </form>

      {showPopup && <SuccessPopup redirectCountdown={redirectCountdown} />}
    </div>
  );
};

export default Form;
