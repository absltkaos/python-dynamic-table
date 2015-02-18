# vim:set et ts=2 sw=2:
"""
-- module:: dynamic_table
   :synopsis: Library for building, and rendering data in tables of different types

============
Introduction
============
This module provides a way to build/create, and print tables.  So you can 
Create a text table, add rows, and then print them in a human readable text
format.  It also supports html and csv renderers.  So if you build a text
table you can print it in html or csv format.

[NOTE] This was written quickly, but could use some additional features such
as:
 * Ability to change text justifcation for text and html tables by column
 * Ability to change the background cell color for html tables
 * Ability to print an html table in html5 supported ways with inline css etc...

 In other words... this is heavily a work in progress

The interface to dynamic table is pretty straight forward and all of the parameters
passed to the general functions, such as:
 * add_row
 * set_table_type
 * set_col_widths
 * set_col_names
 * set_table_renderer

If you want to write the table to a file instead of stdout (the default) you have
to do so when instantiating the Table class.  Like so:
 my_file=open('/path/to/file','rw')
 my_table=Table(output=my_file)

Doing this will ensure that any print functions get written to the file instead of
stdout.

You can also modify this behavior by defining output as 'String' and then 
the print functions will build the table in the variable "built_buffer", this does
not get cleared automatically. When done with the data, call the function empty_output().
[NOTE] This way of doing this is deprecated in favor of calling str(Table). However still
useful if building adhoc tables I guess.
For example with adhoc table:
 my_table=Table(output='String')
 my_table.set_col_names(['Col1','Col2'])
 my_table.print_header()
 my_table.print_row(['a','b'])
 my_table.print_row(['c','d'])
 table_text=my_table.built_buffer
 my_table.empty_output()

Example of rendering the table to a string:
 my_table=Table()
 my_table.set_col_names(['Col1','Col2'])
 my_table.add_row(['a','b'])
 my_table.add_row(['c','d'])
 my_string=str(my_table)

=========
Renderers
=========

All Table objects have to have a Render type object. This can be changed at any time
after the creation of the object using the Table function set_table_renderer. The
default renderer if nothing is passed is RenderText. 

All Render classes must have the folloing functions (as they are called by Table)
the parameters for each differs for each type of table (all return string types):
 * print_header - Prints just the header row/column names
 * print_row    - Prints a single adhoc row
 * print_rows   - Prints all the rows in the table
 * print_table  - Prints the entire table

There are extra functions for the following renderers:
 'RenderText'
  * print_footer - Prints the footer of a text table

Supported parameters for print_table() for each renderer and defaults are below:
(Passed to the Renderer's __init__ functoin):
 'RenderText'
  * indent=0
  * borderless=False
  * color_disabled=False
  * padding=def_padding                    - def_padding=0
  * padding_char=def_txt_padding_char      - def_padding_char=' '
  * fill_char=def_txt_fill_char            - def_fill_char=' '
  * h_border_char=def_txt_horz_border_char - def_horz_border_char='-'
  * v_border_char=def_txt_vert_border_char - def_ver_border_char='|'
  * col_sep_char=def_txt_sep_char          - def_sep_char='|'

 'RenderCSV'
  * sep_char=def_sep_char          - def_sep_char=','

 'RenderHTML'
  [NOTE] this Renderer make use of Table's row_render_opts dict. Which means
         when calling Table's add_row method you can pass in a dict with the
         following keys/values:
           html_row_attr:  String HTMl row attribute/s to add to the 'tr' tag
           html_cell_attr: List of HTML cell attribute/s to add to 'td'/'th'
                           tags
  * color_disabled=False
  * table_attr=''
  * thead_attr=''
  * tbody_attr=''

Quick examples:
  from dynamic_table import *
  #Render the table indented 5 spaces, and cells padded 3 chars
  my_table=Table(RenderText(indent=5,padding=3))
  my_table.set_col_names(['Col1','Col2'])
  my_table.add_row(['a','b'])
  my_table.add_row(['c','d'])
  
  #Render the same table above but in html with a css class of "table"
  my_table.set_table_renderer(RenderHTML(table_attr='class=table"))
  
  #Render the same table, but now in csv pipe '|' separated
  my_table.set_table_renderer(RenderCSV(sep_char='|'))

=============
Table Filters
=============
Table objects can also be filtered using a set rules. This is done through
the use of TableFilter objects. They don't have any required parameters, but
can take an optional filter_txt string when being created.

Filter Expression Syntax (items in parenthesis are optional):
  ([column ids]);[column id][operator][comparison value];\ 
                 ([column id][operator][comparison value])...

Values for above:
  [column ids]:       comma separated list of columns ids. Ranges are
                      specified with a "-". e.g. 1-3. Ending the column ids
                      with a '-' will be from that column id on the left of
                      '-' to the end. Such as: "4-" would be from column 4 to
                      the end.
  [column id]:        Single column id
  [operator]:         One of: '>','<','>=','<=','!=','=','!/','/' which should
                      be self explanatory. '/' is a "contains" operator.
  [comparison value]: Value to compare against the column in [column id]. This
                      can be a string, number, or even a date.

If the first rule is a comma separated list it is referred to as a column
rule, all others are considered row rules. Additional row rules all have to be
true for a row to pass the filter.

Filter expression examples:
  #Only print columns 1,3 and 4 and only rows where column 1 is after
  #"2014-07-30 12:00:00"
  1,3,4;1>"2014-07-30 12:00:00"
  #Only print rows where column 4 is "Active" and column 2 has "tds" in it
  4=Active;2/tds

If not providing a filter_txt when creating a TableFilter object, you can add
more rules using the add_row_rule function and the set_col_rule. Which can be
useful if the [comparison value] contains a semi-colon in it.

TableFilter provides the following useful functions:
  filter_table(table):    returns a Table object that has been filtered
                          according to the rules in the TableFilter
  set_col_rule(col_rule): Add a column rule. (String, comma separated ids) See
                          Filter Expression Syntax, above
  add_row_rule(row_rule): Add a row rule. (String). See Filter Expression
                          Syntax above.

Examples of filtering:
  #Create a table with some data in it:
  thing=dynamic_table.Table()
  thing.set_col_names(['Col1','Col2','Col3','Miscellaneous'])
  thing.add_row(['abc','blah','boo','stuff'])
  thing.add_row(['def','blah','boo','stuff'])
  thing.add_row(['ghi','blah','boo',''])
  thing.add_row(['jkl','blah','boo'])
  thing.add_row(['20140801 4:00:00','Im colored','right?'],['','red'])
  thing.add_row(['2013-04-21 1:00:00','','Yay Multicolors'],['','','bg_brown,black'])
  thing.add_row(['2014-07-30 12:00:00','a'])
  thing.add_row(['2014-07-30 16:00:00','b','c'],['green'])
  #Create a Table Filter to only have column 1 and 3 to the end and where
  # column 1 is after the date/time '2014-07-30 12:00:00'
  tf=dynamic_table.TableFilter(filter_txt='1,3-;1>2014-07-30 12:00:00')
  #Filter the table and render it
  tf.filter_table(thing).render()
  
  #Create a filter that only show column 1,3 and 4, and where column 1 is
  # before '2014-07-30 12:00:00'
  tf=dynamic_table.TableFilter(filter_txt='1,3,4;1<2014-07-30 12:00:00')
  #Create a Table with the filter above that filters as it is being added
  thing=dynamic_table.Table(table_filter=tf)
  #Add some data and column names:
  thing.set_col_names(['Col1','Col2','Col3','Miscellaneous'])
  thing.add_row(['abc','blah','boo','stuff'])
  thing.add_row(['def','blah','boo','stuff'])
  thing.add_row(['ghi','blah','boo',''])
  thing.add_row(['jkl','blah','boo'])
  thing.add_row(['20140801 4:00:00','Im colored','right?'],['','red'])
  thing.add_row(['2013-04-21 1:00:00','','Yay Multicolors'],['','','bg_brown,black'])
  thing.add_row(['2014-07-30 12:00:00','a'])
  thing.add_row(['2014-07-30 16:00:00','b','c'],['green'])
  thing.render()


To see more examples of how all this works out see the file: dynamic_table_examples.py


Written by Dan Farnsworth - Mar 2013

Version: 0.8.3
"""

