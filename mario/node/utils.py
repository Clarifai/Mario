from typing import NamedTuple


def _get_argparse_source(argspec: NamedTuple) -> str:
    ln = []
    ln.append("import argparse")
    ln.append("parser = argparse.ArgumentParser()")

    for arg in argspec.args:
        assert (
            arg in argspec.annotations
        ), f"Arg {arg} is not annotated. All entrypoint args should be annotated kwargs."

    for arg, typ in argspec.annotations.items():
        if hasattr(typ, "__origin__"):
            if typ.__origin__ in (list, tuple):
                nargs = "'+'"
                typ = typ.__args__[0]
            else:
                raise TypeError(
                    f"Only List and Tuple supported but get {arg} as {typ}."
                )
        else:
            nargs = None

        type_name = typ.__name__ if hasattr(typ, "__name__") else None
        ln.append(f"parser.add_argument('--{arg}', type={type_name}, nargs={nargs})")
    ln.append("kwargs = vars(parser.parse_args())")

    return "\n".join(ln)
