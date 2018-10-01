#converting /afs/cern.ch/atlas/conditions/poolcond/vol0/cond09_mc.000087.gen.COND/cond09_mc.000087.gen.COND._0004.pool.root 
#to a file without GUID and notrack branches to be tried on 
#https://twiki.cern.ch/twiki/bin/viewauth/AtlasProtected/ClusteringAndTrackingInDenseEnvironmentsUpdatingNNConditions

import ROOT, re
f = ROOT.TFile("cond09_mc.000087.gen.COND._0004.pool.root")
f.ls()
nextkey = ROOT.TIter(f.GetListOfKeys())
key = ROOT.TKey()
key = nextkey()
fout = ROOT.TFile("newNN.root", 'RECREATE')
while (key.GetTitle() != "object title"):
  dirname = key.GetTitle()
  print ">>> ", dirname
  if (re.search("NoTrack", dirname)): 
    key = nextkey()
    continue
  fout.mkdir(dirname)
  fout.cd(dirname)
  odir = f.Get(dirname)
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
f.Close()
