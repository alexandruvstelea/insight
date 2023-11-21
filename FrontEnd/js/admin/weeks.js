function getAndDisplayWeeks() {
  fetch(`/api/weeks`, { method: "GET" })
    .then(response => {
      if (!response.ok) {
        if (response.status === 404) {
          const tableBody = document.querySelector("#weeksTable tbody");
          tableBody.innerHTML = '<tr><td colspan="4">No weeks found</td></tr>';
        } else {
          throw new Error(`Server error: ${response.status}`);
        }
        return null;
      }
      return response.json();
    })
    .then(weeks => {
      if (!weeks) return;

      const tableBody = document.querySelector("#weeksTable tbody");
      tableBody.innerHTML = '';

      weeks.forEach(week => {
        const startDate = new Date(week.start);
        const endDate = new Date(week.end);
        const formattedStartDate = `${startDate.getDate()} ${startDate.toLocaleString('default', { month: 'short' })} ${startDate.getFullYear()}`;
        const formattedEndDate = `${endDate.getDate()} ${endDate.toLocaleString('default', { month: 'short' })} ${endDate.getFullYear()}`;
        const row = document.createElement("tr");
        row.innerHTML = `
          <tr>
            <td>${week.id}</td>
            <td>${formattedStartDate}</td>
            <td>${formattedEndDate}</td>
            <td>${week.semester}</td>
          </tr>
        `;
        tableBody.appendChild(row);
      });
    })
    .catch(err => {
      console.error('An error occurred:', err);
    });
}
function generateWeeks() {
  event.preventDefault();
  const token = sessionStorage.getItem('access_token');
  const form = document.getElementById("generateWeeks");
  const formData = new FormData(form);
  const url = `/api/weeks`;

  fetch(url, {
    method: "POST",
    body: formData,
    headers: {
      'Authorization': `Bearer ${token}`,
    }
  })
    .then(response => response.json())
    .then(newSubject => {
      console.log(newSubject);
      form.reset();
      getAndDisplayWeeks()
    })
    .catch(err => console.log(err))
}

function deleteWeeks() {
  const token = sessionStorage.getItem('access_token');
  const url = `/api/weeks`;

  fetch(url, {
    method: "DELETE",
    headers: {
      'Authorization': `Bearer ${token}`,
    }
  })
    .then(response => {
      getAndDisplayWeeks()
    })
    .catch(err => console.log(err));
}

document.getElementById("yesButton").addEventListener('click', function () {
  deleteWeeks()
  modal.style.display = "none";
});
document.getElementById("noButton").addEventListener('click', function () {
  modal.style.display = "none";
});