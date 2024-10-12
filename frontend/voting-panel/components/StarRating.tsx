"use client";
import React, { useState } from "react";

interface StarRatingProps {
  title: string;
  name: string;
}

const StarRating: React.FC<StarRatingProps> = ({ title, name }) => {
  const [rating, setRating] = useState<number | null>(null);
  const [hover, setHover] = useState<number | null>(null);

  return (
    <div>
      <h2 className="text-base leading-tight font-semibold py-2">{title}</h2>
      <div className="rating flex flex-row justify-around gap-1 max-w-md ">
        {[...Array(5)].map((_, index) => {
          const currentRating: number = index + 1;

          const isActive =
            currentRating <= (hover !== null ? hover : rating || 0);
          const filter = isActive
            ? "drop-shadow(3px 3px 2px rgba(0, 0, 0, 0.6))"
            : "none";

          return (
            <label key={index}>
              <input
                className="hidden"
                type="radio"
                name={name}
                id={`${name}-${currentRating}`}
                value={currentRating}
                onChange={() => setRating(currentRating)}
              />
              <span
                className="cursor-pointer"
                onMouseEnter={() => setHover(currentRating)}
                onMouseLeave={() => setHover(null)}
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  height="54"
                  width="60"
                  viewBox="0 0 576 512"
                  className="transition-all duration-500 max-w-full"
                  filter={filter}
                >
                  <path
                    className="transition-all duration-500 "
                    fill={isActive ? "#00c6fb" : "#E0E0E0"}
                    d="M316.9 18C311.6 7 300.4 0 288.1 0s-23.4 7-28.8 18L195 150.3 51.4 171.5c-12 1.8-22 10.2-25.7 21.7s-.7 24.2 7.9 32.7L137.8 329 113.2 474.7c-2 12 3 24.2 12.9 31.3s23 8 33.8 2.3l128.3-68.5 128.3 68.5c10.8 5.7 23.9 4.9 33.8-2.3s14.9-19.3 12.9-31.3L438.5 329 542.7 225.9c8.6-8.5 11.7-21.2 7.9-32.7s-13.7-19.9-25.7-21.7L381.2 150.3 316.9 18z"
                  />
                </svg>
              </span>
            </label>
          );
        })}
      </div>
    </div>
  );
};

export default StarRating;
