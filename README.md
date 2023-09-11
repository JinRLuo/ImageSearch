# ImageSearch

### 安装cn_clip
```
pip install -r Chinese-CLIP/requirements.txt
pip install ./Chinese-CLIP
```

### 启动django服务
```
python manage.py runserver 0.0.0.0:8080
```
### 目录结构
图片库上传后会保存在media目录下
训练好的模型需要放在static目录下才能加载
```
ImageSearch
├─Chinese-CLIP/
├─Image/
│  └─...    #代码目录
├─ImageSearch/
│  └─...    #代码目录
├─log/
├─media/
│  └─temp_image
│      └─... #图片库
├─static/
│  └─...     #训练好的模型
├─templates/
   └─...     #bootstrap前端模板文件
```