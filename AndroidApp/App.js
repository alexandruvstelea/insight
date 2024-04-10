import React from "react";
import SelectRoomPage from "./screens/SelectRoomPage";
import MainPage from "./screens/MainPage";
import { NavigationContainer } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";

export default function App() {
  const Stack = createNativeStackNavigator();

  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="SelectRoomPage">
        <Stack.Screen
          name="SelectRoomPage"
          component={SelectRoomPage}
          options={{ headerShown: false }}
        />
        <Stack.Screen
          name="MainPage"
          component={MainPage}
          options={{ headerShown: false }}
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
