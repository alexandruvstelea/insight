import React, { useState } from "react";
import { View, Text, Button, StyleSheet } from "react-native";

import { Picker } from "@react-native-picker/picker";

const SelectRoomPage = ({
  rooms,
  selectedRoom,
  setSelectedRoom,
  goToMainPage,
}) => {
  return (
    <View style={{ flex: 1, justifyContent: "center", alignItems: "center" }}>
      <Text>Selectează sala:</Text>
      <Picker
        selectedValue={selectedRoom}
        onValueChange={(itemValue, itemIndex) => setSelectedRoom(itemValue)}
        style={{ height: 50, width: 200 }}
      >
        {rooms.map((room) => (
          <Picker.Item key={room.id} label={room.name} value={room.name} />
        ))}
      </Picker>
      <Button title="Continuă" onPress={goToMainPage} />
    </View>
  );
};

export default SelectRoomPage;

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
