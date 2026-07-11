import styles from "../styles/Pulsante.module.css";

export default function Pulsante({ setRieseguiFetch, elaborazione }) {
  return (
    <div className={styles.container}>
      <button
        className={styles.button}
        disabled={elaborazione}
        onClick={() =>
          setRieseguiFetch((valorePrecedente) => !valorePrecedente)
        }
      >
        {elaborazione ? "Elaborazione..." : "Rielabora Dati"}
      </button>
    </div>
  );
}
