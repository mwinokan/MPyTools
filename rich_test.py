
import mrich

print(mrich.console)

mrich.print('[red]Hello')
mrich.out('[red]Hello')
mrich.rule('[red]Hello')

mrich.console.log('[red] Hello')

mrich.warning("warning text goes here")
mrich.error("error text goes here")
mrich.success("success text goes here")
mrich.debug("debug text goes here")
mrich.header("header text goes here")
mrich.title("title text goes here")
mrich.reading("reading text goes here")
mrich.writing("writing text goes here")
mrich.var("thing",123)
mrich.var("thing",True, unit='truths')
# mrich.error("Warning!")
# mrich.success("Warning!")
# mrich.header("Warning!")
# mrich.title("Warning!")
# mrich.debug("Warning!")
# mrich.info("Warning!")
# mrich.reading("Warning!")
# mrich.writing("Warning!")
# mrich.var("Warning!")

import time

with mrich.loading('Loading...'):
	time.sleep(2)
with mrich.clock('Loading...'):
	time.sleep(2)

raise NotImplementedError
