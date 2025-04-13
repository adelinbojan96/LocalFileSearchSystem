"use client";
import styles from "./page.module.css";
import { SetStateAction, useState } from "react";
import axios from "axios";


export default function Home() {
  const [fileName, setFileName] = useState("");
    const [results, setResults] = useState<any[]>([]);

  const handleInputChange = (e: { target: { value: SetStateAction<string> } }) => {
    setFileName(e.target.value);
  };

    const handleSearchClick = async () => {
        if (fileName) {
            try {
            const response = await axios.get("http://localhost:8000/api/search/", {
                params: { query: encodeURIComponent(fileName) },
            });
            //display on the console
            console.log("Results:", response.data.results);
            //results for frontend
            setResults(response.data.results);
            } catch (error) {
            console.error("Error from master:", error);
            }
        } else {
            alert("Please enter a file name");
        }
    };

  return (
    <div className={styles.page}>
      <main className={styles.main}>
        <h1>Use multiple workers for search</h1>
        <input
          type="text"
          placeholder="Enter file name"
          className={styles.searchBar}
          value={fileName}
          onChange={handleInputChange}
        />
        <button className={styles.searchButton} onClick={handleSearchClick}>
          Search
        </button>
          {results.length > 0 && (
              <div>
                  <h2 style={{ color: "green" }}>
                      Found {results.length === 1 ? "one matching file" : `${results.length} matching files`}
                  </h2>
                  <h2>Search Results:</h2>
                  <ul>
                      {results.map((file, index) => (
                          <li key={index}>
                              <div className={styles.fileItem}>
                                  <strong>{file.name}</strong>
                                  <div>Server: {file.server}</div>
                              </div>
                          </li>
                      ))}
                  </ul>
              </div>
          )}
      </main>
    </div>
  );
}

