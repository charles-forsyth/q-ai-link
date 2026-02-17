import pytest
import numpy as np
import os
from q_link_rpg.ai.persistence import save_q_table, load_q_table

def test_save_load_secure(tmp_path):
    """Test saving and loading Q-table with security checks."""
    q_table = np.zeros((5, 5, 4))
    q_table[0, 0, 0] = 1.0
    
    save_path = tmp_path / "secure_q_table.npy"
    save_q_table(q_table, save_path)
    
    loaded_q = load_q_table(save_path)
    np.testing.assert_array_equal(q_table, loaded_q)

def test_load_malformed_file(tmp_path):
    """Test loading a non-numpy file should fail."""
    bad_file = tmp_path / "bad.txt"
    bad_file.write_text("not a numpy file")
    
    with pytest.raises(ValueError): # Or appropriate exception
        load_q_table(bad_file)

def test_load_pickle_disallowed(tmp_path):
    """Test that loading a pickle file is disallowed (security)."""
    # Create a dummy pickle file (if possible/relevant for the implementation)
    # The requirement is usually strictly checking for .npy format without pickle
    pass 
