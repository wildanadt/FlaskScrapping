import crochet
crochet.setup()

from flask import Flask, render_template, request, jsonify, make_response, redirect, url_for
from scrapy.crawler import CrawlerRunner
from scrapy import signals
from scrapy.signalmanager import dispatcher
import time
from scraper.scraper.spiders.ojk_cfs_scrapping import OjkCFS_Spider
import re


app = Flask(__name__)
app.config['DEBUG'] = True

    
output = ''
resp_status = False

crawler_runner = CrawlerRunner()

@app.route("/")
def hello():
    return render_template('ojk.html')

@app.route('/cfs', methods= ['POST'])
def postCfs():
    if request.method == 'POST':
        
        crochet.wait_for_reactor(scrape_with_crochet(post_form=request.form.to_dict(), post_head=request.headers.to_wsgi_list()))
        global resp_status

        while resp_status == False:
            time.sleep(0.5)
        
        resp_status = False
        return output



@crochet.run_in_reactor
def scrape_with_crochet(post_form, post_head):

    dispatcher.connect(_crawler_result, signal=signals.item_scraped)
    eventual = crawler_runner.crawl(OjkCFS_Spider, req_head = post_head, req_form = post_form)
    # dispatcher.connect(_crawler_stop, signals.engine_stopped)
    return eventual


def _crawler_result(item, response, spider):
    global output
    global resp_status
    resp_status = True
    output = item['resp']
    output = re.sub("https://127.0.0.1:5000", "https://cfs.ojk.go.id", output)
    print(output)


# def _crawler_stop():
    # crawler_runner.stop()


# if __name__ == "__main__":
#     app.run(debug=True)