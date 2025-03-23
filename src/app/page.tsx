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
  const [exact_match, setExact_match] = useState(false);
  const [selectedFile, setSelectedFile] = useState<FileMetadata | null>(null);

  const handleInputChange = (e: { target: { value: SetStateAction<string> } }) => {
    setFileName(e.target.value);
  };

  const handleSearchClick = async () => {
    if (fileName) {
      try {
        setSelectedFile(null);

        const response = await axios.post("http://localhost:8000/api/search/", {
          file_name: fileName,
          exact_match: exact_match,
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

  const handleFilenameClick = async (file: FileMetadata) => {
    try {
      const response = await axios.get(`http://localhost:8000/api/files/${file.filename}/`);
      setSelectedFile(response.data);
    } catch (error) {
      console.error("Error fetching metadata:", error);
      setSelectedFile(null);
    }
  };

  const handleDownload = () => {
    if (!selectedFile) return;

    const blob = new Blob([JSON.stringify(selectedFile, null, 2)], {
      type: "application/json",
    });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${selectedFile.filename}_metadata.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
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

        <div className="form-row" style={{ textAlign: "left" }}>
          <label htmlFor="exact_match"> Exact Match </label>
          <input
            type="checkbox"
            name="exact_match"
            id="exact_match"
            checked={exact_match}
            onChange={(e) => setExact_match(e.target.checked)}
          />
        </div>

        {results.length === 0 && buttonClicked && (
          <div>
            <h2 style={{ color: "red" }}>Not found</h2>
          </div>
        )}

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
                    <strong
                      className={styles.clickableFilename}
                      onClick={() => handleFilenameClick(file)}
                    >
                      {file.filename}
                    </strong>
                    <div>Path: {file.path}</div>
                    <div>Size: {Math.round(file.size / 1024)} KB</div>
                    <div>Type: {file.file_type}</div>
                  </div>
                </li>
              ))}
            </ul>
          </div>
        )}

        {selectedFile && (
          <div className={styles.metadataPanel}>
            <div className={styles.metadataContent}>
              {selectedFile.preview && (
                <div className={styles.previewSection}>
                  <h3>Preview:</h3>
                  <pre>{selectedFile.preview}</pre>
                </div>
              )}
              <button
                className={styles.downloadButton}
                onClick={handleDownload}
              >
                Download Metadata
              </button>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}