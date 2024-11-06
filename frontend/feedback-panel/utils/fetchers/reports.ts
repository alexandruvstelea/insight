const API_URL = process.env.API_URL;

export const sendIssueReport = async (issueText: string) => {
  const formData = new FormData();
  formData.append("issueText", issueText);
  const text = formData.get("issueText")?.toString() || "";

  const now = new Date();
  const timestamp = now.toISOString().split(".")[0];

  const response = await fetch(`${API_URL}/reports`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      text,
      timestamp,
    }),
  });

  if (!response.ok) return false;
  const result = await response.json();
  return result;
};
