from flask import Flask, render_template, request, jsonify, send_file, Response, send_from_directory
from flask_wtf import CSRFProtect
import yt_dlp
import os
import tempfile
import json
from queue import Queue, Empty
from pathlib import Path
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
csrf = CSRFProtect(app)

# Configure download directory
DOWNLOADS_DIR = Path('downloads')
DOWNLOADS_DIR.mkdir(exist_ok=True)

@app.route('/favicon.ico')
def favicon():
    return '', 204  # No content response for favicon

# Create downloads directory if it doesn't exist
DOWNLOADS_DIR = Path('downloads')
DOWNLOADS_DIR.mkdir(exist_ok=True)

def progress_hook(d):
    if d['status'] == 'downloading':
        progress = {
            'status': 'downloading',
            'downloaded_bytes': d.get('downloaded_bytes', 0),
            'total_bytes': d.get('total_bytes', 0),
            'speed': d.get('speed', 0),
            'eta': d.get('eta', 0),
            'filename': d.get('filename', '')
        }
        
        if progress['total_bytes'] > 0:
            progress['percentage'] = (progress['downloaded_bytes'] / progress['total_bytes']) * 100
        else:
            progress['percentage'] = 0
            
        app.progress_queue.put(progress)
    elif d['status'] == 'finished':
        app.progress_queue.put({'status': 'finished', 'filename': d.get('filename', '')})

@app.route('/progress')
def progress():
    def generate():
        while True:
            if not hasattr(app, 'progress_queue'):
                app.progress_queue = Queue()
            
            try:
                progress = app.progress_queue.get(timeout=30)  # 30 second timeout
                yield f"data: {json.dumps(progress)}\n\n"
                
                if progress['status'] == 'finished':
                    break
            except Empty:
                # Send a keepalive message every 30 seconds
                yield f"data: {json.dumps({'status': 'alive'})}\n\n"
                
    return Response(generate(), mimetype='text/event-stream')

def get_best_format(formats):
    """Select best available MP4 format with both video and audio"""
    # First try to find a format that has both video and audio in MP4
    mp4_formats = [
        f for f in formats
        if f.get('ext') == 'mp4' and 
        f.get('acodec') != 'none' and 
        f.get('vcodec') != 'none'
    ]
    
    if mp4_formats:
        # Sort by quality and pick the best one
        best_format = max(mp4_formats, 
                         key=lambda f: (f.get('height', 0), f.get('tbr', 0)))
        return best_format['format_id']
    
    # If no combined format found, look for any MP4 format
    mp4_only = [f for f in formats if f.get('ext') == 'mp4']
    if mp4_only:
        best_mp4 = max(mp4_only,
                      key=lambda f: (f.get('height', 0), f.get('tbr', 0)))
        return best_mp4['format_id']
    
    # Last resort - try the best format available
    return '18'

def get_video_info(url):
    ydl_opts = {
        'quiet': True,
        'format': 'bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4] / bv*+ba/b',  # Flexible format selection
        'no_warnings': True,
        'prefer_ffmpeg': True,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-us,en;q=0.5'
        },
        'extractor_args': {
            'youtube': {
                'player_client': ['android'],
                'player_skip': ['webpage', 'configs', 'js']
            }
        }
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            app.logger.info(f"Attempting to download video from {url}")
            info = ydl.extract_info(url, download=False)
            
            # Find the best compatible format
            format_id = get_best_format(info['formats'])
            if not format_id:
                return {'error': 'No compatible format found'}
            
            # Get the selected format info
            format_info = next(f for f in info['formats'] if f['format_id'] == format_id)
            app.logger.info(f"Selected format: {format_info}")
            
            # Get filesize - try multiple possible sources
            filesize = format_info.get('filesize') or format_info.get('filesize_approx')
            if not filesize and 'filesize_approx' in info:
                filesize = info['filesize_approx']
            
            # Ensure we always return a number for filesize
            if not filesize or filesize < 0:
                filesize = 0
            
            return {
                'title': info['title'],
                'duration': info.get('duration', 0),
                'resolution': f"{format_info.get('height', 0)}p",
                'filesize': filesize
            }
        except Exception as e:
            app.logger.error(f"Error fetching video info: {str(e)}")
            return {'error': str(e)}

@app.route('/')
def index():
    return render_template('youtube_downloader.html')

