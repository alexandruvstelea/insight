import { NavigationBar } from "@/components/navigationBar/page";

interface SearchParams {
  facultyName?: string;
}

interface PanelProps {
  searchParams: SearchParams;
}

export default function Panel({ searchParams }: PanelProps) {
  const facultyName = searchParams.facultyName || "";
  return (
    <>
      <NavigationBar />
    </>
  );
}
