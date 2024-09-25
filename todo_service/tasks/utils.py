from hashlib import sha256
from time import time_ns


def generate_id(data: str) -> str:
    cur_time = time_ns()
    return sha256(f"{data}{cur_time}".encode()).hexdigest()[:20]
