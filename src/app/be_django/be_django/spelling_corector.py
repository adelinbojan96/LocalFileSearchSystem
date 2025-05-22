from typing import List, Tuple

class SpellingFacade:
    def __init__(self, vocabulary: List[str], cutoff_ratio):
        self.vocabulary = vocabulary
        self.cutoff_ratio = cutoff_ratio

    def correct(self, word: str) -> str:
        candidate, score = self.best_match(word)
        return candidate if score >= self.cutoff_ratio else word

    def best_match(self, word: str) -> Tuple[str, float]:
        best = (word, 0.0)
        for term in self.vocabulary:
            ratio = self.similarity_ratio(word, term)
            if ratio > best[1]:
                best = (term, ratio)
        return best

    def similarity_ratio(self, s1: str, s2: str) -> float:
        distance = self.levenshtein_distance(s1.lower(), s2.lower())
        max_len = max(len(s1), len(s2))
        return 1 - (distance / max_len) if max_len > 0 else 1.0

    @staticmethod
    def levenshtein_distance(s1: str, s2: str) -> int:
        if len(s1) < len(s2):
            return SpellingFacade.levenshtein_distance(s2, s1)
        previous = list(range(len(s2) + 1))
        for i in range(1, len(s1) + 1):
            c1 = s1[i - 1]
            current = [i]
            for j in range(1, len(s2) + 1):
                c2 = s2[j - 1]
                insertions = previous[j] + 1
                deletions = current[j - 1] + 1
                substitutions = previous[j - 1] + (c1 != c2)
                current.append(min(insertions, deletions, substitutions))
            previous = current
        return previous[-1]