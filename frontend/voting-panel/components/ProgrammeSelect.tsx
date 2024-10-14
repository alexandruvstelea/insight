import { Programme } from "@/components/LocationTransit";

interface ProgrammeSelectProps {
  programmes: Programme[];
  selectedProgramme: string;
  handleProgrammeChange: (e: React.ChangeEvent<HTMLSelectElement>) => void;
}

const ProgrammeSelect: React.FC<ProgrammeSelectProps> = ({
  programmes,
  selectedProgramme,
  handleProgrammeChange,
}) => {
  return (
    <select
      id="programme-select"
      name="programme-select"
      className="bg-gray-50 border border-gray-300 text-gray-900 text-base rounded-lg  focus:ring-gray-400 focus:border-gray-400 block w-full  p-2.5"
      value={selectedProgramme}
      onChange={handleProgrammeChange}
      required
    >
      <option value="" disabled hidden>
        Selectează specializarea
      </option>
      {programmes.map((programme) => (
        <option key={programme.id} value={programme.id}>
          {programme.name}
        </option>
      ))}
    </select>
  );
};

export default ProgrammeSelect;
