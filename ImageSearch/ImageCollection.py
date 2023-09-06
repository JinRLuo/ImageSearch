import os

import torch
from PIL import Image
from cn_clip import clip
from cn_clip.clip import load_from_name

from ImageSearch import settings
from ImageSearch.milvue_utils import create_milvus_collection, rebuild_milvus_collection


class ImageCollection:
    DIM = 768

    def __init__(self, custom_model, model_path, dv, collection_name):
        self.collection_name = collection_name
        if custom_model:
            self.model, self.preprocess = load_from_name(
                os.path.join(settings.STATIC_URL, model_path),
                device=dv,
                vision_model_name="ViT-L-14",
                text_model_name="RoBERTa-wwm-ext-base-chinese", input_resolution=224
            )
        else:
            self.model, self.preprocess = load_from_name("ViT-L-14", device=dv, download_root='./')
        self.collection = create_milvus_collection(collection_name, ImageCollection.DIM)
        self.device = dv

    def clear_image(self):
        rebuild_milvus_collection(self.collection_name, ImageCollection.DIM)

    def insert_image(self, image_path):
        with torch.no_grad():
            img = self.preprocess(Image.open(image_path)).unsqueeze(0).to(self.device)
            image_feature = self.model.encode_image(img)
            image_feature /= image_feature.norm(dim=-1, keepdim=True)
            if self.device == 'cpu':
                vct = image_feature.numpy().tolist()[0]
            else:
                vct = image_feature.cpu().numpy().tolist()[0]
            data = {'path': str(image_path), 'image_vector': vct}
            self.collection.insert(data)
        return

    def search_image(self, text, topn=5):
        labels = [text]
        text = clip.tokenize(labels).to(self.device)
        with torch.no_grad():
            text_features = self.model.encode_text(text)
            text_features /= text_features.norm(dim=-1, keepdim=True)
        if self.device == 'cpu':
            vct = text_features.numpy().tolist()[0]
        else:
            vct = text_features.cpu().numpy().tolist()[0]
        search_params = {"metric_type": "L2", "params": {"nprobe": 10}}
        self.collection.load()
        results = self.collection.search([vct], 'image_vector', search_params, topn, output_fields=['path'])
        return results[0].ids
