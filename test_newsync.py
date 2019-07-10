# sh.gunzip( indir / samp[i] ... gz, outidr / ids[i] . w/date n shit)
from pyfakefs.fake_filesystem_unittest import Patcher
# python3 i think from unittest.mock import patch
from mock import patch
import shutil 
import sh
from path import Path 
from datetime import date
import os
import newsync 
from collections import Counter
from nose.tools import eq_, ok_

ids = [21211 ,21212 ,21213 ,21214 ,21215 ,21216 ,21217 ,21218 ,20054 ,20057 ,20058 ,20063 ,20065 ,20066 ,20067 ]
ids_strs = map(str, ids)
samps =  ['00147BLA001xQ' , '00150BLA001xQ' , '00537BLA001xQ' , '00006BLA004xQ' , '00043BLA001xQ' , '00170BLA006xQ' , '00241BLA001xQ' , '00813BLA008xQ' , '00034BLA003' , '00165BLA002' , '00192BLA001' , '00542BLA001' , '00622BLA001' , '00623BLA001' , '00702BLA00']

samp_ids = dict(zip(ids, samps))
mock_id_lst = 'IssueID,SampleName\n' + '\n'.join(map(','.join, zip(ids_strs, samps)))
import random
import string

def rand_string(size):
   return ''.join([random.choice(string.ascii_letters + string.digits) for n in range(size)])
# using context manager for the belw instead
# @patch("sh.gunzip", create=True,  side_effect=fake_gunzip)
#def big_test(sh_gunzip):
def big_test():
    indir =  Path('/foo/indir/')
    rbs =   Path('/bar/outdir')
    with Patcher() as patcher:
        # access the fake_filesystem object via patcher.fs
        # # # Setup fake files 
        in_sheet = Path('/usr/input/id.lst')
        patcher.fs.create_file(in_sheet, contents=mock_id_lst)
        patcher.fs.create_dir(indir)
        patcher.fs.create_dir(rbs)
        # add some random dirs to rbs
        
        patcher.fs.create_dir(rbs / 'prentendoldsample')
        old_rbs_dirs = os.listdir(rbs)
        ftypes = ['R2', 'I1', 'R1', 'I2']
        for samp in samps:
          junk = 'junkstring'
          def make(ftype):
             fn = indir / '{0}_{1}_{2}.fastq.gz'.format(samp, ftype, junk) 
             patcher.fs.create_file(fn, contents=rand_string(100))
          for f in ftypes: make(f) 

        # # # Run
        #def fake_gunzip(inpath, **kwargs):
            #assert kwargs.keys == ['_out']
        def fake_gunzip(inpath):
            contents = open(inpath).read() + '\nunzipped!'
            assert inpath.endswith('.gz')
            patcher.fs.create_file(inpath.rstrip('.gz'), contents=contents)
            
        with patch('sh.gunzip', create=True, side_effect=fake_gunzip):
            newsync.run(indir,rbs, in_sheet)
        
            # # # Assertions
            new_dirs = Counter(os.listdir(rbs))  - Counter(old_rbs_dirs) 
            eq_(new_dirs, Counter(ids_strs))
            print os.listdir(indir)
            print os.listdir(rbs)
            today = date.today().isoformat().replace('-','_')
            for id, samp in samp_ids.items():
               expected = map(lambda x: '{0}_{1}_{2}_{3}.fastq'.format(id, x, junk, today), ftypes)
               print os.listdir(rbs / str(id))
               for ftype, exp in zip(ftypes, expected):
                   fp = rbs / str(id) / exp
                   ok_(os.path.exists(fp), msg=fp +' not exist')
                   exp_contents = open(indir / '{0}_{1}_{2}.fastq.gz'.format(samp, ftype, junk)).read() + '\nunzipped!'
                   eq_(open(fp).read(), exp_contents)
       
    # duplicate dirs are impossible anyway, but still using Counter
def rename_issue_date_test():
  from newsync import rename_issue_date    
  name = '00001BLA001_S17_L002_I1_001.fastq.gz'
  today = date.today().isoformat().replace('-','_')
  id_ = 2415
  p = rename_issue_date(Path('/rbs'),'00001BLA001', id_,  Path(name))
  eq_(p, Path('/rbs/{id}/{id}_S17_L002_I1_001_{date}.fastq'.format(id=id_,date=today)))

