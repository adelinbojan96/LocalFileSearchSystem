"use client";
import styles from "./page.module.css";
import { SetStateAction, useState } from "react";
import axios from "axios";

//types for the metadata
type FileMetadata = {
  filename: string;
  path: string;
  size: number;
  last_modified: string;
  creation_time: string;
  file_type: string;
  preview: string;
};

export default function Home() {
  const [fileName, setFileName] = useState("");
  const [results, setResults] = useState<FileMetadata[]>([]);
  const [buttonClicked, setButtonClicked] = useState(false); 

  const handleInputChange = (e: { target: { value: SetStateAction<string> } }) => {
    setFileName(e.target.value);
  };

  const handleSearchClick = async () => {
    if (fileName) {
      try {
        const response = await axios.post("http://localhost:8000/api/search/", {
          file_name: fileName,
        });

        setResults(response.data.results || []);
        setButtonClicked(true);
      } catch (error) {
        console.error("Search error:", error);
        setResults([]);
        setButtonClicked(true);
      }
    } else {
      alert("Please enter a file name");
    }
  };

  return (
    <div className={styles.page}>
      <main className={styles.main}>
        <h1>Search a file locally</h1>

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

        {/* Not found */}
        {results.length === 0 && buttonClicked && (
          <div>
            <h2 style={{ color: "red" }}>Not found</h2>
          </div>
        )}

        {/* Show results if any */}
        {results.length > 0 && (
          <div>
            <h2 style={{ color: "green" }}>Found: {results.length} matching files</h2>
            <h2>Search Results:</h2>
            <ul>
              {results.map((file, index) => (
                <li key={index}>
                  <div className={styles.fileItem}>
                    <strong>{file.filename}</strong>
                    <div>Path: {file.path}</div>
                    <div>Size: {Math.round(file.size / 1024)} KB</div>
                    <div>Type: {file.file_type}</div>
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