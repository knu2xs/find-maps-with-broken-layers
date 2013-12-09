"""
Purpose:    List all the map documents under a parent directory, check for broken data links and log the results to a
            logfile saved in the parent directory.
Author:     Joel McCune (http://joelmccune.com)
DOB:        25 Nov 2013
"""
__author__ = 'Joel McCune ('

# import modules
import arcpy
import os
import logging
import datetime
import sys


def get_maps(parent_directory):
    """
    @rtype : iterator of strings with the full path to all map documents under the parent directory
    @param parent_directory: the parent directory to iteratively crawl or walk into and find all map documents
    """
    # walk the parent directory
    for parent_dir, child_dir_list, child_obj_list in os.walk(parent_directory):

        # for every child object in the parent directory
        for child_obj in child_obj_list:

            # concatenate the parent directory and the child object to get the full path
            full_path = os.path.join(parent_dir, child_obj)

            # filter out only map documents
            if child_obj.endswith('.mxd'):

                # return the full path to the map document
                yield full_path


def find_broken_layers(mapPath):
    """
    @param mapPath: string with full path to map document
    @return: list of broken layers, if any, in the specified map document
    """
    # create map object instance
    mapdoc = arcpy.mapping.MapDocument(mapPath)

    # create a list of broken map layers
    return arcpy.mapping.ListBrokenDataSources(mapdoc)


def get_report(parent_directory):
    """
    @param parent_directory: the top level directory path where the script should start from to find all map documents
    @return: formatted string of map documents with broken layers and the specific layers broken
    """
    # broken flag
    broken = False

    # start string for report
    mxdString = 'Documents with broken layers found\n'

    # for every map under the parent directory
    for mxd in get_maps(parent_directory):

        # find any broken layers in the map document
        broken_layers = find_broken_layers(mxd)

        # if there are broken layers
        if broken_layers:

            # set flag to true
            broken = True

            # add the map name to the string
            mxdString = mxdString + '\n{0}\n'.format(mxd)

            # for every broken layer in the map
            for layer in broken_layers:

                # add the broken layer to the output report
                mxdString = mxdString + '\t{0}\n'.format(layer.name)

    # if broken layers found
    if broken:
        return mxdString


def create_output_report(parent_dir):
    """
    @param parent_dir: top level directory to crawl and find broken map documents below
    @return: does not return any values, but does write log file to top level directory if broken map layers are found
    """
    # get report
    report = get_report(parent_dir)

    # if broken layers reported
    if report:

        # create logfile in parent directory
        timestamp = datetime.date.today().__format__('%Y%m%d')
        logging.basicConfig(filename=os.path.join(parent_dir, 'brokenLayers_{0}.log'.format(timestamp)))
        logging.warning(report)


# if run directly
if __name__ == '__main__':

    # get top level directory to crawl for broken map documents as parameter
    parent_directory = sys.argv[1]

    # call method to find and report broken map layers
    create_output_report(parent_directory)