#!/usr/bin/python
import dynamic_table

#Example with printing multiple variable length rows that have been added
#Then converting to an html table
print("==Example of a text table printing variable length rows.Then Printing in HTML==")
thing=dynamic_table.Table()
#Set the column headers
print("Setting column names: ['Col1','Col2','Col3','Miscellaneous']")
thing.set_col_names(['Col1','Col2','Col3','Miscellaneous'])
#Add a bunch of rows
print("Adding rows to table. some with too few columns, and some with more, as well as some colors")
thing.add_row(['a','blah','boo','stuff'])
thing.add_row(['a','blah','boo','stuff'])
thing.add_row(['a','blah','boo',''])
#Add a row that doesn't have enough columns (should auto fill and be empty
thing.add_row(['a','blah','boo'])
#Add some rows with color, the second column will have red text, other row will have two attributes set
thing.add_row(['c','Im colored','right?'],['','red'])
thing.add_row(['d','','Yay Multicolors'],['','','bg_brown,black'])
thing.render()
#Adding a row with an extra column should add another column with other cells being empty
thing.add_row(['b','hrmmmmmm','ahhh','stuffing','big empty'])
print("Printing Table")
thing.render()
print("Changing table to type: html")
thing.set_table_renderer(dynamic_table.RenderHTML())
print("Printing Table")
thing.render()
del(thing)

# header and table resizes based on set column lengths and padding etc...
print("\n==Example of a text table with set column widths, and modifying padding==")
thing=dynamic_table.Table(dynamic_table.RenderText(padding=2,indent=2))
print("Setting column names: ['Col1','Col2','Col3','Miscellaneous']")
thing.set_col_names(['Col1','Col2','Col3','Miscellaneous'])
print("Adding a row")
thing.add_row(['a','blah','boo','stuff'])
print("Printing table as is with dynamic columns and indentation")
thing.render()
print("Setting static column widths, with an extra column of width 6")
thing.set_col_widths([5,10,3,5,6])
print("Printing table with indentation, static columns, and padding")
thing.render()
del(thing)


#Multi table test
print("\n==Example of creating two tables to make sure that passed by reference values aren't shared==")
print("Making table: thing")
thing=dynamic_table.Table()
thing.set_col_names(['Col1','Col2','Col3','Miscellaneous'])
thing.add_row(['a','blah','boo','stuff'])
thing.add_row(['a','blah','boo','stuff'])
thing.add_row(['a','blah','boo',''])
thing.add_row(['a','blah','boo'])
thing.add_row(['b','hrmmmmmm','ahhh','stuffing','big empty'])
print("Printing table: thing")
thing.render()
print("Making table: my_table")
my_table=dynamic_table.Table()
my_table.add_row(['1','value1','value2','value3'])
my_table.add_row(['2','value1','value2','value3'])
my_table.add_row(['3','value1','value2','value3'])
my_table.add_row(['4','value1','value2','value3'])
print("Printing table: my_table")
my_table.render()
del(my_table)
del(thing)

#An Adhoc text table example
print("\n==Example of an adhoc printed text table with static columns==")
thing=dynamic_table.Table()
print("Setting column names: ['Col1','Col2','Col3','Miscellaneous']")
thing.set_col_names(['Col1','Col2','Col3','Miscellaneous'])
print("Setting static column widths")
thing.set_col_widths(['5','8','8','8'])
print("Printing header,rows and footer")
thing.print_header()
thing.print_row(['1','value1','value2','value3'])
thing.print_row(['2','value1','value2','value3'],['','green'])
thing.print_row(['3','value1','value2','value3'])
thing.print_row(['4','value1','value2','value3'])
thing.print_footer()
del(thing)

#Creating a csv table and printing in csv, csv with pipes, and text
print("\n==Example of creating a csv table, printing, printing with difference delimeter, and then printing in text==")
render_plain=dynamic_table.RenderCSV()
render_pipes=dynamic_table.RenderCSV(sep_char='|')
thing=dynamic_table.Table(render_plain)
#Set the column headers
print("Setting column names: ['Col1','Col2','Col3','Miscellaneous']")
thing.set_col_names(['Col1','Col2','Col3','Miscellaneous'])
#Add a bunch of rows
print("Adding some various rows")
thing.add_row(['a','blah','boo','stuff'])
thing.add_row(['a','blah','boo','stuff'])
thing.add_row(['a','blah','boo',''])
#Add a row that doesn't have enough columns (should auto fill and be empty
thing.add_row(['a','blah','boo'])
#Add some rows with color, the second column will have red text, other row will have two attributes set
thing.add_row(['c','Im colored','right?'],['','red'])
thing.add_row(['d','','Yay Multicolors'],['','','bg_brown,black'])
#Print standard CSV
print("Printing table as is")
thing.render()
print("Printing table with pipe chars")
thing.set_table_renderer(render_pipes)
thing.render()
print("Printing table in text")
thing.set_table_renderer(dynamic_table.RenderText())
thing.render()
print("Printing table in text with a bunch of custom modifiers like custom padding, padding chars, fill chars etc..")
thing.set_table_renderer(dynamic_table.RenderText(padding=1,indent=2,padding_char='_',fill_char='<'))
thing.render()

