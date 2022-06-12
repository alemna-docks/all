"""Functions that cover low-level formatting for `show` commands, mostly."""
from types import MethodType
import _bigtree.utils
from _bigtree.bigtree import Bigtree
from _bigtree.subtree import Subtree


def msg_no_display_methods_with_args():
    print("(methods that require arguments cannot be displayed and are left blank)")


def show_bigtree_attrs(bigtree: Bigtree, *attr_names: str):
    """Literal formatting showing a `subtree` plus specified properties."""
    print(f"BIGTREE:")
    msg_no_display_methods_with_args()
    attrs: dict = _bigtree.utils.get_attrs(bigtree)
    if len(attr_names) >= 1:
        for property, value in attrs.items():
            if property in attr_names:
                show_kv(property, value)
    else:  # no property names given, so print everything
        for property, value in attrs.items():
            show_kv(property, value)


def show_kv(key, value=None):
    """Literal formatting for showing a key and its value."""
    # some values may be methods, so call them
    if type(value) == MethodType:
        try:
            value = value()
        except TypeError:
            # TypeError is raised if the method requires
            # positional arguments. If this happens, we just
            # keep value as the Method object rather than
            # calling it.
            pass
            value = ""  # "(cannot display, requires arguments)"
    print(f"  {key}: {value}")


def show_subtree_attributes(subtree: Subtree, *attr_names: str):
    """Literal formatting for showing a `subtree` plus specified properties."""
    print(f"SUBTREE: {subtree.name}")
    msg_no_display_methods_with_args()
    attrs: dict = _bigtree.utils.get_attrs(subtree)
    if len(attr_names) >= 1:
        for property, value in attrs.items():
            if property in attr_names:
                show_kv(property, value)
    else:  # no property names given, so print everything
        for property, value in attrs.items():
            show_kv(property, value)
