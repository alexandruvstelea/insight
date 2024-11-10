import { useState } from "react";
import HeaderSection from "@/components/HeaderSection";
import { useNotification } from "@/context/NotificationContext";

export default function ReportForm() {
  const { notify } = useNotification();
  const [text, setText] = useState("");

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    const timestamp = new Date().toISOString();

    try {
      const response = await fetch(`${process.env.API_URL}/reports/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          text,
          timestamp,
        }),
        credentials: "include",
      });

      if (!response.ok) {
        throw new Error(`Eroare ${response.status}: ${response.statusText}`);
      }
      notify("Raportul a fost adăugat cu succes.", "success");
      setText("");
    } catch (error: any) {
      notify(error.message, "error");
    }
  };

  return (
    <div className="w-full mt-20 p-4 flex justify-center items-center flex-col">
      <div className="max-w-2xl w-full bg-slate-700 p-4 rounded">
        <HeaderSection count={false} title="Raportează bug" />
        <form onSubmit={handleSubmit}>
          <div className="mb-5">
            <label htmlFor="text" className="label">
              Descrierea bug-ului *
            </label>
            <textarea
              id="text"
              name="text"
              rows={6}
              placeholder="Descrie bug-ul in detaliu"
              className="input"
              value={text}
              onChange={(e) => setText(e.target.value)}
              required
              minLength={10}
              maxLength={500}
            />
          </div>

          <button type="submit" className="button w-full">
            Trimite raportul
          </button>
        </form>
      </div>
    </div>
  );
}