import sys #This is only really needed so we can default out output to sys.stdout
from dateutil.parser import parse as dateparse #Used for TableFilter class converting strings to dates

class RenderText:
  """
  A Render class to render a Table object in a text representation.
  
  Args:
    indent:             Number of spaces to indent table to (Default=0)
    borderless:         Whether table should be borderless (Default=False)
    color_disabled:     Disable color displays (Default=False)
    padding:            Amount of padding around cell data (Default=0)
    padding_char:       Character to pad with (Default=' ')
    fill_char:          Character to fill empty space in cell (Default=' ')
    h_border_char:      Character for horiz. border (Default='-')
    v_border_char:      Character for vert. border (Default='|')
    col_sep_char:       Character for cell separator (Default='|')
  """
  type_spec='text'
  def_padding=0
  def_padding_char=' '
  def_horz_border_char='-'
  def_vert_border_char='|'
  def_fill_char=' '
  def_sep_char='|'
  txt_color_attr_dict={ 'black': '\033[30m',
               'blue': '\033[94m',
               'green': '\033[92m',
               'dimgray': '\033[90m',
               'yellow': '\033[93m',
               'red': '\033[91m',
               'purple': '\033[95m',
               'cyan': '\033[96m',
               'bg_red': '\033[41m',
               'bg_green': '\033[42m',
               'bg_brown': '\033[43m',
               'bg_blue': '\033[44m',
               'bg_purple': '\033[45m',
               'bg_cyan': '\033[46m',
               'bg_gray': '\033[47m',
               'bold': '\033[1m',
               'underline': '\033[4m',
               'blink': '\033[5m',
              }
  def __init__(self,indent=0,borderless=False,color_disabled=False,padding=def_padding,padding_char=def_padding_char,fill_char=def_fill_char,h_border_char=def_horz_border_char,v_border_char=def_vert_border_char,col_sep_char=def_sep_char):
    self.render_opts=dict()
    self.render_opts['indent']=indent
    self.render_opts['borderless']=borderless
    self.render_opts['padding']=padding
    self.render_opts['padding_char']=padding_char
    self.render_opts['fill_char']=fill_char
    self.render_opts['h_border_char']=h_border_char
    self.render_opts['v_border_char']=v_border_char
    self.render_opts['col_sep_char']=col_sep_char
    self.render_opts['color_disabled']=color_disabled
    if self.render_opts['borderless']:
      self.render_opts['h_border_char']=''
      self.render_opts['v_border_char']=''
      self.render_opts['col_sep_char']=''
  def _indent_lvl(self,lvl):
    i_lvl=''
    for i in range(lvl):
      i_lvl+=' '
    return i_lvl
  def _colorize_row(self,row,cell_colors):
    """
    Generate a dictionary of strings to wrap around cells to give color
    
    Args:
      row:              Array of data cells
      cell_colors:      Array of colors (that the renderer knows about)
                         to convert to proper escape sequences
    Returns:
      Dictionary with two keys, 'start' and 'end' each key contains a List
      corresponding to the row elements passed. and the translated escape
      sequence
    """
    cell_count=len(row)
    cell_color_count=len(cell_colors)
    count=0
    ENDC='\033[0m'
    color_dict={'start': [], 'end': [] }
    if cell_color_count <= 0:
      return None
    while count < cell_color_count and count < cell_count:
      colors=cell_colors[count].split(',')
      start_color=''
      for c in colors:
        if c in self.txt_color_attr_dict:
          start_color+=self.txt_color_attr_dict[c]
      if start_color:
        color_dict['start'].append(start_color)
        color_dict['end'].append(ENDC)
      else:
        color_dict['start'].append('')
        color_dict['end'].append('')
      count+=1
    if count < cell_count:
      while count < cell_count:
        color_dict['start'].append('')
        color_dict['end'].append('')
        count+=1
    return color_dict
  def copy(self):
    """
    Create a copy of the current object
    Returns:
      RenderText
    """
    new_renderer=RenderText()
    new_renderer.render_opts=dict(self.render_opts)
    return new_renderer
  def print_header(self,table,indent_str=''):
    """
    Render's the header of the table
    
    Args:
      table:      The table object where the table metadata is located
      indent_str: String that is prepended to the header
    
    Returns:
      String
    """
    built=[]
    border_width=(len(self.render_opts['h_border_char']) * table.data_max_width) + (2 * len(self.render_opts['v_border_char'])) + (2 * ( table.col_count * len(self.render_opts['padding_char']) * self.render_opts['padding'])) + (len(self.render_opts['col_sep_char']) * (table.col_count-1))
    if self.render_opts['h_border_char']:
      built.append(indent_str+''.ljust(border_width,self.render_opts['h_border_char']) + '\n')
    if len(table.col_names) == 0:
      if built:
        return ''.join(built)
    if len(table.col_names) < table.col_count:
      cells_filled=[]
      count=0
      for c in table.col_names:
        cells_filled.append(c)
        count+=1
      while count != table.col_count:
        cells_filled.append('')
        count+=1
      table.col_names=list(cells_filled)
    built.append(self.print_row(table,table.col_names,adhoc=False,indent_str=indent_str,))
    if self.render_opts['h_border_char']:
      built.append(indent_str+''.ljust(border_width,self.render_opts['h_border_char']) + '\n')
    return ''.join(built)
  def print_row(self,table,cells,colors=None,adhoc=True,indent_str=''):
    """
    Render's a single row (without needing to be in memory).
    
    Args:
      table:      The table object containing table metadata
      cells:      List where each element is a cell
                  (Note not adding the rows to the object and only calling
                  this doesn't help when setting static column widths)
      colors:     list of colors per cell in 'cells' above. Default=None
      adhoc:      True or false if rows being rendered are "adhoc" meaning
                  they aren't in the table object's memory. Default=False
      indent_str: String that is prepended to the header
    
    Returns:
      String
    """
    built=[]
    if adhoc:
      #Adhoc rows are rows not in table.rows so we need to make sure col widths and counts are correct
      tmp_count=len(cells)
      while tmp_count < table.col_count:
        cells.append('')
        tmp_count+=1
      table._row_col_width_adjust(cells)
    col_widths_set_count=len(table.col_widths)
    cells_count=len(cells)
    cur_count=0
    built.append(indent_str+self.render_opts['v_border_char'])
    while cur_count < cells_count:
      built.append(''.ljust(self.render_opts['padding'],self.render_opts['padding_char'])) #Pad beginning of cell
      if colors:
        color_dict=self._colorize_row(cells,colors)
      else:
        color_dict=False
      if cur_count < col_widths_set_count:
        #See if there are set col widths
        if table.col_widths[cur_count] > 0:
          #See if we need to produce colors
          if color_dict:
            built.append(color_dict['start'][cur_count]+cells[cur_count][:table.col_widths[cur_count]].ljust(table.col_widths[cur_count],self.render_opts['fill_char'])+color_dict['end'][cur_count]) #output width set cell width and truncation with color
          else:
            built.append(cells[cur_count][:table.col_widths[cur_count]].ljust(table.col_widths[cur_count],self.render_opts['fill_char'])) #output width set cell width and truncation
        else:
          if color_dict:
            built.append(color_dict['start'][cur_count]+cells[cur_count].ljust(table.col_widths_real[cur_count],self.render_opts['fill_char'])+color_dict['end'][cur_count]) #output non-width set cell width with color
          else:
            built.append(cells[cur_count].ljust(table.col_widths_real[cur_count],self.render_opts['fill_char'])) #output non-width set cell
      else:
        if color_dict:
          built.append(color_dict['start'][cur_count]+cells[cur_count].ljust(table.col_widths_real[cur_count],self.render_opts['fill_char'])+color_dict['end'][cur_count]) #output non-width set cell
        else:
          built.append(cells[cur_count].ljust(table.col_widths_real[cur_count],self.render_opts['fill_char'])) #output non-width set cell
      built.append(''.ljust(self.render_opts['padding'],self.render_opts['padding_char'])) #Pad end of cell
      cur_count+=1
      if cur_count >= cells_count:
        built.append(self.render_opts['v_border_char'])
      else:
        built.append(self.render_opts['col_sep_char'])
    built.append('\n')
    return ''.join(built)
  def print_rows(self,table,indent_str=''):
    """
    Render all rows currently in the table object passed
    
    Args:
      table:      The table object containing table metadata
      indent_str: String that is prepended to the header

    Returns:
      String
    """
    #Print all rows currently added to the object via add_row().
    built=[]
    row_count=0
    for r in table.rows:
      c_count=len(r)
      if c_count < table.col_count:
        count=c_count
        while count != table.col_count:
          r.append('')
          count+=1
      if self.render_opts['color_disabled']:
         built.append(self.print_row(table,r,adhoc=False,indent_str=indent_str))
      else:
        built.append(self.print_row(table,r,table.row_colorization[row_count],adhoc=False,indent_str=indent_str))
      row_count+=1
    return ''.join(built)
  def print_footer(self,table,indent_str=''):
    """
    Render's the footer of the table
    
    Args:
      table:      The table object where the table metadata is located
      indent_str: String that is prepended to the header
    
    Returns:
      String
    """
    built=[]
    border_width=(len(self.render_opts['h_border_char']) * table.data_max_width) + (2 * len(self.render_opts['v_border_char'])) + (2 * ( table.col_count * len(self.render_opts['padding_char']) * self.render_opts['padding'])) + (len(self.render_opts['col_sep_char']) * (table.col_count-1))
    if self.render_opts['h_border_char']:
      built.append(indent_str+''.ljust(border_width,self.render_opts['h_border_char']) + '\n')
    return ''.join(built)
  def print_table(self,table,indent=0):
    """
    Render the full table
    
    Args:
      table:    The table object where the table metadata is located
      indent:   Number of chars to indent table when rendering. Default=0

    Returns:
      String
    """
    built=[]
    #Check and indent table as needed
    if self.render_opts['indent'] > 0:
      indent_str=self._indent_lvl(self.render_opts['indent'])
    else:
      indent_str=''
    header=self.print_header(table=table,indent_str=indent_str)
    rows=self.print_rows(table=table,indent_str=indent_str)
    footer=self.print_footer(table=table,indent_str=indent_str)
    if header:
      built.append(header)
    if rows:
      built.append(rows)
    if footer:
      built.append(footer)
    return ''.join(built)

