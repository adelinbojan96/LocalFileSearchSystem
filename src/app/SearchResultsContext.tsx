"use client";
import React, { createContext, useContext, useState, ReactNode } from "react";

export type FileMetadata = {
    name: string;
    path: string;
    size: number;
    last_modified: string;
    creation_time: string;
    type: string;
    preview: string;
};
export type WidgetData = {
    id_word: number;
    word_name: string;
    image: string;
    description: string;
} | null;

export type SpecialWidget = {
    widget_id: string;
    title: string;
    message: string;
    action_url: string;
};

type SearchResultsContextType = {
    results: FileMetadata[];
    setResults: (results: FileMetadata[]) => void;
    widget: WidgetData;
    setWidget: (widget: WidgetData) => void;
    specialWidget: SpecialWidget[];
    setSpecialWidget: (specialWidget: SpecialWidget[]) => void;
};

const SearchResultsContext = createContext<SearchResultsContextType | undefined>(undefined);

export function SearchResultsProvider({ children }: { children: ReactNode }) {
    const [results, setResults] = useState<FileMetadata[]>([]);
    const [widget, setWidget] = useState<WidgetData>(null);
    const [specialWidget, setSpecialWidget] = useState<SpecialWidget[]>([]);

    return (
        <SearchResultsContext.Provider value={{ results, setResults, widget, setWidget, specialWidget, setSpecialWidget }}>
            {children}
        </SearchResultsContext.Provider>
    );
}

export function useSearchResults() {
    const ctx = useContext(SearchResultsContext);
    if (!ctx) throw new Error("useSearchResults must be used within SearchResultsProvider");
    return ctx;
}
