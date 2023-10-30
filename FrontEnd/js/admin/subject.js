function getAndDisplaySubjects() {
  fetch(`${URL}/subjects`, { method: "GET" })
    .then(response => response.json())
    .then(subjects => {
      subjects.sort((a, b) => a.professor_id - b.professor_id);
      const tableBody = document.querySelector("#subjectsTable tbody");
      tableBody.innerHTML = '';

      subjects.forEach(subject => {
        const row = document.createElement("tr");
        row.innerHTML = `
        <tr>
<td>${subject.id}</td>
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

function addSubject() {
  event.preventDefault();
  const form = document.getElementById("addSubjectForm");
  const formData = new FormData(form);
  const semesterValue = document.querySelector('input[name="semester"]:checked').value;
  formData.set("semester", semesterValue);
  const url = `${URL}/subjects`;

  fetch(url, { method: "POST", body: formData })
    .then(response => response.json())
    .then(newSubject => { 
      console.log(newSubject); 
      form.reset(); 
      getAndDisplaySubjects()
    })
    .catch(err => console.log(err))
}


function deleteSubject(id) {
  event.preventDefault();
  const url = `${URL}/subjects/${id}`;

  fetch(url, { method: "DELETE" })
    .then(response => { getAndDisplaySubjects() })
    .catch(err => console.log(err));
}

function displayEditSubject(id) {
  document.getElementById("addEditTitleSubject").innerText = "Editare"
  fetch(`${URL}/subjects/${id}`, { method: "GET" })
    .then(response => response.json())
    .then(subject => {
      const updateForm = document.getElementById("editSubjectForm");
      updateForm.classList.remove("hide");

      const editFields = updateForm.querySelectorAll("input");
      editFields[0].value = subject.name;
      editFields[1].value = subject.abbreviation;
      editFields[2].value = subject.professor_id;
      editFields[3].value = subject.semester;
      editFields[4].value = subject.id;

      document.getElementById("addSubjectForm").classList.add("hide");
    })
    .catch(err => console.log(err));
}

function editSubject() {
  event.preventDefault();
  document.getElementById("addEditTitleSubject").innerText = "Adaugare"
  const form = document.getElementById("editSubjectForm");
  const formData = new FormData(form);
  const id = document.getElementById("subjectId").value
  const url = `${URL}/subjects/${id}`;

  formData.delete("subjectId");

  fetch(url, { method: "PUT", body: formData })
    .then(response => response.json())
    .then(updatedSubject => {
      console.log(updatedSubject);
      form.reset();
      getAndDisplaySubjects();
      document.getElementById("editSubjectForm").classList.toggle("hide");
      document.getElementById("addSubjectForm").classList.toggle("hide");
    })
    .catch(err => console.log(err));
}
