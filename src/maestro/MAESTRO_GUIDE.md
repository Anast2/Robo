# Пакет `maestro` — Полный обзор

## Назначение

**Maestro** — это центральный "мозг" робота Plantroid. Он выполняет роль **оркестратора**, который:

1. **Координирует все модули** — связывает входные модули (речь, камера, сенсоры) с выходными (TTS, лицо, движение)
2. **Управляет диалогом** — отслеживает состояние разговора через конечные автоматы
3. **Принимает решения** — выбирает что и как отвечать, на основе эмоций и контекста
4. **Обрабатывает проблемы** — реагирует на уведомления от сенсоров почвы

---

## Структура директории

```
src/maestro/
├── maestro/                    # Исходный код Python
│   ├── __init__.py            # Маркер пакета
│   ├── MAESTRO.py             # Главный модуль (точка входа)
│   ├── ChatBot.py             # NLP: pattern matching + sentiment
│   ├── StateMachines.py       # Определения 3-х конечных автоматов
│   ├── simple_state_machine.py # Универсальный класс FSM
│   ├── dialogue.json          # Шаблоны диалогов для каждого состояния
│   └── utils.py               # Утилиты (Wikipedia, Dictionary, SQL)
│
├── launch/
│   └── maestro_launch.py      # ROS2 launch файл
│
├── test/                      # Тесты (только линтеры)
│   ├── test_copyright.py
│   ├── test_flake8.py
│   └── test_pep257.py
│
├── resource/maestro           # Маркер для ament
├── package.xml                # ROS2 метаданные пакета
├── setup.py                   # Python setuptools конфигурация
├── setup.cfg                  # Конфигурация установки
│
└── *.md                       # Документация
```

---

## Файлы и их назначение

### Ядро системы

| Файл | Назначение |
|------|------------|
| **`MAESTRO.py`** | Главный ROS2-узел. Содержит классы `MAESTRO` и `PersonDetector`. Точка входа: `main()` запускает два потока — основной оркестратор и детектор людей |
| **`simple_state_machine.py`** | Универсальная реализация конечного автомата (FSM). Используется для создания всех трёх машин состояний |
| **`StateMachines.py`** | Определяет три экземпляра StateMachine: `problem_state_machine`, `busy_state_machine`, `dialogue_state_machine` с их состояниями и переходами |
| **`ChatBot.py`** | NLP-модуль: pattern matching через NLTK, анализ эмоций через DistilBERT, детекция вопросов/команд |
| **`dialogue.json`** | JSON-конфигурация диалогов. Для каждого состояния — список regex-паттернов и возможных ответов |
| **`utils.py`** | Вспомогательные функции: запросы к Wikipedia/Dictionary, работа с SQLite, генерация случайных фонем |

### Инфраструктура ROS2

| Файл | Назначение |
|------|------------|
| **`package.xml`** | Зависимости пакета (rclpy, std_msgs, rooted_interfaces, etc.) |
| **`setup.py`** | Регистрирует entry point: `maestro = maestro.MAESTRO:main` |
| **`launch/maestro_launch.py`** | Launch-файл для запуска через `ros2 launch maestro maestro_launch.py` |

---

## Три параллельных State Machine

Maestro управляет тремя конечными автоматами одновременно:

### 1. Problem State Machine (2 состояния)

```
OK ←→ Problem
```

- Переходит в `Problem` при событии `problem_detected` (сенсоры обнаружили проблему)
- Возвращается в `OK` при `problem_cleared`

### 2. Busy State Machine (2 состояния)

```
Free ←→ Busy
```

- `move` → робот занят (Busy)
- `finished` → робот свободен (Free)

### 3. Dialogue State Machine (15 состояний)

Основной автомат диалога:

```
Silent → CheckProblemAndBusy → StartDialogue1 → AskIfHumanIsAvailable → AnnounceProblem → WaitHumanQuestion1 → ...
         ↓
       SpokeToMe → BusyCheck → LookAtUser → StartDialogue2 → AnswerHuman → WaitHumanQuestion2 → Goodbye → Silent
```

