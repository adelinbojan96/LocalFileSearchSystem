"use client";

import React from "react";
import { useSearchResults } from "../SearchResultsContext";
import styles from './page.module.css';
import { FileMetadata } from "../SearchResultsContext";

export default function DocsPage() {
    const { results } = useSearchResults();

    const docs = results.filter((file: FileMetadata) => {
        const ext = file.name.split('.').pop()?.toLowerCase();
        return ['txt', 'md', 'rtf'].includes(ext || '');
    });

    return (
        <main className={styles.main}>
            <h1>Document Files in Current Search</h1>


            {docs.length === 0 ? (
                <p className={styles.noDocs}>No text files found in the current search.</p>
            ) : (
                docs.map((doc, idx) => {
                    const ext = doc.name.split('.').pop()?.toLowerCase();
                    if (['txt', 'md', 'rtf'].includes(ext || '')) {
                        return (
                            <section key={idx} className={styles.section}>
                                <h2>{doc.name}</h2>
                                <pre className={styles.textPreview}>{doc.preview}</pre>
                            </section>
                        );
                    }
                    return (
                        <section key={idx} className={styles.section}>
                            <h2>{doc.name}</h2>
                        </section>
                    );
                })
            )}
        </main>
    );
}
