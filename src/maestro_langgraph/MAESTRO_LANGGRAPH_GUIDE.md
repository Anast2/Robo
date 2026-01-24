# Пакет `maestro_langgraph` — Полный обзор

## Назначение

**maestro_langgraph** — это модернизированная версия пакета `maestro`, использующая **LangGraph** для оркестрации диалогов. Ключевые отличия:

1. **100% LLM-генерация ответов** — никаких хардкод-шаблонов
2. **LangGraph workflow** — граф из 9 узлов вместо 15+ состояний FSM
3. **Веб-поиск** — интеграция с DuckDuckGo для фактических вопросов
4. **Двойной бэкенд** — поддержка Ollama и LM Studio
5. **Контекстуальные эмоции** — LLM определяет эмоции на основе диалога
6. **Sensor-Aware Response System** — интеллектуальное отслеживание сенсоров и интеграция в диалог

---

## Сравнение с оригинальным maestro

| Аспект | Старый `maestro` | Новый `maestro_langgraph` |
|--------|------------------|---------------------------|
| **Генерация ответов** | Regex + dialogue.json шаблоны | 100% LLM-генерация |
| **Классификация интента** | NLTK pattern matching | LLM + fuzzy fallback |
| **База знаний** | dialogue.json, Wikipedia, Dictionary | DuckDuckGo веб-поиск |
| **Анализ эмоций** | EmTract-DistilBERT | LLM-определяемые |
| **State Machine** | 15 состояний диалога + 2 robot + 2 problem | 9 LangGraph узлов |
| **Переходы состояний** | Хардкод в StateMachines.py | Условная маршрутизация в графе |
| **Бэкенд LLM** | Только Ollama (rooted_llm) | Ollama + LM Studio |
| **Модель по умолчанию** | llama3 | qwen2:0.5b (быстрая) |
| **Расширяемость** | Требует изменения кода | Изменение промптов |
| **Веб-поиск** | Нет (только Wikipedia) | DuckDuckGo интеграция |
| **Мониторинг сенсоров** | Простые уведомления | Интеллектуальное отслеживание с приоритизацией |

---

## Структура директории

```
src/maestro_langgraph/
├── maestro_langgraph/           # Исходный код Python
│   ├── __init__.py              # Экспорт публичного API
│   ├── state.py                 # Схема состояния диалога
│   ├── prompts.py               # Системные промпты для LLM
│   ├── chains.py                # LangChain цепочки
│   ├── graph.py                 # LangGraph workflow
│   ├── maestro_node.py          # ROS2 узел-обёртка
│   ├── sensor_tracker.py        # Отслеживание сенсоров
│   └── solutions.py             # Решения для проблем с сенсорами
│
├── launch/
│   └── maestro_langgraph_launch.py  # ROS2 launch файл
│
├── test/                        # Тесты
│   ├── test_state.py
│   ├── test_prompts.py
│   ├── test_copyright.py
│   ├── test_flake8.py
│   └── test_pep257.py
│
├── langgraph_simulation.ipynb   # Jupyter notebook для тестирования
├── resource/maestro_langgraph   # Маркер для ament
├── package.xml                  # ROS2 метаданные
├── setup.py                     # Python setuptools
└── setup.cfg                    # Конфигурация
```

---

## Файлы и их назначение

### Ядро системы

| Файл | Назначение |
|------|------------|
| **`state.py`** | Схема состояния: `Intent`, `Emotion`, `RobotStatus` enums и `DialogueState` TypedDict с полями для сенсоров |
| **`prompts.py`** | Все системные промпты для LLM: персона робота, классификация, генерация, эмоции, сенсоры |
| **`chains.py`** | Класс `DialogueChains` — LangChain цепочки для всех LLM-операций включая сенсорные |
| **`graph.py`** | LangGraph workflow: 9 узлов, условная маршрутизация, функция `process_message()` |
| **`maestro_node.py`** | ROS2 узел с интеграцией SensorTracker |
| **`sensor_tracker.py`** | Отслеживание проблем с сенсорами, частоты упоминаний, ответов пользователя |
| **`solutions.py`** | Готовые решения для проблем с влажностью, температурой, светом, pH |

### Инфраструктура ROS2

| Файл | Назначение |
|------|------------|
| **`package.xml`** | Зависимости: rclpy, std_msgs, rooted_msgs, rooted_interfaces |
| **`setup.py`** | Entry point: `maestro_langgraph_node`, зависимости LangChain |
| **`launch/maestro_langgraph_launch.py`** | Launch-файл с параметрами backend, model_name, base_url |

