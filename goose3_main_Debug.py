from goose3 import Goose
import requests
from copy import deepcopy

import lxml.html
from lxml import etree

from goose3.text import innerTrim, encodeValue, get_encodings_from_content, smart_str


def goose_run():
    url = "https://portal.edirepository.org/nis/metadataviewer?packageid=edi.8.4&contentType=application/xml"
    # url = "https://www.pythonforbeginners.com/requests/using-requests-in-python"
    # url = "https://www.facebook.com/135125923270755/posts/friendsi-would-like-you-to-consider-a-proposal-for-an-anti-drone-action-please-p/140479216068759/"
    rqs = requests.get(url)
    g = Goose()
    import pdb; pdb.set_trace()
    article = g.extract(raw_html=rqs.content)
    import pdb; pdb.set_trace()



if __name__ == '__main__':
    goose_run()
