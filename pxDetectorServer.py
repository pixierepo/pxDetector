from PXDetector import PXDetector
import flask
import json
import io

app = flask.Flask(__name__)


@app.route("/detect_motion", methods=["POST"])
def detect_motion():	
	data = {"success": False}
	if flask.request.is_json:
		try:
			print("Detecting motion...")
			req_data = flask.request.get_json()
			timeout = req_data['timeout']
			if timeout is not None:
				detection_time = px.detect_motion(timeout)
			else:
				detection_time = px.detect_motion()

			if detection_time is not None:
				data['success'] = True
				data['detection_time'] =detection_time

		except(e):
			print(e)
			data['error'] = "Bad request."
	return flask.jsonify(data)


@app.route("/get_still", methods=["POST"])
def get_still():	
	data = {"success": False}
	try:
		print("Grabbing still frame...")
		frame = px.get_still()
		if frame is not None:
			# data = flask.make_response(frame)
			# data.headers.set('Content-Type', 'image/jpeg')
			# data.headers.set('Content-Disposition', 'attachment', filename='%s.jpg' % pid)
			return flask.send_file(
		    io.BytesIO(frame),
		    mimetype='image/jpeg',
		    as_attachment=True,
		    attachment_filename='still_image.jpg')
	except(e):
			print(e)
			data['error'] = "Bad request."
	return flask.jsonify(data)


if __name__ == "__main__":
	global px
	px=PXDetector()
	app.run(host='0.0.0.0')