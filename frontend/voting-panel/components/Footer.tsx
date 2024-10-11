"use server";

export default async function Footer() {
  return (
    <>
      <div className="flex items-center justify-center bg-black w-full h-fit text-white text-[0.9rem] font-bold mt-auto py-2">
        ©&nbsp;
        <a
          href="https://alexandrustelea.com"
          target="_blank"
          rel="noopener noreferrer"
          className="text-white no-underline transition-colors duration-150 ease-in-out hover:text-blue-dark "
        >
          Alexandru Stelea
        </a>
        &nbsp;&&nbsp;
        <a
          href="https://www.linkedin.com/in/cristianandreisava"
          target="_blank"
          rel="noopener noreferrer"
          className="text-white no-underline transition-colors duration-150 ease-in-out hover:text-blue-dark"
        >
          Andrei Sava
        </a>
      </div>
    </>
  );
}
