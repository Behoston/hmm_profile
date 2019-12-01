import logging

from hmm_profile import models
from hmm_profile import reader
from tests import resources


def test_one_real_life_example(caplog):
    caplog.set_level(logging.WARNING)
    with resources.EXAMPLE_SINGLE_REAL_DATA_HMM.open() as f:
        model: models.HMM = reader.read_single(f)

    assert hasattr(model, 'metadata')
    assert hasattr(model, 'start_step')
    assert hasattr(model, 'steps')
    metadata = model.metadata
    # Mandatory fields
    assert metadata.version_identifier == 'HMMER3/f [3.1b2 | February 2015]'
    assert metadata.model_name == '1-cysPrx_C'
    assert metadata.length == 40
    assert metadata.alphabet_type == models.AlphabetType.amino
    assert metadata.alphabet == [
        'A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y',
    ]
    assert metadata.consensus_residue_annotation is True
    # Optional fields
    assert metadata.accession_number == 'PF10417.9'
    assert metadata.description == 'C-terminal domain of 1-Cys peroxiredoxin'
    assert metadata.max_instance_length is None
    assert metadata.reference_annotation is False
    assert metadata.model_masked is False
    assert metadata.consensus_structure_annotation is True
    assert metadata.map_annotation is True
    assert metadata.date == 'Thu Aug  2 10:53:47 2018'
    assert metadata.command_line_log is None
    assert metadata.sequence_number == 46
    assert metadata.effective_sequence_number == 19.774048
    assert metadata.checksum == 4280830619
    assert metadata.gathering_threshold == (21.10, 21.10)
    assert metadata.trusted_cutoff == (21.10, 21.10)
    assert metadata.noise_cutoff == (21.0, 21.0)
    assert metadata.statistical_parameters == [
        ('LOCAL', 'MSV', -7.4476, 0.71948),
        ('LOCAL', 'VITERBI', -7.8642, 0.71948),
        ('LOCAL', 'FORWARD', -4.32, 0.71948),
    ]
    assert metadata.build_command == 'hmmbuild HMM.ann SEED.ann'
    assert metadata.search_command == 'hmmsearch -Z 45638612 -E 1000 --cpu 4 HMM pfamseq'
    # No warnings
    assert caplog.text == ''


def test_multi_real_life_example(caplog):
    caplog.set_level(logging.WARNING)

    with resources.EXAMPLE_MULTI_REAL_DATA_HMM.open() as f:
        all_models = list(reader.read_all(f))

    assert len(all_models) == 3
    # No warnings
    assert caplog.text == ''
