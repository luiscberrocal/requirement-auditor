import re

STABLE_VERSION_REGEX = re.compile(r"^(?P<major>\d+)\.(?P<minor>\d+)\.?(?P<patch>\d)?$")