class RenderCSV:
  """
  A Render class to render a Table object in a CSV representation.
  
  Args:
    sep_char:   Separator charactor. Default=','
  """
  type_spec='csv'
  def_sep_char=','
  def __init__(self,sep_char=def_sep_char):
    self.sep_char=sep_char
  def copy(self):
    """
    Create a copy of the current object
    
    Returns:
      RenderCSV
    """
    new_renderer=RenderCSV()
    new_renderer.sep_char=str(self.sep_char)
    return new_renderer
  def print_header(self,table):
    """
    Render's the header of the table
    
    Args:
      table:      The table object where the table metadata is located
    
    Returns:
      String
    """
    if len(table.col_names) == 0:
      return ''
    if len(table.col_names) < table.col_count:
      cells_filled=[]
      count=0
      for c in table.col_names:
        cells_filled.append(c)
        count+=1
      while count != table.col_count:
        cells_filled.append('')
        count+=1
      table.col_names=list(cells_filled)
    return self.print_row(table,table.col_names,adhoc=False)
  def print_row(self,table,cells,adhoc=False):
    """
    Render's a single row (without needing to be in memory).
    
    Args:
      table:      The table object containing table metadata
      cells:      List where each element is a cell
      adhoc:      True or false if rows being rendered are "adhoc" meaning
                  they aren't in the table object's memory. Default=False
    
    Returns:
      String
    """
    built=[]
    if adhoc:
      #Adhoc rows are rows not in table.rows so we need to make sure col widths and counts are correct
      tmp_count=len(cells)
      while tmp_count < table.col_count:
        cells.append('')
        tmp_count+=1
      table._row_col_width_adjust(cells)
    cells_count=len(cells)
    cur_count=0
    while cur_count < cells_count:
      built.append(cells[cur_count])
      cur_count+=1
      if cur_count < cells_count:
        built.append(self.sep_char)
      else:
        built.append('\n')
    return ''.join(built)
  def print_rows(self,table):
    """
    Render all rows currently in the table object passed
    
    Args:
      table:      The table object containing table metadata

    Returns:
      String
    """
    built=[]
    for r in table.rows:
      c_count=len(r)
      if c_count < table.col_count:
        count=c_count
        while count != table.col_count:
          r.append('')
          count+=1
      built.append(self.print_row(table,r,adhoc=False))
    return ''.join(built)
  def print_table(self,table):
    """
    Render the full table
    
    Args:
      table:    The table object where the table metadata is located

    Returns:
      String
    """
    built=[]
    built.append(self.print_header(table))
    built.append(self.print_rows(table))
    return ''.join(built)

