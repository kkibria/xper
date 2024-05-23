import argparse
import sys
import re
from pathlib import Path
from warnings import warn
from xper.add_alpha import color2RGB
from xper.walk import walk

def do_xper(srcdir, dstdir, color, force, **kwargs):
    xper = color2RGB(color)

    # create destination dir
    dstpath = Path(dstdir)
    srcpath = Path(srcdir)

    if dstpath.samefile(srcpath):
        raise argparse.ArgumentTypeError("src and dst can't be same")

    dstpath.mkdir(parents=True, exist_ok=force)
    walk(xper, dstpath, srcpath)

def iscolor(arg_value):
    pat=re.compile(r"^([0-9a-fA-F]{2}){3}$")
    if not pat.match(arg_value):
        raise argparse.ArgumentTypeError("invalid value")
    return arg_value

def issrc(arg_value):
    obj = Path(arg_value)
    if not obj.exists():
        raise argparse.ArgumentTypeError("does not exist")
    return arg_value

def main():
    params = {"app": "xper"}

    parser = argparse.ArgumentParser(
        prog=params["app"],
        description='Creates python command file',
        epilog=f'python -m {params["app"]}')

    parser.add_argument('-s', '--srcdir', type=issrc, required=True)
    parser.add_argument('-d', '--dstdir', required=True)
    parser.add_argument('-c', '--color', type=iscolor, required=True, help="RGB value in 6 hex digits, ex. AB140C")
    parser.add_argument('-f', '--force', default=False,
                    action='store_true')

    args = parser.parse_args()
    params = params | vars(args)

    set_warnigs_hook()
    try:
        do_xper(**params)
    except Exception as e:
        print(f'{e.__class__.__name__}:', *e.args)
        return 1
    
    return 0

def set_warnigs_hook():
    import sys
    import warnings
    def on_warn(message, category, filename, lineno, file=None, line=None):
        print(f'Warning: {message}', file=sys.stderr)
    warnings.showwarning = on_warn

if __name__ == '__main__':
    sys.exit(main())
