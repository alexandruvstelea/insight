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

  const BACKEND_IP = "192.168.1.6:5000";

  const fetchRooms = async () => {
    try {
      const response = await fetch(`http://${BACKEND_IP}/rooms`, {
        method: "GET",
      });

      if (!response.ok) {
        if (response.status === 404) {
          setRooms([]);
        } else {
          throw new Error("Failed to fetch rooms.");
        }
      }
      const data = await response.json();
      setRooms(data);
    } catch (error) {
      console.error(error);
    }
  };

  const handleLogin = async (e) => {
    e.preventDefault();

    const formData = new FormData();
    formData.append("email", email);
    formData.append("password", password);

    try {
      const response = await fetch(`http://${BACKEND_IP}/login`, {
        method: "POST",
        body: formData,
        credentials: "include",
      });

      if (response.ok) {
        navigation.navigate("MainPage");
      } else {
        throw new Error("Authentication failed.");
      }
    } catch (error) {
      console.error(error);
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
      <View style={styles.titleContainer}>
        <Text style={styles.title}>Feedback IESC</Text>
        <Text style={styles.subtitle}>Android Companion</Text>
      </View>
      <View style={styles.contentContainer}>
        <Text style={styles.dropdownLabel}>Selectează sala</Text>
        <Picker
          selectedValue={selectedRoom}
          onValueChange={(itemValue, itemIndex) => setSelectedRoom(itemValue)}
          style={styles.picker}
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
      </View>

      <Button title="Continuă" onPress={handleLogin} />
    </View>
  );
}
