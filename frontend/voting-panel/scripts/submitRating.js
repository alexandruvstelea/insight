function showPopup() {
  const popup = document.getElementById("popup");
  popup.classList.remove("hidden");

  setTimeout(function () {
    window.location.href = "https://www.example.com";
  }, 5000);

  document.getElementById("popup-ok").onclick = function () {
    popup.classList.add("hidden");
    window.location.href = "https://www.example.com";
  };
}

async function submitRating(form) {
  const formData = new FormData(form);

  const ratings = {
    clarity: formData.get("rating_clarity"),
    interactivity: formData.get("rating_interactivity"),
    relevance: formData.get("rating_relevance"),
    comprehension: formData.get("rating_comprehension"),
  };

  for (const [key, value] of Object.entries(ratings)) {
    if (!value) {
      alert(`Te rugăm să selectezi un rating pentru: ${key}`);
      return;
    }
  }

  const ratingData = {
    programme_id: parseInt(formData.get("programme-select")),
    rating_clarity: parseInt(formData.get("rating_clarity")),
    rating_interactivity: parseInt(formData.get("rating_interactivity")),
    rating_relevance: parseInt(formData.get("rating_relevance")),
    rating_comprehension: parseInt(formData.get("rating_comprehension")),
    // timestamp: new Date().toISOString(),
    timestamp: "2023-10-02T10:35:59.961Z",
    room_id: 1,
  };

  console.log("Submitting Rating Data:", ratingData);

  try {
    const response = await fetch("http://localhost:8000/api/ratings/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(ratingData),
    });

    if (response.status === 201) {
      showPopup();
      form.reset();
    } else {
      throw new Error(`Error submitting rating: ${response.statusText}`);
    }

    const comments = formData.get("comments");
    if (comments) {
      await submitComments(
        comments,
        ratingData.programme_id,
        ratingData.room_id
      );
    }
  } catch (error) {
    console.error("Error submitting rating:", error);
  }
}

async function submitComments(comments, programme_id, room_id) {
  const commentData = {
    text: comments,
    // timestamp: new Date().toISOString(),
    timestamp: "2023-10-02T10:35:59.961Z",
    room_id: room_id,
    programme_id: programme_id,
  };

  try {
    const response = await fetch("http://localhost:8000/api/comments", {
      method: "POST",
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

export function handleSubmit(form) {
  form.addEventListener("submit", (event) => {
    event.preventDefault();
    submitRating(form);
  });
}
