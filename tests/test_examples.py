from __future__ import print_function

import os
import re
import sys

import pytest
from matplotlib import pyplot
from matplotlib.backends.backend_pdf import PdfPages

package = 'spm1d'

pattern = re.compile('.*\.(py)$')
examples_folder = os.path.join(os.path.dirname(__file__),
                               '..', package, 'examples')

def filelist():
    """ Return a list of example files"""
    matches = []
    for root, dirnames, filenames in os.walk(examples_folder):
        for filename in filter(lambda name:pattern.match(name),filenames):
            matches.append(os.path.realpath(os.path.join(root, filename)))
    return matches


@pytest.fixture(params=filelist())
def example_file(request):
    """ Fixture that ensures test functions are excuted for each example """
    fullfilename = request.param
    return fullfilename

@pytest.yield_fixture(scope='module')
def pyplot_pdf():
    """ Test fixture to allow saving figures to pdf"""
    pdfname = package+'_examples_py{0}.{1}.pdf'.format(*sys.version_info)
    with PdfPages(pdfname) as pdf:
        yield pdf
        d = pdf.infodict()
        d['Title'] = pdfname


def test_examples(example_file, monkeypatch, pyplot_pdf):
    fname = os.path.basename(example_file)

    def save_to_file(*args,**kwargs):
        pyplot.suptitle(fname)
        pyplot_pdf.savefig()
        pyplot.close()
    monkeypatch.setattr(pyplot,'show', save_to_file)


    # Read an compile the example code
    with open(example_file) as f:
        code = compile(f.read(), example_file, 'exec', dont_inherit = True)
    ns = globals()
    ns['__file__'] = example_file
    try:
        exec(code, ns)
    except Exception as e:
        pyplot.figure()
        save_to_file()
        assert False, fname


if __name__ == '__main__':
    print(filelist())