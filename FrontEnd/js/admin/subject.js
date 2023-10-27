function addSubject() {
  const form = document.getElementById("addSubjectForm");
  const formData = new FormData(form);
  const url = `${URL}/subjects`;

  fetch(url, { method: "POST", body: formData })
    .then(response => response.json())
    .then(newSubject => { console.log(newSubject); form.reset(); })
    .catch(err => console.log(err))
}


function getAndDisplaySubjects() {
  fetch(`${URL}/subjects`, { method: "GET" })
    .then(response => response.json())
    .then(subjects => {
      const tableBody = document.querySelector("#subjectsTable tbody");
      tableBody.innerHTML = '';

      subjects.forEach(subject => {
        const row = document.createElement("tr");
        row.innerHTML = `
        <tr>
<td>${subject.name}</td>
<td>${subject.abbreviation}</td>
<td>${subject.professor_id}</td>
<td>${subject.semester}</td>
<td><button onclick="deleteSubject(${subject.id})">Șterge</button></td>
<td><button onclick="displayEditSubject(${subject.id})">Editează</button></td>
</tr>
                `;
        tableBody.appendChild(row);
      });
    })
    .catch(err => console.log(err));
}

function deleteSubject(id) {
  const url = `${URL}/subjects/${id}`;

  fetch(url, { method: "DELETE" })
    .then(response => { getAndDisplaySubjects() })
    .catch(err => console.log(err));
}