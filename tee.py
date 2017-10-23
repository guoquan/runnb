class Tee:
    def __init__(self, *files):
        self._files = files

    def __del__(self):
        # don't kill them here!
        '''
        if self._file1 != sys.stdout and self._file1 != sys.stderr:
            self.file1.close()
        if self._file2 != sys.stdout and self._file2 != sys.stderr:
            self.file2.close()
        '''

    def write(self, string):
        for file in self._files:
            file.write(string)

    def flush(self):
        for file in self._files:
            file.flush()