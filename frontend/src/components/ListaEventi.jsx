import styles from "../styles/ListaEventi.module.css";

export default function ListaEventi({ dati }) {
  if (!dati || dati.length === 0) {
    return <p>Dati non disponibili</p>;
  }
  return (
    <>
      {dati && (
        <div className={styles.container}>
          <h3>Dati Elaborati</h3>

          <ul className={styles.lista}>
            {dati.map((dato, index) => (
              <li key={index} className={styles.card}>
                <div className={styles.header}>
                  <div className={styles.campo}>
                    <p className={styles.label}>DOY</p>
                    <p>{dato.doy}</p>
                  </div>
                </div>

                <p className={styles.label}>EVENTI</p>

                {dato.events && dato.events.length > 0 ? (
                  <div className={styles.lista}>
                    {dato.events.map((evento, index) => (
                      <div key={index} className={styles.evento}>
                        <div className={styles.campo}>
                          <p className={styles.label}>Index</p>
                          <p>{evento.index}</p>
                        </div>

                        <div className={styles.campo}>
                          <p className={styles.label}>X</p>
                          <p>: {evento.X}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <p className={styles.nessunEvento}>
                    Nessun evento registrato
                  </p>
                )}
              </li>
            ))}
          </ul>
        </div>
      )}
    </>
  );
}
