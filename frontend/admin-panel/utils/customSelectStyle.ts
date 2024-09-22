// styles.ts
export const customSelectStyle= {
  control: (base: any, state: { isFocused: boolean }) => ({
    ...base,
    backgroundColor: "rgb(55, 65, 81)", // Fondul de bază
    borderColor: state.isFocused ? "rgb(107, 114, 128)" : "rgb(75, 85, 99)", // Bordura pe focus și hover
    color: "white",
    padding: "0.2rem",
    fontSize: "0.875rem",
    lineHeight: "1.25rem",
    borderRadius: "0.5rem",
    boxShadow: "none",
    "&:hover": {
      borderColor: "rgb(107 ,114 ,128)",
    },
  }),
  option: (base: any, state: { isSelected: boolean; isFocused: boolean }) => ({
    ...base,
    backgroundColor: state.isSelected
      ? "rgb(59, 130, 246)" // Fondul pentru opțiunea selectată
      : state.isFocused
      ? "rgb(75, 85, 99)" // Fondul pentru hover
      : "rgb(31, 41, 55)", // Fondul normal
    color: state.isSelected || state.isFocused ? "white" : "rgb(156, 163, 175)",
  }),
  menu: (base: any) => ({
    ...base,
    backgroundColor: "rgb(31, 41, 55)", // Fondul meniului dropdown
  }),
  singleValue: (base: any) => ({
    ...base,
    color: "white", // Culoarea pentru valoarea selectată la single select
  }),
  multiValue: (base: any) => ({
    ...base,
    backgroundColor: "rgb(75, 85, 99)", // Fondul pentru valorile selectate la multi-select
    color: "white",
  }),
  multiValueLabel: (base: any) => ({
    ...base,
    color: "white", // Culoarea textului pentru valorile selectate
  }),
  multiValueRemove: (base: any) => ({
    ...base,
    color: "white",
    "&:hover": {
      backgroundColor: "rgb(107, 114, 128)", // Fondul pe hover la remove
      color: "white",
    },
  }),
};