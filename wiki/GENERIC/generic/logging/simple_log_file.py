import logging

logging.basicConfig(
    format='%(asctime)s %(levelname)s: %(message)s',
    # filename='myapp.log',
    level=logging.DEBUG,
)
logging.info('Started')
logging.debug('Finished')
logging.warning('Not added')
