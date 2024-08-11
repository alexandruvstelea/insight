import styles from "./page.module.css";
import Image from "next/image";
import FacultySelector from "@/components/facultySelector/page";
import { fetchFaculties } from "@/utils/fetchers/faculties";

export default async function Home() {
  const faculties = await fetchFaculties();
  return (
    <>
      <div className={styles.landingZone}>
        <h1>inSight</h1>
        <Image
          src={"/svg/hurricane-solid.svg"}
          width={100}
          height={100}
          alt="Faculty logo"
          className={styles.landingImage}
          quality={100}
        />
        <h2>
          Îți place? Spune-ne!
          <br /> Nu-ți place? Schimbăm!
        </h2>
        <a className={styles.facultiesButton} href="#facultiesZone">
          Explorează
        </a>
      </div>
      <div className={styles.mockup}>
        <div className={styles.mockupItem}>
          <div className={styles.backsplash}></div>
          <Image
            src={"/png/feedback-ss-portrait.png"}
            width={100}
            height={100}
            alt="Faculty logo"
            className={styles.screenshot}
          />
          <h1>
            Oferi feedback <br /> rapid și simplu
          </h1>
        </div>
        <div className={styles.mockupItem}>
          <div className={styles.backsplash}></div>
          <Image
            src={"/png/feedback-ss-portrait.png"}
            width={100}
            height={100}
            alt="Faculty logo"
            className={styles.screenshot}
          />
          <h1>
            Vezi ce cred și
            <br /> alți studenți
          </h1>
        </div>
      </div>
      <div className={styles.aboutZone}>
        <h1>Despre noi</h1>
        <div className={styles.aboutZoneItems}>
          <div className={styles.item}>
            <h1>Ce este inSight?</h1>
            <h2>
              InSight este un proiect creat cu scopul de a facilita comunicarea
              dintre studenți și profesori, pentru a oferi un feedback
              constructiv asupra cursurilor lor.
            </h2>
          </div>
          <div className={styles.item}>
            <h1>De ce?</h1>
            <h2>
              Suntem de părere că metodele actuale de colectare a feedback-ului
              din cadrul universității nu sunt destul de eficiente.
            </h2>
          </div>
          <div className={styles.item}>
            <h1>Cum facem asta?</h1>
            <h2>
              Prin această platformă, studenții își pot exprima liber opiniile
              și sugestiile lor cu privire la cursuri, fără teama de a suferi
              repercusiuni, datele fiind 100% anonime.
            </h2>
          </div>
        </div>
      </div>
      <div className={styles.howZone}>
        <h1>Cum oferi feedback?</h1>
        <div className={styles.howZoneList}>
          <h1>1&#x21b4;</h1>
          <h2>
            Participi la cursuri într-o sală în care este prezentă o tabletă
            inSight activă (vezi&nbsp;
            <a href="#" className={styles.roomsList}>
              lista săli
            </a>
            )
          </h2>
          <h1>2&#x21b4;</h1>
          <h2>La sfârșitul cursului, scanezi codul QR de pe tabletă</h2>
          <h1>3&#x21b4;</h1>
          <h2>
            Acorzi calificative cursului și, dacă vrei, transmiți un mesaj
            profesorului
          </h2>
          <h1>4&#x21b4;</h1>
          <h2>Vizualizezi rezultatele pe site-ul nostru</h2>
        </div>
      </div>
      <div className={styles.facultiesZone} id="facultiesZone">
        <h1>FACULTĂȚI</h1>
        <h2 className={styles.universityName}>UnitBV</h2>
        <div className={styles.facultiesList}>
          {faculties.map((faculty: any) => (
            <FacultySelector
              key={faculty.id}
              facultyName={faculty.abbreviation}
              svgPath={`/svg/${faculty.abbreviation.toLowerCase()}.svg`}
            />
          ))}
        </div>

        <div></div>
      </div>
    </>
  );
}
