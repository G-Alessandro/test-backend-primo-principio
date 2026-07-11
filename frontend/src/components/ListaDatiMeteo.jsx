import styles from "../styles/ListaDatiMeteo.module.css";

export default function Lista({ dati }) {
  if (!dati || dati.length === 0) {
    return <p>Dati non disponibili</p>;
  }
  return (
    <>
      {dati && (
        <div className={styles.container}>
          <h3>Dati Meteo</h3>
          <ul className={styles.lista}>
            {dati.map((dato, index) => (
              <li key={index} className={styles.card}>
                <div className={styles.riga}>
                  <div className={styles.campo}>
                    <p className={styles.label}>DOY</p>
                    <p>{dato.doy}</p>
                  </div>

                  <div className={styles.campo}>
                    <p className={styles.label}>Data</p>
                    <p>{dato.date}</p>
                  </div>
                </div>

                <div className={styles.riga}>
                  <div className={styles.campo}>
                    <p className={styles.label}>Temperatura</p>
                    <p>{dato.temperature} °C</p>
                  </div>

                  <div className={styles.campo}>
                    <p className={styles.label}>Umidità</p>
                    <p>{dato.humidity} %</p>
                  </div>
                </div>

                <div className={styles.riga}>
                  <div className={styles.campo}>
                    <p className={styles.label}>Bagnatura</p>
                    <p>
                      Foglia mediamente
                      {dato.bagnatura > 0 ? " asciutta" : " bagnata"}
                    </p>
                  </div>

                  <div className={styles.campo}>
                    <p className={styles.label}>Pioggia</p>
                    <p>{dato.rain} mm</p>
                  </div>
                </div>
              </li>
            ))}
          </ul>
        </div>
      )}
    </>
  );
}
