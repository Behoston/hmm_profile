import logging
import math
import typing

from hmm_profile import models

logger = logging.getLogger(__name__)


def read_all(f: typing.TextIO) -> typing.Generator[models.HMM, None, None]:
    try:
        while True:
            yield read_single(f)
    except EOFError:
        return


def read_single(f: typing.TextIO) -> models.HMM:
    metadata = parse_metadata(f)
    steps: typing.List[models.Step] = list(parse_steps(f, metadata.alphabet))  # type: ignore
    start_step = None
    if isinstance(steps[0], models.StartStep):
        start_step = steps[0]
        steps = steps[1:]
    return models.HMM(metadata, steps, start_step)


def parse_metadata(f) -> models.Metadata:  # noqa: C901
    version = _parse_version(f)
    metadata_dict: typing.Dict[str, typing.Any] = {'version_identifier': version}
    statistical_parameters: typing.List[models.StatisticalParameter] = []
    for line in f:
        tag, unparsed_value = line.strip().split(maxsplit=1)
        if tag == 'HMM':
            metadata_dict['alphabet'] = unparsed_value.split()
            f.readline()
            break
        elif tag == 'NAME':
            metadata_dict['model_name'] = unparsed_value
        elif tag == 'ACC':
            metadata_dict['accession_number'] = unparsed_value
        elif tag == 'DESC':
            metadata_dict['description'] = unparsed_value
        elif tag == 'LENG':
            metadata_dict['length'] = int(unparsed_value)
        elif tag == 'MAXL':
            metadata_dict['max_instance_length'] = int(unparsed_value)
        elif tag == 'ALPH':
            metadata_dict['alphabet_type'] = models.AlphabetType(unparsed_value)
        elif tag == 'RF':
            metadata_dict['reference_annotation'] = _parse_bool(unparsed_value)
        elif tag == 'MM':
            metadata_dict['model_masked'] = _parse_bool(unparsed_value)
        elif tag == 'CONS':
            metadata_dict['consensus_residue_annotation'] = _parse_bool(unparsed_value)
        elif tag == 'CS':
            metadata_dict['consensus_structure_annotation'] = _parse_bool(unparsed_value)
        elif tag == 'MAP':
            metadata_dict['map_annotation'] = _parse_bool(unparsed_value)
        elif tag == 'DATE':
            metadata_dict['date'] = unparsed_value
        elif tag == 'COM':
            if 'command_line_log' not in metadata_dict:
                metadata_dict['command_line_log'] = [unparsed_value]
            else:
                metadata_dict['command_line_log'].append(unparsed_value)
        elif tag == 'NSEQ':
            metadata_dict['sequence_number'] = int(unparsed_value)
        elif tag == 'EFFN':
            metadata_dict['effective_sequence_number'] = float(unparsed_value)
        elif tag == 'CKSUM':
            metadata_dict['checksum'] = int(unparsed_value)
        elif tag == 'GA':
            n1, n2 = unparsed_value.strip(';').split()
            metadata_dict['gathering_threshold'] = (float(n1), float(n2))
        elif tag == 'TC':
            n1, n2 = unparsed_value.strip(';').split()
            metadata_dict['trusted_cutoff'] = (float(n1), float(n2))
        elif tag == 'NC':
            n1, n2 = unparsed_value.strip(';').split()
            metadata_dict['noise_cutoff'] = (float(n1), float(n2))
        elif tag == 'STATS':
            s1, s2, f1, f2 = unparsed_value.split()
            if s1 not in {'LOCAL'}:
                logger.warning(f"Unsupported alignment mode {s1}.")
            if s2 not in {'MSV', 'VITERBI', 'FORWARD'}:
                logger.warning(f"Unsupported score distribution {s2}.")
            statistical_parameters.append(models.StatisticalParameter(
                alignment_mode_configuration=s1,
                score_distribution_name=s2,
                location=float(f1),
                slope=float(f2),
            ))
        elif tag == 'BM':
            metadata_dict['build_command'] = unparsed_value
        elif tag == 'SM':
            metadata_dict['search_command'] = unparsed_value
        else:
            logger.warning(f"Unknown tag '{tag}'!")
        if statistical_parameters:
            metadata_dict['statistical_parameters'] = statistical_parameters
    return models.Metadata(**metadata_dict)


def _parse_version(f: typing.TextIO) -> str:
    version = '\n'
    while version == '\n':
        version = f.readline()
    if version == '':
        raise EOFError
    else:
        return version.strip()


def _parse_bool(value: str) -> bool:
    value = value.lower()
    if value == 'yes':
        return True
    elif value == 'no':
        return False
    else:
        raise Exception(f"Cannot parse bool value: {value}.")


def parse_steps(
        f: typing.IO,
        alphabet: typing.List[str],
) -> typing.Generator[typing.Union[models.StartStep, models.Step], None, None]:
    alphabet_length = len(alphabet)
    while True:
        emission_line = f.readline().strip()
        if emission_line.startswith('//'):
            return

        emission_line = emission_line.split()
        insertion_line = f.readline().strip().split()
        state_switch_line = f.readline().strip().split()

        if emission_line[0] == 'COMPO':
            assert len(emission_line) == alphabet_length + 1, emission_line
            assert len(insertion_line) == alphabet_length, insertion_line
            assert len(state_switch_line) == 7, state_switch_line
            yield models.StartStep(
                p_emission_to_emission=convert_probability(state_switch_line[0]),
                p_emission_to_insertion=convert_probability(state_switch_line[1]),
                p_emission_to_deletion=convert_probability(state_switch_line[2]),
                p_insertion_to_emission=convert_probability(state_switch_line[3]),
                p_insertion_to_insertion=convert_probability(state_switch_line[4]),
                p_deletion_to_emission=convert_probability(state_switch_line[5]),
                p_deletion_to_deletion=convert_probability(state_switch_line[6]),
                p_emission_char=dict(zip(
                    alphabet,
                    [convert_probability(p) for p in emission_line[1:]],
                )),
                p_insertion_char=dict(zip(
                    alphabet,
                    [convert_probability(p) for p in insertion_line],
                )),
            )
        else:
            # TODO: assert next line numbers
            assert len(emission_line) == alphabet_length + 6, emission_line
            assert len(insertion_line) == alphabet_length, insertion_line
            assert len(state_switch_line) == 7, state_switch_line

            yield models.Step(
                p_emission_to_emission=convert_probability(state_switch_line[0]),
                p_emission_to_insertion=convert_probability(state_switch_line[1]),
                p_emission_to_deletion=convert_probability(state_switch_line[2]),
                p_insertion_to_emission=convert_probability(state_switch_line[3]),
                p_insertion_to_insertion=convert_probability(state_switch_line[4]),
                p_deletion_to_emission=convert_probability(state_switch_line[5]),
                p_deletion_to_deletion=convert_probability(state_switch_line[6]),
                p_emission_char=dict(zip(
                    alphabet,
                    [convert_probability(p) for p in emission_line[1:-5]],
                )),
                p_insertion_char=dict(zip(
                    alphabet,
                    [convert_probability(p) for p in insertion_line],
                )),
                alignment_column_index=None if emission_line[-5] == '-' else int(emission_line[-5]),
                consensus_residue_annotation=None if emission_line[-4] == '-' else emission_line[-4],
                reference_annotation=None if emission_line[-3] == '-' else emission_line[-3],
                mask_value=None if emission_line[-2] == '-' else emission_line[-2],
                annotation=None if emission_line[-1] == '-' else emission_line[-1],
            )


def convert_probability(p: str) -> float:
    if p == '*':
        return 0
    else:
        return math.e ** -float(p)
