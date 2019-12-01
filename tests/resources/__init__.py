import os
import pathlib

resources_dir = pathlib.Path(os.path.dirname(os.path.abspath(__file__)))

EXAMPLE_SINGLE_REAL_DATA_HMM = resources_dir / '1-cysPrx_C.hmm'
EXAMPLE_MULTI_REAL_DATA_HMM = resources_dir / 'multi.hmm'
EXAMPLE_MINIMAL_DATA_HMM = resources_dir / 'minimal.hmm'
