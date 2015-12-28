import random
from collections import defaultdict
from heapq import nlargest

from luigi import six

import luigi
import luigi.contrib.hadoop
import luigi.contrib.hdfs
import luigi.postgres


class Streams(luigi.Task):
    """
    Used to generate random data for demonstration.
    """
    date = luigi.DateParameter()

    def run(self):
        """
        Writes to :py:meth:`~.Streams.output` target.
        """
        with self.output().open('w') as output:
            for _ in range(1000):
                output.write('{} {} {}\n'.format(
                    random.randint(0, 999),
                    random.randint(0, 999),
                    random.randint(0, 999)))

    def output(self):
        """
        Returns the target output for this task.
        In this case, a successful execution of this task will create a file in the local file system.

        :return: the target output for this task.
        :rtype: object (:py:class:`luigi.target.Target`)
        """
        return luigi.LocalTarget(self.date.strftime('data/streams_%Y_%m_%d_faked.tsv'))

class AggregateArtists(luigi.Task):
    """
    This task runs over the target data returned by :py:meth:`~/.Streams.output` and
    writes the result into its :py:meth:`~.AggregateArtists.output` target (local file).
    """

    date_interval = luigi.DateIntervalParameter()

    def output(self):
        """
        Returns the target output for this task.
        In this case, a successful execution of this task will create a file on the local filesystem.

        :return: the target output for this task.
        :rtype: object (:py:class:`luigi.target.Target`)
        """
        return luigi.LocalTarget("data/artist_streams_{}.tsv".format(self.date_interval))

    def requires(self):
        """
        This task's dependencies:

        * :py:class:`~.Streams`

        :return: list of object (:py:class:`luigi.task.Task`)
        """
        return [Streams(date) for date in self.date_interval]

    def run(self):
        artist_count = defaultdict(int)

        for t in self.input():
            with t.open('r') as in_file:
                for line in in_file:
                    _, artist, track = line.strip().split()
                    artist_count[artist] += 1

        with self.output().open('w') as out_file:
            for artist, count in six.iteritems(artist_count):
                out_file.write('{}\t{}\n'.format(artist, count))

class Top10Artists(luigi.Task):
    """
    This task runs over the target data returned by :py:meth:`~/.AggregateArtists.output` or
    :py:meth:`~/.AggregateArtistsHadoop.output` in case :py:attr:`~/.Top10Artists.use_hadoop` is set and
    writes the result into its :py:meth:`~.Top10Artists.output` target (a file in local filesystem).
    """

    date_interval = luigi.DateIntervalParameter()
    use_hadoop = luigi.BoolParameter()

    def requires(self):
        """
        This task's dependencies:

        * :py:class:`~.AggregateArtists` or
        * :py:class:`~.AggregateArtistsHadoop` if :py:attr:`~/.Top10Artists.use_hadoop` is set.

        :return: object (:py:class:`luigi.task.Task`)
        """
        if self.use_hadoop:
            # Complete a hadoop MR job and output to output target (local file system)
            # For now I'll just pass...
            pass
        else:
            return AggregateArtists(self.date_interval)

    def output(self):
        """
        Returns the target output for this task.
        In this case, a successful execution of this task will create a file on the local filesystem.

        :return: the target output for this task.
        :rtype: object (:py:class:`luigi.target.Target`)
        """
        return luigi.LocalTarget("data/top_artists_%s.tsv" % self.date_interval)

    def run(self):
        top_10 = nlargest(10, self._input_iterator())
        with self.output().open('w') as out_file:
            for streams, artist in top_10:
                out_line = '\t'.join([
                    str(self.date_interval.date_a),
                    str(self.date_interval.date_b),
                    artist,
                    str(streams)
                ])
                out_file.write((out_line + '\n'))

    def _input_iterator(self):
        with self.input().open('r') as in_file:
            for line in in_file:
                artist, streams = line.strip().split()
                yield int(streams), artist

if __name__ == "__main__":
    luigi.run()
