#!/usr/bin/env python

from dask_jobqueue import SLURMCluster
from dask.distributed import Client


def mycustomfunc(integer):
    import time
    time.sleep(integer)
    with open('~/mynewfile_{0}.txt'.format(integer), 'w') as fhandle:
        fhandle.write(integer + 10)


cluster = SLURMCluster(memory='1 GB', cores=1, walltime=10,
                       job_extra=['--account=rpp-aevans-ab'])
cluster.scale(10)

client = Client(cluster)

a = client.map(mycustomfunc, [1,2,3,4,5,6,7,8,9,10])
