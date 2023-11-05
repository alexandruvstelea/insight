async function getAndDisplayCourses() {
  try {
    const response = await fetch(`${URL}/courses`, { method: "GET" });
    if (response.status === 404) {
      const tableBody = document.querySelector("#coursesTable tbody");
      tableBody.innerHTML = '<tr><td colspan="8">No courses found</td></tr>';
      return;
    }
    const courses = await response.json();

    courses.sort((a, b) => a.id - b.id);

    const tableBody = document.querySelector("#coursesTable tbody");
    tableBody.innerHTML = '';

    for (const course of courses) {
      const subjectResponse = await fetch(`${URL}/subjects/${course.subject_id}`, { method: "GET" });
      const subject = await subjectResponse.json();

      const roomResponse = await fetch(`${URL}/rooms/${course.room_id}`, { method: "GET" });
      const room = await roomResponse.json();



      const row = document.createElement("tr");
      row.innerHTML = `
        <td>${course.id}</td>
        <td>${subject.name}</td>
        <td>${getTypeName(course.type)}</td>
        <td>${room.name}</td>
        <td>${getDayName(course.day)}</td>
        <td>${getWeekTypeName(course.week_type)}</td>
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
function getDayName(dayIndex) {
  const days = ['Luni', 'Marți', 'Miercuri', 'Joi', 'Vineri'];
  return days[dayIndex] || 'Zi necunoscută';
}
function getWeekTypeName(weekTypeIndex) {
  const weekTypes = ['Ambele', 'Impar', 'Par'];
  return weekTypes[weekTypeIndex] || 'Necunoscut';
}
function getTypeName(typeIndex) {
  const types = ['Curs', 'Laborator', 'Seminar'];
  return types[typeIndex] || 'Necunoscut';
}


async function handleDeleteCourseButtonClick(professorId) {
  await deleteCourse(professorId)
  await getAndDisplayCourses();
}
async function handleEditCourseButtonClick(professorId) {
  await displayEditCourse(professorId)
}

async function addCourse() {
  const token = sessionStorage.getItem('access_token');
  try {
    const form = document.getElementById("addCourseForm");
    const formData = new FormData(form);

    const response = await fetch(`${URL}/courses`, {
      method: "POST",
      body: formData,
      headers: {
        'Authorization': `Bearer ${token}`,
      }
    });
    const newCourse = await response.json();

    console.log(newCourse);
    form.reset();
  } catch (err) {
    console.log(err);
  }
}

async function deleteCourse(id) {
  const token = sessionStorage.getItem('access_token');
  try {
    const response = await fetch(`${URL}/courses/${id}`, {
      method: "DELETE",
      headers: {
        'Authorization': `Bearer ${token}`,
      }
    });
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

    editFields[0].value = course.id;

    selectFields[0].querySelector(`option[value="${course.subject_id}"]`).selected = true;
    selectFields[1].querySelector(`option[value="${course.type}"]`).selected = true;
    selectFields[2].querySelector(`option[value="${course.room_id}"]`).selected = true;
    selectFields[3].querySelector(`option[value="${course.day}"]`).selected = true;
    selectFields[4].querySelector(`option[value="${course.week_type}"]`).selected = true;
    selectFields[5].querySelector(`option[value="${course.start}"]`).selected = true;
    selectFields[6].querySelector(`option[value="${course.end}"]`).selected = true;


    document.getElementById("addCourseForm").classList.add("hide");
  } catch (err) {
    console.log(err);
  }
}

async function editCourse() {
  const token = sessionStorage.getItem('access_token');
  try {
    document.getElementById("addEditTitleCourse").innerText = "Adaugare";
    const form = document.getElementById("editCourseForm");
    const formData = new FormData(form);
    const id = document.getElementById("courseID").value;
    formData.delete("courseID");
    const response = await fetch(`${URL}/courses/${id}`, {
      method: "PUT",
      body: formData,
      headers: {
        'Authorization': `Bearer ${token}`,
      }
    });
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