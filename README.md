# VirtualListCtrl
a simple wxpthon virtual ListCtrl widget designed to work with simple data classes such as the generic and specific ones supplied.  

This objective is to will make it easy to povide, for example a display which displays the first page quickly and allows sorting.

## Included Components

VirtualListCtrl - the widget 
VirtuallListData - a model data store
VirtualListColumn - a class used to define a data column: the heading, alignment and how the column value and text are obtained from the frow
VirtualListObjectData - one object per row data store
VirtualListDirData - Directory data with0 Directory, Name, Extension, Size and Date columns

## How to use

the virtual list control is designed to be used with a data object, which can be one of the classes supplied or your own sub-class of the supplied virtual_list_data class.

The data object needs to be provided with

1) the information necessary to obtain each row.  For example, the VirtualListDirData class requires the path to a directory and will use pathlib.Path.glob to obtain each row as required and the VirtualListObjectData needs to be given an iterator (or rahter a generator) that will supply objects.
2) information on the columns and how  individual values or text is obtained for each column of a given row




1.  instantiate data component.
2.  if necessary, define the data component's columns providing heading, alignment and metods for obtaining data for a given row / column
3.  load the data component with data using the populate method
4.  create the control, specifiying a data component to hold and return the data, the data rows and provide trhe  and link to the data component

   
6.  if using the virtuallistobjectdata class provide functions to in some cases functions to obtain the value from the row object.
7.  populate data component.  , perhaps from a generator
8.  instantiate
9.   and link control and data component
   
  


