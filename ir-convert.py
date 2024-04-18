import secrets
from flask import Flask, request, render_template, send_from_directory, jsonify, flash, redirect, url_for
import os
from werkzeug.utils import secure_filename
import numpy as np
from skimage.transform import resize
import rawpy
import imageio
from dataclasses import dataclass

from channel_transform import channel_transform
from params import Params

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'raf', 'cr2', 'nef', 'dng'}
app.config['MAX_CONTENT_LENGTH'] = 128 * 1024 * 1024  # 128 Megabyte Limit
app.config['OUTPUT_FOLDER'] = 'static/output'


def allowed_file(filename):
    return '.' in filename and filename.rsplit(
        '.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/')
def index():
    return render_template('./index.html', params=list(Params().__dict__.items()))


def render_rgb(rgb, params, ):
    id = secrets.token_urlsafe(16)
    output_path = os.path.join(app.config['OUTPUT_FOLDER'], f'test-{id}.png')

    fs_rgb = channel_transform(rgb, params)
    fs_rgb = fs_rgb / fs_rgb.max() * 255.0
    fs_rgb = fs_rgb.astype(np.uint8)

    imageio.imsave(output_path, fs_rgb)

    return output_path.replace('static/', '')  # return web-friendly path


@app.route('/output/<filename>')
def output_file(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename, mimetype='image/png')


@app.route('/process', methods=['POST'])
def process_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        cached_array_name = f'{filepath}.npy'
        print("saving image to ", cached_array_name)
        if os.path.exists(cached_array_name):
            rgb = np.load(cached_array_name)
        else:
            with rawpy.imread(filepath) as raw:
                rgb = raw.postprocess()
                if rgb.shape[1] > 512:
                    new_height = int(rgb.shape[0] * 512 / rgb.shape[1])
                    rgb = resize(rgb, (new_height, 512, 3))
                np.save(cached_array_name, rgb)

        params = Params()
        for key, value in params.__dict__.items():
            if key.startswith("gamma"):
                multiplier = 10.0
            else:
                multiplier = 1.0
            setattr(params, key, float(request.form.get(key, value)) * multiplier)
        output_path = render_rgb(rgb, params)
        return jsonify({'image_url': output_path})

    flash('Invalid file format')
    return redirect(url_for('index'))


"""
with rawpy.imread(path) as raw:
    rgb = raw.postprocess()
    if rgb.shape[0] > 1024:
        new_height = int(rgb.shape[0] * 1024 / rgb.shape[1])
        rgb = resize(rgb, (new_height, 1024, 3))
    # convert to float
    params = Params()
    for gamma in range(0, 10):
        params.gammaRx = 0.2 + gamma * 0.05
        render_rgb(rgb, params)
"""
