# MPyTools

Set of custom python packages for various odds and ends.

- ```mcol``` defines a set of colours as ANSI escape strings.
- ```mout``` provides a set of functions for formatted console output.
- ```module``` provides the module() function that calls lmod to persistently load softare on EUREKA.
- `mplot` provides a variety of plotting functions using matplotlib.

## Requirements

- `mplot` requires `matplotlib`

## Usage

### mplot

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

