
from http.server import BaseHTTPRequestHandler,HTTPServer
from sqlalchemy import create_engine
from  sqlalchemy.orm import sessionmaker
from  te import Base, Restaurant,MenuItem
import cgi,cgitb
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBsession =sessionmaker (bind=engine)
session=DBsession()
class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "<h1>Hello!</h1>"
                output += '''<form method='post'  action='/hello'>
                <h2>What would you like me to say?</h2>
                <input type="text"  name="message" id="message" >
                <input type="submit" value="Submit">
                </form>'''
                output += "</body></html>"


                self.wfile.write(bytes(output, "UTF-8"))
                print(output)
                return
            if self.path.endswith("/ola"):
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()

                output = "<html><body>ola<a href='/hello'> ggg</a></body></html>"
                self.wfile.write(bytes(output, "UTF-8"))
                print(output)
                return
            if self.path.endswith("/edit"):
                restaurantIDPath = self.path.split("/")[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(
                    id=restaurantIDPath).one()
                if myRestaurantQuery:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = "<html><body>"
                    output += "<h1>"
                    output += myRestaurantQuery.name
                    output += "</h1>"
                    output += "<form method='POST' enctype='multipart/form-data' action = '/restaurants/%s/edit' >" % restaurantIDPath
                    output += "<input name = 'newRestaurantName' type='text' placeholder = '%s' >" % myRestaurantQuery.name
                    output += "<input type = 'submit' value = 'Rename'>"
                    output += "</form>"
                    output += "</body></html>"
                    self.wfile.write(bytes(output, "UTF-8"))



            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                restaurants=session.query(Restaurant).all()

                output = "<html><body>ola ggg</a>"
                for restaurant in restaurants:
                    output+=restaurant.name
                    output+="<br>"
                    output+="<a href='/restaurants/%s/edit'>edit</a>"%restaurant.id
                    output+="<br>"

                output+="<a href='restaurants/new'>new restaurant</a><br>"
                output+="</body></html>"
                self.wfile.write(bytes(output, "UTF-8"))
                print(output)
                return
            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                output = "<html><body>ola ggg</a>"
                output+="<form method='post' action='/restaurants/new'>"
                output+="<input type='text' name='resname' placeholder='new name'><input type='submit' value='submit'></form>"
                output+="</body></html>"
                self.wfile.write(bytes(output, "UTF-8"))
                print(output)
                return

        except IOError:
            self.send_error(404,"file not found %s" % self.path)


    def do_POST(self):
        try:
            if self.path.endswith("/edit"):
                resid = self.path.split("/")[2]
                form = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD': 'POST'})
                messagecontent = form.getvalue("resname")
                resquery = session.query(Restaurant).filter_by(id=resid).one()
                if resquery != []:
                    resquery.name = messagecontent
                    session.add(resquery)
                    session.commit()
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()

            if self.path.endswith("/restaurants/new"):
                form = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD': 'POST'})
                messagecontent = form.getvalue("resname")
                print(messagecontent)
                newrestaurant=Restaurant(name=messagecontent)
                session.add(newrestaurant)
                #session.delete(newrestaurant)
                session.commit()
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location','restaurants')
                self.end_headers()


            self.send_response(301)

            form = cgi.FieldStorage( fp=self.rfile, headers=self.headers,environ={'REQUEST_METHOD':'POST'})
            messagecontent = form.getvalue("message")
            self.end_headers()
            print(messagecontent)

            #ctype = cgi.parse_header(self.headers.getheader('Content-type'))
            #pdict = cgi.parse_header(self.headers.getheader('Content-type'))

            #if ctype == 'multipart/form-data':

                #fields=cgi.parse_multipart(self.rfile , pdict)
                #messsagecontent =fields.get('message')
            output = ""
            output += "<html><body>"
            output += " <h2> Okay, how about this: </h2>"
            output += "<h1> %s </h1>" % messagecontent
            output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you ggglike me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
            output += "</body></html>"
            self.wfile.write(bytes(output, "UTF-8"))
            print(output)
            return
        except:
            pass


def main():
    try:
        port=8080
        server = HTTPServer(('',port),webserverHandler)
        print("webserver is running on port %s" %port)
        server.serve_forever()
    except KeyboardInterrupt:
        print ("c pressed stopping webserver........")
        server.socket.close();
if __name__ == '__main__':
    main()
