#!/usr/bin/env python

from DataFormats.FWLite import Events, Handle

# 1) open your file
events = Events('file:clus2Morph.root')

# 2) prepare a handle for the clusters
cluster_h = Handle('edmNew::DetSetVector<SiPixelCluster>')
clusterTag = ('siPixelClusters', '', 'ClusTest')

# 3) loop events
for ievt, ev in enumerate(events):
    ev.getByLabel(clusterTag, cluster_h)
    clusters = cluster_h.product()
    print(f"=== Event {ievt} ===")

    # 4) loop over modules (DetSets)
    for detSet in clusters:
        detId = detSet.id()
        print(f" Module detId = {detId}  ({detSet.size()} clusters)")

        # 5) loop clusters in that module
        for cid, cluster in enumerate(detSet):
            print(f"   Cluster ID = {cid:3d}   nPixels = {cluster.size():3d}")

            # 6) optionally, print individual pixels
            for pix in cluster.pixels():
                print(f"      row={pix.x:3d}  col={pix.y:3d}")

    # stop after 5 events
    if ievt >= 4:
        break

