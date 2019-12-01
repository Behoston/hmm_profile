import dataclasses
import enum
import typing


class AlphabetType(enum.Enum):
    # bio
    amino = 'amino'
    DNA = 'DNA'
    RNA = 'RNA'
    # other
    coins = 'coins'
    dice = 'dice'
    custom = 'custom'


@dataclasses.dataclass
class Metadata:
    version_identifier: str
    model_name: str
    length: int
    alphabet_type: AlphabetType
    alphabet: typing.List[str]
    consensus_residue_annotation: bool

    accession_number: typing.Optional[str] = None
    description: typing.Optional[str] = None
    max_instance_length: typing.Optional[int] = None
    reference_annotation: typing.Optional[str] = None
    model_masked: bool = False
    consensus_structure_annotation: bool = False
    map_annotation: bool = False
    date: typing.Optional[str] = None
    command_line_log: typing.Optional[typing.List[str]] = None
    sequence_number: typing.Optional[int] = None
    effective_sequence_number: typing.Optional[float] = None
    checksum: typing.Optional[int] = None
    gathering_threshold: typing.Optional[typing.Tuple[float, float]] = None
    trusted_cutoff: typing.Optional[typing.Tuple[float, float]] = None
    noise_cutoff: typing.Optional[typing.Tuple[float, float]] = None
    statistical_parameters: typing.Optional[typing.List[typing.Tuple[str, str, float, float]]] = None
    build_command: typing.Optional[str] = None
    search_command: typing.Optional[str] = None


@dataclasses.dataclass
class BaseStep:
    p_emission_to_emission: float
    p_emission_to_insertion: float
    p_emission_to_deletion: float
    p_insertion_to_emission: float
    p_insertion_to_insertion: float
    p_deletion_to_emission: float
    p_deletion_to_deletion: float
    p_emission_char: typing.List[float]
    p_insertion_char: typing.List[float]


@dataclasses.dataclass
class Step(BaseStep):
    alignment_column_index: typing.Optional[int] = None
    consensus_residue_annotation: typing.Optional[str] = None
    reference_annotation: typing.Optional[str] = None
    mask_value: typing.Optional[str] = None
    annotation: typing.Optional[str] = None


@dataclasses.dataclass
class StartStep(BaseStep):
    pass


class HMM:
    def __init__(self, metadata: Metadata, steps: typing.List[Step], start_step: typing.Optional[StartStep] = None):
        self.metadata = metadata
        self.start_step = start_step
        self.steps = steps

    def check_equal_states(self, minimum_equality: float, how_many_min_chars: int = 2) -> int:
        result = 0
        for step in self.steps:
            if sum([p >= minimum_equality for p in step.p_emission_char]) >= how_many_min_chars:
                result += 1
        return result
