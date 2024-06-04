#!/usr/bin/python
import wx
import attr
import logging
from dataclasses import dataclass
from typing import Optional
from typing import Callable
import pathlib
import Icons
import time


class VirtualListCtrl(wx.ListCtrl):
    """Generic Virtual List Control - designed to work with a standard data component"""

    def __init__(
        self,
        parent,
        ID=wx.ID_ANY,
        pos=wx.DefaultPosition,
        size=wx.DefaultSize,
        style=wx.LC_REPORT | wx.LC_VIRTUAL | wx.LC_HRULES | wx.LC_VRULES,
        datasource=None,
    ):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)

        self.datasource = None
        self.columns = []
        self.il = wx.ImageList(16, 16)

        if datasource is not None:
            self.SetDatasource(datasource)

        self.Bind(wx.EVT_LIST_CACHE_HINT, self.CheckCache)
        self.Bind(wx.EVT_LIST_COL_CLICK, self.OnSort)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.OnItemDeselected)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnItemDoubleClick)
        self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.OnItemRightClick)

    def GetDatasource(self):
        """obtain the connected data object"""
        return self.datasource

    def SetDatasource(self, datasource):
        """connect the control to the data
        and set up the columns to match.  it does Not get data
        """

        self.datasource = datasource

        self.ClearAll()
        self.ShowColumns()

        try:
            self.datasource.set_widget(self)
        except AttributeError:
            print(f"Datasource has no set_widget function")
            pass

        # this does not work because the GetCountPerPage is the current number not the number that will fit
        try:
            self.datasource.batch_size = max(
                self.GetCountPerPage() + 1, self.datasource.batch_size
            )
            print(
                f"Datasource batch size set to {self.datasource.batch_size} (widget has {self.CountPerPage} "
            )
        except AttributeError:
            print(f"Datasource batch size not set to match control")
            pass

    def CheckCache(self, event):
        self.datasource.ensure_populated(event.GetCacheFrom(), event.GetCacheTo())

    def OnGetItemText(self, item, col):
        if self.datasource.finished and (
            self.datasource.get_count() != self.GetItemCount()
        ):
            self.SetItemCount(self.datasource.get_count())

        return self.datasource.get_item(item, self.columns[col])

    def OnGetItemAttr(self, item):
        if item < self.datasource.get_count():
            return self.datasource.get_item_state(item)

    def OnGetItemImage(self, item):
        return self.datasource.get_item_image(item)

    def OnSort(self, event):
        # ideally sorting should
        #    retain selection
        #    retain focus
        #    display the focused item at the same page position  as it was before the sort
        #    or perhaps the top item

        selected = self.GetSelectedItemCount()
        self.datasource.set_tag(self.GetFocusedItem(), "current")
        current_page_position = self.GetFocusedItem() - self.GetTopItem()
        self.datasource.sort(self.columns[event.Column])

        self.DeleteAllItems()
        self.UpdateCount()
        self.Refresh()

        scount = 0
        for item in self.datasource.tagged_items("selected"):
            self.Select(item)
            scount += 1

        print(f"restoring selection for  {scount} items")

        scount = 0

        for item in self.datasource.tagged_items("current"):
            current_item = item
            self.datasource.remove_tag(item, "current")
            scount += 1

        print(f"restoring focus  for  {item} items {scount} ")

        new_top = item - current_page_position
        new_top = 0 if new_top < 0 else new_top
        new_bot = new_top + self.GetCountPerPage() - 1
        self.EnsureVisible(new_bot)
        self.Focus(item)

    def UpdateCount(self):
        self.SetItemCount(self.datasource.get_count())

    def OnItemDeselected(self, event):
        trigger_item = event.GetIndex()
        state = self.datasource.remove_tag(trigger_item, "selected")

    def OnItemSelected(self, event):
        trigger_item = event.GetIndex()
        state = self.datasource.set_tag(trigger_item, "selected")

    def SelectAll(self, event):
        ix = 0
        while True:
            self.Select(ix)
            if ix >= self.GetItemCount():
                break
            ix += 1

    def OnItemDoubleClick(self, event):
        ...

    def OnItemRightClick(self, event):
        ...

    def Populate(self):
        self.datasource.MakeImgList(self.il)
        self.SetImageList(self.il, IMAGE_LIST_SMALL)

        r = self.datasource.get_count()
        print(f"Data source starting with {r} rows ")
        self.SetItemCount(r + 1)
        self.ShowColumns()

    def ShowColumns(self):
        for col, colinfo in enumerate(self.datasource.get_columns()):
            self.InsertColumn(col, colinfo.heading, colinfo.format, colinfo.width)
            self.columns.append(colinfo.heading)

    def ShowAvailableColumns(self, evt):
        colMenu = Menu()

        self.id2item = {}

        # for idx, (text, visible) in enumerate(self.datasource.columns):
        for idx, text in enumerate(self.datasource.columns):
            id = NewId()
            visible = True

            self.id2item[id] = (idx, visible, text)

            item = MenuItem(colMenu, id, text, kind=ITEM_CHECK)
            colMenu.AppendItem(item)

            EVT_MENU(colMenu, id, self.ColumnToggle)

            item.Check(visible)

        Frame(self, -1).PopupMenu(colMenu)

        colMenu.Destroy()

    def ColumnToggle(self, evt):
        toggled = self.id2item[evt.GetId()]

        if toggled[1]:
            idx = self.columns.index(toggled[2])

            self.datasource.columns[toggled[0]] = (
                self.datasource.columns[toggled[0]][0],
                False,
            )

            self.DeleteColumn(idx)

            self.columns.pop(idx)

        else:
            self.datasource.columns[toggled[0]] = (
                self.datasource.columns[toggled[0]][0],
                True,
            )

            idx = self.datasource.GetColumnHeaders().index((toggled[2], True))

            self.columns.insert(idx, toggled[2])

            self.InsertColumn(idx, toggled[2], width=-2)

        self.datasource.SaveColumns()