**Все состояния:**
- `Silent` — ожидание
- `SpokeToMe` — человек обратился к роботу
- `BusyCheck` — проверка занятости
- `LookAtUser` — поворот к пользователю
- `AnnounceBusy` — сообщение о занятости
- `StartDialogue1/2` — инициализация диалога
- `AnswerHuman` — ответ на вопрос
- `WaitHumanQuestion1/2` — ожидание вопроса
- `CheckProblemAndBusy` — проверка проблем и занятости
- `AskIfHumanIsAvailable` — спросить, свободен ли человек
- `AnnounceProblem` — объявить о проблеме
- `ClearProblem` — проблема решена
- `Goodbye` — прощание

---

## Как работает система (потоки данных)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              MAESTRO NODE                                    │
│                                                                             │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐                  │
│  │   Problem    │    │    Busy      │    │   Dialogue   │                  │
│  │     FSM      │    │     FSM      │    │     FSM      │                  │
│  │  OK ↔ Problem│    │ Free ↔ Busy  │    │ 15 states    │                  │
│  └──────────────┘    └──────────────┘    └──────────────┘                  │
│         ↑                   ↑                   ↑                          │
└─────────┼───────────────────┼───────────────────┼──────────────────────────┘
          │                   │                   │
          │                   │                   │
    ┌─────┴─────┐       ┌─────┴─────┐       ┌─────┴─────┐
    │notification│       │busy_state │       │ message   │
    │   Topic   │       │ publisher │       │  Topic    │
    └─────┬─────┘       └─────┬─────┘       └─────┬─────┘
          │                   │                   │
          ↓                   ↓                   ↓
   ┌────────────┐      ┌────────────┐      ┌────────────┐
   │  Sensors   │      │ rooted_busy│      │ listening  │
   │  Module    │      │   Module   │      │   Module   │
   └────────────┘      └────────────┘      └────────────┘
