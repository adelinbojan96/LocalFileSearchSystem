"use client";

import Image from "next/image";
import styles from "./page.module.css";
import { SetStateAction, useState } from "react";
import axios from "axios";


export default function Home() {
  const [fileName, setFileName] = useState("");
  const [results, setResults] = useState([]);

  const handleInputChange = (e: { target: { value: SetStateAction<string>; }; }) =>
  {
    setFileName(e.target.value);
  }
  const handleSearchClick = async () =>
  {
    if(fileName)
    {
      try{
        const response = await axios.post("http://localhost:8000/api/search/", {
          file_name: fileName,
        });
        //backend returns a list of matching files
        setResults(response.data);
      }
      catch(error)
      {
        console.error("Error in searching files: ", error);
      }
      
    }
    else
      alert("Please enter a file name in order to search");
  };
  
  return (
    <div className={styles.page}>
      <main className={styles.main}>
        <h1>Search a file locally</h1>
        
        <input
          type="text"
          placeholder="Enter file name"
          className={styles.searchBar}
          value = {fileName}
          onChange = {handleInputChange}
        />
        <button className={styles.searchButton} onClick = {handleSearchClick}>Search</button>
        {/*Partial results for verification*/}
        {results.length > 0 && (
          <div>
            <h2> Search Results:</h2>
            <ul>
              {results.map((file, index) => 
              (
                <li key = {index}>{file}</li>
              ))}
            </ul>
          </div>
        )}
      </main>
    </div>
  );
}
