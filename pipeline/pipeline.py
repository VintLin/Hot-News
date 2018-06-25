from pipeline.word_frequency import *
from pipeline.data_dispose import *
from pipeline.image_dispose import *


def transfer():
    print('BEGIN')
    rm_tree(PATH)
    rm_tree('App/static/news_image')
    copy_tree('packup/page', 'App/templates/page')
    copy_tree('packup/news_image', 'App/static/news_image')
    make_dir(PATH + 'type/')
    make_dir(PATH + 'time/')
    make_dir(PATH + 'times/')
    save_type_time()
    save_news_by_type()
    save_news_by_time()
    save_type_news_list()
    save_time_news_list()
    save_time_page()
    random_image()
    get_word_frequency()
    print('END')