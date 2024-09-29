import Link from "next/link";

export default function InfoTab() {
  return (
    <>
      <div className="p-10 flex flex-col gap-10">
        <section>
          <h2 className="mb-2 text-xl font-semibold text-white">
            Reguli pentru toate tabelele
          </h2>
          <ul className=" text-lg space-y-1  list-disc list-inside text-gray-400">
            <li>Doar câmpurile cu simbolul * sunt obligatorii</li>
          </ul>
        </section>
        <section>
          <h2 className="mb-2 text-xl font-semibold text-white">
            Tabel săptămâni
          </h2>
          <ul className=" text-lg space-y-1 list-disc list-inside text-gray-400">
            <li>Intervalul se referă la perioada de scoala/vacanta/sesiune</li>
            <li>
              Un interval se calculeaza in functie de numărul de săptămâni
            </li>
            <li>
              Structura anului universitar poate fi gasită aici:{" "}
              <a
                href="https://www.unitbv.ro/despre-unitbv/informatii-de-interes-public/structura-anului-universitar.html"
                target="_blank"
                rel="noopener noreferrer"
                className="underline text-blue-600"
              >
                LINK
              </a>
            </li>
          </ul>
        </section>
      </div>
    </>
  );
}
