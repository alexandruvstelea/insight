async function getAndDisplaySubjects() {
  try {
    const response = await fetch(`/api/subjects`, { method: "GET" });
    if (response.status === 404) {
      const tableBody = document.querySelector("#subjectsTable tbody");
      tableBody.innerHTML = '<tr><td colspan="5">No subjects found</td></tr>';
      return;
    }
    const subjects = await response.json();

    subjects.sort((a, b) => a.professor_id - b.professor_id);

    const tableBody = document.querySelector("#subjectsTable tbody");
    tableBody.innerHTML = '';

    for (const subject of subjects) {
      const professorResponse = await fetch(`/api/professors/${subject.professor_id}`, { method: "GET" });
      const professor = await professorResponse.json();

      const row = document.createElement("tr");
      row.innerHTML = `
        <td>${subject.id}</td>
        <td>${subject.name}</td>
        <td>${subject.abbreviation}</td>
        <td>${professor.first_name} ${professor.last_name}</td>
        <td>${subject.semester}</td>
        <td><button onclick="handleDeleteSubjectButtonClick(${subject.id})">Șterge</button></td>
        <td><button onclick="handleEditSubjectButtonClick(${subject.id})">Editează</button></td>
      `;
      tableBody.appendChild(row);
    }
  } catch (err) {
    console.log(err);
  }
}

async function handleDeleteSubjectButtonClick(subjectId) {
  await deleteSubject(subjectId);
  await getAndDisplaySubjects();
  await getAndDisplaySubjectInCourses();
}
async function handleEditSubjectButtonClick(subjectId) {
  await displayEditSubject(subjectId)
}

async function addSubject() {
  const token = sessionStorage.getItem('access_token');
  const form = document.getElementById("addSubjectForm");
  const formData = new FormData(form);

  try {
    const response = await fetch(`/api/subjects`, {
      method: "POST",
      body: formData,
      headers: {
        'Authorization': `Bearer ${token}`,
      }
    });
    const newSubject = await response.json();

    console.log(newSubject);
    form.reset();
  } catch (err) {
    console.log(err);
  }
}

async function deleteSubject(id) {
  const token = sessionStorage.getItem('access_token');

  try {
    const response = await fetch(`/api/subjects/${id}`, {
      method: "DELETE",
      headers: {
        'Authorization': `Bearer ${token}`,
      }
    });

  } catch (err) {
    console.log(err);
  }
}

async function displayEditSubject(id) {
  document.getElementById("addEditTitleSubject").innerText = "Editare";

  try {
    const response = await fetch(`/api/subjects/${id}`, { method: "GET" });
    const subject = await response.json();

    const updateForm = document.getElementById("editSubjectForm");
    updateForm.classList.remove("hide");

    const selectFields = updateForm.querySelectorAll("select");
    const editFields = updateForm.querySelectorAll("input");

    editFields[0].value = subject.name;
    editFields[1].value = subject.abbreviation;
    editFields[2].value = subject.id;
    selectFields[0].querySelector(`option[value="${subject.professor_id}"]`).selected = true;
    selectFields[1].querySelector(`option[value="${subject.semester}"]`).selected = true;

    document.getElementById("addSubjectForm").classList.add("hide");
  } catch (err) {
    console.log(err);
  }
}

async function editSubject() {
  const token = sessionStorage.getItem('access_token');
  document.getElementById("addEditTitleSubject").innerText = "Adaugare";
  const form = document.getElementById("editSubjectForm");
  const formData = new FormData(form);
  const id = document.getElementById("subjectId").value;

  formData.delete("subjectId");

  try {
    const response = await fetch(`/api/subjects/${id}`, {
      method: "PUT",
      body: formData,
      headers: {
        'Authorization': `Bearer ${token}`,
      }
    });
    const updatedSubject = await response.json();

    console.log(updatedSubject);
    form.reset();
    document.getElementById("editSubjectForm").classList.toggle("hide");
    document.getElementById("addSubjectForm").classList.toggle("hide");
  } catch (err) {
    console.log(err);
  }
}

async function getAndDisplaySubjectInCourses() {
  try {
    const response = await fetch(`/api/subjects`, { method: "GET" });
    if (response.status === 404) {
      const select = document.getElementById("subject_id");
      const select2 = document.getElementById("new_subject_id");

      select.innerHTML = '<option value="">-- Selectați Materia --</option>';
      select2.innerHTML = '<option value="">-- Selectați Materia --</option>';
      return;
    }
    const subjects = await response.json();

    const select = document.getElementById("subject_id");
    const select2 = document.getElementById("new_subject_id");

    select.innerHTML = '<option value="">-- Selectați Materia --</option>';
    select2.innerHTML = '<option value="">-- Selectați Materia --</option>';

    subjects.forEach(subject => {
      const option = document.createElement("option");
      option.text = subject.name;
      option.value = subject.id;
      select.appendChild(option.cloneNode(true));

      select2.appendChild(option.cloneNode(true));
    });
  } catch (err) {
    console.log(err);
  }
}