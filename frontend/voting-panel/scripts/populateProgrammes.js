async function fetchProgrammes() {
  try {
    const response = await fetch("http://localhost:8000/api/programmes", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) {
      throw new Error(`Error fetching programmes: ${response.statusText}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error fetching programmes:", error);
  }
}

export async function populateDropdown() {
  const programmeSelect = document.getElementById("programme-select");
  const programmes = await fetchProgrammes();

  if (programmes) {
    programmes.forEach((program) => {
      const option = document.createElement("option");
      option.value = program.id.toString();
      option.textContent = program.name;
      programmeSelect.appendChild(option);
    });
  }
}
