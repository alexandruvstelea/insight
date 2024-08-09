import styles from "./page.module.css";
import Image from "next/image";
import FacultySelector from "@/components/facultySelector/page";
import { Footer } from "@/components/footer/page";

export default function Home() {
  return (
    <>
      <div className={styles.landingZone}>
        <h1>
          FEEDBACK
          <br />
          UNITBV
        </h1>
        <h2>P&#259;rerea ta conteaz&#259;</h2>
        <Image
          src="/svg/thumbs-up-solid.svg"
          height={128}
          width={128}
          alt="Thumbs up image"
          className={styles.thumbsUp}
        />
      </div>
      <div className={styles.facultiesZone}>
        <h1>EXPLOREAZĂ</h1>
        <div className={styles.facultiesList}>
          <FacultySelector facultyName="IESC" svgPath="/svg/iesc.svg" />
          <FacultySelector
            facultyName="MATE-INFO"
            svgPath="/svg/mate-info.svg"
          />
        </div>
        <div></div>
      </div>

      <div className={styles.aboutZone}>
        <div className={styles.aboutZoneItem}>
          <h2>Ce?</h2>
          <p>
            Feedback UnitBV este un proiect care a luat naștere din dorința
            noastră de a îmbunătăți procesul de predare în cadrul facultății.
            <br /> Scopul nostru este să facilităm comunicarea dintre studenți
            și profesori, pentru a oferi un feedback constructiv asupra
            cursurilor.
          </p>
        </div>
        <div className={styles.aboutZoneItem}>
          <h2>De ce?</h2>
          <p>
            Suntem de părere că metodele actuale de colectare si procesare a
            feedback-ului din facultate sunt ineficiente și nu reflectă mereu
            nevoile reale ale studenților.
          </p>
        </div>
        <div className={styles.aboutZoneItem}>
          <h2>Cum?</h2>
          <p>
            Prin această platformă, studenții își pot exprima liber opiniile și
            sugestiile lor cu privire la cursuri, fără teama de repercusiuni.
            Profesorii au acces la acest feedback într-un format structurat și
            ușor de vizualizat, ceea ce le permite să înțeleagă mai bine nevoile
            și așteptările studenților.
          </p>
        </div>
      </div>
      <div className={styles.howZone}>
        <h2>Cum ofer feedback?</h2>
        <ol>
          <li>Participă la un curs</li>
          <li>Scanează codul QR</li>
          <li>Spune-ne părerea ta</li>
          <li>Vizualizează în aplicație</li>
        </ol>
      </div>
      <Footer />
    </>
  );
}
