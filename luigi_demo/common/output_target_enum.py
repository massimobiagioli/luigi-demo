from enum import Enum


class OutputTargetEnum(str, Enum):
    LOCAL = 'local'
    S3 = 's3'
