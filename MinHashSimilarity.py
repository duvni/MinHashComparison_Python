from MinHash import MinHash


class MinHashSimilarity:
    """Quick document comparison using MinHash algorithm."""

    def __init__(self, threshold: float, tokens_in_word: int=5, num_hash_functions: int=400, bands: int=20,
                 rows: int=20):
        if threshold < 0 or threshold > 100:
            raise Exception('MinHashSimilarity - Illegal threshold: {}'.format(tokens_in_word))
        if bands*rows != num_hash_functions:
            raise Exception('MinHashSimilarity - bands * rows != num_hash_functions')
        self._threshold = threshold
        self._tokens_in_word = tokens_in_word
        self._num_hash_functions = num_hash_functions
        self._bands = bands
        self._rows = rows
        self._buckets = {}
        self._min_hash = MinHash(tokens_in_word, num_hash_functions)

    def clear_documents(self):
        """Clear all history of documents."""
        self._buckets.clear()

    def look_for_similar_documents(self, doc: str) -> bool:
        """Given a string document, look whether a similar document was already seen."""
        min_hashes = self._min_hash.compute_sketch(doc.split())
        band_hashes = []
        compared_sketches = set()

        for i in range(0, self._bands):
            band_hashes.append(self._compute_band_hash(min_hashes, i))
            if band_hashes[i] in self._buckets:
                for sketch_to_compare in self._buckets[band_hashes[i]]:
                    sketch_to_compare_key = ''.join(str(x) for x in sketch_to_compare)
                    if sketch_to_compare_key not in compared_sketches:
                        if self._min_hash.compare_sketches(min_hashes, sketch_to_compare) >= self._threshold:
                            # Found a similar document
                            return True

                        # Avoid comparing two documents twice
                        compared_sketches.add(sketch_to_compare_key)

        # No match found, add document to buckets
        for i in range(0, self._bands):
            if band_hashes[i] not in self._buckets:
                self._buckets[band_hashes[i]] = []
            self._buckets[band_hashes[i]].append(min_hashes)

        return False

    def _compute_band_hash(self, min_hashes: [], i: int) -> str:
        """Compute a hash for quick bucket match search."""
        band_hash_list = []
        for j in range(0, self._rows):
            # Adding the rows corresponding to ith band
            band_hash_list.append('%010d' % min_hashes[i * self._rows + j])

        # Adding the number i to distinguish between bands
        band_hash_list.append('%010d' % i)
        return ''.join(band_hash_list)
