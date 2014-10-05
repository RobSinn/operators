import os
import glob
modules = glob.glob(os.path.dirname(__file__)+"/*.py")
#modules += glob.glob(os.path.dirname('operators')+"/*.so")
__all__ = [ os.path.basename(f)[:-3] for f in modules]


