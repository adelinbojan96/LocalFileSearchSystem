import Image from "next/image";
import styles from "./page.module.css";

export default function Home() {
  return (
    <div className={styles.page}>
      <main className={styles.main}>
        <h1>Search a file locally</h1>
        
        <input
          type="text"
          placeholder="Enter file name"
          className={styles.searchBar}
        />
        
        <button className={styles.searchButton}>Search</button>
      </main>
    </div>
  );
}
