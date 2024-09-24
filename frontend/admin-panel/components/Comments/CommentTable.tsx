import React, { FC, useState, useEffect } from "react";
import { Comment } from "@/utils/types";
import DeleteSVG from "@/public/svgs/DeleteSVG";
import { CommentTableProps } from "@/utils/interfaces";
import HeaderSection from "../HeaderSection";

const CommentTable: FC<CommentTableProps> = ({
  comments = [],
  fetchComments,
}) => {
  const [isDeleting, setIsDeleting] = useState(false);

  const handleDelete = async (id: number) => {
    if (confirm("Sigur doriți să ștergeți acest comentariu?")) {
      setIsDeleting(true);
      try {
        const response = await fetch(`${process.env.API_URL}/comments/${id}`, {
          method: "DELETE",
          headers: {
            "Content-Type": "application/json",
          },
        });
        if (!response.ok) {
          throw new Error("A apărut o eroare la ștergerea comentariului");
        }
        fetchComments();
      } catch (error) {
        alert("A apărut o eroare la ștergerea comentariului");
      } finally {
        setIsDeleting(false);
      }
    }
  };

  const [commentData, setCommentData] = useState<Comment[]>([]);

  useEffect(() => {
    const fetchRelatedData = async () => {
      if (!Array.isArray(comments) || comments.length === 0) {
        setCommentData([]);
        return;
      }

      const updatedComments = await Promise.all(
        comments.map(async (comment) => {
          try {
            const roomResponse = await fetch(
              `${process.env.API_URL}/rooms/${comment.room_id}`
            );
            const room = await roomResponse.json();

            const programmeResponse = await fetch(
              `${process.env.API_URL}/programmes/${comment.programme_id}`
            );
            const programme = await programmeResponse.json();

            const subjectResponse = await fetch(
              `${process.env.API_URL}/subjects/${comment.subject_id}`
            );
            const subject = await subjectResponse.json();

            const professorResponse = await fetch(
              `${process.env.API_URL}/professors/${comment.professor_id}`
            );
            const professor = await professorResponse.json();

            const facultyResponse = await fetch(
              `${process.env.API_URL}/faculties/${comment.faculty_id}`
            );
            const faculty = await facultyResponse.json();

            return {
              ...comment,
              roomName: room.name,
              programmeName: programme.name,
              subjectName: subject.name,
              professorName: `${professor.last_name} ${professor.first_name}`,
              facultyName: faculty.abbreviation,
            };
          } catch (error) {
            console.error("Error fetching related data:", error);
            return comment;
          }
        })
      );
      setCommentData(updatedComments);
    };

    fetchRelatedData();
  }, [comments]);
  return (
    <div className=" p-4 flex flex-col items-center justify-center glass-background ">
      <HeaderSection
        title="COMENTARII"
        count={comments?.length || 0}
        buttons={[]}
      />
      <table className="w-full text-base text-left text-gray-400">
        <thead className="text-lg  uppercase  bg-gray-700 text-gray-400">
          <tr>
            <th scope="col" className="px-6 py-3">
              Acțiuni
            </th>
            <th scope="col" className="px-6 py-3">
              Text
            </th>
            <th scope="col" className="px-6 py-3">
              Ora
            </th>
            <th scope="col" className="px-6 py-3">
              Sală
            </th>
            <th scope="col" className="px-6 py-3">
              Specializare
            </th>
            <th scope="col" className="px-6 py-3">
              Materie
            </th>
            <th scope="col" className="px-6 py-3">
              Profesor
            </th>
            <th scope="col" className="px-6 py-3">
              Facultate
            </th>
          </tr>
        </thead>
        <tbody>
          {Array.isArray(comments) ? (
            commentData.map((comment) => (
              <tr
                key={comment.id}
                className="border-b bg-gray-800 border-gray-700"
              >
                <td scope="row" className="w-[100px] px-6 py-4 ">
                  <button
                    onClick={() => handleDelete(comment.id)}
                    disabled={isDeleting}
                  >
                    <DeleteSVG />
                  </button>
                </td>
                <td scope="row" className="px-6 py-4 font-medium   text-white">
                  {comment.text}
                </td>
                <td scope="row" className="px-6 py-4 font-medium   text-white">
                  {new Date(comment.timestamp).toLocaleString()}
                </td>
                <td scope="row" className="px-6 py-4 font-medium   text-white">
                  {comment.roomName}
                </td>
                <td scope="row" className="px-6 py-4 font-medium   text-white">
                  {comment.programmeName}
                </td>
                <td scope="row" className="px-6 py-4 font-medium   text-white">
                  {comment.subjectName}
                </td>
                <td scope="row" className="px-6 py-4 font-medium   text-white">
                  {comment.professorName}
                </td>
                <td scope="row" className="px-6 py-4 font-medium   text-white">
                  {comment.facultyName}
                </td>
              </tr>
            ))
          ) : (
            <tr>
              <td
                colSpan={8}
                className="p-6 text-2xl text-center text-gray-500"
              >
                Nu există comentarii
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
};

export default CommentTable;
