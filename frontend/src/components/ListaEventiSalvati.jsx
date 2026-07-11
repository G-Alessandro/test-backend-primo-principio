import styles from "../styles/ListaEventiSalvati.module.css";

export default function Tabella({ dati }) {
  if (!dati || dati.length === 0) {
    return <p>Dati non disponibili</p>;
  }
  return (
    <div className={styles.container}>
      <h3>Eventi salvati</h3>

      <ul className={styles.lista}>
        {dati.flatMap((dato) =>
          dato.events.map((evento) => (
            <li key={`${dato.doy}-${evento.index}`} className={styles.card}>
              <div className={styles.campo}>
                <p className={styles.label}>DOY</p>
                <p>{dato.doy}</p>
              </div>

              <div className={styles.campo}>
                <p className={styles.label}>Index</p>
                <p>{evento.index}</p>
              </div>

              <div className={styles.campo}>
                <p className={styles.label}>Valore X</p>
                <p>{evento.X}</p>
              </div>
            </li>
          )),
        )}
      </ul>
    </div>
  );
}
