# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:

import os
import time
import numpy as np
import nibabel as nib

# modules for data preparation
import multiprocessing as mps
import functools

import autoroilib as arlib

base_dir = r'/nfs/h1/workingshop/huanglijie/autoroi'
doc_dir = os.path.join(base_dir, 'doc')
data_dir = os.path.join(base_dir, 'multi-atlas', 'data', 'all')

## read all subjects' SID
#sessid_file = os.path.join(doc_dir, 'sessid')
#sessid = open(sessid_file).readlines()
#sessid = [line.strip() for line in sessid]

## generate mask and probability map
#prob_data, mask_data = arlib.make_prior(sessid, data_dir)
#mask_coords = arlib.get_mask_coord(mask_data, data_dir)
#
## extract features from each subject
#pool = mps.Pool(20)
#result = pool.map(functools.partial(arlib.ext_subj_feature,
#                                    mask_coord=mask_coords,
#                                    out_dir=data_dir, mask_out=False),
#                  sessid)

## merge data and compute similarity matrix
#spatial_ptn = None
#for subj in sessid:
#    temp_data = arlib.get_list_data([subj], data_dir)
#    if not isinstance(spatial_ptn, np.ndarray):
#        spatial_ptn = np.zeros((temp_data.shape[0], len(sessid)))
#        count = 0
#    spatial_ptn[..., count] = temp_data[..., 0]
#    count += 1
#
#print spatial_ptn.shape
#np.savetxt('raw.txt', spatial_ptn, delimiter=',')
#r_mtx = np.corrcoef(spatial_ptn.T)
#print r_mtx.shape
#np.savetxt('r.txt', r_mtx, delimiter=',')

# generate mean z-map for each group
group_file = os.path.join(doc_dir, 'group.csv')
f = open(group_file).readlines()
f.pop(0)
f = [line.strip().split(',') for line in f]
group_info = {}
for line in f:
    if not int(line[1]) in group_info:
        group_info[int(line[1])] = [line[0]]
    else:
        group_info[int(line[1])].append(line[0])
# group stats
for idx in group_info:
    print idx,
    print len(group_info[idx])

## generate mean z-map
#stats_dir = os.path.join(data_dir, 'stats')
#src_dir = r'/nfs/t2/atlas/database'
#for idx in group_info:
#    sess_list = group_info[idx]
#    out_file = os.path.join(stats_dir,
#                            'group_' + str(idx) + '.nii.gz')
#    cmd_str = 'fslmerge -a ' + out_file + ' '
#    for sess in sess_list:
#        temp = os.path.join(src_dir, sess, 'face-object',
#                            'zstat1.nii.gz')
#        cmd_str += temp + ' '
#    os.system(cmd_str)
#    mask_file = os.path.join(data_dir, 'mask.nii.gz')
#    cmd_str = 'fslmaths ' + out_file + ' -mul ' + mask_file + \
#              ' ' + out_file
#    os.system(cmd_str)
#    mean_file = os.path.join(stats_dir,
#                             'group_' + str(idx) + '_mean.nii.gz')
#    cmd_str = 'fslmaths ' + out_file + ' -Tmean ' + mean_file
#    os.system(cmd_str)

# compute the similarity of subjects in each group
for idx in group_info:
    sess_list = group_info[idx]
    if len(sess_list) == 1:
        continue
    spatial_ptn = None
    for subj in sess_list:
        temp_data = arlib.get_list_data([subj], data_dir)
        if not isinstance(spatial_ptn, np.ndarray):
            spatial_ptn = np.zeros((temp_data.shape[0], len(sess_list)))
            count = 0
        spatial_ptn[..., count] = temp_data[..., 0]
        count += 1
    print spatial_ptn.shape
    r_mtx = np.corrcoef(spatial_ptn.T)
    print r_mtx.shape
    np.savetxt('r_' + str(idx) + '.txt', r_mtx, delimiter=',')

