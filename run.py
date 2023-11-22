import datetime
import os
import time
from functools import wraps
import yaml
from log import logger
from mail import Mail, check_email, LocalDB
from multiprocessing import Pool as ThreadPool
from ecrypt_user import encrypt_user, decrypt_user
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed, wait


def time_count(func):
    @wraps(func)
    def inner(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f'Затрачено времени {total_time} ')
        return result

    return inner


@time_count
def write_crm():
    """
    Основной функция для запуска работы скрипта, в котором считываются данные из yaml файла и если файл с пользователями
     не зашифрован шифруется при помощи rsa и сохраняется в директории с проектом.
     Если зашифрован раскодировываем и запускается паралелльная обработка пользователей в мультипроцессорной обработке
    :return:
    """

    with open("config.yaml", 'r') as stream:
        data_loaded = yaml.safe_load(stream)
    file_name: str = data_loaded['file_name']
    processing: int = data_loaded['Processing']
    user = []
    if os.path.isfile(file_name):
        encrypt_user(file_name)
    users: list = decrypt_user(file_name)
    for row in users:
        email_user: str
        password: str
        email_user, password = row[0].split(';')
        if not check_email(email_user):
            logger.info(f'{datetime.datetime.now().replace(microsecond=0)}Wrong email {email_user}')
            continue
        else:
            user.append((email_user.strip(), password.strip()))
    # for email, password in user:
    #     Mail().connect_email(email, password)
    with ProcessPoolExecutor(max_workers=processing) as executor:
        future_list = []
        # for email, password in user:
        future_list = executor.map(Mail().connect_email, user)
    # future_list.append(future)
    # executor.map(Mail().connect_email, user)
    # wait(future_list)
    # logger.info('Delete last day')
    # LocalDB().delete_by_date()
    # for f in as_completed(future_list):\
    #     print(f.result())


if __name__ == '__main__':
    logger.info('Run to Work')
    write_crm()
    logger.info('End Work')
