import io

from hmm_profile import reader
from hmm_profile import writer
from tests import resources


def test_cross_check_multiple():
    with resources.EXAMPLE_MULTI_REAL_DATA_HMM.open() as f:
        for hmm in reader.read_all(f):
            in_memory_output_file = io.StringIO()
            writer.save_to_writable(hmm, in_memory_output_file)
            in_memory_output_file.seek(0)
            saved_hmm = reader.read_single(in_memory_output_file)
            assert saved_hmm == hmm, hmm.metadata.model_name
