import mmap


class DataFormatStream:
    def __init__(self, filename):
        self._filename = filename
        self._formats = []

    def addFormat(self, dataformat):
        if isinstance(dataformat, list):
            for df in dataformat:
                df.updateDateTime()
                self._formats.append(df)
        else:
            dataformat.updateDateTime()
            self._formats.append(dataformat)

    def write(self):
        with open(self._filename, "a") as f:
            # mm = mmap.mmap(f.fileno(), 0)
            for data_format in self._formats:
                f.write(data_format.printData())
                # mm.write(data_format.printData())
            # mm.close()
            f.close()
            self._formats = []

    def clear(self):
        self._formats = []
