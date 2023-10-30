
function getAndDisplayRooms() {
  fetch(`${URL}/rooms`, { method: "GET" })
    .then(response => response.json())
    .then(rooms => {
      rooms.sort((a, b) => a.id - b.id);
      const tableBody = document.querySelector("#roomsTable tbody");
      tableBody.innerHTML = '';

      rooms.forEach(room => {
        const row = document.createElement("tr");
        row.innerHTML = `
        <tr>
<td>${room.id}</td>
<td>${room.name}</td>
<td><button onclick="deleteRoom(${room.id})">Șterge</button></td>
<td><button onclick="displayEditRoom(${room.id})">Editează</button></td>
</tr>
                `;
        tableBody.appendChild(row);
      });
    })
    .catch(err => console.log(err));
}


function addRoom() {
  event.preventDefault();
  const form = document.getElementById("addRoomForm");
  const formData = new FormData(form);
  const url = `${URL}/rooms`;

  fetch(url, { method: "POST", body: formData })
    .then(response => response.json())
    .then(newRoom => { 
      console.log(newRoom); 
      form.reset(); 
      getAndDisplayRooms()
    })
    .catch(err => console.log(err))
}

function deleteRoom(id) {
  event.preventDefault();
  const url = `${URL}/rooms/${id}`;

  fetch(url, { method: "DELETE" })
    .then(response => { getAndDisplayRooms() })
    .catch(err => console.log(err));
}


function displayEditRoom(id) {
  event.preventDefault();
  document.getElementById("addEditTitleRoom").innerText = "Editare"
  fetch(`${URL}/rooms/${id}`, { method: "GET" })
    .then(response => response.json())
    .then(room => {
      const updateForm = document.getElementById("editRoomForm");
      updateForm.classList.remove("hide");

      const editFields = updateForm.querySelectorAll("input");
      editFields[0].value = room.name;
      editFields[1].value = room.id;

      document.getElementById("addRoomForm").classList.add("hide");
    })
    .catch(err => console.log(err));
}

function editRoom() {
  event.preventDefault();
  document.getElementById("addEditTitleRoom").innerText = "Adaugare"
  const form = document.getElementById("editRoomForm");
  const formData = new FormData(form);
  const id = document.getElementById("roomID").value
  const url = `${URL}/rooms/${id}`;

  formData.delete("RoomID");

  fetch(url, { method: "PUT", body: formData })
    .then(response => response.json())
    .then(updatedRoom => {
      console.log(updatedRoom);
      form.reset();
      getAndDisplayRooms();
      document.getElementById("editRoomForm").classList.toggle("hide");
      document.getElementById("addRoomForm").classList.toggle("hide");
    })
    .catch(err => console.log(err));
}


