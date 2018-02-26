# -*- coding: utf-8 -*- 
import socket
import time
import os

def get_header(code):
    h = ''
    if (code == 200):
	h = 'HTTP/1.1 200 OK\n'
    elif (code == 404):
	h = 'HTTP/1.1 404 Not found\n'
    current_date = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
    h += 'Date: ' + current_date +'\n'
    h += 'Server: MY_FIRST_SERVER!!!\n'
    h += 'Connection: keep-alive\n'
    return h

    
def get_response(request):
    split_request = request.split('\n')
    request_path = ''
    if len(split_request[0].split(' ')) != 1:
	request_path = split_request[0].split(' ')[1]
    response_code = -1
    response_content = request_path
    if request_path == '/':
	user_agent = 'Wow, who are you???\n'
	for s in split_request:
	    if s.split(' ')[0] == 'User-Agent:':
	        user_agent = (str)(s[11:])
	        break
    	response_code = 200
    	response_content = b"<html><body><p>Hello, mister!</p><p>You are: " + user_agent + "</p></body></html>"
    
    elif request_path == '/test/':
	response_code = 200
	response_content = b"<html><body>"+ request + "</body></html>"
    
    elif request_path == '/media/':
	response_code = 200
    	file_names = os.listdir('files')
	response_content = b"<html><body>"
	for name in file_names:
	    response_content+= "<p>" + '<a href="/media/"'+ str(name) +'">' + str(name) + ' file</a>' + "</p>"
	response_content+= "</body></html>"
    
    elif len(request_path.split('/')) > 2 and request_path.split('/')[1] == 'media':
	file_name = request_path.split('/')[2]
	try:
	    f = open("files/" + file_name, 'rb')
	    response_content = f.read()
	    f.close()
	    response_code = 200
	except Exception as e:
	    print 'File not found\n'
	    response_code = 404
	    response_content = b"<html><body>" + "<p>Error 404: File not found</p>" + "</body></html>"
    
    else:
	response_code = 404
	response_content = b"<html><body><p>Page not found</p></body></html>"
    
    server_response = get_header(response_code)
    server_response += 'Content-Type: text/html\n'
    server_response += 'Content-Length: ' +(str)(len(response_content)) + '\n\n'
    
    return server_response + response_content


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('localhost', 8000))  #
server_socket.listen(0)  #


print 'Started'

while 1:
    try:
        (client_socket, address) = server_socket.accept()
        print 'Got new client', client_socket.getsockname()  #
        request_string = client_socket.recv(2048)  #
        client_socket.send(get_response(request_string))  #
        client_socket.close()
    except KeyboardInterrupt:  #
        print 'Stopped'
        server_socket.close()  #
        exit()
