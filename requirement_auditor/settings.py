import re

STABLE_VERSION_REGEX = re.compile(r"^(?P<major>\d+)\.(?P<minor>\d+)\.?(?P<patch>\d)?$")
FULLY_PINNED_REGEX = re.compile(r"^(?P<name>[\w_\-]+)==(?P<version>[\w.\-]+)\s*(?P<comment>#.*)?$")