class RenderHTML:
  """
  A Render class to render a Table object in an HTML representation.
  [NOTE] this Renderer make use of Table's row_render_opts dict. Which means
         when calling Table's add_row method you can pass in a dict with the
         following keys/values:
           html_row_attr:  String HTMl row attribute/s to add to the 'tr' tag
           html_cell_attr: List of HTML cell attribute/s to add to 'td'/'th'
                           tags
  
  Args:
    color_disabled:     Disable color displays (Default=False)
    table_attr:         Optional attribute to add into <table> tag
    thead_attr:         Optional attribute to add into <thead> tag
    tbody_attr:         Optional attribute to add into <tbody> tag
  """
  type_spec='html'
  def_borderless=False
  def_border=1
  def_padding=1
  def_color_disabled=False
  def __init__(self,color_disabled=def_color_disabled,table_attr='',thead_attr='',tbody_attr=''):
    self.color_disabled=color_disabled
    self.body_tag_rendered=False
    self.table_attr=table_attr
    self.thead_attr=thead_attr
    self.tbody_attr=tbody_attr
  def _colorize_row(self,row,cell_colors):
    """
    Generate a dictionary of strings to wrap around cells to give color
    
    Args:
      row:              Array of data cells
      cell_colors:      Array of colors to convert to html tags
    Returns:
      Dictionary with two keys, 'start' and 'end' each key contains a List
      corresponding to the row elements passed. and the html font color tag
    """
    cell_count=len(row)
    cell_color_count=len(cell_colors)
    count=0
    color_dict={'start': [], 'end': [] }
    if cell_color_count <= 0:
      return None
    while count < cell_color_count and count < cell_count:
      colors=cell_colors[count].split(',')
      start_color=''
      if colors[0]:
        start_color+='<font color="'
        start_color+=colors[0]
        start_color+='">'
      if start_color:
        color_dict['start'].append(start_color)
        color_dict['end'].append("</font>")
      else:
        color_dict['start'].append('')
        color_dict['end'].append('')
      count+=1
    if count < cell_count:
      while count < cell_count:
        color_dict['start'].append('')
        color_dict['end'].append('')
        count+=1
    return color_dict
  def copy(self):
    """
    Create a copy of the current object
    Returns:
      RenderHTML
    """
    new_renderer=RenderHTML()
    return new_renderer
  def print_header(self,table):
    """
    Render's the header of the table
    
    Args:
      table:      The table object where the table metadata is located
    
    Returns:
      String
    """
    built=[]
    if len(table.col_names) == 0:
      if built:
        return ''.join(built)
      else:
        return ''
    if len(table.col_names) < table.col_count:
      cells_filled=[]
      count=0
      for c in table.col_names:
        cells_filled.append(c)
        count+=1
      while count != table.col_count:
        cells_filled.append('')
        count+=1
      table.col_names=list(cells_filled)
    built.append('  <thead %s>\n' % (self.thead_attr))
    built.append(self.print_row(table,table.col_names,th=True,adhoc=False))
    built.append('  </thead>\n')
    return ''.join(built)
  def print_row(self,table,cells,colors=None,attrs=None,adhoc=False,th=False):
    """
    Render's a single row (without needing to be in memory).
    
    Args:
      table:      The table object containing table metadata
      cells:      List where each element is a cell
      attrs:      Dictionary with the following keys/values
                    html_row_attr:  String HTMl row attribute/s to add to the
                                   'tr' tag
                    html_cell_attr: List of HTML cell attribute/s to add to
                                    'td'/'th' tags
      adhoc:      True or false if rows being rendered are "adhoc" meaning
                  they aren't in the table object's memory. Default=False
      colors:     list of colors per cell in 'cells' above. Default=None
      th:         Whether the delimeter should be <th> tags instead of <td>
                  (For the table header). Default=False
    
    Returns:
      String
    """
    built=[]
    if adhoc:
      #Adhoc rows are rows not in self.rows so we need to make sure col widths and counts are correct
      tmp_count=len(cells)
      while tmp_count < self.col_count:
        cells.append('')
        tmp_count+=1
      table._row_col_width_adjust(cells)
    cells_count=len(cells)
    cur_count=0
    if colors:
      color_dict=self._colorize_row(cells,colors)
    else:
      color_dict=False
    if th:
      delim_tag="th"
    else:
      delim_tag="td"
    if attrs:
      try:
        row_attr=attrs['html_row_attr']
      except KeyError:
        row_attr=''
        pass
      try:
        cell_attr=attrs['html_cell_attr']
        if not cell_attr:
          cell_attr=None
      except KeyError:
        cell_attr=None
        pass
    else:
      row_attr=''
      cell_attr=None
    if row_attr:
      built.append('    <tr %s>\n      ' % (row_attr))
    else:
      built.append('    <tr>\n      ')
    while cur_count < cells_count:
      delim_tag_attr=delim_tag
      if cell_attr:
        try:
          delim_tag_attr='%s %s' % (delim_tag,cell_attr[cur_count])
        except IndexError:
          pass
      if color_dict:
        built.append("<%s>%s%s%s</%s>" % (delim_tag_attr,color_dict['start'][cur_count],cells[cur_count],color_dict['end'][cur_count],delim_tag))
      else:
        built.append("<%s>%s</%s>" % (delim_tag_attr,cells[cur_count],delim_tag))
      cur_count+=1
      if cur_count >= cells_count:
        built.append('\n    </tr>\n')
    return ''.join(built)
  def print_rows(self,table):
    """
    Render all rows currently in the table object passed
    
    Args:
      table:      The table object containing table metadata

    Returns:
      String
    """
    built=[]
    row_count=0
    built.append('  <tbody %s>\n' % (self.tbody_attr))
    for r in table.rows:
      c_count=len(r)
      if c_count < table.col_count:
        count=c_count
        while count != table.col_count:
          r.append('')
          count+=1
      if self.color_disabled:
        built.append(self.print_row(table,r,attrs=table.row_render_opts[row_count],adhoc=False))
      else:
        built.append(self.print_row(table,r,colors=table.row_colorization[row_count],attrs=table.row_render_opts[row_count],adhoc=False))
      row_count+=1
    built.append('  </tbody>\n')
    return ''.join(built)
  def print_table(self,table):
    """
    Render the full table
    
    Args:
      table:    The table object where the table metadata is located

    Returns:
      String
    """
    built=[]
    built.append("<table %s>\n" % (self.table_attr) )
    built.append(self.print_header(table))
    built.append(self.print_rows(table))
    built.append("</table>\n")
    return ''.join(built)

