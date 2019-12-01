import math
import pathlib
import typing

from hmm_profile import models


def save_many_to_file(
        hmms: typing.List[models.HMM],
        output: typing.Union[pathlib.Path, str],
) -> typing.Union[pathlib.Path, str]:
    with open(output, 'w') as f:
        for hmm in hmms:
            f.writelines(get_lines(hmm))
    return output


def save_to_file(hmm: models.HMM, output: typing.Union[pathlib.Path, str]) -> typing.Union[pathlib.Path, str]:
    with open(output, 'w') as f:
        f.writelines(get_lines(hmm))
    return output


def get_lines(hmm: models.HMM) -> typing.Generator[str, None, None]:
    yield from metadata_lines(hmm.metadata)
    yield from model_headers()
    if hmm.start_step is not None:
        yield from compo_lines(hmm.start_step)
    for i, step in enumerate(hmm.steps, start=1):
        yield from step_lines(i, step)
    yield from last_line()


def metadata_lines(metadata: models.Metadata) -> typing.Generator[str, None, None]:  # noqa: C901
    yield f'{metadata.version_identifier}\n'
    yield f'NAME  {metadata.model_name}\n'
    if metadata.accession_number is not None:
        yield f'ACC   {metadata.accession_number}\n'
    if metadata.description is not None:
        yield f'DESC  {metadata.description}\n'
    yield f'LENG  {metadata.length}\n'
    yield f'ALPH  {metadata.alphabet_type.value}\n'
    if metadata.reference_annotation is not None:
        yield f'RF    {metadata.reference_annotation}\n'
    if metadata.model_masked is not None:
        yield f'MM    {bool_to_str(metadata.model_masked)}\n'
    yield f'CONS  {bool_to_str(metadata.consensus_residue_annotation)}\n'
    if metadata.consensus_structure_annotation is not None:
        yield f'CS    {bool_to_str(metadata.consensus_structure_annotation)}\n'
    if metadata.map_annotation is not None:
        yield f'MAP   {bool_to_str(metadata.map_annotation)}\n'
    if metadata.date is not None:
        yield f'DATE  {metadata.date}\n'
    if metadata.sequence_number is not None:
        yield f'NSEQ  {metadata.sequence_number}\n'
    if metadata.effective_sequence_number is not None:
        yield f'EFFN  {metadata.effective_sequence_number}\n'
    if metadata.checksum is not None:
        yield f'CKSUM {metadata.checksum}\n'
    if metadata.gathering_threshold:
        a, b = metadata.gathering_threshold
        yield f'GA    {a:.2f} {b:.2f};\n'
    if metadata.trusted_cutoff:
        a, b = metadata.trusted_cutoff
        yield f'TC    {a:.2f} {b:.2f};\n'
    if metadata.noise_cutoff:
        a, b = metadata.noise_cutoff
        yield f'NC    {a:.2f} {b:.2f};\n'
    # TODO:
    # yield f'BM    \n'
    # yield f'SM    \n'
    # yield f'STATS \n'
    # yield f'STATS \n'
    # yield f'STATS \n'


def model_headers() -> typing.Generator[str, None, None]:
    yield ('HMM          A        C        D        E        F        G        H        I        K        '
           'L        M        N        P        Q        R        S        T        V        W        Y\n')
    yield '            m->m     m->i     m->d     i->m     i->i     d->m     d->d\n'


def compo_lines(start_step: models.StartStep) -> typing.Generator[str, None, None]:
    state_switch_values = ''.join([
        float_to_str(convert_probability(start_step.p_emission_to_emission)),
        float_to_str(convert_probability(start_step.p_emission_to_insertion)),
        float_to_str(convert_probability(start_step.p_emission_to_deletion)),
        float_to_str(convert_probability(start_step.p_insertion_to_emission)),
        float_to_str(convert_probability(start_step.p_insertion_to_insertion)),
        float_to_str(convert_probability(start_step.p_deletion_to_emission)),
        float_to_str(convert_probability(start_step.p_deletion_to_deletion)),
    ])
    insertion_values = ''.join([float_to_str(convert_probability(x)) for x in start_step.p_insertion_char])
    emission_values = ''.join([float_to_str(convert_probability(x)) for x in start_step.p_emission_char])
    yield f'  COMPO {emission_values}\n'
    yield f'        {insertion_values}\n'
    yield f'        {state_switch_values}\n'


def step_lines(line_number: int, step: models.Step) -> typing.Generator[str, None, None]:
    state_switch_values = ''.join([
        float_to_str(convert_probability(step.p_emission_to_emission)),
        float_to_str(convert_probability(step.p_emission_to_insertion)),
        float_to_str(convert_probability(step.p_emission_to_deletion)),
        float_to_str(convert_probability(step.p_insertion_to_emission)),
        float_to_str(convert_probability(step.p_insertion_to_insertion)),
        float_to_str(convert_probability(step.p_deletion_to_emission)),
        float_to_str(convert_probability(step.p_deletion_to_deletion)),
    ])
    emission_values = ''.join([float_to_str(convert_probability(x)) for x in step.p_emission_char])
    insertion_values = ''.join([float_to_str(convert_probability(x)) for x in step.p_insertion_char])
    yield f'{line_number:>7} {emission_values}\n'
    yield '        {}\n'.format(insertion_values)
    yield '        {}\n'.format(state_switch_values)


def float_to_str(number: typing.Union[float, str]) -> str:
    if isinstance(number, str):
        return f'{number:>9}'
    else:
        # dirty hack, to prevent negative zero...
        number += 0
        return f'{number:>9.5f}'


def convert_probability(p: float) -> typing.Union[str, float]:
    if p == 0:
        return '*'
    else:
        return -math.log(p)


def last_line() -> typing.Generator[str, None, None]:
    yield '//\n'


def bool_to_str(value: bool) -> str:
    return 'yes' if value else 'no'
