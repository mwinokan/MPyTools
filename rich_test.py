
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

mrich.h1("header 1")
mrich.h2("header 2")
mrich.h3("header 3")

import time

with mrich.loading('Loading...'):
	time.sleep(2)
with mrich.clock('Loading...'):
	time.sleep(2)

for i in mrich.track(range(20), prefix='Sleeping zzzzz...'):
	time.sleep(0.2)

raise NotImplementedError
