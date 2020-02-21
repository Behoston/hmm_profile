0.0.7 (2020-02-21)
------------------

- Enable periodic tests for all Pfam hmm profiles.
- Enable mypy.
- Enabled isort.
- Added model for statistical data.
- Added crosscheck test (load -> save -> load and compare if both loaded model are same).
- Added full database test (all hmm profiles from Pfam).
- Fixed read emission line for start step.
- Added save method with opened file (or file-like object) as parameter.
- Fixed saving RF line (boolean value was false/true instead of no/yes).
- Added saving statistical lines
- Added saving build command
- Added saving search command
- Added saving additional data in emission line

0.0.6 (2020-02-20)
------------------

- Add wheel to release.


0.0.5 (2020-02-20)
------------------

- Auto release from github.


0.0.4 (2020-02-20)
------------------

- Set development status to Alpha.


0.0.3 (2020-02-20)
------------------

- CI/CD tests

0.0.2 (2020-02-19)
------------------

- CI/CD tests

0.0.1 (2020-02-19)
------------------

Initial release

- Reader implemented
- Writer implemented
- Base models implemented
