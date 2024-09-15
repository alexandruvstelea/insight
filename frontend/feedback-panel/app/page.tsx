import styles from "./page.module.css";
import Image from "next/image";
import { InfoBox } from "@/components/infoBox/page";
import { TutorialBox } from "@/components/tutorialBox/page";
import FacultySelector from "@/components/facultySelector/page";
import { fetchFaculties } from "@/utils/fetchers/faculties";

export default async function Home() {
  const faculties = await fetchFaculties();
  return (
    <>
      <div className={styles.landing}>
        <h1 className={styles.landingTitle}>inSight</h1>
        <div className={styles.landingText}>
          <h2>
            Progresul incepe cu feedback-ul
            <br />
            pe care nu vrei să-l auzi
          </h2>
          <h3>
            Ajută-ne să le oferim profesorilor acel feedback valoros care poate
            aduce schimbări reale în modul în care sunt predate cursurile tale.
          </h3>
        </div>
        <a className={styles.facultiesButton} href="#faculties">
          Explorează
        </a>
        <div className={styles.landingImageContainer}>
          <Image
            width={80}
            height={80}
            src={"/svg/analytics.svg"}
            alt="Landing Page Image"
            className={styles.landingImage}
          />
        </div>
      </div>
      <div className={styles.about}>
        <h1>Despre noi</h1>
        <div className={styles.infoBoxes}>
          <InfoBox
            title="Ce este inSight?"
            content="InSight este un proiect creat cu scopul de a facilita comunicarea
              dintre studenți și profesori, pentru a oferi un feedback
              constructiv asupra cursurilor lor."
          />
          <Image
            width={80}
            height={80}
            src={"/svg/social-network.svg"}
            alt="Landing Page Image"
            className={styles.decorativeImage}
          />
          <InfoBox
            title="De ce există inSight?"
            content="Suntem de părere că metodele actuale de colectare a feedback-ului
              din cadrul universității nu sunt destul de eficiente."
          />
          <Image
            width={80}
            height={80}
            src={"/svg/anonymous.svg"}
            alt="Landing Page Image"
            className={styles.decorativeImage}
          />
          <InfoBox
            title="Cum facem asta?"
            content="Prin această platformă, studenții își pot exprima liber opiniile
              și sugestiile lor cu privire la cursuri, fără teama de 
              repercusiuni, datele fiind 100% anonime."
          />
        </div>
      </div>
      <div className={styles.tutorial}>
        <h1>Cum votez?</h1>
        <div className={styles.infoBoxes}>
          <TutorialBox
            step="1"
            content="Participi la cursuri într-o sală în care este prezentă o tabletă
            inSight activă."
          />
          <TutorialBox
            step="2"
            content="La sfârșitul cursului, scanezi codul QR de pe tabletă și acorzi calificative cursului. Dacă vrei, transmiți și un mesaj către
            profesor pentru a-l ajuta."
          />
          <TutorialBox
            step="3"
            content="Vizualizezi rezultatele pe site-ul noastru și te bucuri de cursuri mai bune."
          />
        </div>
      </div>
    </>
  );
}
