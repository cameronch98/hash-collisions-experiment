""" Citations:
https://docs.python.org/3/library/hashlib.html
https://levelup.gitconnected.com/comparing-concurrency-and-parallelism-techniques-in-python-threading-multiprocessing-concurrent-f-7e28c1bf8340
"""

import random
import string
import concurrent.futures
import hashlib
from statistics import mean

TRIALS = 100
STRLEN = 5


class StrongCollision:
    def __init__(self, trials=TRIALS, strlen=STRLEN):
        self.trials = trials
        self.strlen = strlen
        self.results = []

    def start(self):
        """Execute trials number of break_weak_collision tests and report average results."""
        # Start trials number of break_strong_collision test processes
        with concurrent.futures.ProcessPoolExecutor() as executor:
            outputs = [executor.submit(self.break_strong_collision) for _ in range(self.trials)]

            # Print outputs and store results as they arrive
            for future in concurrent.futures.as_completed(outputs):
                output, attempts = future.result()
                self.results.append(attempts)
                print(f"Trial {len(self.results)}:")
                print(output)

        # Report the average number of attempts needed to break weak collision
        print('Experiment Completed:')
        print('-' * 40)
        print(f'Number of trials completed: {self.trials}')
        print(f'Average number of attempts: {int(mean(self.results))}')

    def get_random_byte_string(self) -> bytes:
        """Get a random byte string of length strlen."""
        random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=self.strlen))
        return bytes(random_string, 'utf-8')

    def get_hash_prefix(self, hashes: dict) -> tuple[bytes, str]:
        """Get a 6 char hash prefix from random byte string."""
        data = self.get_random_byte_string()
        while data in hashes:
            data = self.get_random_byte_string()
        hash_object = hashlib.sha256(data)
        hex_digest = hash_object.hexdigest()
        return data, hex_digest[:6]

    def break_strong_collision(self) -> tuple[str, int]:
        """Get first six digits of hash and compare with hashes on random bytes until we get a weak collision."""
        # Perform new hashes on different data until we match with an existing hash
        attempts = 0
        hashes = {}
        data, hash_prefix = self.get_hash_prefix(hashes)
        while hash_prefix not in hashes:
            hashes[hash_prefix] = data
            data, hash_prefix = self.get_hash_prefix(hashes)
            attempts += 1

        # Print trial results and return attempt
        output = '-' * 40 + '\n'
        output += f'1st Data -> Hash: {hashes[hash_prefix]} -> {hash_prefix}\n'
        output += f'2nd Data -> Hash: {data} -> {hash_prefix}\n'
        output += f'Attempts: {attempts}\n'
        return output, attempts


if __name__ == '__main__':
    experiment = StrongCollision()
    experiment.start()
