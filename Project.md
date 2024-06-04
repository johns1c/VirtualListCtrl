# This Project

Provides a simple generic wx.Python virtual list control which will work with a data component.  The data components will have a standardised interface inherited from a template data component class that is provided.  A number of sample data components will also be provided to handle file directories, sqlite3 queries and iterations of objects.

# The wxPython Virtual List Control

like a standard list control has rows and columns and allows scrolling, selecting etc  
but

only knows (but can be assigned)

* how many items
* which items selected
* which item focus

can be assigned

* column headers
* column sort indicators
* array of images (i.e. options ) which can be displayed on a row

it needs to ask or determine

* text to be displayed in given row column
* which image to be displayed on a given row
* attributes such as colour and font for a given row
* sort ordering
* whether display needs refreshing (e.g. after data sorted or updated)

the asking needs to be placed in functions with following names

## Sorting

easier with a virtual control since it does not involve mixins, setting row data etc. Another advantage is that the rows can easily be sorted based on the underlying data rather than its text representation, for example allowing file sizes to be displayed as 200Kb or 3.4Gb whilst allowing sorting of that column.

generally code in **OnColumnClick** handler will

* read and set the column sort indicator
* tell the data object to sort by the given column
* refresh the display

it may also need to

* handle selections
* ensure that the currently focused item is still in view
* handle text attributes.

in a generic implementation of a virtual list control it is useful to have the data component provide the

* default sort order
* column heading
* column width

for each column to be displayed.

This can then be provided when the virtual list control is instantiated

## Selections

selections may need handling to

* get a list of data items that are selected rather than the row numbers
* ensure that the selection is correct after sorting

as far as I can see there are two approaches

1. communicate with the data component each time a row is selected and retrieve this information when required including after sorting.
2. communicate with the data component only when we need to obtain the underling data for the selection or sort it.

## Focus

this is mainly of concern when sorting as we need to ensure that list control's focus is reset to the correct row and that row is visible within the display.

## Other attributes

if attributes such as highlighting or greying out need to move with the data then this needs to be delegated to the data component. One approach would be for the data component to record tags against the rows and the list control determine the appropriate formatting (perhaps with a helper function). An alternative would be for the data component provide the attributes directly.

Row Images are

## Special first row etc.

An example of this would be the "parent directory" row in a file listing. How this is handled is likely be implementation dependent and as such might be better delegated to the data component.

Some lists have special rows which are not really associated with detail data.

## Naming Conventions

wxPython classes and attributes have a CapWords convention that differs from the Python Standard. This convention is not mandatory for the data component and standard Python conventions make it easier to reuse a specific data component under different frameworks.

VirtualListCtrl : The virtual list control with column setting and sorting

VirtualListData : The template for a (read only) Virtual List Control Data Component

VirtualListFileData : A directory list Data Component

VirtualListObjectData : An object based Data Component

VirtualListDBData : A data base query Data Component

## Column Attributes

The most common attributes are those which can be used in the **InsertColumn** call

1. heading
2. alignment (left, right, centre)
3. width( pixels or LIST\_AUTOSIZE\_USEHEADER to fit the column width to heading or to extend to fill all the remaining space for the last column or LIST\_AUTOSIZE which will set the default column width)

An alternative is to use the InsertColumn call to use an image

.

**4.** `LIST_MASK_IMAGE` in the item mask.

## VirtualListObjectData : An object based Data Component

  
No need to inherit from this class - just instantiate it, tell it what the the columns are and how to get the objects.  Instantiate the VirtualListControl and connect to the data.


## VirtualListDirData : file directory data

A directory listing showing file name, extension, size, date and location.  

Just instantiate this class passing the directory as a pathlib.Path object and pass to the VirtualListControl to get file sorting, selecting etc.     




  a column value  from 

  

Needs to be supplied with

  

  

* the virtual list control that will display the object
* a generator which iterate through the objects, returning each one in turn

  

for each desired column

  

1. name
2. width
3. alignment
4. whether it is sortable
5. the sort order that will be applied the first time it is sorted
6. function that return the value of the column from the object (for sorting)
7. function that will return the formatted text from the  object (for display)

  

for example for a directory list giving name, size etc

  

generator is  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

rows  
columns

each row can have  
image  
attributes

1. have to set number of items
2. have to provide data
