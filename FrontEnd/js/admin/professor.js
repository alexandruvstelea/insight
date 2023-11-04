const URL = 'http://127.0.0.1:5000';

async function getAndDisplayProfessors() {
  try {
    const response = await fetch(`${URL}/professors`, { method: "GET" });
    if (response.status === 404) {
      const tableBody = document.querySelector("#professorsTable tbody");
      tableBody.innerHTML = '<tr><td colspan="4">No professors found</td></tr>';
      return;
    }
    const professors = await response.json();




    professors.sort((a, b) => a.id - b.id);

    const tableBody = document.querySelector("#professorsTable tbody");
    tableBody.innerHTML = '';

    professors.forEach(professor => {
      const row = document.createElement("tr");
      row.innerHTML = `
          <td>${professor.id}</td>
          <td>${professor.first_name}</td>
          <td>${professor.last_name}</td>
          <td>${professor.title}</td>
          <td><button onclick="handleDeleteProfessorButtonClick(${professor.id})">Șterge</button></td>
          <td><button onclick="handleEditProfessorButtonClick(${professor.id})">Editează</button></td>
      `;
      tableBody.appendChild(row);
    });
  } catch (err) {
    console.log(err);
  }
}

async function handleDeleteProfessorButtonClick(professorId) {
  await deleteProfessor(professorId);
  await getAndDisplayProfessors();
  await getAndDisplayProfessorInSubjects();
}

async function handleEditProfessorButtonClick(professorId) {
  await displayEditProfessor(professorId)
}

async function addProfessor() {
  const token = sessionStorage.getItem('access_token');
  const form = document.getElementById("addProfessorForm");
  const formData = new FormData(form);

  try {
    const response = await fetch(`${URL}/professors`, {
      method: "POST",
      body: formData,
      headers: {
        'Authorization': `Bearer ${token}`,
      }
    });
    const newProfessor = await response.json();

    console.log(newProfessor);
    form.reset();
  } catch (err) {
    console.log(err);
  }
}

async function deleteProfessor(id) {
  const token = sessionStorage.getItem('access_token');
  try {
    const response = await fetch(`${URL}/professors/${id}`, {
      method: "DELETE",
      headers: {
        'Authorization': `Bearer ${token}`,
      }
    });

  } catch (err) {
    console.log(err);
  }
}

async function displayEditProfessor(id) {
  document.getElementById("addEditTitleProfessor").innerText = "Editare";

  try {
    const response = await fetch(`${URL}/professors/${id}`, { method: "GET" });
    const professor = await response.json();

    const updateForm = document.getElementById("editProfessorForm");
    updateForm.classList.remove("hide");

    const editFields = updateForm.querySelectorAll("input");
    editFields[0].value = professor.first_name;
    editFields[1].value = professor.last_name;
    editFields[2].value = professor.title;
    editFields[3].value = professor.id;

    document.getElementById("addProfessorForm").classList.add("hide");
  } catch (err) {
    console.log(err);
  }
}

async function editProfessor() {
  document.getElementById("addEditTitleProfessor").innerText = "Adaugare";
  const token = sessionStorage.getItem('access_token');
  const form = document.getElementById("editProfessorForm");
  const formData = new FormData(form);
  const id = document.getElementById("professorId").value;

  formData.delete("professorId");

  try {
    const response = await fetch(`${URL}/professors/${id}`, {
      method: "PUT",
      body: formData,
      headers: {
        'Authorization': `Bearer ${token}`,
      }
    });
    const updatedProfessor = await response.json();

    console.log(updatedProfessor);
    form.reset();
    document.getElementById("editProfessorForm").classList.toggle("hide");
    document.getElementById("addProfessorForm").classList.toggle("hide");
  } catch (err) {
    console.log(err);
  }
}

async function getAndDisplayProfessorInSubjects() {
  try {
    const response = await fetch(`${URL}/professors`, { method: "GET" });

    if (response.status === 404) {
      const select = document.getElementById("professor_id");
      const select2 = document.getElementById("new_professor_id");

      select.innerHTML = '<option value="">-- Selectați un profesor --</option>';
      select2.innerHTML = '<option value="">-- Selectați un profesor --</option>';
      return;
    }

    const professors = await response.json();

    const select = document.getElementById("professor_id");
    const select2 = document.getElementById("new_professor_id");

    select.innerHTML = '<option value="">-- Selectați un profesor --</option>';
    select2.innerHTML = '<option value="">-- Selectați un profesor --</option>';

    professors.forEach(professor => {
      const option = document.createElement("option");
      option.text = professor.first_name;
      option.value = professor.id;
      select.appendChild(option.cloneNode(true));

      select2.appendChild(option.cloneNode(true));
    });
  } catch (err) {
    console.log(err);
  }
}

async function submitForm(event, ...functions) {
  event.preventDefault();
  for (const func of functions) {
    await func();
  }
}