---

## Sensor-Aware Response System

### Обзор

Система интеллектуального мониторинга сенсоров, которая:
- Отслеживает показания сенсоров и классифицирует проблемы по серьёзности
- Естественно интегрирует информацию о проблемах в диалог
- Отслеживает реакцию пользователя (согласился, отложил, отказал)
- Адаптирует частоту упоминаний в зависимости от серьёзности
- Празднует когда проблемы решены

### Пороговые значения сенсоров

| Сенсор | Оптимум | Предупреждение | Критический |
|--------|---------|----------------|-------------|
| **Температура** | 20-25°C | <18 или >27°C | <15 или >30°C |
| **Влажность** | 40-60% | <35 или >65% | <30 или >70% |
| **Освещённость** | 2000-4000 lux | <1500 или >4500 | <1000 или >5000 |
| **pH** | 6.0-7.0 | <5.5 или >7.5 | <5.0 или >8.0 |

### Частота упоминаний

| Серьёзность | Частота |
|-------------|---------|
| **Critical** | Каждое взаимодействие |
| **High** | Каждое 2-е взаимодействие |
| **Medium** | Каждое 3-е взаимодействие |
| **Low** | Один раз за разговор |

### Типы ответов пользователя

| Тип | Примеры | Реакция робота |
|-----|---------|----------------|
| `committed` | "Сделаю", "Готово", "Полью" | Благодарность |
| `deferred` | "Позже", "Не сейчас" | Напоминание + quick fix |
| `rejected` | "Нет", "Не могу" | Понимание |
| `question` | "Почему?", "Как?" | Объяснение |
| `unrelated` | Другая тема | Продолжение диалога |

---

## Отслеживание сенсоров (sensor_tracker.py)

### Enums

```python
class SensorType(str, Enum):
    TEMPERATURE = "temperature"
    MOISTURE = "moisture"
    LIGHT = "light"
    PH = "pH"

class IssueSeverity(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    OPTIMAL = "optimal"

class UserResponseType(str, Enum):
    COMMITTED = "committed"      # Сделает сейчас
    DEFERRED = "deferred"        # Сделает позже
    REJECTED = "rejected"        # Отказ
    QUESTION = "question"        # Вопрос
    UNRELATED = "unrelated"      # Не относится к проблеме
```

### Класс SensorThreshold

```python
@dataclass
class SensorThreshold:
    sensor_type: SensorType
    optimal_min: float
    optimal_max: float
    warning_min: float
    warning_max: float
    critical_min: float
    critical_max: float
    unit: str

    def classify(self, value: float) -> IssueSeverity:
        """Классифицирует значение по серьёзности."""

    def get_direction(self, value: float) -> str:
        """Возвращает 'too_low' или 'too_high'."""
```

### Класс SensorIssue

```python
@dataclass
class SensorIssue:
    sensor_type: SensorType
    current_value: float
    severity: IssueSeverity
    direction: str                    # "too_low" или "too_high"
    first_detected: datetime
    last_mentioned: Optional[datetime]
    mention_count: int
    user_response: Optional[UserResponseType]
    solutions_suggested: List[str]

    def to_dict(self) -> dict:
        """Сериализация в dict."""

    @classmethod
    def from_dict(cls, data: dict) -> "SensorIssue":
        """Десериализация из dict."""
```

### Класс SensorTracker

```python
class SensorTracker:
    """Отслеживает проблемы с сенсорами."""

    def __init__(self):
        self.active_issues: Dict[str, SensorIssue] = {}
        self.interaction_count: int = 0
        self.mentioned_this_conversation: set = set()
        self.pending_issue: Optional[str] = None

    def process_reading(self, sensor_type: SensorType, value: float) -> Optional[SensorIssue]:
        """Обрабатывает показание сенсора."""

    def process_notification(self, sensor_name: str, value: float) -> Optional[SensorIssue]:
        """Обрабатывает уведомление от notificationTopic."""

    def get_issues_to_mention(self) -> List[SensorIssue]:
        """Возвращает проблемы для упоминания в этом взаимодействии."""

    def record_mention(self, issue: SensorIssue, solutions: List[str] = None):
        """Записывает что проблема была упомянута."""

    def record_user_response(self, response_type: UserResponseType):
        """Записывает ответ пользователя на проблему."""

    def get_pending_issue(self) -> Optional[SensorIssue]:
        """Возвращает текущую обсуждаемую проблему."""

    def to_state(self) -> dict:
        """Сериализует в dict для передачи через граф."""

    def load_state(self, state: dict):
        """Загружает из сериализованного состояния."""
```

