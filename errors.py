"""Error type for invalid input. main() reports it and exits with status 2."""


class WbgenError(Exception):
    pass


def fail(msg):
    raise WbgenError(msg)