```

---

## Классы

### 1. Класс `StateMachine` (simple_state_machine.py:3)

Универсальная реализация конечного автомата (FSM).

#### Конструктор

```python
def __init__(self, name, states, events, initial_state, transition_table)
```

| Параметр | Описание |
|----------|----------|
| `name` | Имя автомата (для отладки) |
| `states` | Список возможных состояний |
| `events` | Список возможных событий |
| `initial_state` | Начальное состояние |
| `transition_table` | Словарь переходов `{state: {event: next_state}}` |

#### Методы

| Метод | Описание |
|-------|----------|
| `transition(event)` | Выполняет переход по событию |
| `get_current_state()` | Возвращает текущее состояние |
| `set_current_state(state)` | Устанавливает состояние (если оно валидно) |
| `add_event(event)` | Добавляет новое событие в список |
| `add_state(state)` | Добавляет новое состояние |
| `remove_event(event)` | Удаляет событие и все связанные переходы |
| `remove_state(state)` | Удаляет состояние и все переходы к/от него |
| `add_transition(...)` | Добавляет новый переход |
| `validity_check()` | Проверяет консистентность таблицы переходов |
| `reset()` | Сбрасывает автомат в начальное состояние |

---

### 2. Класс `PersonDetector` (MAESTRO.py:46)

Отдельный ROS-узел для детекции людей в кадре.

#### Конструктор

```python
def __init__(self, busy_state_machine, dialogue_state_machine)
```

- Создаёт узел `maestro_person_detector`
- Инициализирует интерфейс камеры
- Создаёт publisher на топик `seenTopic`
- Сохраняет ссылки на state machines

#### Методы

| Метод | Описание |
|-------|----------|
| `get_vision()` | Синхронный запрос к сервису камеры (тип 3 = детекция человека). Блокирует выполнение до получения ответа |
| `detection_routine()` | Основной цикл детекции. Проверяет: если диалог в `Silent` и робот `Free` — запрашивает камеру. При обнаружении человека публикует `"Seen"` в `seenTopic` |

---

### 3. Класс `MAESTRO` (MAESTRO.py:78)

Главный класс-оркестратор. ROS-узел `plantroid`.

#### Подписки (subscribers)

| Топик | Callback | Описание |
|-------|----------|----------|
| `messageTopic` | `cb_function_conversation` | Входящая речь человека |
| `notificationTopic` | `cb_function_notification` | Уведомления от сенсоров |
| `seenTopic` | `cb_function_seen` | Событие "увидел человека" |
| `busy_state_publisher` | `cb_function_busy_listener` | Статус занятости робота |

#### Publishers

| Топик | Описание |
|-------|----------|
| `ListenBlockTopic` | Блокировка микрофона (эхоподавление) |
| `emotionTopic` | Команды для лицевой экспрессии |

#### Service Interfaces

```python
self.vision_control  # Камера
self.busy_interface  # Статус занятости
self.sensor_reader   # Датчики почвы
self.llm             # LLM (Ollama)
self.tts             # Text-to-Speech
self.memory_access   # База данных диалогов
self.robot_mover     # Навигация
```

#### Параметры из launch-файла

| Параметр | Описание |
|----------|----------|
| `store_chat_log` | Сохранять ли логи диалогов |
| `keep_eye_contact` | Следить ли за человеком взглядом |
| `pc_mode` | Режим работы (PC/embedded) |
| `store_emotion_change` | Записывать изменения эмоций |
| `robot_name` | Имя робота |
| `dialogue_json` | Путь к файлу с шаблонами диалогов |

#### Callback-методы

| Метод | Описание |
|-------|----------|
| `cb_function_conversation()` | **Главный обработчик речи.** Парсит `"текст;meta;эмоция"`, анализирует эмоции (голос+контент+лицо), генерирует ответ, отправляет на TTS |
| `cb_function_notification()` | Обрабатывает уведомления сенсоров. Парсит `"sensor:level:priority"`, переводит problem_state в `Problem`, меняет лицо на `sad`/`thirsty` |
| `cb_function_seen()` | При обнаружении человека переводит диалог в `CheckProblemAndBusy`. Если есть проблемы — инициирует приветствие |
| `cb_function_busy_listener()` | Синхронизирует busy_state_machine с внешним состоянием занятости |
| `cb_timeout()` | Обработчик таймаута. Если человек молчит 20 сек — прощается и сбрасывает диалог |

#### Методы работы с сервисами

| Метод | Описание |
|-------|----------|
| `avoidEcho()` | Публикует сигнал блокировки микрофона |
| `busy_request(request)` | Синхронный запрос к busy-сервису (`get`/`set_busy`/`set_idle`) |
| `check_busy()` | Получает текущий статус занятости |
| `set_busy()` | Устанавливает статус "занят" |
| `set_idle()` | Устанавливает статус "свободен" |
| `get_vision()` | Запрос описания сцены (тип 8) |
| `set_face(emotion)` | Публикует эмоцию в `emotionTopic` |
| `get_face_emotion()` | Запрашивает эмоцию лица человека с камеры (тип 0) |
| `get_sensor(num)` | Читает значение датчика по номеру |
| `get_llm_response(msg)` | Синхронный запрос к LLM (llama3) |

#### Методы обработки диалога

| Метод | Описание |
|-------|----------|
| `emotion_fusion(emotion_list)` | Объединяет 3 источника эмоций голосованием (мажоритарное) |
| `generate_response(data, emotion)` | Генерирует ответ: сначала pattern matching через ChatBot, затем обработка спецкоманд (`sensor:`, `wikipedia:`, `vision_check`), потом перефразирование через LLM |
| `assign_prosody(utterance, method)` | Назначает просодию (speed, pitch, volume). Методы: `random`, `angry`, `happy`, `neutral`, `surprise`, `sadness` |
| `store_dialogue_exchange(...)` | Сохраняет обмен репликами в SQLite |
| `dialogue_initialization_routine(speech)` | Цикл инициализации диалога: определяет события и переходы состояний |
| `dialogue_finalization_routine(speech)` | Завершение: если состояние `Wait*` — запускает таймер таймаута |

---

## Функции в ChatBot.py

| Функция | Описание |
|---------|----------|
| `chatter(phrase, pairs)` | Pattern matching через NLTK Chat. Возвращает ответ или `None` |
| `sentiment_analysis(phrase)` | Классификация эмоций через EmTract-DistilBERT. Возвращает: `neutral`, `happy`, `sad`, `anger`, `surprise` |
| `question_detection(phrase)` | Определяет, является ли фраза вопросом (по `?`, wh-words, порядку слов) |
| `get_subject(phrase)` | Извлекает подлежащее из вопроса через POS-tagging |
| `is_command(sentence)` | Определяет, является ли предложение командой (императив) |
| `check_busy(sentence)` | Определяет согласие/отказ по ключевым словам + sentiment analysis |

---

## Функции в utils.py

| Функция | Описание |
|---------|----------|
| `now()` | Возвращает текущее время как кортеж |
| `write_sql(dbLoc, cmd, values)` | Записывает данные в SQLite |
| `gibberish()` | Генерирует случайную "тарабарщину" из фонем (для тестирования TTS) |
| `wikipedia_query(title)` | Запрос к Wikipedia (2 предложения) |
| `dictionary_query(word)` | Запрос определения слова через PyDictionary |

---

## Вспомогательные функции в MAESTRO.py

| Функция | Описание |
|---------|----------|
| `emotion_2_prompt(emotion)` | Конвертирует эмоцию в текстовый промпт (`"in a happy tone"` и т.д.) |
| `process_notifications(notifications)` | Формирует текстовое описание проблем с почвой |
| `maestro()` | Entry point: создаёт и запускает MAESTRO node |
| `person_detection(...)` | Entry point: создаёт и запускает PersonDetector node |
| `main()` | Запускает оба узла в отдельных потоках |

---

## Пример потока диалога

```
1. listening_module публикует: "Hello robot;meta;happy"
                                    ↓
