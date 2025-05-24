"use client";

import React from "react";
import { useSearchResults } from "../SearchResultsContext";
import styles from './page.module.css';
import type { FileMetadata } from "../SearchResultsContext";

export default function LogsPage() {
    const { results } = useSearchResults();
    const logs = results.filter((file: FileMetadata) => {
        const ext = file.name.split('.').pop()?.toLowerCase();
        return ['log'].includes(ext || '');
    });

    return (
        <main className={styles.main}>
            <h1>Log Files in Current Search</h1>
            {logs.length === 0 ? (
                <p className={styles.noDocs}>No log files (.log) found in the current search.</p>
            ) : (
                logs.map((log, idx) => (
                    <section key={idx} className={styles.section}>
                        <h2>{log.name}</h2>
                        <pre className={styles.textPreview}>{log.preview}</pre>
                    </section>
                ))
            )}
        </main>
    );
}
