'use client'
import Image from 'next/image'
import React, { useEffect, useState } from 'react';
import Subject from './Subject';

export default function Card({ professor }) {

  const [isFlipped, setIsFlipped] = useState(false);
  const [subjects, setSubjects] = useState([]);
  const [isLoaded, setIsLoaded] = useState(false);


  async function fetchSubject(professor_id) {
    if (!isLoaded) {
      const url = `${process.env.REACT_APP_API_URL}/subjects/professor/${professor_id}`;
      try {
        const response = await fetch(url);
        const complete_response = await response.json();
        setSubjects(complete_response);
        setIsLoaded(true);
      } catch (err) {
        console.log(err);
      }
    }
  }

  const flipCard = () => {
    setIsFlipped(!isFlipped);
    if (!isFlipped) {
      fetchSubject(professor.id);
    }
  };


  return (
    <>
      <div className={`card ${isFlipped ? 'flipped' : ''}`}>
        <div className="content">
          <div className="front">
            <div className="image-content">
              <span className="overlay"></span>
              <div className="card-image">
                <Image
                  width={158}
                  height={158}
                  src={professor.gender === 'male' ? "/images/maleAvatar.jpg" : "/images/femaleAvatar.jpg"}
                  alt="Avatar"
                  className="card-img" />
              </div>
            </div>
            <div className="card-content">
              <h2 className="name">{professor.first_name} {professor.last_name}</h2>
              <button className="button-card" onClick={flipCard}>Vezi Cursuri</button>
            </div>
          </div>
          <div className="back">

            <h1 className="title-curs">Cursuri:</h1>
            <ul className="courses-list" >
              {isLoaded && subjects.map(subject => (
                <Subject key={subject.id} subject={subject} />
              ))}
            </ul>
            <button className="button-card back-button" onClick={flipCard}>Înapoi</button>
          </div>
        </div>
      </div>
    </>
  )
}