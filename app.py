# import requirements package for the code
from flask import Flask, jsonify
from requests import get as get_request
from bs4 import BeautifulSoup

app = Flask(__name__)

# define extractor
def extractor(channel_id):
    extractor.proxies_tmp_list = []
    extractor.proxies = {""}
    
    html = get_request("https://t.me/s/" + channel_id).content
    soup = BeautifulSoup(html)
    links = soup.find_all("a")

    for tag in links:
        proxy = tag.get("href", None)

        if (proxy != None) and  ("/proxy?" and "&secret=" and "&port=" and "server=" in proxy):
            extractor.proxies.add(proxy)
            
    extractor.proxies.remove("")

# define proxy slicer
def proxy_slicer(proxy):
    new_proxy = "".join(proxy.split("?")[1:]).split("&")

    if "@" in new_proxy[-1]:
        new_proxy = new_proxy[:-1]

    proxy_stuff = []

    for i in new_proxy:
        proxy_stuff.append(i.split("=")[1])

    proxy_slicer.server = proxy_stuff[0]
    proxy_slicer.port = proxy_stuff[1]
    proxy_slicer.secret = proxy_stuff[2]

# route api path
@app.route("/mtproxy/api/<channel_id>")
def extractor_api(channel_id=None):
    extractor(channel_id)

    proxies_json = []

    counter = 0

    for proxy in extractor.proxies:
        proxy_slicer(proxy)
        
        server = proxy_slicer.server
        port = proxy_slicer.port
        secret = proxy_slicer.secret

        proxies_json.append({
            f"proxy{counter}": {
                "link":proxy,
                "server": server,
                "port": port,
                "secret": secret
                }
            }
            )

        counter += 1

    return jsonify(proxies_json)


# run flask app
if __name__ == '__main__':
    app.run()
