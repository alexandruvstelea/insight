
export async function fetchProgrammes() {
  try {
    const response = await fetch("http://localhost:80/api/programmes", {
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
    throw error;
  }
}
