"use client";
import styles from "../page.module.css";
import { SetStateAction, useState } from "react";
import axios from "axios";

type FileMetadata = {
  name: string;
  path: string;
  size: number;
  last_modified: string;
  creation_time: string;
  type: string;
  preview: string;
};

export default function Home() {
  const [fileName, setFileName] = useState("");
  const [buttonClicked, setButtonClicked] = useState(false);
  const [directoryPath, setDirectoryPath] = useState("");

  const handleInputChange = (e: { target: { value: SetStateAction<string> } }) => {
    setFileName(e.target.value);
  };

    const handleSearchClick = async () => {
    if (fileName) {
        try {
        const response = await axios.get("http://localhost:8000/api/search/", {
            params: { query: fileName },
        });
        console.log("Results:", response.data.results);
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
        <h1>Use multiple workers and a master</h1>
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

      </main>
    </div>
  );
}
function setResults(arg0: never[]) {
    throw new Error("Function not implemented.");
}

