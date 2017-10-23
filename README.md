# runnb.py - The run-notebook script

`runnb.py` is a script to run `jupyter` notebooks from the command-line.
It is a [`nbconvert`](http://nbconvert.readthedocs.io) API wrapper.
Notes on executing notebooks can be found [here](http://nbconvert.readthedocs.io/en/latest/execute_api.html).
You may also want to see the format specification of `jupyter` notebooks [`nbformat`](http://nbformat.readthedocs.io).

Current version of `runnb.py` is implemented and tested under `python 2` and `jupyter 4.3.0`.

## Usage
```bash
runnb.py [options] <path/to/notebook.ipynb>
```

## Options
* -h --help                               Display help message.
* -e --allow-error                        Allow error during single cell and continue running.
* -n --no-stdio                           Don't recover STDIO to command line. (You may not see printed messages.)
* -a --allow-not-trusted                  Run the notebook even not trusted.
* -t --to=&lt;path/to/notebook.out.ipynb&gt;   Save the executed notebook to a specific file.

## Examples

Assume we have a notebook `test.ipynb`.
Simply run the notebook from command-line:
```bash
runnb.py test.ipynb
```

If we want to run the notebook not being break by possible error in some cell, pass the `--allow-error` flag:
```bash
runnb.py --allow-error test.ipynb
```
Or do it with the shortcut `-e`:
```bash
runnb.py -e test.ipynb
```

If we wanted to export the executed notebook, use `--to`:
```bash
runnb.py --to=test.out.ipynb test.ipynb
```
or using its shortcut `-t`:
```bash
runnb.py --ttest.out.ipynb test.ipynb
```

By default, we recover the output of notebook to the command-line by boardcasting the `input`/`output`/`error` stream. This is done by adding a small snippet of code handling `sys.stdin`, `sys.stdout`, and `sys.stderr`. A tiny `Tee` Class is used to support such behavior. Make sure `tee.py` is in our python search path. If doing this is not preferable in certain scenario, we can turn it off by passing `--no-stdio` flag:
```bash
runnb.py --no-stdio test.ipynb
```
or using its shortcut `-n`:
```bash
runnb.py -n test.ipynb
```
However, this could mean we may not see output from the execution on the command-line. It could be a good idea to save those outputs to a output notebook by using `--to` flag:
```bash
runnb.py --no-stdio --to test.out.ipynb test.ipynb
```

The most (no exaggeration) dangerous thing we can try here is to run a *not trusted* notebook. By default, running a not-trusted notebook leads to a `DeprecationWarning` that stop it from running. However, if one insists to, we can pass `--allow-not-trusted` flag to allow running.
```bash
runnb.py --allow-not-trusted not_trusted.ipynb
```
Deprecation message will be displayed but it would not block running. The executed not-trusted notebook could also be saved by using `--to`. We will unsign the outcome of not-trusted notebook and mark it not trusted. However, the best practice is do not run not trusted notebooks. At least we should review the notebook first, and sign it trusted if it is safe. Make sure we understand what is happenning and what we are doing.

## Lib usage
`runnb(nb_path, allow_errors=False, no_stdio=False, to_file=None)`

Run a notebook from current path.

Parameters:
* `nb_path` (`str`) - path to a notebook.
* `allow_errors` (`bool`) - Wheither to allow error during single cell and continue running. When set to `True`, the notebook will continue running following cells if error presents in some cell.  Default `False`.
* `no_stdio` (`bool`) - Wheither to stop recovering STDIO to default. When set to `True`, default STDIO (usually command-line) will not be recovered. Results can be found only in the output notebook. Default `False`.
* `to_file` (`str`) - Path to which file the executed notebook will be saved to. The notebook will not be save if set to `None` or empty string. Default `None`.

Raises:
* `DeprecationWarning` - Raise if the notebook is not trusted and the warning is not filtered with `warnings` module.

## TODO
* Implement `setup.py` to allow installing.
