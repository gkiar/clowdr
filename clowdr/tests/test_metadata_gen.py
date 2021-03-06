#!/usr/bin/env python

from unittest import TestCase
import os.path as op
import json
import os

from clowdr import __file__ as cfile
from clowdr.controller import metadata


class TestMetadataGen(TestCase):

    cdir = op.abspath(op.join(op.dirname(cfile), op.pardir))
    descriptor = op.join(cdir, "examples/bids-example/descriptor_d.json")
    invocation1 = op.join(cdir, "examples/bids-example/invocation.json")
    invocation2 = op.join(cdir, "examples/bids-example/invocation_ses.json")
    invocation3 = op.join(cdir, "examples/bids-example/"
                                "invocation_ses_nopart.json")
    invocation4 = op.join(cdir, "examples/bids-example/invocs/")
    invocation5 = op.join(cdir, "examples/bids-example/invocation_sweep.json")
    provdir = op.join(cdir, "examples/bids-example/task/")
    dataloc1 = "localhost"
    dataloc2 = "s3://mybucket/path/"

    def test_metadata_single_invoc(self):
        [tasks, invocs] = metadata.consolidateTask(self.descriptor,
                                                   self.invocation1,
                                                   self.provdir,
                                                   self.dataloc1,
                                                   verbose=True,
                                                   bids=False)
        self.assertTrue(len(tasks) == len(invocs) == 1)

        [tasks, invocs] = metadata.consolidateTask(self.descriptor,
                                                   self.invocation1,
                                                   self.provdir,
                                                   self.dataloc1,
                                                   verbose=True,
                                                   bids=True)
        with open(self.invocation1) as f:
            participants = len(json.load(f)["participant_label"])
        self.assertTrue(len(tasks) == len(invocs) == participants)

        [tasks, invocs] = metadata.consolidateTask(self.descriptor,
                                                   self.invocation2,
                                                   self.provdir,
                                                   self.dataloc1,
                                                   verbose=True,
                                                   bids=True)
        with open(self.invocation2) as f:
            dat = json.load(f)
            total = len(dat["participant_label"]) * len(dat["session_label"])
        self.assertTrue(len(tasks) == len(invocs) == total)

        [tasks, invocs] = metadata.consolidateTask(self.descriptor,
                                                   self.invocation3,
                                                   self.provdir,
                                                   self.dataloc1,
                                                   verbose=True,
                                                   bids=True)
        with open(self.invocation3) as f:
            dat = json.load(f)
            total = len(dat["session_label"])
        self.assertTrue(len(tasks) == len(invocs) == total)

    def test_metadata_directory_invocs(self):
        [tasks, invocs] = metadata.consolidateTask(self.descriptor,
                                                   self.invocation4,
                                                   self.provdir,
                                                   self.dataloc1,
                                                   verbose=True,
                                                   bids=False)
        self.assertTrue(len(tasks) == len(invocs) and
                        len(tasks) == len(os.listdir(self.invocation4)))

    def test_metadata_sweep(self):
        [tasks, invocs] = metadata.consolidateTask(self.descriptor,
                                                   self.invocation5,
                                                   self.provdir,
                                                   self.dataloc1,
                                                   verbose=True,
                                                   sweep=["participant_label",
                                                          "analysis_level"],
                                                   setup=True)

        with open(self.invocation5) as fhandle:
            dat = json.load(fhandle)
            total = len(dat["participant_label"]) * len(dat["analysis_level"])
        self.assertTrue(len(tasks) == len(invocs) == total)

    def test_metadata_to_remote(self):
        [tasks, invocs] = metadata.consolidateTask(self.descriptor,
                                                   self.invocation1,
                                                   self.provdir,
                                                   self.dataloc2,
                                                   verbose=True,
                                                   bids=False)

        metadata.prepareForRemote(tasks, self.provdir, self.dataloc2)
