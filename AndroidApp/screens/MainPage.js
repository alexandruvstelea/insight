import React, { useState, useEffect } from "react";
import { View, Text } from "react-native";
import QRCode from "react-native-qrcode-svg";
import styles from "../styles/styles";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { BACKEND_IP } from "@env";

export default function MainPage() {
  const [name, setName] = useState("");
  const [abbreviation, setAbbreviation] = useState("");
  const [roomId, setRoomId] = useState("");
  const [code, setCode] = useState("");

  const fetchSubject = async () => {
    console.log(`${roomId} wadaw`);
    try {
      const currentTime = "2024-04-09 19:49:53.079";
      const requestData = {
        room: 1,
        date: currentTime,
      };
      console.log(requestData);
      const response = await fetch(`http://${BACKEND_IP}/subjects/current`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(requestData),
      });

      if (!response.ok) {
        console.log(response);
        throw new Error("Network response was not ok");
      }

      const data = await response.json();

      setAbbreviation(data.abbreviation);
      setName(data.name);
    } catch (error) {
      console.error("There was a problem with the fetch operation:", error);
    }
  };
  const fetchCode = async () => {
    try {
      const response = await fetch(`http://${BACKEND_IP}/code/1`, {
        method: "GET",
        credentials: "include",
      });

      if (!response.ok) {
        if (response.status === 404) {
          setCode([]);
        } else {
          console.log(response.status);
          throw new Error("Failed to fetch");
        }
      }
      const data = await response.json();
      console.log(data);
      setCode(data.code);
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    const getRoomFromStorage = async () => {
      try {
        const storedRoom = await AsyncStorage.getItem("@selectedRoomId");
        console.log("storedRoom ", storedRoom);
        if (storedRoom !== null) {
          setRoomId(storedRoom);
          await fetchSubject();
        }
      } catch (error) {
        console.error("AsyncStorage error:", error);
      }
    };

    getRoomFromStorage();

    fetchCode();
  }, [roomId]);

  const qrValue = `https://prkws2bw-3002.euw.devtunnels.ms/vote?roomId=${roomId}`;
  return (
    <View style={styles.container}>
      <Text style={styles.name}>{roomId}</Text>
      <Text style={styles.name}>{name}</Text>
      <Text style={styles.abbreviation}>{abbreviation}</Text>
      <QRCode value={qrValue} size={200} />
      <Text style={styles.code}>{code}</Text>
    </View>
  );
}
