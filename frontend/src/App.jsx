import { useEffect, useState } from "react";
import ListaDatiMeteo from "./components/ListaDatiMeteo";
import ListaEventi from "./components/ListaEventi";
import ListaEventiSalvati from "./components/ListaEventiSalvati";
import Pulsante from "./components/Pulsante";
import styles from "./styles/App.module.css";

export default function App() {
  const [datiMeteo, setDatiMeteo] = useState([]);
  const [eventiOidio, setEventiOidio] = useState([]);
  const [messaggio, setMessaggio] = useState(null);
  const [rieseguiFetch, setRieseguiFetch] = useState(false);
  const [elaborazione, setElaborazione] = useState(false);

  useEffect(() => {
    const fetchDatiMeteo = async () => {
      try {
        setElaborazione(true);
        const response = await fetch(
          `${import.meta.env.VITE_BACKEND_BASE_URL}/registra-eventi/`,
          {
            method: "POST",
            credentials: "include",
            mode: "cors",
          },
        );

        const data = await response.json();

        if (!data) {
          setMessaggio("Nessun dato trovato");
          setTimeout(() => setMessaggio(null), 2000);
        } else {
          setMessaggio(data.messaggio);
          setDatiMeteo(data.dati_meteo);
          setEventiOidio(data.eventi_oidio);
          setTimeout(() => setMessaggio(null), 2000);
        }
      } catch (error) {
        setMessaggio(
          error instanceof Error
            ? error.message
            : "Errore durante la richiesta",
        );
      } finally {
        setElaborazione(false);
      }
    };

    fetchDatiMeteo();
  }, [rieseguiFetch]);

  return (
    <div className={styles.container}>
      {messaggio && <p className={styles.messaggio}>{messaggio}</p>}
      <Pulsante
        setRieseguiFetch={setRieseguiFetch}
        elaborazione={elaborazione}
      />
      <div className={styles.containerListe}>
        <ListaDatiMeteo dati={datiMeteo} />
        <ListaEventi dati={eventiOidio} />
        <ListaEventiSalvati dati={eventiOidio} />
      </div>
    </div>
  );
}
