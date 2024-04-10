import { StyleSheet } from "react-native";

export default styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#daf0f7",
    alignItems: "center",
    justifyContent: "center",
    gap: 50,
  },
  titleContainer: { alignItems: "center" },
  title: { fontSize: 40, fontWeight: "bold" },
  subtitle: { fontSize: 24 },
  contentContainer: { alignItems: "center" },
  dropdownLabel: { fontSize: 20 },
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
  picker: { height: 50, width: 200 },
  input: {
    textAlign: "center",
    width: 250,
    backgroundColor: "#fff",
    padding: 10,
    marginTop: 10,
    marginBottom: 10,
  },
  timerWrapper: { display: "flex", justifyContent: "center" },
  timer: { display: "flex", flexDirection: "column", alignItems: "center" },
  timerText: {
    fontSize: 24,
  },
  timerSeconds: { fontSize: 54 },
});
