import React, { useState, useEffect } from "react";
import { View, Text } from "react-native";
import QRCode from "react-native-qrcode-svg";
import styles from "../styles/styles";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { BACKEND_IP } from "@env";
import { CountdownCircleTimer } from "react-native-countdown-circle-timer";
import { BackHandler, Button } from "react-native";
import PasswordModal from "./PasswordModal";

export default function MainPage({ navigation }) {
  const [currentSubject, setCurrentSubject] = useState("");
  const [roomId, setRoomId] = useState("");
  const [code, setCode] = useState("");
  const [key, setKey] = useState(0);
  const [isModalVisible, setIsModalVisible] = useState(false);

  const handlePasswordEntered = () => {
    navigation.navigate("SelectRoomPage");
  };

  const renderTime = ({ remainingTime }) => {
    return (
      <View style={styles.timer}>
        <Text style={styles.timerText}>Cod valid</Text>
        <Text style={styles.timerSeconds}>{remainingTime}</Text>
      </View>
    );
  };

  const getCurrentDate = () => {
    date = new Date();
    return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(
      2,
      "0"
    )}-${String(date.getDate()).padStart(2, "0")} ${String(
      date.getHours()
    ).padStart(2, "0")}:${String(date.getMinutes()).padStart(2, "0")}:${String(
      date.getSeconds()
    ).padStart(2, "0")}.${String(date.getMilliseconds()).padStart(3, "0")}`;
  };

  const fetchSubject = async () => {
    try {
      if (roomId) {
      }
      const timestamp = getCurrentDate();
      const requestData = {
        room: roomId,
        date: timestamp,
      };
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

      setCurrentSubject(data);
      return true;
    } catch (error) {
      console.error("There was a problem with the fetch operation:", error);
    }
  };
  const fetchCode = async () => {
    try {
      if (roomId) {
        const response = await fetch(`http://${BACKEND_IP}/code/${roomId}`, {
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
        setCode(data.code);
      }
      return true;
    } catch (error) {
      console.error(error);
    }
  };

  const regenerateCode = async () => {
    try {
      if (roomId && currentSubject.id) {
        const formData = new FormData();
        formData.append("subject_id", currentSubject.id);
        const response = await fetch(`http://${BACKEND_IP}/code/${roomId}`, {
          method: "POST",
          credentials: "include",
          body: formData,
        });
        if (!response.ok) {
          console.log(response.status);
          throw new Error(
            `An error has occured during code regeneration. Status : ${response.status}`
          );
        }
      }
      return true;
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    const initialLoadData = async () => {
      try {
        AsyncStorage.getItem("@selectedRoomId")
          .then((value) => {
            setRoomId(value);
          })
          .then(async () => {
            if (roomId) {
              await fetchSubject();
              await regenerateCode();
              await fetchCode();
            }
          });
      } catch (error) {
        console.error(
          `An error has occured during initial data loading: ${error}`
        );
      }
    };
    initialLoadData();
  }, [roomId]);

  useEffect(() => {
    const intervalId = setInterval(async () => {
      console.log("Regenerating code.");
      await regenerateCode();
      fetchCode();
      setKey((prevKey) => prevKey + 1);
    }, 10000);

    return () => clearInterval(intervalId);
  }, [code]);

  useEffect(() => {
    const backAction = () => {
      if (isModalVisible) setIsModalVisible(false);
      return true;
    };

    const backHandler = BackHandler.addEventListener(
      "hardwareBackPress",
      backAction
    );

    return () => backHandler.remove();
  }, []);

  const qrValue = `https://prkws2bw-3002.euw.devtunnels.ms/vote?roomId=${roomId}`;
  return (
    <View style={styles.container}>
      <Text style={styles.name}>{currentSubject.name}</Text>
      <QRCode value={qrValue} size={200} />
      <Text style={styles.code}>{code}</Text>
      <View style={styles.timerWrapper}>
        <CountdownCircleTimer
          key={key}
          isPlaying
          duration={10}
          colors="#007fff"
          onComplete={() => [true, 1000]}
        >
          {renderTime}
        </CountdownCircleTimer>
      </View>
      <Button title="Inapoi" onPress={() => setIsModalVisible(true)} />
      <PasswordModal
        visible={isModalVisible}
        onClose={() => setIsModalVisible(false)}
        onPasswordEntered={handlePasswordEntered}
      />
    </View>
  );
}
