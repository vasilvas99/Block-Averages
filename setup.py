from setuptools import setup
from Cython.Build import cythonize
from setuptools import setup
from setuptools.command.build_ext import build_ext

link_args = ['-static-libgcc',
             '-static-libstdc++',
             '-Wl,-Bstatic,--whole-archive',
             '-lwinpthread',
             '-Wl,--no-whole-archive']

...  # Add extensions
#aa
class Build(build_ext):
    def build_extensions(self):
        if self.compiler.compiler_type == 'mingw32':
            for e in self.extensions:
                e.extra_link_args = link_args
        super(Build, self).build_extensions()

setup(
    name='Fast Calculations Module',
    ext_modules=cythonize("calc.pyx"),
    zip_safe=False,
    cmdclass={'build_ext': Build},

)