class Table:
  """
  The table class. This contains rows, and metadata such as colum counts/size
  etc...
  
  Args:
    renderer:      Render oject which is how to render the table data
    output:        A file like object to write data to, This can also be the
                   key word 'String' to write to the internal string:
                     built_buffer. Default=sys.stdout
    table_filter:  TableFilter object, to filter data as they are added
                   to the table
  """
  col_count=0 #Number of columns the table currently has
  data_cur_max_width=0 #This holds the max chars without any truncation etc..
  data_max_width=0 #This holds what will be the max chars taking into account truncation from static set col widths
  def_padding=0 #Amount of padding to add to the sides of cells
  def __init__(self,renderer=RenderText(),output=sys.stdout,table_filter=None):
    self._output_file=''
    self.built_buffer=''
    self.col_widths=[] #List of column widths that have been passed in and will truncate or have space if values don't fit
    self.col_widths_real=[] #List of column widths that are a max width per column
    self.col_names=[] #List of names of the columns, used mostly for the header
    self.rows=[]
    self.row_colorization=[]
    self.row_render_opts=[]
    #Check that the output passed is a file like object:
    try:
      if (output != "String"):
        getattr(output,'write')
        self._output_file=output
    except NameError:
      raise NameError("Name passed as Table output is invalid. Is sys module imported?")
    except AttributeError:
      raise AttributeError("Output object passed is not a 'File Like' object with a 'write' method")
    self.set_table_renderer(renderer)
    if table_filter:
      #Check that the table filter passed is a valid TableFilter object
      try:
        getattr(table_filter,'filter_table')
        self.table_filter=table_filter
      except AttributeError:
        AttributeError("TableFilter passed is not a valid TableFilter")
    else:
      self.table_filter=None
  def __str__(self):
    """
    Converts the table to a string object using the supplied renderer
    
    Returns:
      String
    """
    return self.renderer.print_table(self)
  def __len__(self):
    """
    Converts the table representation to a specified length, which
    is the number of rows currently added to the table.
    
    Returns:
      String
    """
    return len(self.rows)
  ####These functions are helper functions meant to be somewhat private####
  def _output(self,data):
    """
    Handle writes, either to file like object passed to __init__.output or
    to the built in string buffer "built_buffer"
    """
    if self._output_file:
      #This handles writing out our content
      self._output_file.write(data)
    else:
      self.built_buffer+=data
  def _update_col_widths(self):
    """
    This looks at the length of the static set column widths and the max column
    width of all the cells (col_widths_real) to determing col_count and/or one
    of the column width arrays needs to be updated to have the same number of
    columns
    """
    col_set_count=len(self.col_widths)
    col_real_count=len(self.col_widths_real)
    if col_set_count != col_real_count:
      if col_set_count > col_real_count:
        col_diff=col_set_count - col_real_count
        new_count=col_set_count
        count=0
        i=col_set_count-1
        while count < col_diff:
          self.col_widths_real.append(self.col_widths[i])
          i+=1
          count+=1
      else:
        col_diff=col_real_count - col_set_count
        new_count=col_real_count
        count=0
        while count < col_diff:
          self.col_widths.append(0)
          count+=1
      self.col_count=new_count
  def _update_data_max_width(self):
    """
    This compares what is in self.col_widths_real to self.col_widths to determine what
    the actual data length (including any possible truncation) should be, and updates
    self.data_max_width
    """
    count=0
    width=0
    self._update_col_widths()
    col_set_count=len(self.col_widths)
    col_real_count=len(self.col_widths_real)
    for c in self.col_widths_real:
      if count < col_set_count:
        if self.col_widths[count] <= 0:
          width+=self.col_widths_real[count]
        else:
          width+=self.col_widths[count]
      else:
        width+=self.col_widths_real[count]
      count+=1
    self.data_max_width=width
  def _row_col_width_adjust(self,row):
    """
    This is usually called after a new row is inserted and updates
    col_widths_real incase columns need to be expanded etc.. 
    
    Args:
      row:      List where each element is a cell
    """
    count=0
    col_widths_real_count=len(self.col_widths_real)
    for c in row:
      try:
        c_len=len(c)
      except TypeError:
        c_len=len(str(c))
      if count < col_widths_real_count:
        if c_len > self.col_widths_real[count]:
          self.col_widths_real[count]=c_len
      else:
        self.col_widths_real.append(c_len)
      count+=1
    self._update_data_max_width()
  ####These are the externally supported functions####
  def copy(self):
    """
    Creates a copy of the current table object
    
    Returns:
      Table
    """
    new_table=Table()
    new_table.rows=list(self.rows)
    new_table.row_colorization=list(self.row_colorization)
    new_table.row_render_opts=list(self.row_render_opts)
    new_table.col_widths=list(self.col_widths)
    new_table.col_widths_real=list(self.col_widths_real)
    new_table.data_max_width=int(self.data_max_width)
    new_table.data_cur_max_width=int(self.data_cur_max_width)
    new_table.col_names=list(self.col_names)
    new_table.col_count=int(self.col_count)
    new_table.renderer=self.renderer.copy()
    new_table._output_file=self._output_file
    new_table.color_disabled=bool(self.color_disabled)
    return new_table
  def empty_output(self):
    """
    When the table is created with output="String" the print/render functions
    will store the table in memory at self.built_buffer. This function empties
    that buffer.
    """
    if self._output_file:
      return
    else:
      self.built_buffer=''
  def set_table_renderer(self,renderer):
    """
    Change the renderer for the table to the new rendere.
    
    Args:
      renderer:         Render object to use when rendering the table
    """
    self.renderer=renderer
    try:
      getattr(renderer,'print_table')
      self.renderer=renderer
    except AttributeError:
      raise AttributeError("Renderer passed does not appear to be a proper Render object")
  def render(self):
    """
    Render the table using the renderer
    """
    self._output(self.renderer.print_table(table=self))
  def print_header(self):
    """
    Render just the header of the table
    """
    self._output(self.renderer.print_header(self))
  def print_row(self,cells,colors=None):
    """
    Render a single passed row without adding to memory, this is how
    adhoc tables are created
    
    Args:
      cells:      List where each element is a cell
      colors:     list of colors per cell in 'cells' above. Default=None

    """
    if self.renderer.type_spec == 'csv':
      self._output(self.renderer.print_row(self,cells,adhoc=True))
    else:
      self._output(self.renderer.print_row(self,cells,colors,adhoc=True))
  def print_footer(self):
    """
    Render the footer of the table, useful with adhoc tables
    """
    if self.renderer.type_spec == 'text':
      self._output(self.renderer.print_footer(self))
  def print_table(self):
    """
    Render the Table, this is provided for backward compatibility
    """
    self.render()
  def set_col_widths(self,col_widths):
    """
    This sets a hard static column length.  A column of size 0 or '' will 
    auto adjust based on the cell length.
    
    Args:     List of integers where each element is the length of the column.
    """
    count=1
    tmp_col_widths=[]
    col_count=len(col_widths)
    col_width_total=0
    for i in col_widths:
      try:
        #column width of 0 or '' implies dynamically adjust column width
        if i == '':
          w=0
        else:
          w=int(i) #Check that the static width is an integer
        tmp_col_widths.append(w)
      except ValueError:
        raise ValueError('Defined column width is not a number at column:' + str(count))
      count+=1
    self.col_widths=list(tmp_col_widths)
    self._update_col_widths()
    self._update_data_max_width()
  def set_col_names(self,col_names):
    """
    Set the column heading names.
    
    Args:
      col_names:      List of strings, where each element is is a column name
    """
    if self.table_filter:
      c=self.table_filter._filter_cols(col_names)
      col_names=c
    cell_count=len(col_names)
    tmp_col_names=[]
    count=0
    for n in col_names:
      cell_len=len(str(n))
      tmp_col_names.append(str(n))
      if count < len(self.col_widths_real):
        if cell_len > self.col_widths_real[count]:
          self.col_widths_real[count]=cell_len
      else:
        self.col_widths_real.append(cell_len)
      count+=1
    if cell_count > self.col_count:
      self.col_count=cell_count
    while count != self.col_count:
      tmp_col_names.append('')
      count+=1
    self.col_names=list(tmp_col_names)
    self._row_col_width_adjust(tmp_col_names)
  def add_row(self,cells,color_cells=[],renderer_opts=None):
    """
    Add a row to the table in memory
    
    Args:
      cells:          List where each element is a cell
      color_cells:    List where each element is a color for the cells elements
      renderer_opts:  Dictionary with arbitrary keys depending on the Renderer.
                      this can add additional attributes per row/cell.
                      For Example: with RenderHTML renderer the following dict
                      keys add HTML attribute to tr and th/td tags

                        html_row_attr:  String HTMl row attribute/s to add to the
                                   'tr' tag
                        html_cell_attr: List of HTML cell attribute/s to add to
                                    'td'/'th' tags
    """
    if self.table_filter:
      if self.table_filter._check_row(cells):
        c=self.table_filter._filter_cols(cells)
        if color_cells:
          cc=self.table_filter._filter_cols(color_cells)
        else:
          cc=color_cells
      else:
        return
      cells=c
      color_cells=cc
    cell_count=len(cells)
    if cell_count > self.col_count:
      self.col_count=cell_count
      self.rows.append(cells)
      self.row_colorization.append(color_cells)
      self.row_render_opts.append(renderer_opts)
      self._row_col_width_adjust(cells)
    elif cell_count == self.col_count:
      self.rows.append(cells)
      self.row_colorization.append(color_cells)
      self.row_render_opts.append(renderer_opts)
      self._row_col_width_adjust(cells)
    else:
      cells_filled=[]
      count=0
      for c in cells:
        cells_filled.append(str(c))
        count+=1
      while count != self.col_count:
        cells_filled.append('')
        count+=1
      self.rows.append(cells_filled)
      self.row_colorization.append(color_cells)
      self.row_render_opts.append(renderer_opts)
      self._row_col_width_adjust(cells_filled)