---

## Решения (solutions.py)

### Класс Solution

```python
@dataclass
class Solution:
    description: str          # Краткое описание
    action: str               # Что нужно сделать
    timeframe: str            # Когда сделать
    consequence: str          # Последствия если не сделать
    time_until_damage: str    # Время до повреждения
    complexity: int           # 1=простое, 2=среднее, 3=сложное
    is_quick_fix: bool        # Быстрое решение?
```

### Примеры решений

**Влажность слишком низкая:**
```python
Solution(
    description="Manual watering",
    action="water the plant thoroughly until water drains from the bottom",
    timeframe="immediately",
    consequence="wilting and potential plant death",
    time_until_damage="24 hours",
    complexity=1,
    is_quick_fix=True,
)
```

**Температура слишком высокая:**
```python
Solution(
    description="Increase airflow",
    action="turn on a fan or open windows for better air circulation",
    timeframe="immediately",
    consequence="heat stress and wilting",
    time_until_damage="6-12 hours",
    complexity=1,
    is_quick_fix=True,
)
```

### Функции

```python
def get_solutions(sensor_type: SensorType, direction: str, exclude: List[str] = None) -> List[Solution]:
    """Получает решения, исключая уже предложенные."""

def get_quick_fix(sensor_type: SensorType, direction: str) -> Optional[Solution]:
    """Получает самое простое быстрое решение."""
```

---

## Схема состояния (state.py)

### DialogueState

```python
class DialogueState(TypedDict, total=False):
    # Входные данные
    human_message: str
    voice_emotion: str

    # Контекст робота
    robot_busy: bool
    robot_status: str
    has_problem: bool
    notifications: dict

    # Контекст разговора
    conversation_history: list

    # Результаты обработки
    intent: str
    entities: dict
    search_context: Optional[str]
    context_response: Optional[str]

    # Выходные данные
    response: str
    response_emotion: str
    prosody: tuple
    should_end_early: bool

    # Sensor awareness fields (NEW)
    sensor_tracker_state: dict          # Сериализованный SensorTracker
    issues_to_mention: list             # Список проблем для упоминания
    sensor_context: Optional[str]       # Контекст для генерации
    user_response_type: Optional[str]   # committed/deferred/rejected/question/unrelated
    pending_issue: Optional[dict]       # Обсуждаемая проблема
    improvement_detected: Optional[dict] # Решённая проблема для празднования
    last_suggested_solution: Optional[str] # Последнее предложенное решение
```

---

## Системные промпты (prompts.py)

### Промпты для сенсоров

**Классификация ответа пользователя:**
```
Classify the user's response to a sensor issue.

The robot mentioned this issue: {issue_description}
User said: {message}

Categories:
- committed: User will fix it now
- deferred: User will fix it later
- rejected: User won't fix it
- question: User asks about it
- unrelated: User didn't address the issue

Respond with ONLY the category name.
```

**Интеграция сенсора в ответ:**
```
You have a base response to the user. Now add sensor issue information naturally.

Your base response: {base_response}

Sensor issue to mention:
- Type: {sensor_type}
- Current value: {value}{unit}
- Optimal range: {optimal_min}-{optimal_max}{unit}
- Problem: {direction}
- Severity: {severity}

Suggested action: {action}
Expected outcome: {outcome}

Create a combined response that:
1. First delivers your base response naturally
2. Smoothly transitions ("I notice...", "By the way...")
3. Mentions the issue with the actual value
4. Suggests the action
5. Explains briefly why it matters

Keep total response to 3-4 sentences. Be caring but not alarming.
```

**Отложенный ответ:**
```
The user said they will fix the issue later. Respond empathetically.

Issue: {sensor_type} at {value}{unit}
User said: {message}
Time until damage: {time_until_damage}
Quick fix alternative: {quick_fix_action}

Generate a response that:
1. Acknowledges their situation
2. Gently reminds about consequences with timeframe
3. Offers the quick fix as an easier alternative
4. Asks if that would be possible

Be friendly and understanding, not pushy.
```

**Празднование решения:**
```
A sensor issue was resolved! Respond happily.

Your base response: {base_response}
Resolved issue: {sensor_type} is now back to normal

Add a brief, warm celebration. Thank the user for their help.
```