2. MAESTRO.cb_function_conversation() парсит сообщение
                                    ↓
3. ChatBot.sentiment_analysis() → определяет эмоцию контента
                                    ↓
4. MAESTRO.get_face_emotion() → запрашивает эмоцию лица с камеры
                                    ↓
5. MAESTRO.emotion_fusion() → объединяет 3 источника эмоций
                                    ↓
6. dialogue.json["AnswerHuman"] → ищет regex-паттерн для "Hello"
                                    ↓
7. ChatBot.chatter() → возвращает "Hello!" или "Hi!"
                                    ↓
8. MAESTRO.get_llm_response() → перефразирует через LLM
                                    ↓
9. MAESTRO.assign_prosody() → добавляет [speed, pitch, volume]
                                    ↓
10. MAESTRO.tts.send_request() → отправляет на синтез речи
                                    ↓
11. emotionTopic ← публикует "happy" для лица робота
```

---

## dialogue.json — Формат

Ключ = состояние FSM, значение = список `[regex, [ответы]]`:

```json
{
  "AnswerHuman": [
    ["(hi|hello|howdy)", ["Hello!", "Hi!", "Hello, my friend!"]],
    ["what is your name", ["My name is Plantroid!"]],
    ["(.*)soil moisture(.*)", ["sensor:3"]],
    ["what is (.*)", ["wikipedia:%1"]],
    ["what do you see(.*)", ["vision_check"]]
  ]
}
```

**Специальные ответы:**
- `sensor:N` → читает датчик N
- `wikipedia:X` → запрос к Wikipedia
- `dictionary:X` → запрос определения
- `vision_check` → описание сцены с камеры
- `not_proc` → обработка уведомлений о проблемах

---

## Запуск

```bash
# Через ROS2 launch
ros2 launch maestro maestro_launch.py

# Или напрямую
ros2 run maestro maestro
```

Запускаются два потока:
1. **maestro_thread** — основной узел MAESTRO
2. **person_detection_thread** — узел PersonDetector (детекция людей в кадре)

---

## Датчики (Sensor IDs)

| ID | Sensor | ID | Sensor |
|----|--------|----|----|
| 0 | Right ear light | 6 | Salinity (EC) |
| 1 | Tail light | 7 | pH |
| 2 | Left ear light | 8 | Nitrogen |
| 3 | Soil moisture | 9 | Phosphorus |
| 4 | Temperature | 10 | Potassium |
