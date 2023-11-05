async function getAndDisplayRooms() {
  try {
    const response = await fetch(`${URL}/rooms`, { method: "GET" });
    if (response.status === 404) {
      const tableBody = document.querySelector("#roomsTable tbody");
      tableBody.innerHTML = '<tr><td colspan="2">No rooms found</td></tr>';
      return;
    }
    const rooms = await response.json();
    rooms.sort((a, b) => a.id - b.id);
    const tableBody = document.querySelector("#roomsTable tbody");
    tableBody.innerHTML = '';
    rooms.forEach(room => {
      const row = document.createElement("tr");
      row.innerHTML = `
        <td>${room.id}</td>
        <td>${room.name}</td>
        <td><button onclick="handleDeleteRoomButtonClick(${room.id})">Șterge</button></td>
        <td><button onclick="handleEditRoomButtonClick(${room.id})">Editează</button></td>
      `;
      tableBody.appendChild(row);
    });
  } catch (err) {
    console.log(err);
  }
}

async function handleDeleteRoomButtonClick(professorId) {
  await deleteRoom(professorId)
  await getAndDisplayRooms();
  await getAndDisplayRoomInCourses()
}
async function handleEditRoomButtonClick(professorId) {
  await displayEditRoom(professorId)
}

async function addRoom() {
  const token = sessionStorage.getItem('access_token');
  const form = document.getElementById("addRoomForm");
  const formData = new FormData(form);

  try {
    const response = await fetch(`${URL}/rooms`, {
      method: "POST",
      body: formData,
      headers: {
        'Authorization': `Bearer ${token}`,
      }
    });
    const newRoom = await response.json();
    console.log(newRoom);
    form.reset();
  } catch (err) {
    console.log(err);
  }
}


async function deleteRoom(id) {
  const token = sessionStorage.getItem('access_token');
  try {
    const response = await fetch(`${URL}/rooms/${id}`, {
      method: "DELETE",
      headers: {
        'Authorization': `Bearer ${token}`,
      }
    });
  } catch (err) {
    console.log(err);
  }
}

async function displayEditRoom(id) {
  document.getElementById("addEditTitleRoom").innerText = "Editare";
  try {
    const response = await fetch(`${URL}/rooms/${id}`, { method: "GET" });
    const room = await response.json();
    const updateForm = document.getElementById("editRoomForm");
    updateForm.classList.remove("hide");
    const editFields = updateForm.querySelectorAll("input");
    editFields[0].value = room.name;
    editFields[1].value = room.id;
    document.getElementById("addRoomForm").classList.add("hide");
  } catch (err) {
    console.log(err);
  }
}

async function editRoom() {
  const token = sessionStorage.getItem('access_token');
  document.getElementById("addEditTitleRoom").innerText = "Adaugare";
  const form = document.getElementById("editRoomForm");
  const formData = new FormData(form);
  const id = document.getElementById("roomID").value;
  formData.delete("RoomID");
  try {
    const response = await fetch(`${URL}/rooms/${id}`, {
      method: "PUT",
      body: formData,
      headers: {
        'Authorization': `Bearer ${token}`,
      }
    });
    const updatedRoom = await response.json();
    console.log(updatedRoom);
    form.reset();
    document.getElementById("editRoomForm").classList.toggle("hide");
    document.getElementById("addRoomForm").classList.toggle("hide");
  } catch (err) {
    console.log(err);
  }
}

async function getAndDisplayRoomInCourses() {
  try {
    const response = await fetch(`${URL}/rooms`, { method: "GET" });
    if (response.status === 404) {
      const select = document.getElementById("room_id");
      const select2 = document.getElementById("new_room_id");

      select.innerHTML = '<option value="">-- Selectați sala --</option>';
      select2.innerHTML = '<option value="">-- Selectați sala --</option>';
      return;
    }
    const rooms = await response.json();

    const select = document.getElementById("room_id");
    const select2 = document.getElementById("new_room_id");

    select.innerHTML = '<option value="">-- Selectați sala --</option>';
    select2.innerHTML = '<option value="">-- Selectați sala --</option>';

    rooms.forEach(room => {
      const option = document.createElement("option");
      option.text = room.name;
      option.value = room.id;
      select.appendChild(option.cloneNode(true));

      select2.appendChild(option.cloneNode(true));
    });
  } catch (err) {
    console.log(err);
  }
}