---

## LangChain цепочки (chains.py)

### Новые методы для сенсоров

```python
class DialogueChains:
    # ... существующие методы ...

    def classify_user_response(self, message: str, issue_description: str) -> UserResponseType:
        """Классифицирует ответ пользователя на проблему с сенсором."""

    def generate_sensor_integrated_response(
        self,
        base_response: str,
        issue: dict,
        solution: dict,
    ) -> str:
        """Генерирует ответ с естественной интеграцией информации о сенсоре."""

    def generate_deferred_response(
        self,
        message: str,
        issue: dict,
        quick_fix: dict,
    ) -> str:
        """Генерирует эмпатичный ответ когда пользователь откладывает действие."""

    def generate_celebration_response(
        self,
        base_response: str,
        sensor_type: str,
        previous_value: float,
        current_value: float,
    ) -> str:
        """Генерирует радостный ответ при решении проблемы."""
```

---

## LangGraph workflow (graph.py)

### Обновлённый граф узлов

```
START
  │
  ▼
┌─────────────────┐
│ check_context   │ ◄── Проверяет busy/problem статус
└────────┬────────┘
         │
         ▼
    ┌─────────┐
    │ BUSY?   │
    └────┬────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
[BUSY]    [FREE/PROBLEM]
    │         │
    │         ▼
    │   ┌──────────────────┐
    │   │ process_sensors  │ ◄── Обработка уведомлений сенсоров (NEW)
    │   └────────┬─────────┘
    │            │
    │            ▼
    │   ┌─────────────────┐
    │   │ classify_intent │ ◄── LLM классификация интента
    │   └────────┬────────┘
    │            │
    │            ▼
    │   ┌─────────────────────┐
    │   │ check_user_response │ ◄── Проверка ответа на проблему (NEW)
    │   └────────┬────────────┘
    │            │
    │            ▼
    │   ┌─────────────┐
    │   │ check_search│ ◄── Веб-поиск если нужно
    │   └──────┬──────┘
    │          │
    └──────────┼──────────┐
               │          │
               ▼          │
       ┌───────────────┐  │
       │generate_resp. │◄─┘ ◄── Генерация ответа
       └───────┬───────┘
               │
               ▼
       ┌──────────────────┐
       │integrate_sensors │ ◄── Интеграция сенсоров в ответ (NEW)
       └───────┬──────────┘
               │
               ▼
       ┌───────────────┐
       │determine_emot.│ ◄── Определение эмоции
       └───────┬───────┘
               │
               ▼
       ┌───────────────┐
       │update_history │ ◄── Сохранение в историю
       └───────┬───────┘
               │
               ▼
              END
```

### Новые узлы

| Узел | Функция | Описание |
|------|---------|----------|
| `process_sensors` | `process_sensor_issues_node()` | Обрабатывает уведомления, определяет проблемы для упоминания |
| `check_user_response` | `check_user_response_node()` | Классифицирует ответ пользователя на pending issue |
| `integrate_sensors` | `integrate_sensor_response_node()` | Интегрирует информацию о сенсорах в ответ |

### Логика integrate_sensor_response_node

```python
def integrate_sensor_response_node(state: DialogueState) -> DialogueState:
    # Case 1: Празднование улучшения
    if improvement:
        return celebration_response + emotion="happy"

    # Case 2: Пользователь отложил действие
    if user_response_type == "deferred":
        return deferred_response с quick_fix

    # Case 3: Пользователь согласился
    if user_response_type == "committed":
        return base_response + "Thank you!"

    # Case 4: Новые проблемы для упоминания
    if issues_to_mention:
        return sensor_integrated_response
```

### Обновлённая функция process_message

```python
def process_message(
    message: str,
    voice_emotion: str = "neutral",
    history: list = None,
    robot_busy: bool = False,
    notifications: dict = None,
    sensor_tracker_state: dict = None,  # NEW
) -> DialogueState:
    """
    Обрабатывает сообщение через sensor-aware LangGraph workflow.

    Возвращает:
    {
        "response": str,
        "response_emotion": str,
        "prosody": tuple,
        "intent": str,
        "robot_status": str,
        "conversation_history": list,
        "sensor_tracker_state": dict,      # NEW
        "user_response_type": str,         # NEW
        "pending_issue": dict,             # NEW
        "improvement_detected": dict,      # NEW
    }
    """
```

