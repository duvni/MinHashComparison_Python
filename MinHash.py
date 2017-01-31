from random import randint


class MinHash:
    """Quick document comparison using MinHash algorithm."""

    class HashGenerator:
        """Hash function generator.

        Given a set of hash function parameters (a, b, c) and a bound on possible hash value,
        generate a hash function that given an element x returns its hashed value.
        """

        def __init__(self, a: int, b: int, c: int, universe_size: int):
            self._a = a
            self._b = b
            self._c = c
            self._universe_size = universe_size

        def calculate_hash(self, x: int) -> int:
            """Hash function calculator."""
            x &= self._universe_size
            # Modify the hash family as per the size of possible elements in a set
            hashed_value = ((self._a * (x >> 4)) + (self._b * x) + self._c) & self._universe_size
            return abs(hashed_value)

    def __init__(self, tokens_in_word: int, num_hash_functions: int):
        if tokens_in_word <= 0:
            raise Exception('MinHash - Illegal number of tokens in a word: {}'.format(tokens_in_word))
        if num_hash_functions <= 0:
            raise Exception('MinHash - Illegal number of hash functions: {}'.format(num_hash_functions))

        self._tokens_in_word = tokens_in_word
        self._num_hash_functions = num_hash_functions
        self._hash_functions = []

        self._universe_size = 2147483647  # 2^31-1 Mersenne prime
        for i in range(num_hash_functions):
            a = randint(0, self._universe_size)
            b = randint(0, self._universe_size)
            c = randint(0, self._universe_size)
            self._hash_functions.append(MinHash.HashGenerator(a, b, c, self._universe_size))

    def compute_sketch(self, tokens: []) -> []:
        """Compute the MinHash Sketch from an array of tokens.
        
        Update the hash tables according to the min values of the sketch.
        """
        hash_min_values = [self._universe_size] * self._num_hash_functions

        if tokens is None or len(tokens) == 0:
            return hash_min_values

        # Go over all tokens and generate words (k-shingling)
        for token_index in range(self._num_hash_functions):
            # Build the word by concatenating consecutive tokens
            word_builder = []
            for i in range(token_index, token_index + self._tokens_in_word):
                if i < len(tokens):
                    word_builder.append(tokens[i])
                else:
                    break

            hash_code = hash(''.join(word_builder))
            # Go over all hash functions
            for hash_index in range(self._num_hash_functions):
                hash_function = self._hash_functions[hash_index]  # type: MinHash.HashGenerator

                # Compute hash value of token with current hash function
                hash_value = hash_function.calculate_hash(hash_code)

                # Update minimum value at index hashIndex
                hash_min_values[hash_index] = min(hash_min_values[hash_index], hash_value)

        return hash_min_values

    def compare_sketches(self, first_min_hash_sketch: [], second_min_hash_sketch: []) -> float:
        """Compare two MinHash sketches."""
        equal_hashes = 0
        for i in range(self._num_hash_functions):
            if first_min_hash_sketch[i] == second_min_hash_sketch[i]:
                equal_hashes += 1

        return equal_hashes / self._num_hash_functions
