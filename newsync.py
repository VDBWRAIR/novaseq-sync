import sh
import date
import csv
import date
from path import Path
import os


# fails on py3 because map gets drained as a generator
# TODO: we now have three versions of the data. the bcl, the gzipped, and the uncompressed fastqs.
# we should elminate one of those, probably. just delete the gzipped later, probably.
# the advantage of using symlinks is that the symlinks tell us the runpath these originally come from, 
# which is nice. 

def rename_issue_date(rbs, sname, sid, inpath): # -> str
    # (Path, str, int) ->  Path
    id_basename = Path(inpath.basename().replace(sname, str(sid)))
    today = date.today().isoformat().replace('-','_')
    new_basename = "{}_{}".format(id_basename.stripext().stripext(), today)).with_suffix('.fastq')
    return rbs / str(sid) / new_basename

def flatten(*seq):
    return list(itertools.chain.from_iterable(*seq))

def newnames_by_dict(indir, rbs, snames, sids):
 # str : int -> [(Path, Path)]
  def get_zipped(samp):
    # path -> [path]
    return indir.glob(samp + '*') # side-effect :(
  fastq_groups = map(get_zipped, snames) # [[path]]
  new_names = map(rename_issue_date, to_rename, snames, sids) 
  
  # [(Path, path)]
  old_and_new = flatten([ map(lambda f: (f, rename_issue_date(rbs, sname, sid, f)), fastqs) \
        for fastqs, sname, sid in zip(fastq_groups, snames, sids) ]) 
  return old_and_new

def run(indir, rbs, id_lst):
  names_and_ids = list(csv.DictReader(open('id.lst'), delimiter=',')) 
  snames, sids = zip(*names_and_ids.items())
  for sid in sids:
    (rbs / sid).mkdir_p()
  old_and_new = newnames_by_dict(indir, rbs, snames, sids) 
  for old, new in old_and_new:
    sh.gunzip(old)
    os.symlink(old.stripext(), new)
    

#flatten([ map(partial(rename_issue_date, sname, sid), fastqs) \
#      for fastqs, sname, sid in zip(fastq_groups, snames, sids) ])

