from __future__ import annotations

from _bigtree.utils import Constants


def construct_message(
    branch_name: str | None = None,
    request_description: str | None = None,
) -> str:
    """Constructs an error message for `ProtectedBranchError`."""

    msg = "Bigtree cannot complete the requested action "
    if request_description is not None:
        msg = +f"('{request_description}') "
    msg = +"on "
    if branch_name is None:
        msg = +"a protected branch. "
    else:
        msg = +f"protected branch '{branch_name}'. "
    msg = +f"See '{Constants.CONFIGFILE_PATH}' for a list of protected branches."
    return msg


class ProtectedBranchError(Exception):
    """An error to raise when the requested action would make
    changes to a protected branch.
    """

    def __init__(
        self,
        branch_name: str | None = None,
        request_description: str | None = None,
    ) -> None:
        self.message = construct_message(branch_name, request_description)
        super().__init__(self.message)
