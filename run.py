import os
import time
from functools import wraps
import yaml
from log import logger
from mail import Mail, check_email, LocalDB
from multiprocessing import Pool as ThreadPool
from ecrypt_user import encrypt_user, decrypt_user
from concurrent.futures import ThreadPoolExecutor


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
                logger.info(f'Wrong email {email_user}')
                continue
            else:
                user.append((email_user, password))
        # for email, password in user:
        #     Mail().connect_email(email, password)
        with ThreadPoolExecutor(max_workers=None) as executor:
            # for email, password in user:
            #     executor.submit(Mail().connect_email, email, password)
            executor.map(Mail().connect_email, user)


if __name__ == '__main__':
    logger.info('Run to Work')
    write_crm()
    LocalDB().delete_by_date()
    logger.info('End Work')
