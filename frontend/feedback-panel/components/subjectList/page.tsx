import SubjectDropdown from "../subjectDropdown/page";
import styles from "./page.module.css";
import { SubjectWithAssociation } from "@/utils/fetchers/subjects";

interface SubjectList {
  subjectsList: SubjectWithAssociation[] | false;
  facultyAbbreviation: string;
  transformedProfessorName: string;
}

export default function SubjectList({
  subjectsList,
  facultyAbbreviation,
  transformedProfessorName,
}: SubjectList) {
  return (
    <>
      <div className={styles.professorClasses}>
        <h1>Materii</h1>
        <div className={styles.classesList}>
          {subjectsList &&
            subjectsList.map((subject: any) => (
              <div key={subject.id}>
                <SubjectDropdown
                  subject={subject}
                  facultyAbbreviation={facultyAbbreviation}
                  transformedProfessorName={transformedProfessorName}
                />
              </div>
            ))}
          {subjectsList &&
            subjectsList.map((subject: any) => (
              <div key={subject.id}>
                <SubjectDropdown
                  subject={subject}
                  facultyAbbreviation={facultyAbbreviation}
                  transformedProfessorName={transformedProfessorName}
                />
              </div>
            ))}
          {subjectsList &&
            subjectsList.map((subject: any) => (
              <div key={subject.id}>
                <SubjectDropdown
                  subject={subject}
                  facultyAbbreviation={facultyAbbreviation}
                  transformedProfessorName={transformedProfessorName}
                />
              </div>
            ))}
          {subjectsList &&
            subjectsList.map((subject: any) => (
              <div key={subject.id}>
                <SubjectDropdown
                  subject={subject}
                  facultyAbbreviation={facultyAbbreviation}
                  transformedProfessorName={transformedProfessorName}
                />
              </div>
            ))}
          {subjectsList &&
            subjectsList.map((subject: any) => (
              <div key={subject.id}>
                <SubjectDropdown
                  subject={subject}
                  facultyAbbreviation={facultyAbbreviation}
                  transformedProfessorName={transformedProfessorName}
                />
              </div>
            ))}
        </div>
      </div>
    </>
  );
}
