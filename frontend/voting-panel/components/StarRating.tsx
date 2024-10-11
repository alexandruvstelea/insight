"use client";
import React from "react";

interface StarRatingProps {
  title: string;
  name: string;
}

const StarRating: React.FC<StarRatingProps> = ({ title, name }) => {
  return (
    <div>
      <h2 className="text-lg font-semibold">{title}</h2>
      <div className="rating flex flex-row-reverse max-w-md min-h-[4rem]">
        {[5, 4, 3, 2, 1].map((value) => (
          <React.Fragment key={value}>
            <input
              type="radio"
              name={name}
              id={`${name}-${value}`}
              value={value}
              className="hidden"
            />
            <label
              className="flex flex-1 relative cursor-pointer"
              htmlFor={`${name}-${value}`}
            ></label>
          </React.Fragment>
        ))}
      </div>
    </div>
  );
};

export default StarRating;
