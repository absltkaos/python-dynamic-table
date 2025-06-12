`python-dynamic-table`
=====================

Python module for creating text table respresentations in various table. Including Text, CSV, and HTML


Introduction
============

This module provides a way to build/create, and print tables.  So you can create a text table, add rows, and then print them in a human readable text format.  It also supports html and csv renderers.  So if you build a text table you can print it in html or csv format.

> [!NOTE]
> This was written quickly, but could use some additional features such as:
> 
> * Ability to change text justifcation for text and html tables by column
> * Ability to change the background cell color for html tables
> * Ability to print an html table in html5 supported ways with inline css etc...
> * In other words... this is heavily a work in progress

The interface to dynamic table is pretty straight forward. All Table objects have the following functions:

* `add_row`
* `set_table_type`
* `set_col_widths`
* `set_col_names`
* `set_table_renderer`

If you want to write the table to a file instead of stdout (the default) you do so when instantiating the *Table* class. Like so:

```py
my_file=open('/path/to/file','rw')
my_table=*Table*(output=my_file)
```

Doing this will ensure that any print functions get written to the file instead of stdout.

You can also modify this behavior by defining output as 'String' and then the print functions will build the table in the variable "built_buffer", this does not get cleared automatically. When done with the data, call the function empty_output().

> [!NOTE]
> This way of doing this is deprecated in favor of calling str(*Table*). However, it is still useful if building ad-hoc tables, I guess.

Example of deprecated 'String' output, with an ad-hoc table:

```py
my_table=Table(output='String')
my_table.set_col_names(['Col1','Col2'])
my_table.print_header()
my_table.print_row(['a','b'])
my_table.print_row(['c','d'])
table_text=my_table.built_buffer
my_table.empty_output()
```

Example of newer method to render to a string:

```py
my_table=Table()
my_table.set_col_names(['Col1','Col2'])
my_table.add_row(['a','b'])
my_table.add_row(['c','d'])
my_string=str(my_table)
```


Renderers
=========

All *Table* objects have to have a Render type object. This can be changed at any time after the creation of the object using the *Table* function set_table_renderer. The default renderer if nothing is passed is `RenderText`. 

All Render classes must have the folloing functions (as they are called by *Table*) the parameters for each differs for each type of table (all return string types):

Name           | Explanation
---------------|----------------------------------------
`print_header` | Prints just the header row/column names
`print_row`    | Prints a single adhoc row
`print_rows`   | Prints all the rows in the table
`print_table`  | Prints the entire table

There are extra functions for the following renderers:

* `RenderText`
* `print_footer`

  Prints the footer of a text table.


Supported parameters for `print_table()` for each renderer and defaults are below: (Passed to the Renderer's `__init__` function):


`RenderText`
------------

Parameter        | Default | Explanation
-----------------|---------|------------------
`indent`         | `0`     | Number of spaces to indent the output
`borderless`     | `False` | Whether to add a border to the table or not
`color_disabled` | `False` | When to render colors
`padding`        | `0`     | Amount of padding to add to values in cells
`padding_char`   | `" "`   | The character to padd the cells with
`fill_char`      | `" "`   | Character to use for filling remaing empty space in the cell
`h_border_char`  | `"-"`   | Horizontal border character
`v_border_char`  | `"\|"`   | Vertical border character
`col_sep_char`   | `"\|"`   | Column separator character


`RenderCSV`
-----------

Parameter        | Default | Explanation
-----------------|---------|------------------
`sep_char`       | `","`     | The character to use for separating cells

`RenderHTML`
------------

> [!NOTE]
> This *Renderer* makes use of **Table**'s `row_render_opts` *dict*. Which means when calling **Table**'s `add_row` method, you can pass in a *dict* with the following keys/values:
> 
> * `html_row_attr`
> 
>   String HTML row attribute/s to add to the `tr` tag.
> 
> * `html_cell_attr`
> 
>   List of HTML cell attribute/s to add to `td`/`th` tags:
> 
>   * `color_disabled=False`
>   * `table_attr=''`
>   * `thead_attr=''`
>   * `tbody_attr=''`


Quick examples
--------------

```py
from dynamic_table import *
#Render the table indented 5 spaces, and cells padded 3 chars
my_table=Table(RenderText(indent=5,padding=3))
my_table.set_col_names(['Col1','Col2'])
my_table.add_row(['a','b'])
my_table.add_row(['c','d'])
my_table.render()
```

```py
#Render the same table above but in html with with a css class of "table":
my_table.set_table_renderer(RenderHTML(table_attr='class="table"'))
my_table.render()
```

```py
#Render the same table, but now in csv pipe '|' separated
my_table.set_table_renderer(RenderCSV(sep_char='|'))
my_table.render()
#Assign the built table to a variable:
built_table=str(my_table)
```


Table Filters
=============

Table objects can also be filtered using a set rules. This is done through the use of *Table* filter objects. They don't have any required parameters, but can take an optional `filter_txt` string when being created.

Filter Expression Syntax (items in parenthesis are optional):

```txt
([column ids]);[column id][operator][comparison value];\
              ([column id][operator][comparison value])...
```

Values for above:

Name                 | Explanation
---------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
`[column ids]`       | Comma-separated list of columns ids. Ranges are specified with a "-". e.g. 1-3. Ending the column ids with a '-' will be from that column id on the left of '-' to the end. Such as: "4-" would be from column 4 to the end.
`[column id]`        | Single column id.
`[operator]`         | One of: '>','<','>=','<=','!=','=','!/','/' which should be self explanatory. '/' is a "contains" operator.
`[comparison value]` | Value to compare against the column in [column id]. This can be a string, number, or even a date.


If the first rule is a comma separated list it is referred to as a column rule, all others are considered row rules. Additional row rules all have to be true for a row to pass the filter.

Filter expression examples:

```py
#Only print columns 1,3 and 4 and only rows where column 1 is after
#"2014-07-30 12:00:00"
1,3,4;1>"2014-07-30 12:00:00"
#Only print rows where column 4 is "Active" and column 2 has "tds" in it
4=Active;2/tds
```

If not providing a filter_txt when creating a *Table*Filter object, you can add more rules using the `add_row_rule` function and the `set_col_rule`. Which can be useful if the [comparison value] contains a semi-colon in it.

`*Table*Filter` provides the following useful functions:

Name                     | Explanation
-------------------------|----------------------------------------------------------------------------------------------
`filter_table(table)`    | returns a *Table* object that has been filtered according to the rules in the *Table* filter.
`set_col_rule(col_rule)` | Add a column rule. (String, comma separated ids) See filter Expression Syntax, above.
`add_row_rule(row_rule)` | Add a row rule. (String). See Filter Expression syntax above.


Examples of filtering:

```py
#Create a table with some data in it:
thing=dynamic_table.Table()
thing.set_col_names(['Col1','Col2','Col3','Miscellaneous'])
thing.add_row(['abc','blah','boo','stuff'])
thing.add_row(['def','blah','boo','stuff'])
thing.add_row(['ghi','blah','boo',''])
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
```

```py
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
```

To see more examples of how all this works out see the file: [`dynamic_table_examples.py`](https://github.com/absltkaos/python-dynamic-table/blob/master/dynamic_table_examples.py) [^1]

[^1]: https://github.com/absltkaos/python-dynamic-table/blob/5c5df6b0c29811d79827ca81663e7dcf11103f93/dynamic_table_examples.py