@dataclass
class VirtualListColumn:
    """Column Atrributes of the data supporting a virtual list control
    the last two function are used to return column values
    from the row object for display and sorting.

    the object also supplies convienience functions to obtain
    columns from a list
    """

    def get_list_column_text(thing, column):
        """standard getter where can be used where the row
        object is subscrptable
        """
        return str(thing[column])

    def get_list_column(thing, column):
        """standard getter where can be used where the row
        object is subscrptable
        """
        return thing[column]

    ASC = True
    DESC = False

    heading: str
    format: int
    width: int
    sort_direction: Optional[int] = None
    first_direction: int = ASC
    get_text: Callable = get_list_column_text
    get_value: Callable = get_list_column


class VirtualListData:

    """
    cached data made up of a list of objects with attributes to be displayed
    as rows and columns.  Generally populated from an iterator

    """

    batch_size: int = 10

    def __init__(self):
        ...

    def clear(self):
        """removes all rows"""
        ...

    def append(self, thing):
        """manually add a row to the data"""
        raise NotImplementedError

    def populate(self, iterator):
        """supplies an iterator which will populate the datasource
        maybe this should be called set_generator or extend (cf a list)

        normally this will
        *   use the next function to obtain a batch of rows
        *   update the display widget's row count beyond the first batch to ensure
            that we can scroll forward
        *   keep a note of the generator so we can obtain further rows when required

        """
        raise NotImplementedError

    def sort(self, column_index: int):
        """sort the items"""

        raise NotImplementedError

    def get_count(self) -> int:
        """total number of data items stored so far"""
        ...

    def get_item(self, row_index: int, column_index: int):
        """retrieve text data associated with given row / column
            used to supply information to the list ctrl OnGetItemText
        OnGetItemText
        OnGetItemImage ,
        OnGetItemColumnImage ,
        OnGetItemColumnAttr
        OnGetItemIsChecked
        """
        print("get_item")

    def get_item_image(self, row_index: int) -> int:
        """returns an index into a list of images"""
        return -1

    def is_populated(self) -> bool:
        """does the datasource contain all the items"""
        raise NotImplementedError

    def ensure_populated(self, from_ix, to_ix):
        """ensures that the object has retrieved data
        for the given range of rows - normally means
        that we have iterated to get to_ix
        """
        if to_ix < self.get_count():
            return
        else:
            raise NotImplementedError



