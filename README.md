# HMM_profile

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](./LICENSE)
[![Actions Status](https://github.com/Behoston/hmm_profile/workflows/Test/badge.svg)](https://github.com/Behoston/hmm_profile/actions?query=workflow%3ATest)

Hidden Markov Model profile toolkit. 

Written in the base of [HMMER User's Guide](http://eddylab.org/software/hmmer3/3.1b2/Userguide.pdf).


## Usage

With my package you can read and write hmm profile files.
It's easy to use and easy to read - the best documentation is a well-written code itself,
so don't be scared about reading source code.

I decided to use an already opened file as a function parameter,
due to file can come from different places, not only local drive.

For a writer's functions, I decided to use local file.
But you can use an underlying function to get file content directly without saving to file.

### Reader

#### Read all hmm from file

The `read_all` function returns generator to optimise memory usage - 
it's a common pattern that one file contains many models.


```python
from hmm_profile import reader


with open('/your/hmm/profile/file.hmm') as f:
    model_generator = reader.read_all(f)  # IMPORTANT: returns generator

models = list(model_generator)

```

#### Read single model

If you have only single model files, you can use this method. It will return `models.HMM` ready to use.

```python
from hmm_profile import reader


with open('/your/hmm/profile/file.hmm') as f:
    model = reader.read_single(f) 

```

### Writer

#### Write multiple models to single file 

```python
from hmm_profile import writer

models = [...]
path = '/your/hmm/profile/file.hmm'

writer.save_many_to_file(hmms=models, output=path)
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

In the near future, I will implement the periodic task, that will be testing if all hmm profiles
from Pfam are readable and writable without errors.