---

## ROS2 узел (maestro_node.py)

### Обновления

```python
class MaestroLangGraphNode(Node):
    def __init__(self):
        # ... существующая инициализация ...

        # Persistent sensor tracker (NEW)
        self.sensor_tracker = SensorTracker()
        set_tracker(self.sensor_tracker)

    def cb_function_conversation(self, msg: String):
        # ... парсинг сообщения ...

        # Process with sensor tracker state (NEW)
        result = process_message(
            message=human_speech,
            voice_emotion=voice_emotion,
            history=self.conversation_history,
            robot_busy=self.robot_busy,
            notifications=self.notifications,
            sensor_tracker_state=self.sensor_tracker.to_state(),  # NEW
        )

        # Update tracker from result (NEW)
        if result.get("sensor_tracker_state"):
            self.sensor_tracker.load_state(result["sensor_tracker_state"])

        # Handle notification clearing based on user response (NEW)
        if result.get("user_response_type") == "committed":
            pending = result.get("pending_issue")
            if pending:
                self._clear_notification_for_sensor(pending.get("sensor_type"))

    def _clear_notification_for_sensor(self, sensor_type: str):
        """Очищает уведомления для конкретного типа сенсора."""
        mapping = {
            "moisture": ["moisture", "soil_moisture"],
            "temperature": ["temperature", "temp"],
            "light": ["light", "lux"],
            "pH": ["ph", "acidity"],
        }
        keys_to_remove = mapping.get(sensor_type, [])
        for key in list(self.notifications.keys()):
            if key.lower() in keys_to_remove:
                del self.notifications[key]
```

---

## Примеры диалогов

### Сценарий 1: Низкая влажность почвы

```
1. notificationTopic: "moisture:32:critical"

2. User: "Hello, how are you today?"

3. process_sensors_node:
   - SensorTracker.process_notification("moisture", 32)
   - severity = CRITICAL, direction = "too_low"
   - issues_to_mention = [moisture_issue]

4. classify_intent_node:
   - intent = "greeting"

5. check_user_response_node:
   - pending_issue = None (первое упоминание)

6. generate_response_node:
   - base_response = "Hi! I'm doing well, thank you for asking."

7. integrate_sensors_node:
   - issue = moisture at 32%
   - solution = "water the plant thoroughly"
   - response = "Hi! I'm doing well, thank you for asking.
     I notice the soil moisture is quite low (32%).
     Would you mind watering the plant thoroughly?
     This will help prevent wilting."

8. determine_emotion_node:
   - emotion = "neutral" (concerned but friendly)

9. Robot: "Hi! I'm doing well, thank you for asking. I notice the
           soil moisture is quite low (32%). Would you mind watering
           the plant thoroughly? This will help prevent wilting."
```

### Сценарий 2: Пользователь откладывает

```
1. User: "I'll do it later."

2. check_user_response_node:
   - pending_issue = moisture_issue
   - classify_user_response("I'll do it later", "moisture is too low")
   - user_response_type = "deferred"

3. integrate_sensors_node:
   - user_response_type = "deferred"
   - quick_fix = Solution(action="water manually", time_until_damage="24 hours")
   - generate_deferred_response(...)

4. Robot: "I understand you're busy. Just keep in mind that the plants
           might start showing stress signs within 24 hours if this
           isn't addressed. The quickest fix would be a manual watering
           for now. Would that be possible?"
```

### Сценарий 3: Пользователь соглашается

```
1. User: "OK, I'll water it now."

2. check_user_response_node:
   - classify_user_response(...) → "committed"
   - record_user_response(COMMITTED)

3. integrate_sensors_node:
   - user_response_type = "committed"
   - base_response + " Thank you, I appreciate your help!"

4. Robot: "Great! Thank you, I appreciate your help!"
```

### Сценарий 4: Проблема решена

```
1. notificationTopic: "moisture:45:normal" (или просто отсутствие critical)

2. User: "Hi again"

3. process_sensors_node:
   - process_notification("moisture", 45)
   - severity = OPTIMAL
   - improvement_detected = moisture_issue (была 32%, стала 45%)

4. integrate_sensors_node:
   - improvement_detected → celebration mode
   - generate_celebration_response(...)

5. Robot: "Hello! Great news - the soil moisture is back to normal
           levels now. Thank you so much for taking care of that!
           Your plant will be much happier."
```

---

## Тестирование

### ROS2 команды

