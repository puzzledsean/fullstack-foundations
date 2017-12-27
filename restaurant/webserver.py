from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

# initialize a session
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()


class webServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # list all restaurants
            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += '''<a href="/restaurants/new">Make new restaurant</a>'''
                restaurants = session.query(Restaurant).all()
                for restaurant in restaurants:
                    output += '<h1>{}</h1>'.format(restaurant.name) 
                    output += '<a href="/restaurants/{}/edit">Edit</a>'.format(restaurant.id)
                    output += '</br>'
                    output += '''<a href="/restaurants/{}/delete">Delete</a>'''.format(restaurant.id)
                output += "</body></html>"
                self.wfile.write(output)
                return
            # create new restaurant name
            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants/new'><h2>Make a new restaurant</h2><input name="newRestaurant" type="text" ><input type="submit" value="Create"> </form>'''
                self.wfile.write(output)
                return
            # edit restaurant name
            if self.path.endswith("/edit"):
                restaurant_id = self.path.split('/')[2]
                edit_restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
                if edit_restaurant != []:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = ""
                    output += "<html><body>"
                    output += '<h1>{}</h1>'.format(edit_restaurant.name)
                    output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants/{}/edit'><h2>Edit restaurant name</h2><input name="editedRestaurant" type="text" ><input type="submit" value="Edit"> </form>'''.format(restaurant_id)
                    output += "</body></html>"
                    self.wfile.write(output)
                return
            # delete restaurant name
            if self.path.endswith("/delete"):
                restaurant_id = self.path.split('/')[2]
                edit_restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
                if edit_restaurant != []:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = ""
                    output += "<html><body>"
                    output += '<h1>Are you sure you want to delete {}?</h1>'.format(edit_restaurant.name)
                    output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants/{}/delete'><input type="submit" value="Delete"></form>'''.format(restaurant_id)
                    output += "</body></html>"
                    self.wfile.write(output)
                return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            # delete restaurant name
            if self.path.endswith('/delete'):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                
                restaurant_id = self.path.split('/')[2]
                del_restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
                session.delete(del_restaurant) 
                session.commit()
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()
                return

            # edit old restaurant name
            if self.path.endswith('/edit'):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('editedRestaurant')[0]
                
                print(messagecontent)
                # form has restaurant name, add to db
                if messagecontent:
                    restaurant_id = self.path.split('/')[2]
                    edit_restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
                    edit_restaurant.name = messagecontent
                    session.add(edit_restaurant)
                    session.commit()
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()
                return

            # create new restaurant 
            if self.path.endswith('/restaurants/new'):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurant')[0]
                
                print(messagecontent)
                # form has restaurant name, add to db
                if messagecontent:
                    new_restaurant = Restaurant(name = messagecontent)
                    session.add(new_restaurant)
                    session.commit()
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()
            return

        except:
            pass


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()
