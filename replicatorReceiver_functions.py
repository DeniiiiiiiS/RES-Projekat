import time

def logger(message):
    time_now = time.localtime()
    with open("writer.txt", 'a') as f:
        a = f"{time_now.tm_mday}.{time_now.tm_mon}.{time_now.tm_year}, {time_now.tm_hour}:{time_now.tm_min}:{time_now.tm_sec}, {message}\n"
        f.write(f"{time_now.tm_mday}.{time_now.tm_mon}.{time_now.tm_year}, {time_now.tm_hour}:{time_now.tm_min}:{time_now.tm_sec}, {message}\n")
        return a
