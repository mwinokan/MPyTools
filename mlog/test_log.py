#!/usr/bin/env python3

import mcol
from logs import setup_logger

logger = setup_logger('MLogTest')

logger.debug('debug')
logger.info('info')
logger.out('out')
# logger.var('variable', 'value', 'unit')
logger.reading('path')
logger.writing('path')
logger.warning('message')
logger.success('success')
logger.header('header')
logger.title('title')
logger.error('error')
logger.fatal('fatal')
logger.critical('critical')

logger.var('variable','value')
logger.var('variable','value',dict(unit='unit'))
logger.var('variable','value',dict(color='file'))
logger.var('variable','value',dict(unit='unit',color='file'))
