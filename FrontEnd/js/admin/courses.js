async function getAndDisplayCourses() {
  try {
    const response = await fetch(`${URL}/courses`, { method: "GET" });
    const courses = await response.json();

    courses.sort((a, b) => a.id - b.id);

    const tableBody = document.querySelector("#coursesTable tbody");
    tableBody.innerHTML = '';

    for (const course of courses) {
      const subjectResponse = await fetch(`${URL}/subjects/${course.subject_id}`, { method: "GET" });
      const subject = await subjectResponse.json();

      const row = document.createElement("tr");
      row.innerHTML = `
        <td>${course.id}</td>
        <td>${subject.name}</td>
        <td>${course.type}</td>
        <td>${course.room_id}</td>
        <td>${course.day}</td>
        <td>${course.week_type}</td>
        <td>${course.start}</td>
        <td>${course.end}</td>
        <td><button onclick="handleDeleteCourseButtonClick(${course.id})">Șterge</button></td>
        <td><button onclick="handleEditCourseButtonClick(${course.id})">Editează</button></td>
      `;
      tableBody.appendChild(row);
    };
  } catch (err) {
    console.log(err);
  }
}

async function handleDeleteCourseButtonClick(professorId) {
  await deleteCourse(professorId)
  await getAndDisplayCourses();
}
async function handleEditCourseButtonClick(professorId) {
  await displayEditCourse(professorId)
}

async function addCourse() {
  try {
    const form = document.getElementById("addCourseForm");
    const formData = new FormData(form);

    const response = await fetch(`${URL}/courses`, { method: "POST", body: formData });
    const newCourse = await response.json();

    console.log(newCourse);
    form.reset();
  } catch (err) {
    console.log(err);
  }
}

async function deleteCourse(id) {
  try {
    const response = await fetch(`${URL}/courses/${id}`, { method: "DELETE" });
  } catch (err) {
    console.log(err);
  }
}

async function displayEditCourse(id) {
  try {
    document.getElementById("addEditTitleCourse").innerText = "Editare";
    const response = await fetch(`${URL}/courses/${id}`, { method: "GET" });
    const course = await response.json();
    const updateForm = document.getElementById("editCourseForm");
    updateForm.classList.remove("hide");

    const editFields = updateForm.querySelectorAll("input");
    const selectFields = updateForm.querySelectorAll("select");

    editFields[0].value = course.subject_id;
    editFields[1].value = course.room_id;
    editFields[2].value = course.id;

    selectFields[0].querySelector(`option[value="${course.type}"]`).selected = true;
    selectFields[1].querySelector(`option[value="${course.day}"]`).selected = true;
    selectFields[2].querySelector(`option[value="${course.week_type}"]`).selected = true;
    selectFields[3].querySelector(`option[value="${course.start}"]`).selected = true;
    selectFields[4].querySelector(`option[value="${course.end}"]`).selected = true;

    document.getElementById("addCourseForm").classList.add("hide");
  } catch (err) {
    console.log(err);
  }
}

async function editCourse() {
  try {
    document.getElementById("addEditTitleCourse").innerText = "Adaugare";
    const form = document.getElementById("editCourseForm");
    const formData = new FormData(form);
    const id = document.getElementById("courseID").value;
    formData.delete("courseID");
    const response = await fetch(`${URL}/courses/${id}`, { method: "PUT", body: formData });
    const updatedCourse = await response.json();

    console.log(updatedCourse);
    form.reset();
    document.getElementById("editCourseForm").classList.toggle("hide");
    document.getElementById("addCourseForm").classList.toggle("hide");
  } catch (err) {
    console.log(err);
  }
}


function populateHoursSelect(selectId, startHour, endHour, step) {
  const select = document.getElementById(selectId);

  for (let hour = startHour; hour <= endHour; hour += step) {
    const option = document.createElement("option");
    const formattedHour = hour < 10 ? `0${hour}` : `${hour}`;
    option.value = `${formattedHour}:00`;
    option.text = `${formattedHour}:00`;
    select.appendChild(option);
  }
}
populateHoursSelect("start", 8, 22, 2);
populateHoursSelect("end", 8, 22, 2);
populateHoursSelect("new_start", 8, 22, 2);
populateHoursSelect("new_end", 8, 22, 2);


function logFormData(formData) {
  formData.forEach((value, key) => {
    console.log(`${key}: ${value}`);
  });
}