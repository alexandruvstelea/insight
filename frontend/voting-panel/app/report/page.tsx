"use server";
import { redirect } from "next/navigation";

export async function submitReport(formData: FormData) {
  const text = formData.get("bugText")?.toString() || "";
  const timestamp = new Date().toISOString();

  try {
    const response = await fetch(`${process.env.API_URL}/reports`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        text,
        timestamp,
      }),
    });

    if (response.status === 200) {
      redirect("/");
    }

    if (!response.ok) {
      if (response.status === 429) {
        redirect("/toManyRequests");
      } else {
        redirect("/generalError");
      }
    }
  } catch (error) {
    return redirect("/generalError");
  }
}

export default async function Report() {
  return (
    <div className="max-w-md w-full mx-auto">
      <form
        action={submitReport}
        method="POST"
        className="w-full p-3 flex flex-col"
      >
        <label
          htmlFor="bugText"
          className="block mb-2 text-base font-medium text-gray-900"
        >
          Descrie cât mai detaliat problema întâmpinată:
        </label>
        <textarea
          id="bugText"
          name="bugText"
          rows={4}
          maxLength={2000}
          minLength={20}
          className="block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 resize-none"
          placeholder="Scrie aici..."
          required
        ></textarea>
        <button
          type="submit"
          className="bg-blue-700 w-full hover:bg-blue-800 text-white text-base font-bold p-2 rounded transition-colors duration-300 whitespace-nowrap uppercase mt-8"
        >
          Trimite
        </button>
      </form>
    </div>
  );
}
