import React from "react";
import { StyleSheet, View, Text } from "react-native";
import QRCode from "react-native-qrcode-svg";

const MainPage = ({ name, abbreviation, qrValue }) => {
  return (
    <View style={{ flex: 1, justifyContent: "center", alignItems: "center" }}>
      <Text style={styles.name}>{name}</Text>
      <Text style={styles.abbreviation}>{abbreviation}</Text>
      <QRCode value={qrValue} size={200} />
      <Text style={styles.code}>472912</Text>
    </View>
  );
};

export default MainPage;

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
