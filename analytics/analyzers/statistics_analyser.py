import os


class StatisticsAnalyser:
    def __init__(self, dataformat, analyze_algorithm):
        self._dataformat = dataformat
        self._analyser = analyze_algorithm

    def parse(self, collect_dir, logfile, log_data=None):
        parsed_log = []
        if os.path.exists(logfile) or self._dataformat is not None:
            with open(logfile, 'r') as f:
                for line in f:
                    parsed_log.append(self._dataformat.parseData(line))
                f.close()
        stat_data = {
            'data': parsed_log,
            'logfile': logfile,
            'logdata': log_data,
            'collection_dir': collect_dir
        }
        if self._analyser is not None:
            self._analyser.apply(stat_data)
