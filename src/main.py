import time
import RPi.GPIO as GPIO

# -----------------------
# Константы.
# -----------------------

# Порты GPIO.
GPIO_TRIGGER = 23
GPIO_ECHO    = 24

# Остальные константы.
TIME_BETWEEN_MEASURE = 1 # Время между измерениями (в секундах).
SOUND_SPEED = 34300 # Скорость звука в воздухе.

# -----------------------
# Нужные функции.
# -----------------------

def measure():
  # Измерить расстояние.
  GPIO.output(GPIO_TRIGGER, True)
  time.sleep(0.00001) # Импульс должен быть 10 мкс, чтобы модуль выпустил сигнал.
  GPIO.output(GPIO_TRIGGER, False)
  start = time.time() # Время отправки сигнала.

  # Ждем, пока модуль не выставит ECHO в 1 (т.е. пока не отправит сигнал).
  while GPIO.input(GPIO_ECHO)==0:
    start = time.time()

  # Пока сигнал не пришел обратно - обновляем время прилета.
  while GPIO.input(GPIO_ECHO)==1:
    stop = time.time()

  pulse_duration = stop-start # Время прохождения импульса.
  distance = (pulse_duration * SOUND_SPEED)/2 # Вычисление расстояния.

  return distance

# Измерить среднее расстояние за 3 вычисления.
def measure_average():
  # Делаем 3 измерения и возвращаем среднее.
  distance1=measure()
  time.sleep(0.1)
  distance2=measure()
  time.sleep(0.1)
  distance3=measure()
  distance = distance1 + distance2 + distance3
  distance = distance / 3
  return distance

# -----------------------
# Основная программа.
# -----------------------

# Используем BCM номера (например, GRIO 23)
# вместо фактических порядковых номеров пинов.
GPIO.setmode(GPIO.BCM)

print("Измерение расстояния")

# Устанавливаем пины на вход и выход.
GPIO.setup(GPIO_TRIGGER,GPIO.OUT)  # Trigger (издать звуковой сигнал).
GPIO.setup(GPIO_ECHO,GPIO.IN)      # Echo (сообщить, что приняли обратно сигнал).

# Устанавливаем Trigger в False (низкий уровень сигнала). 
GPIO.output(GPIO_TRIGGER, False)

# Оборачиваем основные действия в блок try так,
# мы можем обработать нажатие пользователем "CTRL-C"
# и запустить функцию очистки GPIO. Кроме того, мы
# ограждаем пользователя от возможных сообщениях об ошибках.
try:

  while True:

    distance = measure_average()
    print ("Расстояние : %.1f сантиметров." % distance)
    time.sleep(TIME_BETWEEN_MEASURE)

except KeyboardInterrupt:
  # Пользователь нажал CTRL-С.
  # Сбрасываем настройки GPIO.
  GPIO.cleanup()

