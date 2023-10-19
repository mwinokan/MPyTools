    
import re
from plotly.offline import plot

def fig_html(fig,include_plotlyjs=False,customdata_callback=False):

    # Get HTML representation of plotly.js and this figure
    plot_div = plot(fig, output_type='div', include_plotlyjs=include_plotlyjs)


    if customdata_callback:
        # Get id of html div element that looks like
        # <div id="301d22ab-bfba-4621-8f5d-dc4fd855bb33" ... >
        res = re.search('<div id="([^"]*)"', plot_div)
        div_id = res.groups()[0]

        # Build JavaScript callback for handling clicks
        # and opening the URL in the trace's customdata 
        js_callback = """
        <script>
        var plot_element = document.getElementById("{div_id}");
        plot_element.on('plotly_click', function(data){{
            console.log(data);
            var point = data.points[0];
            if (point) {{
                console.log(point.customdata);
                window.open(point.customdata);
            }}
        }})
        </script>
        """.format(div_id=div_id)

        # Build HTML string
        html_str = """{plot_div}
        {js_callback}
        """.format(plot_div=plot_div, js_callback=js_callback)

        return html_str

    else:
        return plot_div
