import { HeaderSectionProps } from "@/utils/interfaces";
import { FC } from "react";

const HeaderSection: FC<HeaderSectionProps> = ({
  title,
  buttons = [],
  count,
}) => {
  return (
    <div className="flex mb-6 w-full justify-between">
      {buttons.length > 0 ? (
        <div className="flex gap-2 w-1/4">
          {buttons.map((button, index) => (
            <button
              key={index}
              className={` button  ${button.className || ""}`}
              onClick={button.onClick}
            >
              {button.text}
            </button>
          ))}
        </div>
      ) : (
        <div className="w-1/4" />
      )}

      <div className="w-1/2 text-center text-gray-400 uppercase text-2xl font-bold">
        {title}
      </div>
      <h2 className="text-lg font-medium text-gray-400 w-1/4 lowercase text-right">{`${count} ${title}`}</h2>
    </div>
  );
};

export default HeaderSection;
