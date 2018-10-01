# Creating the DB file with the local CTIDE neural network

cd /eos/user/s/sosen/LOCALTESTATHENA/localNN

#copy a legit conditional db (COOL db) trained CTIDE NN
cp /afs/cern.ch/atlas/conditions/poolcond/vol0/cond09_mc.000087.gen.COND/cond09_mc.000087.gen.COND._0004.pool.root .

#initializing github repo
setupATLAS
lsetup git
git init
echo "# Creating the DB file with the local CTIDE neural network" >> README.md
git add README.md
git commit -m "first commit"
git remote add origin https://github.com/SuperSourav/CTIDE_NN_local_insert.git
git push -u origin master

#get and run the copier.py script to create dummy local CTIDE NN from cond db CTIDE NN by just removing (not copying) the db id
cp ../newNetwork/copier.py .
python copier.py

#check if the local CTIDE NN has the correct branches
asetup Athena, 21.0.34
python
Python 2.7.13 (default, Apr 22 2017, 20:06:00) 
[GCC 6.2.0] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> import ROOT
Warning in <TInterpreter::ReadRootmapFile>: class  UCharDbArray found in libRootCnvDict.so  is already in libStorageSvcDict.so 
>>> f = ROOT.TFile("newNN.root")
>>> f.ls()
TFile**        newNN.root    
 TFile*        newNN.root    
  KEY: TDirectoryFile    NumberParticles;1    NumberParticles
  KEY: TDirectoryFile    ImpactPoints1P;1    ImpactPoints1P
  KEY: TDirectoryFile    ImpactPoints2P;1    ImpactPoints2P
  KEY: TDirectoryFile    ImpactPoints3P;1    ImpactPoints3P
  KEY: TDirectoryFile    ImpactPointErrorsX1;1    ImpactPointErrorsX1
  KEY: TDirectoryFile    ImpactPointErrorsX2;1    ImpactPointErrorsX2
  KEY: TDirectoryFile    ImpactPointErrorsX3;1    ImpactPointErrorsX3
  KEY: TDirectoryFile    ImpactPointErrorsY1;1    ImpactPointErrorsY1
  KEY: TDirectoryFile    ImpactPointErrorsY2;1    ImpactPointErrorsY2
  KEY: TDirectoryFile    ImpactPointErrorsY3;1    ImpactPointErrorsY3
>>> 

# add the copier script to git
git add copier.py
git commit -m "script to copy CTIDE NN branch minus the GUID to create dummy local CTIDE NN"
git push -u origin master

#adding a GUID (cond db id) to the dummy CTIDE NN (GUID as a 'ROOT.TObjString')
coolHist_setFileIdentifier.sh newNN.root
Generated GUID is 5B2B52B4-8392-4B79-99C2-337C8E2CC51D
Warning in <TInterpreter::ReadRootmapFile>: class  UCharDbArray found in libRootCnvDict.so  is already in libStorageSvcDict.so 
   ------------------------------------------------------------
  | Welcome to ROOT 6.08/06                http://root.cern.ch |
  |                               (c) 1995-2016, The ROOT Team |
  | Built for linuxx8664gcc                                    |
  | From tag v6-08-06, 2 March 2017                            |
  | Try '.help', '.demo', '.license', '.credits', '.quit'/'.q' |
   ------------------------------------------------------------

root [0] 
Processing /tmp/coolHist_setFileIdentifier_4598.C("newNN.root","5B2B52B4-8392-4B79-99C2-337C8E2CC51D")...
Record GUID 5B2B52B4-8392-4B79-99C2-337C8E2CC51D in file newNN.root
TFile**        newNN.root    
 TFile*        newNN.root    
  KEY: TDirectoryFile    NumberParticles;1    NumberParticles
  KEY: TDirectoryFile    ImpactPoints1P;1    ImpactPoints1P
  KEY: TDirectoryFile    ImpactPoints2P;1    ImpactPoints2P
  KEY: TDirectoryFile    ImpactPoints3P;1    ImpactPoints3P
  KEY: TDirectoryFile    ImpactPointErrorsX1;1    ImpactPointErrorsX1
  KEY: TDirectoryFile    ImpactPointErrorsX2;1    ImpactPointErrorsX2
  KEY: TDirectoryFile    ImpactPointErrorsX3;1    ImpactPointErrorsX3
  KEY: TDirectoryFile    ImpactPointErrorsY1;1    ImpactPointErrorsY1
  KEY: TDirectoryFile    ImpactPointErrorsY2;1    ImpactPointErrorsY2
  KEY: TDirectoryFile    ImpactPointErrorsY3;1    ImpactPointErrorsY3
  KEY: TObjString    fileGUID;1    object title

#make a local copy of the POOL catalog
cp /cvmfs/atlas-condb.cern.ch/repo/conditions/poolcond/PoolFileCatalog.xml .

