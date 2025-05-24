import { SearchResultsProvider } from "./SearchResultsContext";

export default function RootLayout({ children }: { children: React.ReactNode }) {
    return (
        <html lang="en">
        <body>
        <SearchResultsProvider>
            {children}
        </SearchResultsProvider>
        </body>
        </html>
    );
}
