from flask import Flask, render_template, request, redirect, url_for, flash, send_file
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
            # Download and serve the thumbnail file
            thumbnail_path = youtube.download_youtube_thumbnail()
            if thumbnail_path:
                return send_file(thumbnail_path, as_attachment=True, download_name=os.path.basename(thumbnail_path))
            else:
                flash("Failed to download thumbnail", "danger")
                return redirect(url_for('index'))
        else:
            if "playlist" in url:
                # Download playlist videos and serve as a zip file
                youtube.download_playlist_videos()
                # Placeholder for the actual zip file creation and sending logic
                playlist_zip_path = os.path.join(download_path, 'playlist.zip')  # Ensure this path is correct
                return send_file(playlist_zip_path, as_attachment=True, download_name='playlist.zip')
            else:
                # Download single video and serve
                video_path = youtube.download_youtube_video()
                if video_path:
                    return send_file(video_path, as_attachment=True, download_name=os.path.basename(video_path))
                else:
                    flash("Failed to download video", "danger")
                    return redirect(url_for('index'))
    except Exception as e:
        flash(f"Error: {e}", "danger")
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
