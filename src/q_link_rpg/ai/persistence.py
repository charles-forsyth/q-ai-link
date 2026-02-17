import numpy as np
from pathlib import Path
from typing import Union


def save_q_table(q_table: np.ndarray, path: Union[str, Path]) -> None:
    """
    Save the Q-table to a file using numpy format.
    """
    try:
        np.save(path, q_table, allow_pickle=False)
    except Exception as e:
        raise ValueError(f"Failed to save Q-table: {e}")


def load_q_table(path: Union[str, Path]) -> np.ndarray:
    """
    Load the Q-table from a file, disallowing pickle for security.
    """
    try:
        # allow_pickle=False is the default in newer numpy, but explicit is better for security
        q_table = np.load(path, allow_pickle=False)
        return q_table
    except FileNotFoundError:
        raise
    except Exception as e:
        raise ValueError(f"Failed to load Q-table: {e}")
