import argparse
import ftplib
import gzip
import io
import logging
import os
import pathlib
import tempfile
import time
import typing

import pytest

from hmm_profile import reader
from hmm_profile import writer

logger = logging.getLogger(__name__)

ALL_HMM_ENV_VAR = 'HMM_PROFILE_ALL_HMM_FILE'
CACHE_DIR_ENV_VAR = 'HMM_PROFILE_CACHE_DIR'
ALL_HMM_FILE_NAME = 'Pfam-A.hmm.gz'
FTP_HOST = 'ftp.ebi.ac.uk'
FTP_DIRECTORY = 'pub/databases/Pfam/current_release/'
MIN_ALL_HMM_FILE_SIZE = 1024 * 1024
GZIP_MAGIC = b'\x1f\x8b'


def default_cache_dir() -> pathlib.Path:
    cache_dir = os.environ.get(CACHE_DIR_ENV_VAR)
    if cache_dir:
        return pathlib.Path(cache_dir)
    return pathlib.Path.home() / '.cache' / 'hmm_profile'


def is_valid_all_hmm_file(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    if path.stat().st_size < MIN_ALL_HMM_FILE_SIZE:
        return False
    with path.open('rb') as all_hmm_file:
        return all_hmm_file.read(len(GZIP_MAGIC)) == GZIP_MAGIC


def verify_all_hmm_file(path: pathlib.Path, expected_size: typing.Optional[int] = None) -> None:
    if not is_valid_all_hmm_file(path):
        raise RuntimeError(f'Database file {path} is not a valid gzip archive.')
    if expected_size is not None and path.stat().st_size != expected_size:
        raise RuntimeError(f'Database file {path} is incomplete, expected {expected_size} bytes.')


def close_ftp(ftp: ftplib.FTP) -> None:
    try:
        ftp.quit()
    except (ftplib.Error, OSError):
        ftp.close()


def download_to_file(target: pathlib.Path) -> typing.Optional[int]:
    ftp = ftplib.FTP(FTP_HOST)
    ftp.login()
    try:
        ftp.cwd(FTP_DIRECTORY)
        expected_size = ftp.size(ALL_HMM_FILE_NAME)
        with target.open('wb') as output:
            ftp.retrbinary(f'RETR {ALL_HMM_FILE_NAME}', output.write)
    finally:
        close_ftp(ftp)
    return expected_size


def remove_file(path: pathlib.Path) -> None:
    if path.exists():
        path.unlink()


def download_all_hmm_file(target: pathlib.Path) -> pathlib.Path:
    target.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=str(target.parent), delete=False) as temporary_file:
        temporary_path = pathlib.Path(temporary_file.name)
    try:
        logger.info('Downloading %s from %s ...', ALL_HMM_FILE_NAME, FTP_HOST)
        expected_size = download_to_file(temporary_path)
        verify_all_hmm_file(temporary_path, expected_size)
        temporary_path.replace(target)
    finally:
        remove_file(temporary_path)
    logger.info('Database file saved in %s.', target)
    return target


def get_requested_all_hmm_file(output: typing.Optional[pathlib.Path]) -> typing.Optional[pathlib.Path]:
    if output:
        return pathlib.Path(output)
    env_value = os.environ.get(ALL_HMM_ENV_VAR)
    if env_value:
        return pathlib.Path(env_value)
    return None


def resolve_all_hmm_file(output: typing.Optional[pathlib.Path] = None) -> pathlib.Path:
    candidate = get_requested_all_hmm_file(output)
    if candidate is not None:
        if is_valid_all_hmm_file(candidate):
            logger.info('Using already downloaded database file: %s', candidate)
            return candidate
        logger.warning('Database file %s is missing or invalid, downloading it again.', candidate)
        return download_all_hmm_file(candidate)
    cached_file = default_cache_dir() / ALL_HMM_FILE_NAME
    if is_valid_all_hmm_file(cached_file):
        logger.info('Using cached database file: %s', cached_file)
        return cached_file
    return download_all_hmm_file(cached_file)


@pytest.fixture(scope='session')
def all_hmm_file() -> typing.Iterator[str]:
    yield str(resolve_all_hmm_file())


@pytest.mark.skipif(
    os.environ.get('HMM_PROFILE_RUN_INTEGRITY_TESTS', 'FALSE') != 'TRUE',
    reason="This test is for CI only. It will download",
)
def test_full_database_readable(all_hmm_file):
    hmm_counter = 0
    with gzip.open(all_hmm_file, mode='rt') as all_hmm_file_content:
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


def main() -> int:
    parser = argparse.ArgumentParser(description='Download the Pfam database used by the full database test.')
    parser.add_argument('--output', help='Path of the database file, an already downloaded file is reused.')
    arguments = parser.parse_args()
    output = pathlib.Path(arguments.output) if arguments.output else None
    print(resolve_all_hmm_file(output))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
