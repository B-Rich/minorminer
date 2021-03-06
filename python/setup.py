from setuptools import setup, extension
from setuptools.command.build_ext import build_ext
from Cython.Build import cythonize
import sys
import os

extra_compile_args = {
    'msvc': ['/std:c++latest', '/MT', '/EHsc'],
    'unix': ['-std=c++11', '-Wextra', '-Wno-format-security', '-Ofast', '-fomit-frame-pointer', '-DNDEBUG', '-fno-rtti'],
}

extra_link_args = {
    'msvc': [],
    'unix': ['-std=c++11'],
}


if '--debug' in sys.argv or '-g' in sys.argv or 'CPPDEBUG' in os.environ:
    extra_compile_args['msvc'].append('/DCPPDEBUG')
    extra_compile_args['unix'] = ['-std=c++1y', '-w',
                                  '-O0', '-g', '-fipa-pure-const', '-DCPPDEBUG']


class build_ext_compiler_check(build_ext):
    def build_extensions(self):
        compiler = self.compiler.compiler_type

        compile_args = extra_compile_args[compiler]
        for ext in self.extensions:
            ext.extra_compile_args = compile_args

        link_args = extra_compile_args[compiler]
        for ext in self.extensions:
            ext.extra_compile_args = link_args

        build_ext.build_extensions(self)


class Extension(extension.Extension, object):
    pass


setup(
    name="minorminer",
    description="heuristic algorithm to find graph minor embeddings",
    long_description="minorminer is a tool for finding graph minors, developed to embed Ising problems onto quantum annealers (QA). Where it can be used to find minors in arbitrary graphs, it is particularly geared towards the state of the art in QA: problem graphs of a few to a few hundred variables, and hardware graphs of a few thousand qubits.",
    author="Kelly Boothby",
    author_email="boothby@dwavesys.com",
    url="https://github.com/dwavesystems/minorminer",
    version="0.1.2",
    license="Apache 2.0",
    ext_modules=cythonize(Extension(
        name="minorminer",
        sources=["minorminer.pyx"],
        include_dirs=['.', '../include'],
        language='c++',
    )),
    cmdclass={'build_ext': build_ext_compiler_check}
)
