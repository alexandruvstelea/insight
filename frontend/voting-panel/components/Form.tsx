"use client";
import React, { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
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
  latitude,
  longitude,
  programmes,
  roomCode,
  timestamp,
}) => {
  const [selectedProgramme, setSelectedProgramme] = useState<string>("");
  const [showPopup, setShowPopup] = useState(false);
  const [redirectCountdown, setRedirectCountdown] = useState(5);
  const [ratingError, setRatingError] = useState<string | null>(null);
  const router = useRouter();
  const [timeLeft, setTimeLeft] = useState(180);

  useEffect(() => {
    if (timeLeft === 0) {
      router.push("/sessionExpired");
      return;
    }

    const timerInterval = setInterval(() => {
      setTimeLeft((prevTime) => prevTime - 1);
    }, 1000);

    return () => clearInterval(timerInterval);
  }, [timeLeft, router]);

  const minutes = Math.floor(timeLeft / 60);
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

    if (
      !ratingClarity ||
      !ratingInteractivity ||
      !ratingRelevance ||
      !ratingComprehension
    ) {
      setRatingError("Toate evaluările trebuie completate.");
      return;
    } else {
      setRatingError(null);
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
          await submitComments(comments as string, ratingData.programme_id);
        }
      } else {
        throw new Error(`Error submitting rating: ${response.statusText}`);
      }
    } catch (error) {
      console.error("Error submitting rating:", error);
    }
  };

  async function submitComments(comments: string, programme_id: number) {
    const commentData = {
      text: comments,
      timestamp: timestamp,
      room_id: 1,
      programme_id: programme_id,
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
      console.error("Error submitting comments:", error);
    }
  }

  return (
    <div className="max-w-md w-full mx-auto">
      <p
        className={`text-center ${
          timeLeft <= 60 ? "text-red-500" : "text-black"
        }`}
      >
        {minutes}:{seconds < 10 ? `0${seconds}` : seconds}
      </p>
      <form
        onSubmit={handleSubmit}
        className="w-full p-3 flex flex-col jus gap-10"
      >
        <div className="flex flex-col gap-6 ">
          <StarRating
            title="Cursul a fost ușor de înțeles"
            name="rating_clarity"
          />
          <StarRating
            title="Cursul mi-a captat atenția și a fost implicativ"
            name="rating_interactivity"
          />
          <StarRating
            title="Informațiile prezentate sunt utile și aplicabile"
            name="rating_relevance"
          />
          <StarRating
            title="Am înțeles pe deplin conceptele prezentate"
            name="rating_comprehension"
          />
        </div>
        <div>
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

        <div className="w-full relative">
          {ratingError && (
            <div className=" text-red-500 absolute top-[-20px] left-0 text-sm font-bold mb-1">
              {ratingError}
            </div>
          )}
          <button
            type="submit"
            className="bg-blue-700 w-full hover:bg-blue-800 text-white text-base font-bold p-2 rounded transition-colors duration-300 whitespace-nowrap uppercase"
          >
            Trimite Evaluarea
          </button>
        </div>
      </form>

      {showPopup && <SuccessPopup redirectCountdown={redirectCountdown} />}
    </div>
  );
};

export default Form;