@app.route('/info', methods=['POST'])
def get_info():
    url = request.json.get('url')
    if not url:
        return jsonify({'error': 'No URL provided'})
    return jsonify(get_video_info(url))

@app.route('/download', methods=['POST'])
def download():
    url = request.json.get('url')
    if not url:
        return jsonify({'error': 'No URL provided'})

    # Validate URL format
    if not url.startswith(('http://', 'https://', 'www.youtube.com', 'youtube.com', 'youtu.be')):
        return jsonify({'error': 'Invalid YouTube URL'})

    # Create a temporary directory for this download
    temp_dir = tempfile.mkdtemp()
    app.logger.info(f"Created temp directory: {temp_dir}")

    try:
        # First get video info to get the title
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            try:
                info = ydl.extract_info(url, download=False)
                format_id = get_best_format(info['formats'])
                if not format_id:
                    return jsonify({'error': 'No compatible format found'})
                
                # Create a safe filename from the title
                safe_title = ''.join(c for c in info['title'] if c.isalnum() or c in (' ', '-', '_')).strip()
                safe_title = safe_title.replace(' ', '_')  # Replace spaces with underscores
                output_path = os.path.join(temp_dir, f"{safe_title}.mp4")
                app.logger.info(f"Output path: {output_path}")
                app.logger.info(f"Using format ID: {format_id}")
            except Exception as e:
                app.logger.error(f"Error extracting info: {str(e)}")
                return jsonify({'error': str(e)})
        
        ydl_opts = {
            'format': 'bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4] / bv*+ba/b',  # Flexible format selection
            'outtmpl': output_path,
            'quiet': True,
            'no_warnings': True,
            'prefer_ffmpeg': True,
            'progress_hooks': [progress_hook],
            'retries': 10,
            'fragment_retries': 10,
            'skip_unavailable_fragments': True,
            'merge_output_format': 'mp4',
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-us,en;q=0.5'
            },
            'extractor_args': {
                'youtube': {
                    'player_client': ['android'],
                    'player_skip': ['webpage', 'configs', 'js']
                }
            }
        }
        
        try:
            app.logger.info(f"Downloading video with options: {ydl_opts}")
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            app.logger.info(f"Video downloaded to {output_path}")
            
            if not os.path.exists(output_path):
                raise Exception(f"Download completed but file not found at {output_path}")
                
            download_name = os.path.basename(output_path).replace('_', ' ')  # Convert back to spaces for display
            return send_file(
                output_path,
                as_attachment=True,
                download_name=download_name,
                mimetype='video/mp4'
            )
        except Exception as e:
            app.logger.error(f"Error during download: {str(e)}")
            return jsonify({'error': str(e)})
    except Exception as e:
        app.logger.error(f"Error serving file: {str(e)}")
        return jsonify({'error': f'Error serving file: {str(e)}'})
    finally:
        # Clean up temp directory
        try:
            if os.path.exists(temp_dir):
                app.logger.info(f"Cleaning up temp directory: {temp_dir}")
                for f in os.listdir(temp_dir):
                    file_path = os.path.join(temp_dir, f)
                    try:
                        if os.path.isfile(file_path):
                            os.unlink(file_path)
                        elif os.path.isdir(file_path):
                            os.rmdir(file_path)
                    except Exception as e:
                        app.logger.error(f"Error removing {file_path}: {str(e)}")
                os.rmdir(temp_dir)
                app.logger.info("Temp directory cleaned up successfully")
        except Exception as e:
            app.logger.error(f"Error during cleanup: {str(e)}")

@app.route('/serve-file', methods=['POST'])
def serve_file():
    try:
        temp_path = request.json.get('temp_path')
        if not temp_path:
            return jsonify({'error': 'No file path provided'})
        
        if not os.path.exists(temp_path):
            return jsonify({'error': 'File not found on server'})
        
        if not os.path.isfile(temp_path):
            return jsonify({'error': 'Invalid file path'})
        
        return send_file(
            temp_path,
            as_attachment=True,
            download_name=os.path.basename(temp_path),
            mimetype='video/quicktime'
        )
    except Exception as e:
        app.logger.error(f'Error serving file: {str(e)}')
        return jsonify({'error': f'Error serving file: {str(e)}'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5012))
    app.run(debug=True, port=port)
