find-maps-with-broken-layers
============================
For shops maintaining a large catalog of map products, if paths to data change for some reason, it can be difficult to keep up with and maintain the layer links to all the data layer sources. This small script can automate the process of broken path discovery.

The script expects one parameter, a parent directory. It will recursively walk down into this directory, locate all map documents, check the integrity of the layers and log any broken layers. If broken layers are discovered, a log file will be written to the parent directory with the maps containing broken layers along with the individual broken layers in each map listed.
