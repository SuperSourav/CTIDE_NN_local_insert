import h5py
import numpy as np
import ROOT

ROOT.gStyle.SetOptStat(0)

##====num NN ======##
fwtname = "8bitTOT"
fwt = h5py.File("%s.weights.hdf5"%fwtname, 'r')
dirwt = fwt['model_weights']
l = []
[l.append(dirwt.get('dense_%i'%(i+1))) for i in range(3)]
dW = []
dB = []
[[dW.append(np.array(l[i].get('dense_%i_W'%(i+1)))), dB.append(np.array(l[i].get('dense_%i_b'%(i+1))))] for i in range(3)]

norm = []
fnorm = open("%s.normalization.txt"%fwtname, 'r')
norm.append(np.array(fnorm.readline().split())) #mean
norm.append(np.array(fnorm.readline().split())) #std

##=================##


foutname = "newNN"
fout = ROOT.TFile("%s.root"%foutname, "RECREATE")

t = fout.mkdir("NumberParticles")

t.cd()
hLb = []
[hLb.append(ROOT.TH1D("Layer%i_thresholds"%i, "Layer%i_thresholds"%i, len(dB[i]), 0, len(dB[i]))) for i in range(3)]
[[hLb[i].SetBinContent(j+1, dB[i][j]) for j in range(len(dB[i]))] for i in range(3)]
[hLb[i].Write() for i in range(3)]

hLW = []
[hLW.append(ROOT.TH2D("Layer%i_weights"%i, "Layer%i_weights"%i, len(dW[i]), 0, len(dW[i]), len(dW[i][0]), 0, len(dW[i][0]))) for i in range(3)]
[[[hLW[k].SetBinContent(i+1, j+1, dW[k][i][j]) for j in range(len(dW[k][i]))] for i in range(len(dW[k]))] for k in range(3)]
[hLW[k].Write() for k in range(3)]

hnorm = ROOT.TH2D("InputsInfo", "InputsInfo", len(norm[0]), 0, len(norm[0]), 2, 0, 1)
[[hnorm.SetBinContent(j+1, i+1, float(norm[i][j])) for j in range(len(norm[i]))] for i in range(2)]
hnorm.Write()

hLayer = ROOT.TH1D("LayersInfo", "LayersInfo", 4, 0, 4)
hLayer.SetBinContent(1, len(norm[0]))
[hLayer.SetBinContent(i+2, len(dB[i])) for i in range(3)]
hLayer.Write()

t.Write()
fout.Close()