```bash
# Инъекция критического уведомления
ros2 topic pub /notificationTopic std_msgs/String "data: 'moisture:32:critical'"

# Отправка сообщения
ros2 topic pub /messageTopic std_msgs/String "data: 'Hello how are you;meta;neutral'"

# Симуляция решения проблемы
ros2 topic pub /notificationTopic std_msgs/String "data: 'moisture:45:normal'"
```

### Python тест

```python
from maestro_langgraph import (
    process_message,
    SensorTracker,
    set_tracker,
)

# Создаём tracker
tracker = SensorTracker()
set_tracker(tracker)

# Добавляем проблему
tracker.process_notification("moisture", 32.0)

# Первое сообщение
result = process_message(
    message="Hello, how are you?",
    notifications={"moisture": ["32", "critical"]},
    sensor_tracker_state=tracker.to_state(),
)

print(result["response"])
# "Hi! I'm doing well... I notice the soil moisture is quite low (32%)..."

# Обновляем tracker
tracker.load_state(result["sensor_tracker_state"])

# Пользователь откладывает
result = process_message(
    message="I'll do it later",
    sensor_tracker_state=tracker.to_state(),
)

print(result["response"])
# "I understand you're busy... The quickest fix would be..."
```

---

## Зависимости

### Python (setup.py)

```python
install_requires=[
    'setuptools',
    'langchain>=0.1',
    'langgraph>=0.0.30',
    'langchain-community>=0.0.20',
    'langchain-ollama>=0.0.1',
]
```

### ROS2 (package.xml)

```xml
<depend>rclpy</depend>
<depend>std_msgs</depend>
<depend>rooted_msgs</depend>
<depend>rooted_interfaces</depend>
```

---

## Запуск

### Через ROS2 launch

```bash
# С параметрами по умолчанию (Ollama, qwen2:0.5b)
ros2 launch maestro_langgraph maestro_langgraph_launch.py

# С LM Studio
ros2 launch maestro_langgraph maestro_langgraph_launch.py backend:=lmstudio

# С другой моделью
ros2 launch maestro_langgraph maestro_langgraph_launch.py model_name:=llama3
```

### Напрямую

```bash
ros2 run maestro_langgraph maestro_langgraph_node \
    --ros-args \
    -p model_name:=qwen2:0.5b \
    -p backend:=ollama
```

---

## Расширение системы

### Добавление нового типа сенсора

1. Добавить в `sensor_tracker.py`:
```python
class SensorType(str, Enum):
    # ... существующие ...
    HUMIDITY = "humidity"  # Новый сенсор
```

2. Добавить пороговые значения:
```python
THRESHOLDS[SensorType.HUMIDITY] = SensorThreshold(
    sensor_type=SensorType.HUMIDITY,
    optimal_min=40.0, optimal_max=60.0,
    warning_min=30.0, warning_max=70.0,
    critical_min=20.0, critical_max=80.0,
    unit="%"
)
```

3. Добавить решения в `solutions.py`:
```python
SOLUTIONS[SensorType.HUMIDITY] = {
    "too_low": [Solution(...)],
    "too_high": [Solution(...)],
}
```

### Изменение частоты упоминаний

```python
# В sensor_tracker.py
MENTION_FREQUENCY = {
    IssueSeverity.CRITICAL: 1,   # Каждое взаимодействие
    IssueSeverity.HIGH: 3,       # Изменено: каждое 3-е
    IssueSeverity.MEDIUM: 5,     # Изменено: каждое 5-е
    IssueSeverity.LOW: 999999,   # Один раз за разговор
}
```

---

## Известные ограничения

1. **Зависимость от LLM** — требуется работающий Ollama или LM Studio
2. **Латентность** — LLM-вызовы медленнее хардкод-ответов
3. **Нет детекции людей** — PersonDetector не реализован
4. **История ограничена** — только 10 последних обменов
5. **Веб-поиск** — может быть медленным, требует интернет
6. **Один pending issue** — одновременно отслеживается только одна обсуждаемая проблема

---

## Миграция с maestro

Для замены старого maestro на maestro_langgraph:

1. В `pc_launch.py` заменить:
```python
# Было:
Node(package='maestro', executable='maestro', ...)

# Стало:
Node(package='maestro_langgraph', executable='maestro_langgraph_node', ...)
```

2. Убедиться что Ollama/LM Studio запущен

3. Топики совместимы — никаких изменений в других пакетах не требуется