class CustomOp:
  """
  Creates an object that can offer specialized methods for magic methods.
  Currently, this is mostly only useful for __contains__ with strings so that
  we can reverse the statement.

  Args:
    obj:  Object to pass in and reverse the magic method

  """
  def __init__(self,obj):
    self.obj=obj
  def __contains__(self,v):
    if v.__contains__(self.obj):
      return True
    else:
      return False
  def __notcontains__(self,v):
    return not(self.__contains__(v))

class TableFilter:
  """
  Creates an object for filtering Table objects
  
  Filter Expression Syntax (items in parenthesis are optional):
    ([column ids]);[column id][operator][comparison value];\ 
                  ([column id][operator][comparison value])...

  Values for above:
    [column ids]:       comma separated list of columns ids. Ranges are
                        specified with a "-". e.g. 1-3. Ending the column ids
                        with a '-' will be from that column id on the left of
                        '-' to the end. Such as: "4-" would be from column 4
                        to the end.
    [column id]:        Single column id
    [operator]:         One of: '>','<','>=','<=','!=','=','!/','/' which
                        should be self explanatory. '/' is a "contains" operator.
    [comparison value]: Value to compare against the column in [column id].
                        This can be a string, number, or even a date.
  Args:
    filter_txt:         String following Filter Expression Syntax above
  
  """
  row_ops=[ '>=','<=','>','<','!=','=','!/','/' ]
  def __init__(self,filter_txt=None):
    self.row_rules=[]
    self.col_rule=[]
    self.col_rule_len=0
    if filter_txt:
      self._parse_filter_txt(filter_txt)
  #Functions that are somewhat private
  def _parse_filter_txt(self,filter_txt):
    """
    Parses a full filter_txt, and populates self.col_rule and self.row_rules
    """
    f_split=filter_txt.split(';')
    rule_cnt=len(f_split)
    xtra_col_rule=True
    #Only column rules have ',' in the first ';' separated column
    if f_split[0].find(',') > 0:
      self.set_col_rule(f_split[0])
    else:
      #Make sure there isn't an operator(Which would imply a row rule)
      for op in self.row_ops:
        if op in f_split[0]:
          xtra_col_rule=False
          break
      #Support column rules that have no commas but only have col ranges
      if xtra_col_rule:
        #Assume this is a column rule
        self.set_col_rule(f_split[0])
      else:
        #Assume no column rule specified, so is a row rule
        self.add_row_rule(f_split[0])
    for i in range(1,rule_cnt):
      self.add_row_rule(f_split[i])
  def _check_row(self,row):
    """
    Checks a row of cells against the current rules in self.row_rules
    
    Args:
      row:      List of cells
      
    Returns:
      True/False
    """
    for rule in self.row_rules:
      try:
        if rule['val_type'] == 'date':
          v=float(dateparse(row[rule['col']-1]).strftime('%s'))
        elif rule['val_type'] == 'number':
          v=float(row[rule['col']-1])
        else:
          v=str(row[rule['col']-1])
        if not rule['op'](v):
          return False
      except:
        return False
    return True
  def _filter_cols(self,cols):
    """
    Filters a list of cells according to the col_rule
    
    Args:
      cols:     List of cells
    
    Returns:
      List
    """
    end_range=False
    e_r=self.col_rule_len
    if e_r == 0:
      return cols
    filter_cols=[]
    if self.col_rule[-1] == '-':
      end_range=True
      e_r-=2
    for i in range(0,e_r):
      c=self.col_rule[i]-1
      try:
        filter_cols.append(cols[c])
      except IndexError:
        pass
    if end_range:
      try:
        filter_cols.append(cols[self.col_rule[-2]-1])
      except IndexError:
        pass
      try:
        cc_len=len(cols)
        if cc_len > self.col_rule[-2]:
          for i in range(self.col_rule[-2],cc_len):
            filter_cols.append(cols[i])
      except IndexError:
        pass
    return filter_cols
  def filter_table(self,table):
    """
    Filter a full table, based on current column and row rules
    
    Args:
      table:    A Table object to filter
    
    Returns:
      Table
    """
    #Create new Table object
    new_table=Table(renderer=table.renderer.copy())
    new_table._output_file=table._output_file
    new_table.set_col_names(self._filter_cols(table.col_names))
    #Filter the table and only add the rows with needed columns to the new
    # object
    r_cnt=0
    for r in table.rows:
      if self._check_row(r):
        new_table.add_row(self._filter_cols(r),self._filter_cols(table.row_colorization[r_cnt]))
      r_cnt+=1
    return new_table
  def set_col_rule(self,col_rule):
    """
    Set a column rule for filtering
    
    Args:
      col_rule: String with comma separated columns ids. Ranges are
                specified with a "-". e.g. 1-3. Ending the column ids
                with a '-' will be from that column id on the left of
                '-' to the end. Such as: "4-" would be from column 4 to
                the end.
    """
    end_range=False
    crs=col_rule.split(',')
    cr_len=len(crs)
    r_end=cr_len
    try:
      if crs[-1][-1] == '-':
        end_val=int(crs[-1].split('-')[0])
        r_end-=1
        end_range=True
    except TypeError:
      end_range=False
    except IndexError:
      end_range=False
    except ValueError:
      raise ValueError("column filter ending range must be a number to start with")
    for i in range(0,r_end):
      c=crs[i]
      if '-' in c:
        #A column range was specified, check that it has a start and stop.
        c_split=c.split('-')
        if len(c_split) == 2:
          try:
            from_c=int(c_split[0])
            to_c=int(c_split[1])
            for cr in range(from_c,to_c+1):
              self.col_rule.append(cr)
          except ValueError:
            raise ValueError("column filter range must be from a number to a number")
        else:
          #Looks poorly formatted
          raise ValueError("column filter can only end with the range operator if it is the last value")
      else:
        try:
          self.col_rule.append(int(c))
        except ValueError:
          raise ValueError("column filter must be a number")
    if end_range:
      self.col_rule.append(end_val)
      self.col_rule.append('-')
    self.col_rule_len=len(self.col_rule)
  def add_row_rule(self,row_rule):
    """
    Add a new row rule to the current row_rules
    
    Row Rule Syntax:
      [column id][operator][comparison value]
      
      [column id]:        Single column id
      [operator]:         One of: '>','<','>=','<=','!=','=','!/','/' which
                          should be self explanatory. '/' is a "contains" operator.
      [comparison value]: Value to compare against the column in [column id].
                          This can be a string, number, or even a date.
    
    Args:
      row_rule:    String formatted row rule. Following "Row Rule Syntax".
    """
    op_found=False
    #Check the row rule to make sure it has a valid operator in it
    for op in self.row_ops:
      if op in row_rule:
        #Valid operator found, split on it
        op_found=True
        rule_split=row_rule.split(op)
        #Check for missing options
        if len(row_rule) < 2:
          raise ValueError("Missing arguments for row rule:" + row_rule)
        #Make a new dictionary for holding our rule information
        new_rule=dict()
        new_rule['val_type']=None
        #Check to make sure first argument is an int
        try:
          new_rule['col']=int(rule_split[0])
        except ValueError:
          raise ValueError("row rule column specified must be a number:" + str(rule_split[0]) + "for row rule: " + row_rule)
        #Check to see if the value comparison is against numbers
        try:
          new_rule['val']=float(rule_split[1])
          new_rule['val_type']='number'
        except ValueError:
          #Check to see if the value comparison is against dates
          try:
            new_rule['val']=float(dateparse(rule_split[1]).strftime('%s'))
            new_rule['val_type']='date'
          except ValueError:
            #Nope, must be a string
            new_rule['val']=rule_split[1]
            new_rule['val_type']='string'
            pass
        if new_rule['val_type'] == 'string':
          if op not in [ '=','!=','!/','/' ]:
            raise ValueError("row rule operator: " + op + " is invalid for comparing string values for row rule:"+row_rule)
        #Find the proper comparison function for the value type
        #Yes, the functions are reversed for gt and lt comparisons, this is intentional
        if op == '>':
          new_rule['op']=new_rule['val'].__lt__
        elif op == '>=':
          new_rule['op']=new_rule['val'].__le__
        elif op == '<':
          new_rule['op']=new_rule['val'].__gt__
        elif op == '<=':
          new_rule['op']=new_rule['val'].__ge__
        elif op == '!=':
          new_rule['op']=new_rule['val'].__ne__
        elif op == '=':
          new_rule['op']=new_rule['val'].__eq__
        elif op == '/':
          new_rule['op']=CustomOp(new_rule['val']).__contains__
        elif op == '!/':
          new_rule['op']=CustomOp(new_rule['val']).__notcontains__
        else:
          raise RuntimeError("You shouldn't have gotten here, op list doesnt match row_ops")
        self.row_rules.append(new_rule)
        break
    if not op_found:
      raise ValueError("row rule MUST have a valid operator for rule:" + row_rule)
