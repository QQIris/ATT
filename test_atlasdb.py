# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 et:1

"Test for atlas extraction and analysis"

from atlasdb_htc import *
import pandas as pd
import random
import os
import time


def random_split_list(raw_list):
    length_list = len(raw_list)
    split_list = random.sample(raw_list,length_list)
    pre_splitlist = split_list[0:length_list/2]
    post_splitlist = split_list[length_list/2:]
    return pre_splitlist,post_splitlist

fpath = os.path.join

time0 = time.time()
# Index files
rawdatapath = '/nfs/j3/userhome/huangtaicheng/workingdir/parcellation_MT/BAA/mergedata/mergedata_mt'

zstat_img_file = fpath(rawdatapath, 'zstat_combined.nii.gz')
mask_img_file = fpath(rawdatapath, 'mt_z5.0.nii.gz')
psc_img_file = fpath(rawdatapath, 'psc_combined.nii.gz')
alff_img_file = fpath(rawdatapath, 'alff_combined.nii.gz')
falff_img_file = fpath(rawdatapath, 'falff_combined.nii.gz')
reho_img_file = fpath(rawdatapath, 'reho_combined.nii.gz')

# roi files
zgf_img_file = fpath(rawdatapath, 'zgf_z5.0.nii.gz')
lzg_img_file = fpath(rawdatapath, 'lzg_z5.0.nii.gz')
htc_img_file = fpath(rawdatapath, 'htc_z5.0.nii.gz')

output_path = '/nfs/t3/workingshop/huangtaicheng/program/ATT/data'

areaname = ['rV3','lV3','rMT','lMT']
areanum = [1,2,3,4]
taskname = 'motion'
contrast = 'motion-fix'
threshold = 5.0
roi_name = dict(zip(areaname, areanum))

pathsex = '/nfs/j3/userhome/huangtaicheng/workingdir/parcellation_MT/doc/dfsf/modeID'
gender = pd.read_csv(os.path.join(pathsex, 'act_sex.csv'))['gender'].tolist()
sessid = open('/nfs/j3/userhome/huangtaicheng/workingdir/parcellation_MT/doc/dfsf/modeID/actID','rU').read().splitlines()

time1 = time.time()
print 'time of initial directory : %d' % (time1 - time0)
#-----------------------------------------------------------------------------#
# Split sessid into two halves
# pre_enum,post_enum = random_split_list(range(len(list(sessid))))
# pre_sessid = list(np.array(sessid)[pre_enum])
# post_sessid = list(np.array(sessid)[post_enum])
# pre_gender = list(np.array(gender)[pre_enum])
# post_gender = list(np.array(gender)[post_enum])
#-----------------------------------------------------------------------------#
# Prepare data
sessn = range(len(sessid))
# zstat
zstat_rawdata = Dataset(zstat_img_file, mask_img_file, areaname, areanum, gender, sessid, taskname, contrast, 'zstat')
zstat_rawdata.loadfile()
# psc
psc_rawdata = Dataset(psc_img_file, mask_img_file, areaname, areanum, gender, sessid, taskname, contrast, 'psc')
psc_rawdata.loadfile()
#alff
alff_rawdata = Dataset(alff_img_file, mask_img_file, areaname, areanum, gender, sessid, taskname, contrast, 'alff')
alff_rawdata.loadfile()
# falff
falff_rawdata = Dataset(falff_img_file, mask_img_file, areaname, areanum, gender, sessid, taskname, contrast, 'falff')
falff_rawdata.loadfile()
# reho
reho_rawdata = Dataset(reho_img_file, mask_img_file, areaname, areanum, gender, sessid, taskname, contrast, 'reho')
reho_rawdata.loadfile()

time2 = time.time()
print 'time of loadfile : %d' % (time2 - time1)

#---------------------------calculate index for whole data---------------------#
atlas_info = AtlasInfo(taskname, contrast, threshold, roi_name, sessid, gender)

adb = AtlasDB(atlas_info.bas)
adb.import_data(zstat_rawdata, 'act', 'zstat')
adb.import_data(zstat_rawdata, 'geo', 'volume')
adb.import_data(zstat_rawdata, 'geo', 'peakcoor')
adb.import_data(psc_rawdata, 'act', 'psc')
adb.import_data(psc_rawdata, 'geo', 'peakcoor')
adb.import_data(alff_rawdata, 'rest', 'alff')
adb.import_data(alff_rawdata, 'geo', 'peakcoor')
adb.import_data(falff_rawdata, 'rest', 'falff')
adb.import_data(falff_rawdata, 'geo', 'peakcoor')
adb.import_data(reho_rawdata, 'rest', 'reho')
adb.import_data(reho_rawdata, 'geo', 'peakcoor')

#adb.save_to_pkl(output_path, 'index_data.pkl')
#adb.save_to_mat(output_path, 'index_data.mat')

#zstat_index = cal_index(zstat_rawdata)
#zstat_index.volume_index()
#zstat_index.mask_index('zstat', 'mean')
#zstat_index.mask_index('zstat', 'max')
#zstat_index.mask_index('zstat', 'min')
#zstat_index.mask_index('zstat', 'std')
#zstat_index.mask_index('zstat', 'skewness')
#zstat_index.mask_index('zstat', 'kurtosis')
#zstat_index.peakcoord_index('zstat')

#psc_index = cal_index(psc_rawdata, sessid, sessn, gender)
#psc_index.mask_index('psc','mean')
#psc_index.mask_index('psc','max')
#psc_index.mask_index('psc','min')
#psc_index.mask_index('psc','std')
#psc_index.mask_index('psc','skewness')
#psc_index.mask_index('psc','kurtosis')
#psc_index.peakcoord_index('psc')



# psc_index.peakcoord_index()

# alff_index = cal_index(alff_rawdata, sessid, sessn, gender)
# alff_index.mask_index('alff')
# alff_index.peakcoord_index()

# falff_index = cal_index(falff_rawdata, sessid, sessn, gender)
# falff_index.mask_index('falff')
# falff_index.peakcoord_index()

# reho_index = cal_index(reho_rawdata, sessid, sessn, gender)
# reho_index.mask_index('reho')
# reho_index.peakcoord_index()

time3 = time.time()
print 'time of calculate index : %d' % (time3 - time2)

#---------------------------calculate PM and MPM------------------------------#
# getprob = make_atlas(zstat_rawdata, sessid, sessn)
# getprob.probatlas()
# getprob.MPM(0.2)


time4 = time.time()
print 'time of calculate probdata and mpmdata : %d' % (time4 - time3)
# --------------------------calculate reliability-----------------------------#
# reliab_hz = reliability(areanum)
# reliab_hz.loadfile(htc_img_file, zgf_img_file)
# reliab_hz.cal_dice()
# reliab_hl = reliability(areanum)
# reliab_hl.loadfile(htc_img_file, lzg_img_file)
# reliab_hl.cal_dice()
# reliab_zl = reliability(areanum)
# reliab_zl.loadfile(zgf_img_file, lzg_img_file)
# reliab_zl.cal_dice()

time5 = time.time()
print 'time of reliability : %d' % (time5 - time4)








