from flask import Flask, render_template, request, redirect, url_for, flash
from yUtility import YoutubeUtility
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    download_path = './downloads'
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    try:
        youtube = YoutubeUtility(url, download_path)
        if request.form.get('download_thumbnail'):
            youtube.download_youtube_thumbnail()
            flash("Thumbnail downloaded successfully!", "success")
        else:
            if "playlist" in url:
                youtube.download_playlist_videos()
                flash("Playlist downloaded successfully!", "success")
            else:
                youtube.download_youtube_video()
                flash(f"Video '{youtube.get_video_title()}' downloaded successfully!", "success")
    except Exception as e:
        flash(f"Error: {e}", "danger")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
