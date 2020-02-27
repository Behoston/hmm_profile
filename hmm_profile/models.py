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
    reference_annotation: typing.Optional[bool] = None
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
    statistical_parameters: typing.Optional[typing.List['StatisticalParameter']] = None
    build_command: typing.Optional[str] = None
    search_command: typing.Optional[str] = None


@dataclasses.dataclass
class StatisticalParameter:
    alignment_mode_configuration: str
    score_distribution_name: str
    location: float
    slope: float


@dataclasses.dataclass
class BaseStep:
    p_emission_to_emission: float
    p_emission_to_insertion: float
    p_emission_to_deletion: float
    p_insertion_to_emission: float
    p_insertion_to_insertion: float
    p_deletion_to_emission: float
    p_deletion_to_deletion: float
    p_emission_char: typing.Dict[str, float]
    p_insertion_char: typing.Dict[str, float]


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


@dataclasses.dataclass
class HMM:
    metadata: Metadata
    steps: typing.List[Step]
    start_step: typing.Optional[StartStep] = None
