from argparse import ArgumentError


class IncompatibleArgumentError(ArgumentError):
    def __init__(self, incompatible, *incompatibles) -> None:
        _message = f"The {incompatible} argument is incompatible with the "
        if len(incompatibles) == 1:
            _message += f"argument {incompatibles}."
        elif len(incompatibles) == 2:
            _message += f"arguments {incompatibles[0]} and {incompatibles[-1]}."
        elif len(incompatibles) >= 3:
            _message += (
                f"arguments {', '.join(incompatibles[0:-1])}, and {incompatibles[-1]}."
            )
        else:
            raise ValueError(
                "Somebody tried to raise an error saying that the "
                + f"argument {incompatible} is incompatible with one or"
                + " more other arguments, but they did not specify which "
                + f"arguments {incompatible} is incompatible with."
            )

        super().__init__(argument=None, message=_message)
