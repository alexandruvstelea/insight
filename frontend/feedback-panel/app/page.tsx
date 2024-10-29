import styles from "./page.module.css";
import Image from "next/image";
import { InfoBox } from "@/components/infoBox/page";
import { TutorialBox } from "@/components/tutorialBox/page";
import { ScrollButton } from "@/components/scrollButton/page";

export default async function Home() {
  return (
    <>
      <div className={styles.landing}>
        <div className={styles.landingTextContainer}>
          <h1 className={styles.landingTitle}>inSight</h1>
          <div className={styles.landingText}>
            <h2>
              Progresul începe cu feedback-ul
              <br />
              pe care nu vrei să îl auzi
            </h2>
            <h3>
              Ajută-ne să le oferim profesorilor acel feedback valoros care
              poate aduce schimbări reale în modul în care sunt predate
              cursurile tale.
            </h3>
          </div>
          <ScrollButton text="Explorează" scrollId="faculties" />
        </div>
        <div className={styles.landingImageContainer}>
          {/* <Image
            width={80}
            height={80}
            src={"/svg/feedback.svg"}
            alt="Landing Page Image"
            className={styles.landingImage}
          /> */}
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
            imagePath="/svg/social-network.svg"
            reversable={false}
          />
          <InfoBox
            title="De ce există inSight?"
            content="Suntem de părere că metodele actuale de colectare a feedback-ului
              din cadrul universității nu sunt destul de eficiente."
            imagePath="/svg/analytics.svg"
            reversable={true}
          />
          <InfoBox
            title="Cum facem asta?"
            content="Prin această platformă, studenții își pot exprima liber opiniile
              și sugestiile lor cu privire la cursuri, fără teama de 
              repercusiuni, datele fiind 100% anonime."
            imagePath="svg/anonymous.svg"
            reversable={false}
          />
        </div>
      </div>
      <div className={styles.tutorial}>
        <h1>Cum votez?</h1>
        <div className={styles.tutorialBoxes}>
          <TutorialBox
            step="1"
            content="Participi la cursuri într-o sală în care este prezent un poster dedicat platoformei inSight. Îl vei recunoaște când îl vei vedea."
          />
          <TutorialBox
            step="2"
            content="La finalul cursului, scanezi codul QR afișat și oferi feedback. Dacă dorești, poți trimite și un mesaj profesorului pentru a-l ajuta să îmbunătățească cursul."
          />
          <TutorialBox
            step="3"
            content="Urmărești rezultatele pe site-ul nostru și te bucuri de cursuri mai bine organizate."
          />
        </div>
      </div>
      <div className={styles.faculties} id="faculties">
        <h1>Facultăți</h1>
        <div className={styles.facultiesList}>
          <h1>
            Universitatea <br />
            Transilvania
          </h1>
          <h1>În curând</h1>
        </div>
      </div>
    </>
  );
}
