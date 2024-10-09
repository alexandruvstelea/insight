import { populateDropdown } from "./populateProgrammes.js";
import { handleSubmit } from "./submitRating.js";

document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("rating-form");

  populateDropdown();
  handleSubmit(form);
});
