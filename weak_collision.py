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


class WeakCollision:
    """Run trials of breaking hash function weak collision resistance"""
    def __init__(self, trials=TRIALS, strlen=STRLEN):
        self.trials: int = trials
        self.strlen: int = strlen
        self.results: list[int] = []

    def start(self):
        """Execute trials number of break_weak_collision tests and report average results."""
        # Start trials number of break_weak_collision test processes
        with concurrent.futures.ProcessPoolExecutor() as executor:
            outputs = [executor.submit(self.break_weak_collision) for _ in range(self.trials)]

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

    def get_hash_prefix(self, init_data: bytes = None) -> tuple[bytes, str]:
        """Get a 6 char hash prefix from random byte string."""
        data = self.get_random_byte_string()
        while data == init_data:
            data = self.get_random_byte_string()
        hash_object = hashlib.sha256(data)
        hex_digest = hash_object.hexdigest()
        return data, hex_digest[:6]

    def break_weak_collision(self) -> tuple[str, int]:
        """Get first six digits of hash and compare with hashes on random bytes until we get a weak collision."""
        # Get the initial hex string to compare against
        init_data, init_hash_prefix = self.get_hash_prefix()

        # Perform new hashes on different data until we get a match
        attempts = 0
        hash_prefix = ''
        data = None
        while hash_prefix != init_hash_prefix:
            data, hash_prefix = self.get_hash_prefix(init_data)
            attempts += 1

        # Print trial results and return attempt
        output = '-' * 40 + '\n'
        output += f'Initial Data -> Hash: {init_data} -> {init_hash_prefix}\n'
        output += f'Results Data -> Hash: {data} -> {hash_prefix}\n'
        output += f'Attempts: {attempts}\n'
        return output, attempts


if __name__ == '__main__':
    experiment = WeakCollision()
    experiment.start()
