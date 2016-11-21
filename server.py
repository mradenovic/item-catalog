'''Project: Item catalog

Item Catalog is the fifth project built during completion of the Udacity's
Nanodegree program Full Stack Web Developer. Run this file to start the server.
'''

from catalog import app


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
