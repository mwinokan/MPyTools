# MPyTools

Set of custom python packages for various odds and ends.

- [mcol](#mcol) defines a set of colours as ANSI escape strings.
- [module](#module) provides the module() function that calls lmod to persistently load softare on EUREKA.
- [mout](#mout) provides a set of functions for formatted console output.
- [mplot](#mplot) provides a variety of plotting functions using matplotlib.

## mcol

Provides ANSI escape strings for colourised terminal output that fits into a colour scheme. I.e. green success messages, red errors, orange warnings, yellow filenames etc...

For example to output an error message: 

```
import mcol
print(mcol.error + "Error: Something went wrong!" + mcol.clear)
```

Please note that for most cases the functions in [mout](#mout) will achieve the same functionality with less code:

```
import mout
mout.errorOut("Something went wrong!")
```

Colour strings in the scheme: 

*   `varName` Variable names, turqoise
*   `varType` Variable types/units, pink
*   `func` Function/script name, underlined turqoise
*   `file` Filename/path, yellow
*   `error` For error messages, bold red
*   `success` For success messages, bold green
*   `warning` For warning messages, bold green
*   `result` For results/variable values, blue
*   `arg` For function arguments, lime

General colour strings:

*   `clear`
*   `bold`
*   `inverse`
*   `underline`

*   `red`
*   `green`
*   `yellow`

## module

Access the unix `modulecmd` from within python. Load and unload packages, which will persist so that subsequest `exec()` or `os.system()` commands will see them. Comma delimited arguments instead of spaces:

```
import module
module.module('load','lammps/2018/mpi+intel-xe_2017_3')
```

## mout

Write formatted output to the console.

*General console message*

`mout.out(string,printScript=False,end="\n")`

*   `string` The message to be displayed
*   `printScript` Prepend the output with the name of the script?
*   `end` End the output with this string.

*Output a variable and its value*

`def varOut(name, value, unit="",valCol="",precision=8,printScript=False,end="\n")`

*   `name` The name of the variable
*   `value` Value of the variable
*   `unit` Unit string for the variable
*   `valCol` Custom colour string for the value
*   `precision` Significant figures of the value output
*   `printScript` Prepend the output with the name of the script?
*   `end` End the output with this string.

*Warning message*

`def warningOut(string,printScript=False,code=None,end="\n")`

*   `string` The message to be displayed
*   `printScript` Prepend the output with the name of the script?
*   `code` The warning code
*   `end` End the output with this string.

*Error message*

`def errorOut(string,printScript=False,fatal=False,code=None,end="\n"):`

*   `string` The message to be displayed
*   `printScript` Prepend the output with the name of the script?
*   `fatal` Exit the script?
*   `code` The warning code
*   `end` End the output with this string.

## mplot

Functions for plotting data using [matplotlib](#https://matplotlib.org).

### Requirements

`mplot` requires `matplotlib`

### Usage

*Plotting 2D data:*

`mplot.graph2D(xdata,ydata,ytitles=None,filename=None,show=True,xmin=None,xmax=None,ymin=None,ymax=None,xlab='x',ylab='y',title=None)`

*   `xdata` List of x-axis values
*   `ydata` List of y-axis values or list of list of y-axis values.
*   `ytitles` List of titles for the different y-axis data-sets.
*   `filename` Output filename.
*   `show` Open a GUI window with the plot?
*   `xmin` Lower bound of x-axis.
*   `xmax` Upper bound of x-axis.
*   `ymin` Lower bound of y-axis.
*   `ymax` Upper bound of y-axis.
*   `xlab` x-axis label.
*   `xlab` y-axis label.
*   `title` Title of plot.
*   `verbosity` Verbosity level. Every nested function call will pass `verbosity=verbosity-1`.

**Example:**
```
import mplot
xdata = [1,2,3,4]
ydata1 = [1,2,3,4]
ydata2 = [3,4,5,6]
mplot.graph2D(xdata,ydata1,filename="test1.png",title="Test 1")
mplot.graph2D(xdata,[ydata1,ydata2],ytitles=["ydata1","ydata2"],filename="test2.png",title="Test 2")
```

*Open figures in GUI windows*

To show all the figures created in the interactive session:

`mplot.show(verbosity=1)`

