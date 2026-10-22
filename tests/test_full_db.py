import ftplib
import gzip
import io
import logging
import os
import time

import pytest

from hmm_profile import reader
from hmm_profile import writer
from tests import resources

logger = logging.getLogger(__name__)


@pytest.mark.skipif(
    os.environ.get('HMM_PROFILE_RUN_INTEGRITY_TESTS', 'FALSE') != 'TRUE',
    reason="This test is for CI only. It will test all hmm profiles from Pfam database.",
)
def test_full_database_readable():
    hmm_counter = 0
    with gzip.open(resources.FULL_DB, mode='rt') as all_hmm_file_content:
        start_time = time.time()
        for hmm in reader.read_all(all_hmm_file_content):
            hmm_counter += 1
            in_memory_output_file = io.StringIO()
            writer.save_to_writable(hmm, in_memory_output_file)
            in_memory_output_file.seek(0)
            saved_hmm = reader.read_single(in_memory_output_file)
            assert saved_hmm == hmm, hmm.metadata.model_name
    complete = time.time() - start_time
    print(f"Benchmark for {hmm_counter} profiles complete in {complete} seconds.")


def update_database():
    ftp = ftplib.FTP('ftp.ebi.ac.uk')
    ftp.login()
    ftp.cwd('pub/databases/Pfam/current_release/')
    file_name = 'Pfam-A.hmm.gz'
    with open(resources.FULL_DB, 'wb') as all_hmm_file:
        ftp.retrbinary(f'RETR {file_name}', all_hmm_file.write)
        ftp.quit()


if __name__ == "__main__":
    update_database()
