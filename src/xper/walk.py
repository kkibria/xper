from pathlib import Path
import re
from xper.add_alpha import convertImage

def walk(xper, dstpath:Path, srcpath:Path):
    pat=re.compile(r"^\.(jpg|jpeg|png)$")
    for fpath in srcpath.iterdir():
        if fpath.is_dir():
            ch_srcpath = srcpath.joinpath(fpath.name)
            ch_dstpath = dstpath.joinpath(fpath.name)
            ch_dstpath.mkdir(parents=True, exist_ok=True)
            walk(xper, ch_dstpath, ch_srcpath)
        else:
            if pat.match(fpath.suffix):
                outpath = dstpath.joinpath(fpath.stem + ".png")
                print(f'{fpath} -> {outpath}')
                convertImage(fpath, xper, outpath)
