#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import getopt, sys, os
import nbformat
import nbformat.sign
from nbconvert.preprocessors import ExecutePreprocessor
from nbconvert.preprocessors.execute import CellExecutionError
import warnings

STDIO_CODE = u'''
import sys
import tee
sys.stdin = tee.Tee(sys.__stdin__, sys.stdin)
sys.stdout = tee.Tee(sys.__stdout__, sys.stdout)
sys.stderr = tee.Tee(sys.__stderr__, sys.stderr)
del sys.modules['tee']
del tee
'''

def runnb(nb_path, allow_errors=False, no_stdio=False, to_file=None):
    with open(nb_path, 'r') as nb_file:
        nb = nbformat.read(nb_file, nbformat.NO_CONVERT)
    notary = nbformat.sign.NotebookNotary()
    trusted = notary.check_signature(nb)
    if not trusted:
        warnings.warn('The notebook is NOT trusted.', DeprecationWarning)
    ep = ExecutePreprocessor(timeout=-1, allow_errors=allow_errors)
    try:
        if not no_stdio or not nb.metadata.kernelspec.language=='python':
            '''
            cell = nbformat.v4.new_code_cell(source=STDIO_CODE)
            nb.cells.insert(0, cell)
            '''
            for cell in nb.cells:
                if cell.cell_type == 'code':
                    cell.source = STDIO_CODE + cell.source
                    break
        out = ep.preprocess(nb, {'metadata':{'path':os.getcwd()}})
    except CellExecutionError:
        print 'Error executing the notebook "%s".\n\n' % nb_path
        raise
    finally:
        if to_file:
            if not no_stdio or not nb.metadata.kernelspec.language=='python':
                '''
                nb.cells.remove(nb.cells[0])
                '''
                cell.source = cell.source[len(STDIO_CODE):]
            for cell in nb.cells:
                if cell.cell_type == 'code' and cell.outputs:
                    cell.metadata.collapsed = False
                    cell.metadata.autoscroll = 'auto'
            if trusted:
                notary.sign(nb)
            else:
                notary.unsign(nb)
            with open(to_file, mode='wt') as f:
                nbformat.write(nb, f)

'''
def runnb(*args, **kwargs):
    print args, kwargs
'''

def usage():
    print 'Usage:'
    print sys.argv[0], '[options] <path/to/notebook.ipynb>'
    print 'Options:'
    print '-h --help', '\t'*4, 'Display help message.'
    print '-e --allow-error', '\t'*3, 'Allow error during single cell and continue running.'
    print '-n --no-stdio', '\t'*4, 'Don\'t recover STDIO to command line. (You may not see printed messages.)'
    print '-a --allow-not-trusted', '\t'*3, 'Run the notebook even not trusted.'
    print '-t --to=<path/to/notebook.out.ipynb>', '\t'*1, 'Save the executed notebook to a specific file.'

def main():
    warnings.filterwarnings('error', '.*trusted.*', DeprecationWarning, __name__)
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'henat:', ['help', 'allow-error', 'no-stdio', 'allow-not-trusted', 'to='])
        
        allow_errors = False
        no_stdio = False
        allow_not_trusted = False
        to_file = None
        for o, a in opts:
            if o in ("-h", "--help"):
                usage()
                sys.exit()
            elif o in ("-e", "--allow-error"):
                allow_errors = True
            elif o in ("-n", "--no-stdio"):
                no_stdio = True
            elif o in ("-a", "--allow-not-trusted"):
                allow_not_trusted = True
                warnings.filterwarnings('always', '.*trusted.*', DeprecationWarning, __name__)
            elif o in ("-t", "--to"):
                to_file = a
            else:
                raise getopt.GetoptError('Unhandled option: (%s, %s)'%(str(o), str(a)))
                
        if allow_not_trusted and to_file:
            warnings.warn('Allowing not-trusted notebook and saving the not-trusted notebook!', DeprecationWarning)
            
        if not len(args)==1:
            raise getopt.GetoptError('Please specify one and only one notebook.')
        nb_path = args[0]
    except getopt.GetoptError as err:
        # print help information and exit:
        print 'Error:'
        print str(err), '\n'  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
        
    try:
        runnb(nb_path, allow_errors, no_stdio, to_file)
    except DeprecationWarning as err:
        print str(err), 'If you still want to run the not-trusted notebook, try `--allow-not-trusted` option.'

if __name__ == '__main__':
    main()