#the original CTIDE NN file is in the POOL catalog (just sanity check that this is a correct POOL catalog)
grep cond09_mc.000087.gen.COND._0004.pool.root PoolFileCatalog.xml
    <pfn filetype="ROOT_All" name="/cvmfs/atlas-condb.cern.ch/repo/conditions/cond09/cond09_mc.000087.gen.COND/cond09_mc.000087.gen.COND._0004.pool.root"/>
    <lfn name="cond09_mc.000087.gen.COND._0004.pool.root"/>


# Insert the file into the POOL catalogue
coolHist_insertFileToCatalog.py newNN.root
#check if inserted
grep newNN.root PoolFileCatalog.xml
      <pfn filetype="ROOT_All" name="newNN.root"/>
#physical file name (pfn) added to the catalog, but logical file name (lfn) not there yet! moving on

#PATH VARIABLE set to CERN POOL data by Athena from where the POOL catalog was copied here
echo $ATLAS_POOLCOND_PATH
/cvmfs/atlas-condb.cern.ch/repo/conditions

#Now as we are going to work with a local POOL catalog, reset the PATH VARIABLE set to CERN POOL data to the $PWD
export ATLAS_POOLCOND_PATH=$PWD
#check if the path set correctly
echo $ATLAS_POOLCOND_PATH
/eos/user/s/sosen/LOCALTESTATHENA/localNN

#create new local conditions DB (use AtlCoolCopy instead of AtlCoolCopy.exe (obsolete))
$ AtlCoolCopy "COOLOFL_PIXEL/OFLP200" "sqlite://X;schema=newpixelNNdb.db;dbname=OFLP200" -f /PIXEL/PixelClustering/PixelClusNNCalib -nd -rdo -c
Using machine hostname lxplus062.cern.ch for DB replica resolution
Frontier server at (serverurl=http://atlasfrontier-local.cern.ch:8000/atlr)(serverurl=http://atlasfrontier-ai.cern.ch:8000/atlr)(serverurl=http://lcgft-atlas.gridpp.rl.ac.uk:3128/frontierATLAS)(serverurl=http://ccfrontier.in2p3.fr:23128/ccin2p3-AtlasFrontier)(proxyurl=http://ca-proxy.cern.ch:3128)(proxyurl=http://ca-proxy-meyrin.cern.ch:3128)(proxyurl=http://ca-proxy-wigner.cern.ch:3128)(proxyurl=http://atlasbpfrontier.cern.ch:3127)(proxyurl=http://atlasbpfrontier.fnal.gov:3127) will be considered
Total of 10 servers found for host lxplus062.cern.ch
Open source database: COOLOFL_PIXEL/OFLP200
Allowed replica to try (priority -700) : frontier://ATLF/()/ATLAS_COOLOFL_PIXEL
Allowed replica to try (priority -699) : oracle://ATLAS_COOLPROD/ATLAS_COOLOFL_PIXEL
Allowed replica to try (priority -200) : frontier://ATLF/()/ATLAS_COOLOFL_PIXEL
Open destination database: sqlite://X;schema=newpixelNNdb.db;dbname=OFLP200
COOL exception caught: The database does not exist
Try to create new conditions DB
Creation succeeded
Add folders in path:/PIXEL/PixelClustering/PixelClusNNCalib [ /PIXEL/PixelClustering/PixelClusNNCalib ]
Creating folder /PIXEL/PixelClustering/PixelClusNNCalib payload-type 0 on destination
Created 1 new channels for /PIXEL/PixelClustering/PixelClusNNCalib

# Write data on local conditional db
$ coolHist_setReference.py 'sqlite://X;schema=newpixelNNdb.db;dbname=OFLP200' /PIXEL/PixelClustering/PixelClusNNCalib 1 PixClusNNCalib-XX-YY-ZZ newNN.root 
Warning in <TInterpreter::ReadRootmapFile>: class  UCharDbArray found in libRootCnvDict.so  is already in libStorageSvcDict.so 
>== Data valid for run,LB [ 0 , 0 ] to [ 2147483647 , 4294967294 ]
>== Inserting reference to file: newNN.root  - find GUID
Warning in <TInterpreter::ReadRootmapFile>: class  UCharDbArray found in libRootCnvDict.so  is already in libStorageSvcDict.so 
   ------------------------------------------------------------
  | Welcome to ROOT 6.08/06                http://root.cern.ch |
  |                               (c) 1995-2016, The ROOT Team |
  | Built for linuxx8664gcc                                    |
  | From tag v6-08-06, 2 March 2017                            |
  | Try '.help', '.demo', '.license', '.credits', '.quit'/'.q' |
   ------------------------------------------------------------

root [0] 
Processing /tmp/coolHist_extractFileIdentifier_26165.C("newNN.root")...
Get GUID from file newNN.root
GUID is 5B2B52B4-8392-4B79-99C2-337C8E2CC51D

>== Write data on COOL connection: sqlite://X;schema=newpixelNNdb.db;dbname=OFLP200
>== To folder: /PIXEL/PixelClustering/PixelClusNNCalib channel: 1
>== COOL tag: PixClusNNCalib-XX-YY-ZZ
>== Store object with IOV [ 0 , 9223372036854775807 ] channel 1 and tag PixClusNNCalib-XX-YY-ZZ