print("\n==Example of Creating a table, Creating a Filter, then applying the filter to the table==")
#Creating a table and filtering it
thing=dynamic_table.Table()
#Set the column headers
thing.set_col_names(['Col1','Col2','Col3','Miscellaneous'])
#Add a bunch of rows
thing.add_row(['abc','blah','boo','stuff'])
thing.add_row(['def','blah','boo','stuff'])
thing.add_row(['ghi','blah','boo',''])
thing.add_row(['jkl','blah','boo'])
thing.add_row(['20140801 4:00:00','Im colored','right?'],['','red'])
thing.add_row(['2013-04-21 1:00:00','','Yay Multicolors'],['','','bg_brown,black'])
thing.add_row(['2014-07-30 12:00:00','a'])
thing.add_row(['2014-07-30 16:00:00','b','c'],['green'])
print("Table before filtering")
thing.render()
#Create the Table filter
print("Creating a table filter that will only return columns 1, and 3 to the end. but only rows where column 1 is after: 2014-07-30 12:00:00")
tf=dynamic_table.TableFilter(filter_txt='1,3-;1>2014-07-30 12:00:00')
#Filter and render the table:
tf.filter_table(thing).render()
del(thing)
del(tf)

print("\n==Example of creating a filter and creating a table with the filter, so data is filtered as it is added==")
#Create a filter that only show column 1,3 and 4, and where column 1 is
# before '2014-07-30 12:00:00'
print("Creating a table filter that will only return columns 1, 3, and 4. but only rows where column 1 is before: 2014-07-30 12:00:00")
tf=dynamic_table.TableFilter(filter_txt='1,3,4;1<2014-07-30 12:00:00')
#Create a Table with the filter above that filters as it is being added
print("Creating table, and adding filter to it")
thing=dynamic_table.Table(table_filter=tf)
#Add some data and column names:
print("Adding some data to the table")
thing.set_col_names(['Col1','Col2','Col3','Miscellaneous'])
thing.add_row(['abc','blah','boo','stuff'])
thing.add_row(['def','blah','boo','stuff'])
thing.add_row(['ghi','blah','boo',''])
thing.add_row(['jkl','blah','boo'])
thing.add_row(['20140801 4:00:00','Im colored','right?'],['','red'])
thing.add_row(['2013-04-21 1:00:00','','Yay Multicolors'],['','','bg_brown,black'])
thing.add_row(['2014-07-30 12:00:00','a'])
thing.add_row(['2014-07-30 16:00:00','b','c'],['green'])
#Show the filtered table
print("Rendering the filtered data")
thing.render()
del(thing)

print("\n==Example of creating an HTML table with special attributes for table, tr and td tags==")
print("Creating HTML Renderer that will have a class attribute of 'tablesort'")
rend=dynamic_table.RenderHTML(table_attr='class="tablesort"')
thing=dynamic_table.Table(rend)
thing.set_col_names(['Col1','Col2','Col3','Miscellaneous'])
thing.add_row(['a','blah','boo','stuff'])
print("Create second row with a class attribute of 'my_class', and third cell with class attribute set to o_class")
thing.add_row(['a','blah','boo','stuff'],[],{'html_row_attr': 'class="my_class"', 'html_cell_attr': ['','','class="o_class"']})
thing.add_row(['a','blah','boo',''])
thing.add_row(['a','blah','boo'])
thing.add_row(['c','Im colored','right?'],['','red'])
print("Create 6th row that will have just a row attribute of class=my_class")
thing.add_row(['d','','Yay Multicolors'],['','','bg_brown,black'],{'html_row_attr': 'class="my_class"'})
thing.add_row(['b','hrmmmmmm','ahhh','stuffing','big empty'])
print("Rendering the HTML table")
thing.render()
del(rend)
del(thing)
