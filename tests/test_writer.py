import logging

from hmm_profile import models
from hmm_profile import writer
from tests import resources


def test_write_minimal_data(caplog):
    caplog.set_level(logging.WARNING)
    model = models.HMM(
        metadata=models.Metadata(
            version_identifier='HMMER3/f [3.1b2 | February 2015]',
            model_name='1-cysPrx_C',
            length=1,
            alphabet_type=models.AlphabetType.amino,
            alphabet=[
                'A',
                'C',
                'D',
                'E',
                'F',
                'G',
                'H',
                'I',
                'K',
                'L',
                'M',
                'N',
                'P',
                'Q',
                'R',
                'S',
                'T',
                'V',
                'W',
                'Y',
            ],
            consensus_residue_annotation=True,
        ),
        steps=[
            models.Step(
                p_emission_to_emission=0.25,
                p_emission_to_insertion=0.25,
                p_emission_to_deletion=0.5,
                p_insertion_to_emission=0.25,
                p_insertion_to_insertion=0.75,
                p_deletion_to_emission=1,
                p_deletion_to_deletion=0,
                p_emission_char={
                    'A': 0.05,
                    'C': 0.05,
                    'D': 0.05,
                    'E': 0.05,
                    'F': 0.05,
                    'G': 0.05,
                    'H': 0.05,
                    'I': 0.05,
                    'K': 0.05,
                    'L': 0.05,
                    'M': 0.05,
                    'N': 0.05,
                    'P': 0.05,
                    'Q': 0.05,
                    'R': 0.05,
                    'S': 0.05,
                    'T': 0.05,
                    'V': 0.05,
                    'W': 0.05,
                    'Y': 0.05,
                },
                p_insertion_char={
                    'A': 0.05,
                    'C': 0.05,
                    'D': 0.05,
                    'E': 0.05,
                    'F': 0.05,
                    'G': 0.05,
                    'H': 0.05,
                    'I': 0.05,
                    'K': 0.05,
                    'L': 0.05,
                    'M': 0.05,
                    'N': 0.05,
                    'P': 0.05,
                    'Q': 0.05,
                    'R': 0.05,
                    'S': 0.05,
                    'T': 0.05,
                    'V': 0.05,
                    'W': 0.05,
                    'Y': 0.05,
                },
            ),
        ],
    )

    result = ''.join(writer.get_lines(model))

    with open(resources.EXAMPLE_MINIMAL_DATA_HMM) as f:
        expected = f.read()
    assert result == expected
    # No warnings
    assert caplog.text == ''
