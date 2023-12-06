import Link from "next/link";


export default function Subject({ subject }) {
  return (
    <li>
      <Link href={`/professors/infoCourse?subjectId=${subject.id}`}>
        <button className='button-courses' role='button'>
          {subject.abbreviation}
        </button>
      </Link>
    </li>
  )
}
