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
            Oferi feedback <br /> simplu și rapid
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
              Un proiect creat cu scopul de a facilita comunicarea dintre
              studenți și profesori, pentru a oferi un feedback constructiv
              asupra cursurilor lor.
            </h2>
          </div>
          <div className={styles.item}>
            <h1>De ce?</h1>
            <h2>
              Suntem de părere că metodele actuale de colectare a feedback-ului
              din cadrul universității nu sunt destul de eficiente și nu
              avantajează studenții.
            </h2>
          </div>
          <div className={styles.item}>
            <h1>Cum facem asta?</h1>
            <h2>
              Prin această platformă, studenții își pot exprima liber opiniile
              și sugestiile lor cu privire la cursuri, fără repercusiuni, datele
              fiind 100% anonime.
            </h2>
          </div>
        </div>
      </div>
      <div className={styles.howZone}>
        <h1>Cum oferi feedback?</h1>
        <div className={styles.howZoneList}>
          <div className={styles.howZoneCard}>
            <h1>1</h1>
            <h2>
              Participi la cursuri într-o sală în care există o tabletă inSight
              activă
            </h2>
          </div>
          <div className={styles.howZoneCard}>
            <h1>2</h1>
            <h2>
              La sfârșitul cursului, scanezi codul QR de pe tableta inSight
            </h2>
          </div>
          <div className={styles.howZoneCard}>
            <h1>3</h1>
            <h2>
              Acorzi calificative cursului și transmiți un mesaj profesorului cu
              părerea ta
            </h2>
          </div>
          <div className={styles.howZoneCard}>
            <h1>4</h1>
            <h2>
              Vizualizezi rezultatele pe site-ul nostru și te bucuri de cursuri
              îmbunătățite
            </h2>
          </div>
        </div>
      </div>
      <div className={styles.facultiesZone} id="facultiesZone">
        <h1>FACULTĂȚI</h1>
        <h2 className={styles.universityName}>UnitBV</h2>
        <div className={styles.facultiesList}>
          {faculties.map((faculty: any) => (
            <FacultySelector
              key={faculty.id}
              facultyID={faculty.id}
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
