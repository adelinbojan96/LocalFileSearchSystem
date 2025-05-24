"use client";

import React from "react";
import { useSearchResults } from "../SearchResultsContext";
import styles from './page.module.css';
import type { FileMetadata } from "../SearchResultsContext";

function getRelativePath(absPath: string) {
    // Just hardcode the base path to remove
    let normalized = absPath.replace(/\\/g, "/");
    let base = "D:/SoftwareDesign_Iteartion1_LocalFileSeachSystem/src/app/";
    if (normalized.startsWith(base)) {
        normalized = normalized.substring(base.length);
    }
    return "../" + normalized;
}

export default function ImagesPage() {
    const resultsObj = useSearchResults();
    const results = resultsObj.results;

    const images = results.filter(function (file) {
        const parts = file.name.split('.');
        const ext = parts[parts.length - 1].toLowerCase();
        return (
            ext === "jpg" ||
            ext === "jpeg" ||
            ext === "png" ||
            ext === "gif" ||
            ext === "bmp" ||
            ext === "webp"
        );
    });

    return (
        <main className={styles.main}>
            <h1>Images in Current Search</h1>
            {images.length === 0 ? (
                <p className={styles.noDocs}>No images found in the current search.</p>
            ) : (
                images.map(function(img, idx) {
                    return (
                        <section key={idx} className={styles.section}>
                            <h2>{img.name}</h2>
                            <pre className={styles.pathPreview}>{getRelativePath(img.path)}</pre>
                        </section>
                    );
                })
            )}
        </main>
    );
}
