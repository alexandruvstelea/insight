import React, { useState, useEffect } from "react";
import { View, Text } from "react-native";
import QRCode from "react-native-qrcode-svg";
import styles from "../styles/styles";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { BACKEND_IP } from "@env";
import { CountdownCircleTimer } from "react-native-countdown-circle-timer";
import { BackHandler, Button } from "react-native";
import PasswordModal from "./PasswordModal";

const noCourseList = [
  "S-a luat curentu'",
  "Lasa copiutele",
  "Pauza de tigara?",
  "Mi-e foame",
  "As manca o rata",
  "Veverita jongleaza nuci",
];

export default function MainPage({ navigation }) {
  const [currentSubject, setCurrentSubject] = useState("");
  const [isSubject, setIsSubject] = useState(false);
  const [roomId, setRoomId] = useState("");
  const [code, setCode] = useState("");
  const [key, setKey] = useState(0);
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [rant, setRant] = useState("");

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
    console.log("fetchSubject()");
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
        if (response.status === 404) {
          console.log("Nu s-a gasit curs");
          setCode(false);
          setIsSubject(false);
          const randomIndex = Math.floor(Math.random() * noCourseList.length);
          setRant(noCourseList[randomIndex]);
          return;
        }
        console.log(response);
      }
      console.log("S-a gasit curs");
      setIsSubject(true);
      const data = await response.json();
      setCurrentSubject(data);
      return;
    } catch (error) {
      console.error("There was a problem with the fetch operation:", error);
    }
  };
  const fetchCode = async () => {
    console.log("fetchCode()");
    try {
      console.log("fetch code ->", roomId, isSubject);
      if (roomId && isSubject) {
        const response = await fetch(`http://${BACKEND_IP}/code/${roomId}`, {
          method: "GET",
          credentials: "include",
        });

        if (!response.ok) {
          if (response.status === 404) {
            console.log("Nu s-a putut lua noul cod.");
            setCode(false);
          } else {
            console.log(response.status);
            throw new Error("Failed to fetch");
          }
        }
        console.log("S-a luat noul cod.");
        const data = await response.json();
        setCode(data.code);
      } else {
        setCode(false);
      }
      return;
    } catch (error) {
      console.error(error);
    }
  };

  const regenerateCode = async () => {
    console.log("regenerateCode()");
    try {
      console.log("regenerate code ->", roomId, currentSubject, isSubject);
      if (roomId && currentSubject.id && isSubject) {
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
        console.log("S-a putut regenera codul.");
      } else {
        setCode(false);
      }
      return;
    } catch (error) {
      console.error(error);
    }
  };

  const pingAlive = async () => {
    try {
      const response = await fetch(`http://${BACKEND_IP}/ping/${roomId}`, {
        method: "POST",
        credentials: "include",
      });

      if (!response.ok) {
        console.log(response.status);
        throw new Error("Failed to ping");
      }
      return;
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
              setCode("Generare cod");
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
      console.log("Se regenereaza cod");
      if (isSubject) {
        await regenerateCode();
        fetchCode();
        setKey((prevKey) => prevKey + 1);
      } else {
        const randomIndex = Math.floor(Math.random() * noCourseList.length);
        setCurrentSubject(noCourseList[randomIndex]);
      }
    }, 10000);

    return () => clearInterval(intervalId);
  }, [code]);

  useEffect(() => {
    const intervalId = setInterval(async () => {
      await fetchSubject();
      await pingAlive();
      console.log("Se cauta curs.");
    }, 10000);

    return () => clearInterval(intervalId);
  }, [isSubject]);

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
    <>
      {isSubject ? (
        <View style={styles.container}>
          <Text style={styles.name}>
            {isSubject ? currentSubject.name : currentSubject}
          </Text>
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
      ) : (
        <View style={styles.container}>
          <Text>Nu se tine curs.</Text>
          <Text>{rant}</Text>
        </View>
      )}
    </>
  );
}
