from PIL import Image
from io import BytesIO
from model.model import News
from pipeline.data_dispose import make_dir


def save_image(content, path, repath):
    save_resize_image(content, repath)
    path = make_dir('./packup/' + path)
    with open(path, 'wb') as f:
        f.write(content)


def save_resize_image(content, path):
    path = make_dir('./packup/' + path)
    im = Image.open(BytesIO(content))
    w, h = im.size
    times = int(w / 200)
    if times >= 2:
        im.thumbnail((w // times, h // times))
    im.save(path)


def random_image():
    to_path = 'App/info/image.txt'
    news = News().set_no_field(img_filename='').select(limit=100, oderby='time', isasc=False)
    for n in news:
        if len(n.img_filename) > 20:
            with open(to_path, 'a', encoding='utf-8') as f:
                f.write(str(n.id) + '\n')


if __name__ == "__main__":
    pass
