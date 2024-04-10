import React, { useState } from "react";
import { View, TextInput, Button, Modal } from "react-native";
import { PASSWORD } from "@env";

export default function PasswordModal({ visible, onClose, onPasswordEntered }) {
  const [password, setPassword] = useState("");

  const handlePasswordSubmit = () => {
    const isPasswordCorrect = password === PASSWORD;
    if (isPasswordCorrect) {
      onPasswordEntered();
    } else {
      alert("Incorrect password");
    }
  };

  return (
    <Modal visible={visible} animationType="slide" transparent>
      <View
        style={{
          flex: 1,
          justifyContent: "center",
          alignItems: "center",
          backgroundColor: "rgba(0,0,0,0.5)",
        }}
      >
        <View
          style={{ backgroundColor: "white", padding: 20, borderRadius: 10 }}
        >
          <TextInput
            secureTextEntry
            placeholder="Enter password"
            onChangeText={setPassword}
            value={password}
            style={{
              marginBottom: 10,
              borderBottomWidth: 1,
              borderBottomColor: "#ccc",
            }}
          />
          <Button title="Submit" onPress={handlePasswordSubmit} />
          <Button title="Close" onPress={onClose} color="red" />
        </View>
      </View>
    </Modal>
  );
}
