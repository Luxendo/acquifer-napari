"""
This module is an example of a barebones numpy reader plugin for napari.

It implements the ``napari_get_reader`` hook specification, (to create
a reader plugin) but your plugin may choose to implement any of the hook
specifications offered by napari.
see: https://napari.org/docs/dev/plugins/hook_specifications.html

Replace code below accordingly.  For complete documentation see:
https://napari.org/docs/dev/plugins/for_plugin_developers.html
"""
from napari_plugin_engine import napari_hook_implementation
from dask_image.imread import imread
from sortedcontainers import SortedSet
import napari
import os
import numpy as np
import dask.array as da
import xarray as xr


# Function extracted for the MetadataParser, put here for convenience
def getWellId(imageName):
	"""Extract well Id (ex:A001) from the imageName (for IM4)."""
	return imageName[1:5]

def getZSlice(imageName):
	"""Return image slice number of the associated Z-Stack serie."""
	return int(imageName[27:30])

def getChannelIndex(imageName):
	"""
	Return integer index of the image channel.
	
	1 = DAPI (385)
	3 = FITC (GFP...)
	5 = TRITC (mCherry...)
	"""
	return int(imageName[22:23])

def getTimepoint(imageName):
	"""Return the integer index corresponding to the image timepoint."""
	return int(imageName[15:18])


DataArray = xr.core.dataarray.DataArray # this is just a type-alias used in function signature (shorter than the full thing)

def array_from_directory(directory: str) -> DataArray:
    """
    Create a 6-dimensional xarray backed by a Dask array from an IM directory.  
    
    The dask array uses lazy-loading for computation and visualization of the images.
    The dimensions order is as following channel-well-time-z.
    
    The xarray allows to label the dimensions, and the value along the dimensions (well names, channels...) 
    """
    listFiles = os.listdir(directory)
    listFiles = [file for file in listFiles if file.endswith(".tif")]
    
    # Find unique well, and CZT in this dataset
    # Sorted since we use those sets for ordering of the image in the nD-array
    setChannels = SortedSet()
    setWells    = SortedSet()
    setT        = SortedSet()
    setZ        = SortedSet()
    
    for filename in listFiles:
        setChannels.add( getChannelIndex(filename) )
        setWells.add( getWellId(filename) )
        setT.add( getTimepoint(filename) )
        setZ.add( getZSlice(filename) )
    
    # Create an empty numpy array of shape [nC][nWells][nT][nZ]
    shape = (len(setChannels),
             len(setWells),
             len(setT),
             len(setZ))
    
    filepathArray = np.empty(shape, dtype=object) # dont use dtype str here
    
    # Fill the numpy array with the image filepaths
    # the positional indexes are recovered from the position of the matching dimension value in the sorted sets
    for filename in listFiles:
        
        imageC    = getChannelIndex(filename)
        imageWell = getWellId(filename)
        imageT    = getTimepoint(filename)
        imageZ    = getZSlice(filename) 
        
        # Fill the numpy array using the positional index as stored in the sets
        filepathArray[setChannels.index(imageC)] \
                     [setWells.index(imageWell)] \
                     [setT.index(imageT)] \
                     [setZ.index(imageZ)]  = os.path.join(directory, filename)
    
    
    # Turn the nD-numpy array to a nD-Dask array
    # The nD dask array is made by first reading each image into a single plane dask array
    # and by then stacking each dask array for each dimensions
    listChannels = []
    for channel in filepathArray:
        
        listWells = []
        for well in channel:
            
            listTime = []
            for timepoint in well:
                
                listZ = []
                for zSlice in timepoint:
                    listZ.append( imread(zSlice) )
                
                listTime.append( da.concatenate(listZ) ) # here use concatenate not stack since we extend the 3rd dimension, we dont want to add another dimension
            
            # Turn listTime into a stacked dask array and append to upper level list
            listWells.append(da.stack(listTime))
            
        listChannels.append(da.stack(listWells))
    
    mainArray = da.stack(listChannels)
    
    return xr.DataArray(mainArray, 
                        dims=["Channel", "Well", "Time", "Z", "Y", "X"],
                        coords={"Channel": setChannels, # define discrete values available on this dimension
                                "Well":    setWells,
                                "Time" :   setT,
                                "Z":       setZ} )

@napari_hook_implementation
def napari_get_reader(path):
    """This function is responsible for providing a suitable viewer function, depending on what file, directory is selected.

    Parameters
    ----------
    path : str
        Path to an IM dataset directory.

    Returns
    -------
    function or None
        If the path is a directory, return the reader function. Otherwise (list of path to files, or directories), return None.
    """
    if not isinstance(path, str):
        return None # our reader except a single path to a directory only
    
    if not os.path.isdir(path):
        return None

    # otherwise we return the *function* that can read ``path``.
    return reader_function


def reader_function(path):
    """Take a path to an IM dataset, and return a list of LayerData tuples.

    Readers are expected to return data as a list of tuples, where each tuple
    is (data, [add_kwargs, [layer_type]]), "add_kwargs" and "layer_type" are
    both optional.

    Parameters
    ----------
    path : path to an IM directory.

    Returns
    -------
    layer_data : list of tuples
        A list of LayerData tuples where each tuple in the list contains
        (data, metadata, layer_type), where data is a numpy array, metadata is
        a dict of keyword arguments for the corresponding viewer.add_* method
        in napari, and layer_type is a lower-case string naming the type of layer.
        Both "meta", and "layer_type" are optional. napari will default to
        layer_type=="image" if not provided
    """
    array6D = array_from_directory(path)
    
    DEFAULT_CHANNEL_COLORS = ["cyan", "green","yellow", "red", "magenta", "gray"] # ordered from CO1 to CO6
    
    listNames     = [] # as shown in left channel-panel in napari, default Cx with x in [1,6]
    listColormaps = [] # color map/LUT for the channels
    listOpacities = [] # default opacities (1 for BF, 0.5 for Fluo to hava good blend)
    
    for channel in array6D["Channel"].values:
        listNames.append( "C" + str(channel) )
        listColormaps.append( DEFAULT_CHANNEL_COLORS[channel-1] ) # channel-1 since IM-channels are 1-based while positional-indexes are 0-base
        listOpacities.append( 1 if channel==6 else 0.5)
    
    metadata = {"channel_axis" : 0,
                "name"     : listNames,
                "colormap" : listColormaps,
                "opacity"  : listOpacities
                }
    
    return [ (array6D, metadata ) ]