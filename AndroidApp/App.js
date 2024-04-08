import React, { useState, useEffect } from "react";
import { StyleSheet, View, Text } from "react-native";
import QRCode from "react-native-qrcode-svg";
import SelectRoomPage from "./SelectRoomPage";
import MainPage from "./MainPage";

const App = () => {
  const [selectedRoom, setSelectedRoom] = useState("");
  const [rooms, setRooms] = useState([]);
  const [name, setName] = useState("");
  const [abbreviation, setAbbreviation] = useState("");
  const [currentPage, setCurrentPage] = useState("RoomPicker");

  const fetchSubject = async () => {
    try {
      const room = 1;
      const currentTime = "2024-03-11 09:42:00.00";
      const requestData = {
        room: room,
        date: currentTime,
      };

      const response = await fetch(
        "http://192.168.1.50:5000/subjects/current",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(requestData),
        }
      );

      if (!response.ok) {
        throw new Error("Network response was not ok");
      }

      const data = await response.json();

      setAbbreviation(data.abbreviation);
      setName(data.name);
    } catch (error) {
      console.error("There was a problem with the fetch operation:", error);
    }
  };
  const fetchRooms = async () => {
    try {
      const response = await fetch("http://192.168.1.50:5000/rooms", {
        method: "GET",
      });

      if (!response.ok) {
        if (response.status === 404) {
          setRooms([]);
        } else {
          throw new Error("Failed to fetch");
        }
      }
      const data = await response.json();
      console.log(data);
      setRooms(data);
    } catch (err) {
      console.error("Fetch error:", err);
    }
  };

  useEffect(() => {
    fetchSubject();
    fetchRooms();
  }, []);

  const qrValue = "https://www.feedbackiesc.ro";

  const goToMainPage = () => {
    setCurrentPage("Main");
  };

  return (
    <View style={styles.container}>
      {currentPage === "RoomPicker" && (
        <SelectRoomPage
          rooms={rooms}
          selectedRoom={selectedRoom}
          setSelectedRoom={setSelectedRoom}
          goToMainPage={goToMainPage}
        />
      )}
      {currentPage === "Main" && (
        <MainPage name={name} abbreviation={abbreviation} qrValue={qrValue} />
      )}
    </View>
  );
};

export default App;

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#fff",
    alignItems: "center",
    justifyContent: "center",
  },
  name: {
    fontSize: 30,
    fontWeight: "bold",
    textAlign: "center",
  },
  abbreviation: {
    fontSize: 30,
    fontWeight: "bold",
    marginBottom: 10,
  },
  code: {
    marginTop: 40,
    fontSize: 60,
    fontWeight: "bold",
  },
});
