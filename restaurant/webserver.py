# -*- coding: utf-8 -*-
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from restaurants import *


class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            output = ""
            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output += "<html><body><h1>Restaurants</h1>"
                output += "<h2><a href='/restaurants/new'>Create New Restaurant</a></h2>"
                restaurants = get_restaurants()
                for restaurant in restaurants:
                    output += restaurant.name
                    output += "<br><a href='/restaurants/%s/edit'>Edit</a>" % restaurant.id
                    output += " | <a href='/restaurants/%s/delete'>Delete</a><br><br>" % restaurant.id
                output += "</body></html>"
                self.wfile.write(output)
            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output += "<html><body><h1>Create Restaurant</h1>"
                output += "<form method='POST' enctype='multipart/form-data' "
                output += "action='/restaurants/new'><h2>Restaurant name:</h2>"
                output += "<input name='restaurant' type='text'>"
                output += "<input type='submit' value='Create'></form>"
                output += "<a href='/restaurants'>Go back</a>"
                output += "</body></html>"
                self.wfile.write(output)
            if self.path.endswith("/edit"):
                restaurant_id = self.path.split("/")[2]
                restaurant = get_restaurant(restaurant_id)
                if restaurant:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()

                    output += "<html><body><h1>Edit Restaurant</h1>"
                    output += "<form method='POST' enctype='multipart/form-data' "
                    output += "action='/restaurants/%s/edit'><h2>Restaurant name:</h2>" % restaurant_id
                    output += "<input name='restaurant' type='text' value='%s'>" % restaurant.name
                    output += "<input type='submit' value='Update'></form>"
                    output += "<a href='/restaurants'>Go back</a>"
                    output += "</body></html>"
                    self.wfile.write(output)
            if self.path.endswith("/delete"):
                restaurant_id = self.path.split("/")[2]
                restaurant = get_restaurant(restaurant_id)
                if restaurant:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()

                    output += "<html><body><h1>Delete Restaurant</h1>"
                    output += "<form method='POST' enctype='multipart/form-data' "
                    output += "action='/restaurants/%s/delete'>" % restaurant_id
                    output += "<h2>Are you sure you want to delete %s?</h2>" % restaurant.name
                    output += "<input type='submit' value='Delete'></form>"
                    output += "<a href='/restaurants'>Go back</a>"
                    output += "</body></html>"
                    self.wfile.write(output)
        except IOError:
            self.send_error(404, "File Not Found %s" % self.path)

    def do_POST(self):
        try:
            output = ""
            if self.path.endswith("/restaurants/new"):
                print self.headers.getheader('Content-Type')
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))

                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('restaurant')
                    insert_restaurant(messagecontent[0])
                    output += "<html><body>"
                    output += "<h1>Restaurant Created: %s </h1>" % messagecontent[0]
                    output += "<a href='/restaurants'>Go back</a>"
                    output += "</body></html>"
                    self.wfile.write(output)
            if self.path.endswith("/edit"):
                restaurant_id = self.path.split("/")[2]
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))

                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('restaurant')
                    update_restaurant(restaurant_id, messagecontent[0])
                    output += "<html><body><h2>Restaurant Updated: </h2>"
                    output += "<h1> %s </h1>" % messagecontent[0]
                    output += "<a href='/restaurants'>Go back</a>"
                    output += "</body></html>"
                    self.wfile.write(output)
            if self.path.endswith("/delete"):
                restaurant_id = self.path.split("/")[2]
                delete_restaurant(restaurant_id)
                output += "<html><body><h2>Restaurant Deleted</h2>"
                output += "<a href='/restaurants'>Go back</a>"
                output += "</body></html>"
                self.wfile.write(output)
        except:
            pass


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webserverHandler)
        print "Web server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print "Stopping web server..."
        server.socket.close()


if __name__ == '__main__':
    main()
