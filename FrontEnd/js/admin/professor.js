const URL = 'http://127.0.0.1:5000'

function getAndDisplayProfessors() {
  fetch(`${URL}/professors`, { method: "GET" })
    .then(response => response.json())
    .then(professors => {
      professors.sort((a, b) => a.id - b.id);

      const tableBody = document.querySelector("#professorsTable tbody");
      tableBody.innerHTML = '';

      professors.forEach(professor => {
        const row = document.createElement("tr");
        row.innerHTML = `
            <tr>
    <td>${professor.id}</td>
    <td>${professor.first_name}</td>
    <td>${professor.last_name}</td>
    <td>${professor.title}</td>
    <td><button onclick="deleteProfessor(${professor.id})">Șterge</button></td>
    <td><button onclick="displayEditProfessor(${professor.id})">Editează</button></td>
</tr>
                    `;
        tableBody.appendChild(row);
      });
    })
    .catch(err => console.log(err));
}

function addProfessor() {
  event.preventDefault();
  const form = document.getElementById("addProfessorForm");
  const formData = new FormData(form);
  const url = `${URL}/professors`;

  fetch(url, { method: "POST", body: formData })
    .then(response => response.json())
    .then(newProfessor => {
      console.log(newProfessor);
      form.reset();
      getAndDisplayProfessors();
    })
    .catch(err => console.log(err));
}

function deleteProfessor(id) {
  event.preventDefault();
  const url = `${URL}/professors/${id}`;

  fetch(url, { method: "DELETE" })
    .then(response => { getAndDisplayProfessors() })
    .catch(err => console.log(err));
}

function displayEditProfessor(id) {
  document.getElementById("addEditTitleProfessor").innerText = "Editare"
  fetch(`${URL}/professors/${id}`, { method: "GET" })
    .then(response => response.json())
    .then(professor => {
      const updateForm = document.getElementById("editProfessorForm");
      updateForm.classList.remove("hide");

      const editFields = updateForm.querySelectorAll("input");
      editFields[0].value = professor.first_name;
      editFields[1].value = professor.last_name;
      editFields[2].value = professor.title;
      editFields[3].value = professor.id;

      document.getElementById("addProfessorForm").classList.add("hide");
    })
    .catch(err => console.log(err));
}

function editProfessor() {
  event.preventDefault();
  document.getElementById("addEditTitleProfessor").innerText = "Adaugare"
  const form = document.getElementById("editProfessorForm");
  const formData = new FormData(form);
  const id = document.getElementById("professorId").value
  const url = `${URL}/professors/${id}`;

  formData.delete("professorId");

  fetch(url, { method: "PUT", body: formData })
    .then(response => response.json())
    .then(updatedProfessor => {
      console.log(updatedProfessor);
      form.reset();
      getAndDisplayProfessors();
      document.getElementById("editProfessorForm").classList.toggle("hide");
      document.getElementById("addProfessorForm").classList.toggle("hide");
    })
    .catch(err => console.log(err));
}

