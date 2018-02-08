#!/usr/bin/env python
# -*- coding: utf-8 -*-


# All the imports done here
import csv


class UnicodeDictWriter(csv.DictWriter, object):
    """
    Extend csv.DictWriter to handle Unicode input
    https://github.com/python/cpython/blob/7bd5a75bbe28219d3fc18a239c2c554d1850abcb/Lib/csv.py#L131
    """

    def writerow(self, row):
        # super(UnicodeDictWriter, self).writerow({
        #     k: (v.encode('utf-8') if isinstance(v, 'utf-8') else v) for k, v in row.items()
        # })
        return self.writer.writerow(self._dict_to_list(row))

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)
