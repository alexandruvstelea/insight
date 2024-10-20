"use server";

import Footer from "@/components/Footer";
import NavigationBar from "@/components/NavigationBar";

const messages: Record<string, string> = {
  sessionExpired: "Sesiunea a expirat. Vă rugăm să începeți din nou.",
  incorrectURL:
    "Link-ul nu este corect, scanează codul QR pentru a accesa pagina.",
  wrongDevice: "Dispozitivul dvs. nu este compatibil cu această aplicație.",
  timestampOrRoomCodeInvalid:
    "Codul camerei sau ora la care votezi sunt invalide.",
  error500: "A apărut o eroare. Vă rugăm să încercați mai târziu.",
  generalError: "A apărut o eroare. Vă rugăm să încercați din nou.",
  tooManyRequests: "Prea multe cereri. Vă rugăm să încercați mai târziu.",
  default: "Welcome to the dynamic page!",
};

async function getMessage(slug: string): Promise<string> {
  return messages[slug] || messages.default;
}

export default async function DynamicPage({
  params,
}: {
  params: { slug: string };
}) {
  const message = await getMessage(params.slug);

  return (
    <div className="flex items-center justify-center mx-2">
      <div className="bg-gray-200 p-4 rounded shadow-xl text-center">
        <img
          src="/svgs/denny.svg"
          className="mx-auto mb-4 w-12 h-auto"
          alt="Error"
        />
        <p>{message}</p>
      </div>
    </div>
  );
}
