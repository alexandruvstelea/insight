import React, { useState, useEffect } from "react";
import { StyleSheet, View, Text } from "react-native";
import QRCode from "react-native-qrcode-svg";

const App = () => {
  const [abbreviation, setAbbreviation] = useState("");
  const [name, setName] = useState("");

  useEffect(() => {
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
        console.log(data);
        setAbbreviation(data.abbreviation);
        setName(data.name);
      } catch (error) {
        console.error("There was a problem with the fetch operation:", error);
      }
    };

    fetchSubject();

    const interval = setInterval(() => {
      fetchSubject();
    }, 60000);

    return () => clearInterval(interval);
  }, []);

  const qrValue = "https://www.feedbackiesc.ro";

  return (
    <View style={styles.container}>
      <Text> {abbreviation}</Text>
      <Text> {name}</Text>
      <QRCode value={qrValue} size={200} />
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
});
