from vklabs.goose3 import Goose
import requests


def goose_run():
    url = "https://portal.edirepository.org/nis/metadataviewer?packageid=edi.8.4&contentType=application/xml"
    # url = "https://www.pythonforbeginners.com/requests/using-requests-in-python"
    # url = "https://www.facebook.com/135125923270755/posts/friendsi-would-like-you-to-consider-a-proposal-for-an-anti-drone-action-please-p/140479216068759/"
    rqs = requests.get(url)
    g = Goose()
    article = g.extract(raw_html=rqs.content)
    print(article.title)


if __name__ == '__main__':
    goose_run()
