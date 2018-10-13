#converting /afs/cern.ch/atlas/conditions/poolcond/vol0/cond09_mc.000087.gen.COND/cond09_mc.000087.gen.COND._0004.pool.root 
#to a file without GUID and notrack branches to be tried on 
#https://twiki.cern.ch/twiki/bin/viewauth/AtlasProtected/ClusteringAndTrackingInDenseEnvironmentsUpdatingNNConditions

import ROOT, re
import h52root
fdummy = ROOT.TFile("cond09_mc.000087.gen.COND._0004.pool.root")
fdummy.ls()
nextkey = ROOT.TIter(fdummy.GetListOfKeys())
key = ROOT.TKey()
key = nextkey()
fout = ROOT.TFile("newNN.root", 'RECREATE')
while (key.GetTitle() != "object title"):
  dirname = key.GetTitle()
  print ">>> ", dirname
  if (re.search("NoTrack", dirname)): 
    key = nextkey()
    continue

  if (dirname == "NumberParticles"):
    fwtname = "8bitTOT"
    print "fetching numNN from standalone CTIDENN %s"%fwtname
    h52root.numNN(fout, fwtname)
    key = nextkey()
    continue

  fout.mkdir(dirname)
  fout.cd(dirname)
  odir = fdummy.Get(dirname)
  keydir = ROOT.TKey()
  nextkeydir = ROOT.TIter(odir.GetListOfKeys())
  keydir = nextkeydir()
  print ">>> ", dirname
  while(keydir):
    fname = keydir.GetTitle()
    h = odir.Get(fname)
    print h
    h.Write()
    print fname
    keydir = nextkeydir()  
  key = nextkey()
  fout.cd()
fdummy.Close()
