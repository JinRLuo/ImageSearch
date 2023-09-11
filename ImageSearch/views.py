import os
import shutil
import zipfile
import logging
from cn_clip.clip import load_from_name
from django.core.files import File
from django.shortcuts import render
from Image import models
from ImageSearch import settings
import torch
import traceback

from ImageSearch.ImageCollection import ImageCollection
from django.core.files.storage import default_storage
import base64
from PIL import Image
from io import BytesIO


logger = logging.getLogger(__name__)

device = "cuda" if torch.cuda.is_available() else "cpu"
#device = 'cpu'
logging.info("current use device: %s", device)

collections = {
    'CN-CLIP ViT-L/14': ImageCollection(custom_model=False, dv=device, model_path='', collection_name='image_cn_clip_vit_l_14'),
#    'jx3-0-0-1-ep1 ViT-L/14': ImageCollection(custom_model=True, dv=device, model_path='l-jx3-0-0-1-ep1.pt', collection_name='image_jx3_0_0_1_ep1_vit_l_14'),
    'jx3-11-l-001 ViT-L/14': ImageCollection(custom_model=True, dv=device, model_path='jx3-11-l-001.pt', collection_name='image_jx3_11_l_001_ep1_vit_l_14')
}

current_select_model = 'jx3-11-l-001 ViT-L/14'


def index(request):
    return render(request, 'index.html', {"active_tab":"work_search"})


def word_search_image(request):
    if request.method == 'POST':
        search_text = request.POST.get('search_text', '')
        result_count = int(request.POST.get('result_count', 20))
        model_name = request.POST.get('model_name', 'jx3-11-l-001 ViT-L/14')
        imageCollection = collections[model_name]
        if imageCollection is None:
            logger.error("not find model")
            return
        logger.info("word search images: %s", search_text)
        images = imageCollection.search_image(search_text, result_count)
        return render(request, 'index.html', {'search_label': search_text, 'image_paths': images, 'model_name': model_name,"active_tab":"work_search"})

    return render(request, 'index.html', {"active_tab":"work_search"})


def image_search_image(request):
    if request.method == 'POST':
        upload_image = request.FILES.get('uploaded_image')
        if upload_image is None:
            logger.error("upload_image is None!")
            return render(request, 'index.html', {"active_tab":"image_search"})
        result_count = int(request.POST.get('result_count', 20))
        model_name = request.POST.get('model_name', 'jx3-11-l-001 ViT-L/14')
        image_path = os.path.join(settings.MEDIA_ROOT, upload_image.name)
        default_storage.save(image_path, upload_image)
        imageCollection = collections[model_name]
        if imageCollection is None:
            logger.error("not find model")
            return render(request, 'index.html', {"active_tab":"image_search"})
        logger.info("image search images: %s", image_path)

        with Image.open(image_path) as img:
            buffered = BytesIO()
            img.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()

        images = imageCollection.image_search_images(image_path, result_count)
        return render(request, 'index.html', {'uploaded_image_base64_image_search': img_str, 'res_image_paths': images, 'model_name': model_name, 'active_tab': 'image_search'})

    return render(request, 'index.html', {"active_tab":"image_search"})

def image_zt_tag(request):
    if request.method == 'POST':
        uploaded_file = request.FILES.get('uploaded_image')
        file_path = os.path.join(settings.MEDIA_ROOT, uploaded_file.name)
        default_storage.save(file_path, uploaded_file)
        labs_text = request.POST.get('labs_text', '')
        model_name = request.POST.get('model_name', 'jx3-11-l-001 ViT-L/14')
        imageCollection = collections[model_name]
        if imageCollection is None:
            logger.error("not find model")
            return
        labs = labs_text.split(',')
        restext = imageCollection.classF( file_path,labs)

        with Image.open(file_path) as img:
            buffered = BytesIO()
            img.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()

        return render(request, 'index.html', {'restext': restext,"active_tab":"image_zt_tag",'labs_text': labs_text,'uploaded_image_base64': img_str})

    return render(request, 'index.html', {"active_tab":"image_zt_tag"})


# 上传所有图片 通过zip文件压缩
def upload_images(request):
    if request.method == 'POST':
        zip_file = request.FILES.get('zip_file')
        if zip_file:
            handle_uploaded_zip(zip_file)
    return render(request, 'index.html', {})


def handle_uploaded_zip(zip_file):
    # 清空图片库 重新生成collection
    for collection in collections.values():
        collection.clear_image()

    temp_dir = os.path.join(settings.MEDIA_URL, 'temp_image')
    os.makedirs(temp_dir, exist_ok=True)
    shutil.rmtree(temp_dir)
    os.makedirs(temp_dir, exist_ok=True)

    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)

    cnt = 0
    for root, _, files in os.walk(temp_dir):
        for filename in files:
            image_path = os.path.join(root, filename)
            with torch.no_grad():
                try:
                    for collection in collections.values():
                        collection.insert_image(image_path)
                    cnt = cnt + 1
                except BaseException as e:
                    logger.error("import image %s fail! Error: %s", image_path, traceback.format_exc())
                    continue
                logger.info("import image %s...  success count[%d]", image_path, cnt)

    logger.info("成功导入%d张图片!", cnt)


