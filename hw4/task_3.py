import multiprocessing
import time
import codecs
from datetime import datetime


LOG_FILE = "hw4/artifacts/interaction_log.txt"

def worker_a(queue_from_main, queue_to_b):
    """
    Процесс A:
    - берет сообщения из очереди от главного процесса
    - делает их маленькими буквами
    - кидает в очередь для процесса B
    """
    while True:
        if not queue_from_main.empty():
            msg = queue_from_main.get()
            
            # Если получили exit - заканчиваем работу
            if msg == "exit":
                queue_to_b.put("exit")
                write_log("Process A: получил exit, завершаюсь")
                break
                
            # Обрабатываем сообщение
            small_msg = msg.lower()
            queue_to_b.put(small_msg)
            write_log(f"Process A: получил '{msg}', отправил '{small_msg}' в B")

def worker_b(queue_from_a, queue_to_main):
    """
    Процесс B:
    - берет сообщения из очереди от процесса A
    - ждет 5 секунд
    - кодирует в rot13
    - печатает на экран
    - отправляет обратно в главный процесс
    """
    while True:
        if not queue_from_a.empty():
            msg = queue_from_a.get()
            
            if msg == "exit":
                queue_to_main.put("exit")
                write_log("Process B: получил exit, завершаюсь")
                break
            
            time.sleep(5)
            
            # Кодируем сообщение
            coded_msg = codecs.encode(msg, 'rot13')
            print(f"Process B выводит: {coded_msg}")
            
            # Отправляем в главный процесс
            queue_to_main.put(coded_msg)
            write_log(f"Process B: получил '{msg}', отправил '{coded_msg}' в main")

def write_log(message):
    """Пишем сообщение в лог файл с текущим временем"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{now}] {message}\n")

def main():
    open(LOG_FILE, "w").close()
    write_log("Программа запущена")
    
    # Создаем очереди для общения между процессами
    main_to_a = multiprocessing.Queue()
    a_to_b = multiprocessing.Queue()
    b_to_main = multiprocessing.Queue()
    
    # Запускаем оба процесса
    write_log("Запускаем процесс A")
    proc_a = multiprocessing.Process(target=worker_a, args=(main_to_a, a_to_b))
    proc_a.start()
    
    write_log("Запускаем процесс B")
    proc_b = multiprocessing.Process(target=worker_b, args=(a_to_b, b_to_main))
    proc_b.start()
    
    try:
        # Главный цикл программы
        while True:
            
            user_input = input("Введите сообщение (exit для выхода): ")
            
            # Отправляем в процесс A
            main_to_a.put(user_input)
            write_log(f"Main: отправил '{user_input}' в A")
            
            # Проверяем не хочет ли пользователь выйти
            if user_input == "exit":
                write_log("Main: получил команду exit")
                break
            
            # Проверяем не прислал ли что-то процесс B
            if not b_to_main.empty():
                msg_from_b = b_to_main.get()
                write_log(f"Main: получил от B '{msg_from_b}'")
                
    except KeyboardInterrupt:
        main_to_a.put("exit")
        write_log("Main: завершение по Ctrl+C")
    
    proc_a.join()
    proc_b.join()
    write_log("Все процессы завершены")

if __name__ == "__main__":
    main()