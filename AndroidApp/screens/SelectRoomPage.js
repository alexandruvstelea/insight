import React, { useState, useEffect } from "react";
import { View, Text, Button, TextInput } from "react-native";
import { Picker } from "@react-native-picker/picker";
import styles from "../styles/styles";
import AsyncStorage from "@react-native-async-storage/async-storage";

export default function SelectRoomPage({ navigation }) {
  const [rooms, setRooms] = useState([]);
  const [selectedRoom, setSelectedRoom] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  // useEffect(() => {
  //   const checkSelectedRoom = async () => {
  //     try {
  //       const selectedRoomId = await AsyncStorage.getItem("@selectedRoomId");
  //       if (selectedRoomId) {
  //         navigation.replace("MainPage");
  //       }
  //     } catch (err) {
  //       console.error("AsyncStorage error:", err);
  //     }
  //   };
  //   checkSelectedRoom();
  // }, []);

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
      setRooms(data);
    } catch (err) {
      console.error("Fetch error:", err);
    }
  };

  const handleLogin = async (e) => {
    e.preventDefault();

    const formData = new FormData();
    formData.append("email", email);
    formData.append("password", password);

    try {
      const response = await fetch("http://192.168.1.50:5000/login", {
        method: "POST",
        body: formData,
        credentials: "include",
      });

      if (response.ok) {
        navigation.navigate("MainPage");
      } else {
        console.error("Autentificare eșuată");
      }
    } catch (error) {
      console.error("Eroare la autentificare:", error);
    }
  };

  useEffect(() => {
    fetchRooms();
  }, []);

  useEffect(() => {
    const saveSelectedRoom = async () => {
      try {
        await AsyncStorage.setItem("@selectedRoomId", selectedRoom);
      } catch (err) {
        console.error("AsyncStorage error:", err);
      }
    };
    saveSelectedRoom();
  }, [selectedRoom]);

  return (
    <View style={styles.container}>
      <Text>Selectează sala:</Text>
      <Picker
        selectedValue={selectedRoom}
        onValueChange={(itemValue, itemIndex) => setSelectedRoom(itemValue)}
        style={{ height: 50, width: 200 }}
      >
        {rooms.map((room) => (
          <Picker.Item
            key={room.id}
            label={room.name}
            value={room.id.toString()}
          />
        ))}
      </Picker>
      <TextInput
        placeholder="Email"
        value={email}
        onChangeText={setEmail}
        style={styles.input}
      />
      <TextInput
        placeholder="Password"
        secureTextEntry={true}
        value={password}
        onChangeText={setPassword}
        style={styles.input}
      />

      <Button title="Continuă" onPress={handleLogin} />
    </View>
  );
}
