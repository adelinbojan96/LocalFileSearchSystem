"use client";
import styles from "./page.module.css";
import React, { useState, useCallback } from "react";
import axios from "axios";
import { useRouter } from "next/navigation";
import "./globals.css";
import { useSearchResults } from "./SearchResultsContext";
import type { FileMetadata } from "./SearchResultsContext"

export default function Home() {
  const router = useRouter();

  const [fileName, setFileName] = useState("");
  const [buttonClicked, setButtonClicked] = useState(false);
  const [exact_match, setExact_match] = useState(false);
  const [json_format, setJson_format] = useState(false);
  const [selectedFile, setSelectedFile] = useState<FileMetadata | null>(null);
  const [suggestions, setSuggestions] = useState<string[]>([]);
  const { results, setResults, widget, setWidget, specialWidget, setSpecialWidget } = useSearchResults();
  const [correction, setCorrection] = useState<string | null>(null);

  const debounce = useCallback(<F extends (...args: any[]) => void>(func: F, delay: number) => {
    let timer: NodeJS.Timeout;
    return (...args: Parameters<F>) => {
      clearTimeout(timer);
      timer = setTimeout(() => func(...args), delay);
    };
  }, []);

  const fetchSuggestions = useCallback(async (query: string) => {
    if (query.length > 2) {
      try {
        const response = await axios.get(
            "http://localhost:8000/api/suggestions/",
            { params: { q: query } }
        );
        setSuggestions(response.data.suggestions || []);
      } catch {
        setSuggestions([]);
      }
    } else {
      setSuggestions([]);
    }
  }, []);

  const fetchCorrection = useCallback(async (query: string) => {
    if (query.length) {
      try {
        const { data } = await axios.get(
            "http://localhost:8000/api/corrections/",
            { params: { q: query } }
        );
        setCorrection(data.correction || null);
      } catch {
        setCorrection(null);
      }
    } else {
      setCorrection(null);
    }
  }, []);

  const fetchWidget = useCallback(async (query: string) => {
    if (query.length > 0) {
      try {
        const response = await axios.get(
            "http://localhost:8000/api/widgets/",
            { params: { q: query } }
        );
        setWidget(response.data.widget || null);
      } catch {
        setWidget(null);
      }
    } else {
      setWidget(null);
    }
  }, []);

  const debouncedFetchSuggestions = useCallback(
      debounce(fetchSuggestions, 200),
      [debounce, fetchSuggestions]
  );
  const debouncedFetchCorrection = useCallback(
      debounce(fetchCorrection, 300),
      [debounce, fetchCorrection]
  );

  const handleInputChange = useCallback(
      (e: React.ChangeEvent<HTMLInputElement>) => {
        const value = e.target.value;
        setFileName(value);
        debouncedFetchSuggestions(value);
        debouncedFetchCorrection(value);
      },
      [debouncedFetchSuggestions, debouncedFetchCorrection]
  );

  const handleSearchClick = async () => {
    if (!fileName) {
      alert("Please enter a file name");
      return;
    }
    try {
      setSelectedFile(null);
      setWidget(null);
      const payload = { file_name: fileName, exact_match, json_format };
      const response = await axios.post("http://localhost:8000/api/search/", payload);
      setResults(response.data.results || []);
      setSpecialWidget(response.data.widgets || []);
      await fetchWidget(fileName);
    } catch {
      setResults([]);
      setWidget(null);
    } finally {
      setButtonClicked(true);
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
    a.download = `${selectedFile.name}_metadata.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
      <div className={styles.page}>
        <main className={styles.main}>
          <h1>Search files locally</h1>

          <div className={styles.centerColumn}>
            <div className={styles.searchContainer}>
              <input
                  type="text"
                  placeholder="Enter file name"
                  className={styles.searchBar}
                  value={fileName}
                  onChange={handleInputChange}
              />

              {correction && correction !== fileName && (
                  <div
                      className={styles.correctionSuggestion}
                      onClick={() => {
                        setFileName(correction!);
                        setCorrection(null);
                        setSuggestions([]);
                      }}
                  >
                    Correction suggestion: <span className={styles.correctionLink}>{correction}</span>
                  </div>
              )}

              {widget && (
                  <div className={styles.widgetImageContainer}>
                    <img
                        src={`data:image/png;base64,${widget.image}`}
                        alt={widget.word_name}
                        className={styles.widgetImage}
                    />
                    <p className={styles.widgetDescription}>{widget.description}</p>
                  </div>
              )}

              {suggestions.length > 0 && (
                  <div className={styles.suggestionsDropdown}>
                    {suggestions.map((term, i) => (
                        <div
                            key={i}
                            className={styles.suggestionItem}
                            onClick={() => {
                              setFileName(term);
                              setSuggestions([]);
                            }}
                        >
                          {term}
                        </div>
                    ))}
                  </div>
              )}
            </div>
          </div>

          <button className={styles.searchButton} onClick={handleSearchClick}>
            Search
          </button>

          <div className="form-row" style={{ textAlign: "left" }}>
            <label htmlFor="exact_match">Exact Match </label>
            <input
                type="checkbox"
                id="exact_match"
                checked={exact_match}
                onChange={(e) => setExact_match(e.target.checked)}
            />
          </div>

          <div className="form-row" style={{ textAlign: "left" }}>
            <label htmlFor="json_format">Report as Json </label>
            <input
                type="checkbox"
                id="json_format"
                checked={json_format}
                onChange={(e) => setJson_format(e.target.checked)}
            />
          </div>

          <p
              className={styles.clickableFilename}
              onClick={() => router.push("/multiple_workers")}
          >
            MultipleWorkers Mode
          </p>

          {buttonClicked && specialWidget.length > 0 && (
              <div className={styles.specialWidgetsContainer}>
                {specialWidget.map((w, idx) => (
                    <div key={idx} className={styles.specialWidget}>
                      <div
                          className={styles.specialWidgetTitle}
                          onClick={() => router.push(w.action_url)}
                          tabIndex={0}
                          onKeyDown={e => { if (e.key === "Enter" || e.key === " ") router.push(w.action_url); }}
                          role="button"
                          aria-label={`Go to ${w.title}`}
                      >
                        {w.title}
                      </div>
                      <div className={styles.specialWidgetMessage}>{w.message}</div>
                    </div>
                ))}
              </div>
          )}

          {results.length === 0 && buttonClicked && (
              <h2 style={{ color: "red" }}>Not found</h2>
          )}

          {results.length > 0 && (
              <>
                <h2 style={{ color: "green" }}>
                  Found {results.length} matching file{results.length !== 1 && "s"}
                </h2>
                <h2>Search Results:</h2>
                <ul>
                  {results.map((file, i) => (
                      <li key={i}>
                        <div className={styles.fileItem}>
                          <strong className={styles.clickableFilename}>
                            {file.name}
                          </strong>
                          <div>Path: {file.path}</div>
                          <div>Size: {Math.round(file.size / 1024)} KB</div>
                          <div>Type: {file.type}</div>
                        </div>
                      </li>
                  ))}
                </ul>
              </>
          )}

          {selectedFile && (
              <div className={styles.metadataPanel}>
                {selectedFile.preview && (
                    <div className={styles.previewSection}>
                      <h3>Preview:</h3>
                      <pre>{selectedFile.preview}</pre>
                    </div>
                )}
                <button className={styles.downloadButton} onClick={handleDownload}>
                  Download Metadata
                </button>
              </div>
          )}
        </main>
      </div>
  );
}
