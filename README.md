# HMM_profile

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](./LICENSE)
[![Actions Status](https://github.com/Behoston/hmm_profile/workflows/Test/badge.svg)](https://github.com/Behoston/hmm_profile/actions?query=workflow%3ATest)
[![Wheel Status](https://img.shields.io/pypi/wheel/hmm-profile)](https://pypi.python.org/pypi/hmm-profile/)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/hmm-profile)](https://pypi.python.org/pypi/hmm-profile/)
[![PyPI - Status](https://img.shields.io/pypi/status/hmm-profile)](https://pypi.python.org/pypi/hmm-profile/)
[![Latest version](https://img.shields.io/pypi/v/hmm-profile)](https://pypi.python.org/pypi/hmm-profile/)

Hidden Markov Model profile toolkit. 

Written in the base of [HMMER User's Guide](http://eddylab.org/software/hmmer3/3.1b2/Userguide.pdf) p.107.


## Usage

With my package you can read and write hmm profile files.
It's easy to use and easy to read - the best documentation is a well-written code itself,
so don't be scared about reading source code.

### Reader

#### Read all hmm from file

The `read_all` function returns generator to optimise memory usage - 
it's a common pattern that one file contains many profiles.


```python
from hmm_profile import reader


with open('/your/hmm/profile/file.hmm') as f:
    model_generator = reader.read_all(f)  # IMPORTANT: returns generator

profiles = list(model_generator)

```

#### Read single model

If you have only single model files, you can use this method. It will return `models.HMM` ready to use.

```python
from hmm_profile import reader


with open('/your/hmm/profile/file.hmm') as f:
    model = reader.read_single(f) 

```

### Writer

#### Write multiple profiles to single file 

```python
from hmm_profile import writer

profiles = [...]
path = '/your/hmm/profile/file.hmm'

writer.save_many_to_file(hmms=profiles, output=path)
```

#### Write single model to file

```python
from hmm_profile import writer

model = ...
path = '/your/hmm/profile/file.hmm'

writer.save_to_file(hmm=model, output=path)
```

#### Get file content without saving

```python
from hmm_profile import writer

model = ...

lines = writer.get_lines(model)  # IMPORTANT: returns generator
content = ''.join(lines)
```

## Support/bugs

If you have a file that is not readable or has some glitches on save, please crate the issue and attach this file.
**Bug reports without files (or good examples if you can't provide full file) will be ignored.**

## Guarantees

[![Full database test](https://github.com/Behoston/hmm_profile/workflows/Full%20database%20test/badge.svg)](https://github.com/Behoston/hmm_profile/actions?query=workflow%3A%22Full+database+test%22)

Above you can see if all hmm profiles from Pfam works. Test are running every day. 

Test flow:

1. Download all hmm profiles from Pfam.
2. Load profiles sequentially.
3. Write model to file.
4. Load saved model from file.
5. Check if both loaded profiles are equals.

For this test the latest version of `hmm_profile` from pypi is used. 

Full DB test also runs before each release, but badge above shows only periodic tests results.

## Performance

Whole package is written in pure Python, without C extensions. 

You can treat full DB test as benchmark.

Benchmark should be depended mainly on single core of CPU and secondarily on storage and eventually on RAM.
Storage is used only for read from then files will be saved to "in-memory file" (StringIO).

Remember: Results may vary when CPU is under load.
Also, hmm profiles in db can be modified in future or some profiles may be added/removed from DB.


|          Processor       |          Storage          | Time [s] | Profiles |    Date    | Version | Python  |
|--------------------------|---------------------------|----------|----------|------------|---------|---------|
| Intel Core i7-4702MQ     | Crucial MX500 500 GB      |   342    |   17928  | 2020.02.22 |  0.0.9  |   3.7   |
| Intel Core i7-4702MQ     | Crucial MX500 500 GB      |   322    |   17928  | 2020.02.22 |  0.0.9  |   3.6   |
| Intel Core i7-4702MQ     | GoodRAM Iridium Pro240 GB |   TBA    |   TBA    |     TBA    |   TBA   |   3.6   |


To run benchmark:

```bash
pip install .
export HMM_PROFILE_RUN_INTEGRITY_TESTS=TRUE
python setpu.py test --addopts -s
```

Run test at least 3 times if you want to share results (last line) and close as much process as possible. 
**Important:** do not run tests inside so-called terminal in IDE - 
it will do much more job with output and benchmark result will be affected. 


As you can see python 3.6 is a little faster, 
probably due to different implementation of backported dataclasses, but I'm not sure.

## Development

### Release

1. Change version in setup.py to `x.y.z.dev0` (or leave if minor version bump) and ensure changelog is up to date.
(`Nothing changed yet.` is not ok, CI will fail)
2. Tag head of master branch with `x.y.z` without `.dev0`

**Important**: release ALWAYS is from master branch! So keep master untouched when you want to release.
