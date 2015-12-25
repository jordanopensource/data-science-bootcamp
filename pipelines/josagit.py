import random
from collections import defaultdict
from heapq import nlargest

from luigi import six

import luigi
import luigi.postgres

import urllib2
import StringIO
import gzip
import json

class GetArchive(luigi.Task):
    """
    Get the archive unit from github
    """
    def run(self):
        """
        Download the main archive data from the data.githubarchive.org
        """

        baseURL = "http://data.githubarchive.org/2015-01-01-15.json.gz"
        outpath = "github.json"

        response = urllib2.urlopen(baseURL)
        compressedFile = StringIO.StringIO()
        compressedFile.write(response.read())
        compressedFile.seek(0)

        decompressedFile = gzip.GzipFile(fileobj=compressedFile, mode='rb')

        with open(outpath, 'w+') as outfile:
            outfile.write(decompressedFile.read())

    def output(self):
        """
        Returns the target output for this task.
        In this case, a successful execution of this task will create a file in the local file system.

        :return: the target output for this task.
        :rtype: object (:py:class:`luigi.target.Target`)
        """
        return luigi.LocalTarget('github.json')

class AggregateLanguages(luigi.Task):
    """
    Loops over all josn entries
    get all "PullRequestEvent" from the dump
    json parse to get the language
    increment coutner for each language.
    output new file with lang -> count
    Output on log to prep for Hadoop
    """

    def output(self):
        """
        Returns the target output for this task.
        In this case, a successful execution of this task will create a file on the local filesystem.

        :return: the target output for this task.
        :rtype: object (:py:class:`luigi.target.Target`)
        """
        return luigi.LocalTarget("cleaned-data/aggregated-languages.json")

    def requires(self):
        """
        This task's dependencies:
        * :py:class:`~.GetArchive`
        :return: list of object (:py:class:`luigi.task.Task`)
        """
        return [GetArchive()]

    def run(self):
        language_count = defaultdict(int)

        for t in self.input():
            with t.open('r') as in_file:
                for line in in_file:
                    values = json.loads(line)
                    if values['type'] == "PullRequestEvent":
                        try:
                            language = values['payload']['pull_request']['head']['repo']['language']
                            language_count[language] += 1
                        except:
                            pass

        with self.output().open('w') as out_file:
            for language, count in six.iteritems(language_count):
                out_file.write('{}\t{}\n'.format(language, count))


class histogram(luigi.Task):
    """
    Get the count of each event available
    """

    def output(self):
        """
        Returns the target output for this task.
        In this case, a successful execution of this task will create a file on the local filesystem.

        :return: the target output for this task.
        :rtype: object (:py:class:`luigi.target.Target`)
        """
        return luigi.LocalTarget("cleaned-data/histogram.json")

    def requires(self):
        """
        This task's dependencies:
        * :py:class:`~.GetArchive`
        :return: list of object (:py:class:`luigi.task.Task`)
        """
        return [GetArchive()]

    def run(self):
        event_count = defaultdict(int)

        for t in self.input():
            with t.open('r') as in_file:
                for line in in_file:
                    values = json.loads(line)
                    try:
                        event_type = values['type']
                        event_count[event_type] += 1
                    except:
                        pass

        with self.output().open('w') as out_file:
            for event_type, count in six.iteritems(event_count):
                out_file.write('{}\t{}\n'.format(event_type, count))


if __name__ == "__main__":
    luigi.run()
