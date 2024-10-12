"use server";
import Link from "next/link";

export default async function NavigationBar() {
  return (
    <div className="text-center w-full h-fit bg-gradient text-white">
      <Link
        href={{
          pathname: "/",
        }}
        className="text-white no-underline"
      >
        <h1 className="flex justify-center items-center text-[2.5rem] m-0 flex-col font-bold">
          inSight
        </h1>
      </Link>
    </div>
  );
}
