
function getAndDisplayCourses() {
  fetch(`${URL}/courses`, { method: "GET" })
    .then(response => response.json())
    .then(courses => {
      courses.sort((a, b) => a.id - b.id);
      const tableBody = document.querySelector("#coursesTable tbody");
      tableBody.innerHTML = '';

      courses.forEach(course => {
        const row = document.createElement("tr");
        row.innerHTML = `
        <tr>
<td>${course.id}</td>
<td>${course.subject_id}</td>
<td>${course.type}</td>
<td>${course.room_id}</td>
<td>${course.day}</td>
<td>${course.week_type}</td>
<td>${course.start}</td>
<td>${course.end}</td>
<td><button onclick="deleteCourse(${course.id})">Șterge</button></td>
<td><button onclick="displayEditCourse(${course.id})">Editează</button></td>
</tr>
                `;
        tableBody.appendChild(row);
      });
    })
    .catch(err => console.log(err));
}

function addCourse() {
  event.preventDefault();
  const form = document.getElementById("addCourseForm");
  const formData = new FormData(form);
  const url = `${URL}/courses`;

  fetch(url, { method: "POST", body: formData })
    .then(response => response.json())
    .then(newCourse => { 
      console.log(newCourse); 
      form.reset(); 
      getAndDisplayCourses()
    })
    .catch(err => console.log(err))
}

function deleteCourse(id) {
  event.preventDefault();
  const url = `${URL}/courses/${id}`;

  fetch(url, { method: "DELETE" })
    .then(response => { getAndDisplayCourses() })
    .catch(err => console.log(err));
}

function displayEditCourse(id) {
  event.preventDefault();
  document.getElementById("addEditTitleCourse").innerText = "Editare"
  fetch(`${URL}/courses/${id}`, { method: "GET" })
    .then(response => response.json())
    .then(course => {
      const updateForm = document.getElementById("editCourseForm");
      updateForm.classList.remove("hide");

      const editFields = updateForm.querySelectorAll("input");
      editFields[0].value = course.subject_id;
      editFields[1].value = course.type;
      editFields[2].value = course.room_id;
      editFields[3].value = course.day;
      editFields[4].value = course.week_type;
      editFields[5].value = course.start;
      editFields[6].value = course.end;
      editFields[7].value = course.id;

      document.getElementById("addCourseForm").classList.add("hide");
    })
    .catch(err => console.log(err));
}

function editCourse() {
  event.preventDefault();
  document.getElementById("addEditTitleCourse").innerText = "Adaugare"
  const form = document.getElementById("editCourseForm");
  const formData = new FormData(form);
  const id = document.getElementById("courseID").value
  const url = `${URL}/courses/${id}`;

  formData.delete("courseID");

  fetch(url, { method: "PUT", body: formData })
    .then(response => response.json())
    .then(updatedCourse => {
      console.log(updatedCourse);
      form.reset();
      getAndDisplayCourses();
      document.getElementById("editCourseForm").classList.toggle("hide");
      document.getElementById("addCourseForm").classList.toggle("hide");
    })
    .catch(err => console.log(err));
}
