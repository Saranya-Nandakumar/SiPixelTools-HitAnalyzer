#!/usr/bin/env python

from DataFormats.FWLite import Events, Handle
#from DataFormats.SiPixelCluster import SiPixelCluster

# 1) open your file
events = Events('file:clus2Morph.root')

# 2) prepare a handle for the clusters
cluster_h = Handle('edmNew::DetSetVector<SiPixelCluster>')
clusterTag = ('hltSiPixelClusters', '', 'TEST')

# 3) loop events
for ievt, ev in enumerate(events):
    ev.getByLabel(clusterTag, cluster_h)
    clusters = cluster_h.product()
    print(f"=== Event {ievt} ===")
    # 4) loop over modules (DetSets)
    for detSet in clusters:
        detId = detSet.id()
#        if(detId != 
        print(f" Module detId = {detId}  ({detSet.size()} clusters)")
        # 5) loop clusters in that module
        for cid,cluster in enumerate(detSet):
#            print(cluster)
           # … after you have a cluster object …
#            first_cluster = next(iter(clusters[0]))  # grab the first cluster of the first module
#            print("SiPixelCluster methods/attributes:")
#            print([m for m in dir(first_cluster) if not m.startswith('_')])


            # each SiPixelCluster knows its own ID:
#            cid = cluster.Id
            # cluster.size() is how many pixels in it
            print(f"   Cluster ID = {cid:3d}   nPixels = {cluster.size():3d}")
            # if you still want the pixels themselves:
            for pix in cluster.pixels():  
                print(f"      row={pix.x:3d}  col={pix.y:3d}")
    if ievt >= 4:
        break

