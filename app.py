from flask import Flask, render_template, request, send_file
import yt_dlp
import os
import uuid

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url', '').strip()

        if not url:
            return "<h3 style='color:red;'>Please provide a video URL.</h3>"

        try:
            output_path = f"downloads/video_{uuid.uuid4().hex}.mp4"
            os.makedirs("downloads", exist_ok=True)

            ydl_opts = {
                'format': 'best',
                'outtmpl': output_path,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            return send_file(output_path, as_attachment=True)

        except Exception as e:
            return f"<h3 style='color:red;'>Download error: {e}</h3>"

    return render_template('yt.html')

if __name__ == '__main__':
    app.run(debug=True)
