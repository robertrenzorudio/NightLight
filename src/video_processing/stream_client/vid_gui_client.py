import io
import socket
import struct
from PIL import Image
import matplotlib.pyplot as pl

#gui_client_socket = socket.socket()
#gui_client_socket.connect(('0.0.0.0', 6667))  # ADD IP HERE
gui_sock = socket.socket()
gui_sock.bind(('0.0.0.0',6667))
gui_sock.listen(0)
connection = gui_sock.accept()[0].makefile('rb')

# try:
#     while True:

#         data = gui_client_socket.recv(8192)
#         print(data)


# finally:
#     print("closing socket")
#     gui_client_socket.close()

try:
	img = None
	while True:
		print("running")
		image_len = struct.unpack('<L',connection.read(struct.calcsize('<L')))[0]
		if not image_len:
			print("not image len")
			break
			#continue
		print(image_len)
		# Construct a stream to hold the image data and read the image
		# data from the connection
		image_stream = io.BytesIO()
		#print(connection.read(image_len))
		image_stream.write(connection.read(image_len)) #stuck here
		print("stream_written")
		# Rewind the stream, open it as an image with PIL and do some
		# processing on it
		image_stream.seek(0)
		image = Image.open(image_stream)
		print("image opened")

		if img is None:
			print("Image is none")
			img = pl.imshow(image)
		else:
			print("image is set")
			img.set_data(image)

		pl.pause(0.0001)
		pl.draw()

		# print('Image is %dx%d' % image.size)
		# image.verify()
		# print('Image is verified')
finally:
	gui_client_socket.close()