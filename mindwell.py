"""
MindWell - Современное мобильное приложение для ментального здоровья
Создано с использованием Kivy для кроссплатформенной разработки
Включает трекер настроения, медитацию, концентрацию и эмоциональный интеллект
"""

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.uix.progressbar import ProgressBar
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.graphics import Color, RoundedRectangle, Line, Ellipse
from kivy.uix.widget import Widget
from kivy.metrics import dp
import json
import datetime
import random
import math

class NeumorphicButton(Button):
    """Кнопка с neumorphism эффектом"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = [0, 0, 0, 0]
        with self.canvas.before:
            Color(0.1, 0.1, 0.15, 1)  # Тёмный фон
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[15])
        self.bind(pos=self.update_graphics, size=self.update_graphics)
        
    def update_graphics(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

class GlassmorphicPanel(Widget):
    """Панель с glassmorphism эффектом"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(0.15, 0.15, 0.25, 0.8)  # Полупрозрачный фон
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[20])
        self.bind(pos=self.update_graphics, size=self.update_graphics)
        
    def update_graphics(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

class MoodChart(Widget):
    """Виджет для отображения графика настроения"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mood_data = [3, 4, 2, 5, 3, 4, 4]  # Примерные данные за неделю
        self.bind(pos=self.update_chart, size=self.update_chart)
        
    def update_chart(self, *args):
        self.canvas.clear()
        if self.size[0] == 0 or self.size[1] == 0:
            return
            
        with self.canvas:
            # Градиентная линия графика
            Color(0.4, 0.8, 1, 1)  # Неоновый синий
            points = []
            for i, mood in enumerate(self.mood_data):
                x = self.x + (i / (len(self.mood_data) - 1)) * self.width
                y = self.y + (mood / 5) * self.height
                points.extend([x, y])
            
            if len(points) >= 4:
                Line(points=points, width=3, cap='round', joint='round')
                
            # Точки на графике
            Color(1, 0.4, 0.8, 1)  # Неоновый розовый
            for i, mood in enumerate(self.mood_data):
                x = self.x + (i / (len(self.mood_data) - 1)) * self.width
                y = self.y + (mood / 5) * self.height
                Ellipse(pos=(x-5, y-5), size=(10, 10))

class DataManager:
    """Менеджер данных для сохранения состояния приложения"""
    def __init__(self):
        self.data = {
            'mood_history': [],
            'meditation_sessions': 0,
            'concentration_score': 0,
            'language': 'en'
        }
        
    def save_mood(self, mood, note=""):
        entry = {
            'date': datetime.datetime.now().isoformat(),
            'mood': mood,
            'note': note
        }
        self.data['mood_history'].append(entry)
        
    def get_recent_moods(self, days=7):
        if not self.data['mood_history']:
            return [3, 4, 2, 5, 3, 4, 4]  # Пример данных
        return [entry['mood'] for entry in self.data['mood_history'][-days:]]

class LanguageManager:
    """Менеджер локализации для многоязычной поддержки"""
    def __init__(self):
        self.translations = {
            'en': {
                'mood_tracker': 'Mood\nTracker',
                'meditate': 'Meditate',
                'concentration': 'Concentration',
                'emotional_intelligence': 'Emotional Intelligence',
                'track_mood': 'Track your mood\nand reflect on your\nemotional patterns',
                'track_button': 'Track',
                'start_button': 'Start',
                'meditation_benefit': 'Regular meditation has\nbeen shown to reduce\nstress and improve overall\nwell-being.',
                'concentration_desc': 'Focus on a task to enhance\ncognitive performance',
                'ei_desc': 'Improve self-awareness and\ninterpersonal skills',
                'how_feeling': 'How are you feeling today?',
                'very_bad': 'Very Bad',
                'bad': 'Bad',
                'okay': 'Okay',
                'good': 'Good',
                'excellent': 'Excellent',
                'save_mood': 'Save Mood',
                'meditation_timer': 'Meditation Timer',
                'breathe_in': 'Breathe In',
                'breathe_out': 'Breathe Out',
                'hold': 'Hold',
                'well_done': 'Well Done!',
                'session_complete': 'Meditation session completed',
                'concentration_game': 'Concentration Exercise',
                'focus_circle': 'Focus on the circle and tap when it turns green',
                'reaction_time': 'Reaction Time: {} ms',
                'ei_tip': 'Daily EQ Tip',
                'settings': 'Settings',
                'language': 'Language'
            },
            'ru': {
                'mood_tracker': 'Трекер\nНастроения',
                'meditate': 'Медитация',
                'concentration': 'Концентрация',
                'emotional_intelligence': 'Эмоциональный Интеллект',
                'track_mood': 'Отслеживайте настроение\nи анализируйте свои\nэмоциональные паттерны',
                'track_button': 'Отследить',
                'start_button': 'Начать',
                'meditation_benefit': 'Регулярная медитация\nснижает стресс и улучшает\nобщее самочувствие.',
                'concentration_desc': 'Сосредоточьтесь на задаче\nдля улучшения когнитивных\nспособностей',
                'ei_desc': 'Развивайте самосознание\nи навыки общения',
                'how_feeling': 'Как вы себя чувствуете сегодня?',
                'very_bad': 'Очень плохо',
                'bad': 'Плохо',
                'okay': 'Нормально',
                'good': 'Хорошо',
                'excellent': 'Отлично',
                'save_mood': 'Сохранить',
                'meditation_timer': 'Таймер Медитации',
                'breathe_in': 'Вдох',
                'breathe_out': 'Выдох',
                'hold': 'Задержка',
                'well_done': 'Отлично!',
                'session_complete': 'Сессия медитации завершена',
                'concentration_game': 'Упражнение на Концентрацию',
                'focus_circle': 'Следите за кругом и нажмите, когда он станет зеленым',
                'reaction_time': 'Время реакции: {} мс',
                'ei_tip': 'Совет дня по EQ',
                'settings': 'Настройки',
                'language': 'Язык'
            },
            'zh': {
                'mood_tracker': '情绪\n追踪器',
                'meditate': '冥想',
                'concentration': '专注力',
                'emotional_intelligence': '情商',
                'track_mood': '追踪您的情绪\n并反思您的\n情感模式',
                'track_button': '追踪',
                'start_button': '开始',
                'meditation_benefit': '定期冥想已被证明\n可以减轻压力并改善\n整体健康状况。',
                'concentration_desc': '专注于任务以增强\n认知能力',
                'ei_desc': '提高自我意识和\n人际交往技能',
                'how_feeling': '您今天感觉如何？',
                'very_bad': '很差',
                'bad': '差',
                'okay': '还行',
                'good': '好',
                'excellent': '非常好',
                'save_mood': '保存情绪',
                'meditation_timer': '冥想计时器',
                'breathe_in': '吸气',
                'breathe_out': '呼气',
                'hold': '屏息',
                'well_done': '做得好！',
                'session_complete': '冥想课程已完成',
                'concentration_game': '专注力练习',
                'focus_circle': '注视圆圈，当它变绿时点击',
                'reaction_time': '反应时间：{} 毫秒',
                'ei_tip': '每日情商小贴士',
                'settings': '设置',
                'language': '语言'
            }
        }
        self.current_language = 'en'
        
    def get_text(self, key):
        return self.translations[self.current_language].get(key, key)
        
    def set_language(self, lang_code):
        if lang_code in self.translations:
            self.current_language = lang_code

class MainScreen(Screen):
    """Главный экран с основными функциями"""
    def __init__(self, app, **kwargs):
        super().__init__(name='main', **kwargs)
        self.app = app
        self.build_ui()
        
    def build_ui(self):
        # Основной контейнер
        main_layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        
        # Заголовок приложения
        title = Label(
            text='MindWell',
            font_size='32sp',
            color=[1, 1, 1, 1],
            size_hint_y=0.1,
            halign='left'
        )
        title.bind(size=title.setter('text_size'))
        
        # Сетка карточек функций
        cards_grid = GridLayout(cols=2, spacing=dp(10), size_hint_y=0.8)
        
        # Карточка трекера настроения
        mood_card = self.create_mood_card()
        cards_grid.add_widget(mood_card)
        
        # Карточка медитации
        meditation_card = self.create_meditation_card()
        cards_grid.add_widget(meditation_card)
        
        # Карточка концентрации
        concentration_card = self.create_concentration_card()
        cards_grid.add_widget(concentration_card)
        
        # Карточка эмоционального интеллекта
        ei_card = self.create_ei_card()
        cards_grid.add_widget(ei_card)
        
        # Нижняя навигация
        bottom_nav = BoxLayout(size_hint_y=0.1, spacing=dp(10))
        
        settings_btn = NeumorphicButton(
            text='⚙️',
            font_size='20sp',
            size_hint_x=0.2
        )
        settings_btn.bind(on_press=lambda x: self.show_settings())
        
        bottom_nav.add_widget(Widget())  # Заполнитель
        bottom_nav.add_widget(settings_btn)
        
        main_layout.add_widget(title)
        main_layout.add_widget(cards_grid)
        main_layout.add_widget(bottom_nav)
        
        # Фон с градиентом
        with self.canvas.before:
            Color(0.05, 0.05, 0.1, 1)  # Тёмно-синий фон
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_bg, size=self.update_bg)
        
        self.add_widget(main_layout)
        
    def update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
        
    def create_mood_card(self):
        """Создание карточки трекера настроения"""
        card_layout = BoxLayout(orientation='vertical', padding=dp(15), spacing=dp(10))
        
        # Glassmorphic панель
        panel = GlassmorphicPanel()
        
        # Заголовок
        title = Label(
            text=self.app.lang_manager.get_text('mood_tracker'),
            font_size='18sp',
            color=[1, 1, 1, 1],
            size_hint_y=0.3,
            halign='center'
        )
        title.bind(size=title.setter('text_size'))
        
        # График настроения
        chart = MoodChart(size_hint_y=0.4)
        
        # Описание
        desc = Label(
            text=self.app.lang_manager.get_text('track_mood'),
            font_size='12sp',
            color=[0.8, 0.8, 0.8, 1],
            size_hint_y=0.3,
            halign='center',
            valign='middle'
        )
        desc.bind(size=desc.setter('text_size'))
        
        # Кнопка
        track_btn = NeumorphicButton(
            text=self.app.lang_manager.get_text('track_button'),
            size_hint_y=0.2,
            font_size='14sp',
            color=[1, 0.4, 0.8, 1]  # Неоновый розовый
        )
        track_btn.bind(on_press=lambda x: self.open_mood_tracker())
        
        card_layout.add_widget(title)
        card_layout.add_widget(chart)
        card_layout.add_widget(desc)
        card_layout.add_widget(track_btn)
        
        # Добавляем всё на панель
        panel.add_widget(card_layout)
        return panel
        
    def create_meditation_card(self):
        """Создание карточки медитации"""
        card_layout = BoxLayout(orientation='vertical', padding=dp(15), spacing=dp(10))
        
        panel = GlassmorphicPanel()
        
        # Иконка медитации
        icon = Label(
            text='🧘‍♀️',
            font_size='40sp',
            size_hint_y=0.4
        )
        
        title = Label(
            text=self.app.lang_manager.get_text('meditate'),
            font_size='18sp',
            color=[1, 1, 1, 1],
            size_hint_y=0.2
        )
        
        desc = Label(
            text=self.app.lang_manager.get_text('meditation_benefit'),
            font_size='11sp',
            color=[0.8, 0.8, 0.8, 1],
            size_hint_y=0.3,
            halign='center',
            valign='middle'
        )
        desc.bind(size=desc.setter('text_size'))
        
        start_btn = NeumorphicButton(
            text=self.app.lang_manager.get_text('start_button'),
            size_hint_y=0.2,
            font_size='14sp',
            color=[0.4, 0.8, 1, 1]  # Неоновый синий
        )
        start_btn.bind(on_press=lambda x: self.start_meditation())
        
        card_layout.add_widget(icon)
        card_layout.add_widget(title)
        card_layout.add_widget(desc)
        card_layout.add_widget(start_btn)
        
        panel.add_widget(card_layout)
        return panel
        
    def create_concentration_card(self):
        """Создание карточки концентрации"""
        card_layout = BoxLayout(orientation='vertical', padding=dp(15), spacing=dp(10))
        
        panel = GlassmorphicPanel()
        
        # Иконка мозга
        icon = Label(
            text='🧠',
            font_size='40sp',
            size_hint_y=0.3,
            color=[0.8, 0.4, 1, 1]  # Фиолетовый
        )
        
        title = Label(
            text=self.app.lang_manager.get_text('concentration'),
            font_size='16sp',
            color=[1, 1, 1, 1],
            size_hint_y=0.2
        )
        
        desc = Label(
            text=self.app.lang_manager.get_text('concentration_desc'),
            font_size='11sp',
            color=[0.8, 0.8, 0.8, 1],
            size_hint_y=0.3,
            halign='center',
            valign='middle'
        )
        desc.bind(size=desc.setter('text_size'))
        
        start_btn = NeumorphicButton(
            text=self.app.lang_manager.get_text('start_button'),
            size_hint_y=0.2,
            font_size='14sp',
            color=[0.8, 0.4, 1, 1]
        )
        start_btn.bind(on_press=lambda x: self.start_concentration())
        
        card_layout.add_widget(icon)
        card_layout.add_widget(title)
        card_layout.add_widget(desc)
        card_layout.add_widget(start_btn)
        
        panel.add_widget(card_layout)
        return panel
        
    def create_ei_card(self):
        """Создание карточки эмоционального интеллекта"""
        card_layout = BoxLayout(orientation='vertical', padding=dp(15), spacing=dp(10))
        
        panel = GlassmorphicPanel()
        
        # Иконка лампочки
        icon = Label(
            text='💡',
            font_size='40sp',
            size_hint_y=0.3,
            color=[1, 0.8, 0.2, 1]  # Жёлтый
        )
        
        title = Label(
            text=self.app.lang_manager.get_text('emotional_intelligence'),
            font_size='14sp',
            color=[1, 1, 1, 1],
            size_hint_y=0.2,
            halign='center'
        )
        title.bind(size=title.setter('text_size'))
        
        desc = Label(
            text=self.app.lang_manager.get_text('ei_desc'),
            font_size='11sp',
            color=[0.8, 0.8, 0.8, 1],
            size_hint_y=0.3,
            halign='center',
            valign='middle'
        )
        desc.bind(size=desc.setter('text_size'))
        
        start_btn = NeumorphicButton(
            text=self.app.lang_manager.get_text('start_button'),
            size_hint_y=0.2,
            font_size='14sp',
            color=[1, 0.8, 0.2, 1]
        )
        start_btn.bind(on_press=lambda x: self.show_ei_tips())
        
        card_layout.add_widget(icon)
        card_layout.add_widget(title)
        card_layout.add_widget(desc)
        card_layout.add_widget(start_btn)
        
        panel.add_widget(card_layout)
        return panel
        
    def open_mood_tracker(self):
        """Открыть трекер настроения"""
        self.app.root.transition = SlideTransition(direction='left')
        self.app.root.current = 'mood'
        
    def start_meditation(self):
        """Запустить медитацию"""
        self.app.root.transition = SlideTransition(direction='left')
        self.app.root.current = 'meditation'
        
    def start_concentration(self):
        """Запустить упражнения на концентрацию"""
        self.app.root.transition = SlideTransition(direction='left')
        self.app.root.current = 'concentration'
        
    def show_ei_tips(self):
        """Показать советы по эмоциональному интеллекту"""
        self.app.root.transition = SlideTransition(direction='left')
        self.app.root.current = 'ei'
        
    def show_settings(self):
        """Показать настройки"""
        # Создание всплывающего окна настроек
        content = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))
        
        title = Label(
            text=self.app.lang_manager.get_text('settings'),
            font_size='20sp',
            size_hint_y=0.2
        )
        
        lang_label = Label(
            text=self.app.lang_manager.get_text('language'),
            font_size='16sp',
            size_hint_y=0.2
        )
        
        lang_buttons = BoxLayout(spacing=dp(10), size_hint_y=0.3)
        
        en_btn = NeumorphicButton(text='English', font_size='14sp')
        ru_btn = NeumorphicButton(text='Русский', font_size='14sp')
        zh_btn = NeumorphicButton(text='中文', font_size='14sp')
        
        en_btn.bind(on_press=lambda x: self.change_language('en'))
        ru_btn.bind(on_press=lambda x: self.change_language('ru'))
        zh_btn.bind(on_press=lambda x: self.change_language('zh'))
        
        lang_buttons.add_widget(en_btn)
        lang_buttons.add_widget(ru_btn)
        lang_buttons.add_widget(zh_btn)
        
        close_btn = NeumorphicButton(
            text='Close',
            size_hint_y=0.2,
            font_size='16sp'
        )
        
        content.add_widget(title)
        content.add_widget(lang_label)
        content.add_widget(lang_buttons)
        content.add_widget(close_btn)
        
        popup = Popup(
            title='',
            content=content,
            size_hint=(0.8, 0.6),
            background_color=[0.1, 0.1, 0.15, 0.95]
        )
        
        close_btn.bind(on_press=popup.dismiss)
        popup.open()
        
    def change_language(self, lang_code):
        """Изменить язык приложения"""
        self.app.lang_manager.set_language(lang_code)
        # Здесь можно добавить обновление интерфейса
        
class MoodScreen(Screen):
    """Экран трекера настроения"""
    def __init__(self, app, **kwargs):
        super().__init__(name='mood', **kwargs)
        self.app = app
        self.mood_value = 3
        self.build_ui()
        
    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(20))
        
        # Заголовок
        title = Label(
            text=self.app.lang_manager.get_text('how_feeling'),
            font_size='24sp',
            color=[1, 1, 1, 1],
            size_hint_y=0.2
        )
        
        # Слайдер настроения
        mood_slider = Slider(
            min=1, max=5, value=3, step=1,
            size_hint_y=0.1
        )
        mood_slider.bind(value=self.on_mood_change)
        
        # Текстовые метки настроения
        mood_labels = BoxLayout(size_hint_y=0.1)
        labels_text = ['very_bad', 'bad', 'okay', 'good', 'excellent']
        
        for label_key in labels_text:
            label = Label(
                text=self.app.lang_manager.get_text(label_key),
                font_size='12sp',
                color=[0.8, 0.8, 0.8, 1]
            )
            mood_labels.add_widget(label)
        
        # Индикатор настроения
        self.mood_indicator = Label(
            text='😐',
            font_size='80sp',
            size_hint_y=0.3
        )
        
        # Кнопки
        buttons = BoxLayout(size_hint_y=0.2, spacing=dp(10))
        
        back_btn = NeumorphicButton(
            text='←',
            font_size='20sp',
            size_hint_x=0.3
        )
        back_btn.bind(on_press=self.go_back)
        
        save_btn = NeumorphicButton(
            text=self.app.lang_manager.get_text('save_mood'),
            font_size='16sp',
            color=[0.4, 1, 0.4, 1]  # Зелёный
        )
        save_btn.bind(on_press=self.save_mood)
        
        buttons.add_widget(back_btn)
        buttons.add_widget(save_btn)
        
        layout.add_widget(title)
        layout.add_widget(self.mood_indicator)
        layout.add_widget(mood_slider)
        layout.add_widget(mood_labels)
        layout.add_widget(buttons)
        
        # Фон
        with self.canvas.before:
            Color(0.05, 0.05, 0.1, 1)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_bg, size=self.update_bg)
        
        self.add_widget(layout)
        
    def update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
        
    def on_mood_change(self, instance, value):
        """Обработка изменения настроения"""
        self.mood_value = int(value)
        emojis = ['😢', '😟', '😐', '😊', '😄']
        colors = [
            [1, 0.3, 0.3, 1],    # Красный
            [1, 0.6, 0.3, 1],    # Оранжевый
            [1, 1, 0.3, 1],      # Жёлтый
            [0.3, 1, 0.6, 1],    # Зелёный
            [0.3, 0.8, 1, 1]     # Синий
        ]
        
        self.mood_indicator.text = emojis[self.mood_value - 1]
        self.mood_indicator.color = colors[self.mood_value - 1]
        
        # Анимация изменения размера
        anim = Animation(font_size='100sp', duration=0.1) + Animation(font_size='80sp', duration=0.1)
        anim.start(self.mood_indicator)
        
    def save_mood(self, instance):
        """Сохранить настроение"""
        self.app.data_manager.save_mood(self.mood_value)
        
        # Показать подтверждение
        popup_content = Label(
            text='✓ Mood saved!',
            font_size='20sp'
        )
        popup = Popup(
            title='',
            content=popup_content,
            size_hint=(0.6, 0.3),
            auto_dismiss=True
        )
        popup.open()
        Clock.schedule_once(lambda dt: popup.dismiss(), 1.5)
        
    def go_back(self, instance):
        """Вернуться на главный экран"""
        self.app.root.transition = SlideTransition(direction='right')
        self.app.root.current = 'main'

class MeditationScreen(Screen):
    """Экран медитации"""
    def __init__(self, app, **kwargs):
        super().__init__(name='meditation', **kwargs)
        self.app = app
        self.meditation_active = False
        self.breath_phase = 0  # 0: вдох, 1: задержка, 2: выдох, 3: задержка
        self.breath_timer = None
        self.session_time = 0
        self.build_ui()
        
    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(20))
        
        # Заголовок
        title = Label(
            text=self.app.lang_manager.get_text('meditation_timer'),
            font_size='24sp',
            color=[1, 1, 1, 1],
            size_hint_y=0.15
        )
        
        # Дыхательный круг
        self.breathing_circle = Widget(size_hint_y=0.5)
        with self.breathing_circle.canvas:
            Color(0.4, 0.8, 1, 0.7)  # Неоновый синий
            self.circle = Ellipse(size=(200, 200), pos=(0, 0))
        self.breathing_circle.bind(pos=self.update_circle, size=self.update_circle)
        
        # Инструкция по дыханию
        self.breath_instruction = Label(
            text=self.app.lang_manager.get_text('breathe_in'),
            font_size='20sp',
            color=[0.4, 0.8, 1, 1],
            size_hint_y=0.1
        )
        
        # Таймер сессии
        self.session_timer = Label(
            text='00:00',
            font_size='18sp',
            color=[0.8, 0.8, 0.8, 1],
            size_hint_y=0.1
        )
        
        # Кнопки управления
        controls = BoxLayout(size_hint_y=0.15, spacing=dp(10))
        
        back_btn = NeumorphicButton(
            text='←',
            font_size='20sp',
            size_hint_x=0.3
        )
        back_btn.bind(on_press=self.go_back)
        
        self.meditation_btn = NeumorphicButton(
            text=self.app.lang_manager.get_text('start_button'),
            font_size='16sp',
            color=[0.4, 1, 0.4, 1]
        )
        self.meditation_btn.bind(on_press=self.toggle_meditation)
        
        controls.add_widget(back_btn)
        controls.add_widget(self.meditation_btn)
        
        layout.add_widget(title)
        layout.add_widget(self.breathing_circle)
        layout.add_widget(self.breath_instruction)
        layout.add_widget(self.session_timer)
        layout.add_widget(controls)
        
        # Фон с градиентом
        with self.canvas.before:
            Color(0.05, 0.05, 0.1, 1)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_bg, size=self.update_bg)
        
        self.add_widget(layout)
        
    def update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
        
    def update_circle(self, *args):
        center_x = self.breathing_circle.center_x - 100
        center_y = self.breathing_circle.center_y - 100
        self.circle.pos = (center_x, center_y)
        
    def toggle_meditation(self, instance):
        """Запуск/остановка медитации"""
        if not self.meditation_active:
            self.start_meditation()
        else:
            self.stop_meditation()
            
    def start_meditation(self):
        """Начать сессию медитации"""
        self.meditation_active = True
        self.session_time = 0
        self.breath_phase = 0
        self.meditation_btn.text = 'Stop'
        self.meditation_btn.color = [1, 0.4, 0.4, 1]  # Красный
        
        # Запуск дыхательного цикла и таймера
        self.breath_timer = Clock.schedule_interval(self.breath_cycle, 1)
        Clock.schedule_interval(self.update_session_timer, 1)
        
    def stop_meditation(self):
        """Остановить медитацию"""
        self.meditation_active = False
        if self.breath_timer:
            self.breath_timer.cancel()
        self.meditation_btn.text = self.app.lang_manager.get_text('start_button')
        self.meditation_btn.color = [0.4, 1, 0.4, 1]  # Зелёный
        
        # Показать результат
        if self.session_time > 0:
            self.show_completion_popup()
            
    def breath_cycle(self, dt):
        """Цикл дыхания: 4 секунды вдох, 2 секунды задержка, 6 секунд выдох, 2 секунды задержка"""
        cycle_times = [4, 2, 6, 2]  # Время для каждой фазы
        instructions = ['breathe_in', 'hold', 'breathe_out', 'hold']
        colors = [
            [0.4, 0.8, 1, 1],    # Синий для вдоха
            [0.8, 0.8, 1, 1],    # Светло-синий для задержки
            [0.4, 1, 0.8, 1],    # Зелёный для выдоха
            [0.8, 1, 0.8, 1]     # Светло-зелёный для задержки
        ]
        circle_sizes = [250, 250, 150, 150]  # Размеры круга
        
        # Обновляем инструкцию и цвет
        self.breath_instruction.text = self.app.lang_manager.get_text(instructions[self.breath_phase])
        self.breath_instruction.color = colors[self.breath_phase]
        
        # Анимация круга
        target_size = circle_sizes[self.breath_phase]
        anim = Animation(
            size=(target_size, target_size),
            duration=cycle_times[self.breath_phase]
        )
        anim.start(self.circle)
        
        # Переход к следующей фазе
        Clock.schedule_once(
            lambda dt: self.next_breath_phase(),
            cycle_times[self.breath_phase]
        )
        
    def next_breath_phase(self):
        """Переход к следующей фазе дыхания"""
        self.breath_phase = (self.breath_phase + 1) % 4
        
    def update_session_timer(self, dt):
        """Обновление таймера сессии"""
        if self.meditation_active:
            self.session_time += 1
            minutes = self.session_time // 60
            seconds = self.session_time % 60
            self.session_timer.text = f'{minutes:02d}:{seconds:02d}'
            
    def show_completion_popup(self):
        """Показать окно завершения сессии"""
        content = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))
        
        congrats = Label(
            text=self.app.lang_manager.get_text('well_done'),
            font_size='24sp',
            color=[0.4, 1, 0.4, 1]
        )
        
        message = Label(
            text=self.app.lang_manager.get_text('session_complete'),
            font_size='16sp',
            halign='center'
        )
        message.bind(size=message.setter('text_size'))
        
        time_label = Label(
            text=f'Session time: {self.session_time // 60}:{self.session_time % 60:02d}',
            font_size='18sp',
            color=[0.4, 0.8, 1, 1]
        )
        
        close_btn = NeumorphicButton(
            text='OK',
            size_hint_y=0.3,
            font_size='16sp'
        )
        
        content.add_widget(congrats)
        content.add_widget(message)
        content.add_widget(time_label)
        content.add_widget(close_btn)
        
        popup = Popup(
            title='',
            content=content,
            size_hint=(0.8, 0.6),
            background_color=[0.1, 0.1, 0.15, 0.95]
        )
        
        close_btn.bind(on_press=popup.dismiss)
        popup.open()
        
        # Сохранить данные о сессии
        self.app.data_manager.data['meditation_sessions'] += 1
        
    def go_back(self, instance):
        """Вернуться на главный экран"""
        if self.meditation_active:
            self.stop_meditation()
        self.app.root.transition = SlideTransition(direction='right')
        self.app.root.current = 'main'

class ConcentrationScreen(Screen):
    """Экран упражнений на концентрацию"""
    def __init__(self, app, **kwargs):
        super().__init__(name='concentration', **kwargs)
        self.app = app
        self.game_active = False
        self.reaction_start_time = 0
        self.score = 0
        self.rounds = 0
        self.build_ui()
        
    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(20))
        
        # Заголовок
        title = Label(
            text=self.app.lang_manager.get_text('concentration_game'),
            font_size='22sp',
            color=[1, 1, 1, 1],
            size_hint_y=0.15
        )
        
        # Игровая область
        game_area = Widget(size_hint_y=0.5)
        
        # Круг для игры
        self.game_circle = Widget(size_hint=(0.3, 0.3))
        with self.game_circle.canvas:
            Color(1, 0.4, 0.4, 1)  # Красный по умолчанию
            self.circle_shape = Ellipse(size=(100, 100), pos=(0, 0))
        
        self.game_circle.bind(on_touch_down=self.on_circle_touch)
        game_area.add_widget(self.game_circle)
        
        # Центрирование круга
        def center_circle(*args):
            self.game_circle.center = game_area.center
            circle_center_x = self.game_circle.center_x - 50
            circle_center_y = self.game_circle.center_y - 50
            self.circle_shape.pos = (circle_center_x, circle_center_y)
            
        game_area.bind(pos=center_circle, size=center_circle)
        
        # Инструкция
        self.instruction = Label(
            text=self.app.lang_manager.get_text('focus_circle'),
            font_size='16sp',
            color=[0.8, 0.8, 0.8, 1],
            size_hint_y=0.15,
            halign='center'
        )
        self.instruction.bind(size=self.instruction.setter('text_size'))
        
        # Статистика
        stats = BoxLayout(size_hint_y=0.1, spacing=dp(20))
        
        self.score_label = Label(
            text='Score: 0',
            font_size='16sp',
            color=[0.4, 1, 0.4, 1]
        )
        
        self.reaction_label = Label(
            text=self.app.lang_manager.get_text('reaction_time').format(0),
            font_size='16sp',
            color=[0.4, 0.8, 1, 1]
        )
        
        stats.add_widget(self.score_label)
        stats.add_widget(self.reaction_label)
        
        # Кнопки
        controls = BoxLayout(size_hint_y=0.1, spacing=dp(10))
        
        back_btn = NeumorphicButton(
            text='←',
            font_size='20sp',
            size_hint_x=0.3
        )
        back_btn.bind(on_press=self.go_back)
        
        self.start_btn = NeumorphicButton(
            text=self.app.lang_manager.get_text('start_button'),
            font_size='16sp',
            color=[0.8, 0.4, 1, 1]  # Фиолетовый
        )
        self.start_btn.bind(on_press=self.start_game)
        
        controls.add_widget(back_btn)
        controls.add_widget(self.start_btn)
        
        layout.add_widget(title)
        layout.add_widget(game_area)
        layout.add_widget(self.instruction)
        layout.add_widget(stats)
        layout.add_widget(controls)
        
        # Фон
        with self.canvas.before:
            Color(0.05, 0.05, 0.1, 1)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_bg, size=self.update_bg)
        
        self.add_widget(layout)
        
    def update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
        
    def start_game(self, instance):
        """Начать игру на концентрацию"""
        if not self.game_active:
            self.game_active = True
            self.score = 0
            self.rounds = 0
            self.start_btn.text = 'Stop'
            self.start_btn.color = [1, 0.4, 0.4, 1]
            self.schedule_green_circle()
        else:
            self.stop_game()
            
    def stop_game(self):
        """Остановить игру"""
        self.game_active = False
        self.start_btn.text = self.app.lang_manager.get_text('start_button')
        self.start_btn.color = [0.8, 0.4, 1, 1]
        Clock.unschedule(self.make_circle_green)
        
        # Сделать круг красным
        with self.game_circle.canvas:
            Color(1, 0.4, 0.4, 1)
            self.circle_shape = Ellipse(size=(100, 100), pos=self.circle_shape.pos)
            
    def schedule_green_circle(self):
        """Запланировать появление зелёного круга"""
        if self.game_active:
            # Случайная задержка от 2 до 5 секунд
            delay = random.uniform(2, 5)
            Clock.schedule_once(self.make_circle_green, delay)
            
    def make_circle_green(self, dt):
        """Сделать круг зелёным"""
        if self.game_active:
            with self.game_circle.canvas:
                Color(0.4, 1, 0.4, 1)  # Зелёный
                self.circle_shape = Ellipse(size=(100, 100), pos=self.circle_shape.pos)
            
            self.reaction_start_time = Clock.get_time()
            # Планируем возврат к красному через 2 секунды, если не нажали
            Clock.schedule_once(self.make_circle_red, 2)
            
    def make_circle_red(self, dt):
        """Вернуть круг к красному цвету"""
        if self.game_active:
            with self.game_circle.canvas:
                Color(1, 0.4, 0.4, 1)  # Красный
                self.circle_shape = Ellipse(size=(100, 100), pos=self.circle_shape.pos)
            
            # Планируем следующий раунд
            self.schedule_green_circle()
            
    def on_circle_touch(self, instance, touch):
        """Обработка нажатия на круг"""
        if not self.game_active or not self.game_circle.collide_point(*touch.pos):
            return False
            
        # Проверяем, зелёный ли круг
        current_color = self.game_circle.canvas.children[-2].rgba  # Получаем цвет
        if abs(current_color[1] - 1.0) < 0.1:  # Зелёный цвет
            # Рассчитываем время реакции
            reaction_time = (Clock.get_time() - self.reaction_start_time) * 1000
            self.score += max(0, int(1000 - reaction_time))  # Больше очков за быструю реакцию
            self.rounds += 1
            
            # Обновляем интерфейс
            self.score_label.text = f'Score: {self.score}'
            self.reaction_label.text = self.app.lang_manager.get_text('reaction_time').format(int(reaction_time))
            
            # Анимация успеха
            anim = Animation(size=(120, 120), duration=0.1) + Animation(size=(100, 100), duration=0.1)
            anim.start(self.circle_shape)
            
            # Сохраняем лучший результат
            if reaction_time < 500:  # Хорошая реакция
                self.app.data_manager.data['concentration_score'] = max(
                    self.app.data_manager.data.get('concentration_score', 0),
                    self.score
                )
            
            # Возвращаем к красному и планируем следующий
            Clock.unschedule(self.make_circle_red)
            self.make_circle_red(0)
            
        return True
        
    def go_back(self, instance):
        """Вернуться на главный экран"""
        if self.game_active:
            self.stop_game()
        self.app.root.transition = SlideTransition(direction='right')
        self.app.root.current = 'main'

class EmotionalIntelligenceScreen(Screen):
    """Экран развития эмоционального интеллекта"""
    def __init__(self, app, **kwargs):
        super().__init__(name='ei', **kwargs)
        self.app = app
        self.current_tip = 0
        self.tips = [
            {
                'title': 'Self-Awareness',
                'content': 'Take 5 minutes daily to identify and name your current emotions. This simple practice increases emotional vocabulary and self-understanding.',
                'science': 'Research shows that labeling emotions activates the prefrontal cortex, which helps regulate emotional responses.'
            },
            {
                'title': 'Empathy Building',
                'content': 'When interacting with others, try to identify their emotional state before responding. Ask yourself: "What might they be feeling right now?"',
                'science': 'Mirror neuron research indicates that consciously observing others\' emotions strengthens our empathic neural pathways.'
            },
            {
                'title': 'Emotional Regulation',
                'content': 'Use the "STOP" technique: Stop what you\'re doing, Take a breath, Observe your feelings, Proceed mindfully.',
                'science': 'The pause between stimulus and response allows the prefrontal cortex to override automatic emotional reactions.'
            },
            {
                'title': 'Social Skills',
                'content': 'Practice active listening by summarizing what others say before adding your own thoughts. This builds stronger connections.',
                'science': 'Studies show that feeling heard and understood releases oxytocin, strengthening social bonds and trust.'
            },
            {
                'title': 'Motivation',
                'content': 'Connect daily tasks to your larger values and goals. Ask: "How does this align with what matters most to me?"',
                'science': 'Intrinsic motivation research shows that value-aligned activities increase dopamine and sustained effort.'
            }
        ]
        self.build_ui()
        
    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(20))
        
        # Заголовок
        title = Label(
            text=self.app.lang_manager.get_text('ei_tip'),
            font_size='24sp',
            color=[1, 1, 1, 1],
            size_hint_y=0.15
        )
        
        # Контент совета (скроллируемый)
        scroll = ScrollView(size_hint_y=0.6)
        content_layout = BoxLayout(orientation='vertical', spacing=dp(15), size_hint_y=None)
        content_layout.bind(minimum_height=content_layout.setter('height'))
        
        # Заголовок совета
        self.tip_title = Label(
            text=self.tips[0]['title'],
            font_size='20sp',
            color=[1, 0.8, 0.2, 1],  # Жёлтый
            size_hint_y=None,
            height=dp(40),
            halign='center'
        )
        self.tip_title.bind(size=self.tip_title.setter('text_size'))
        
        # Основной контент
        self.tip_content = Label(
            text=self.tips[0]['content'],
            font_size='16sp',
            color=[1, 1, 1, 1],
            size_hint_y=None,
            text_size=(None, None),
            halign='left',
            valign='top'
        )
        self.tip_content.bind(texture_size=self.tip_content.setter('size'))
        
        # Научное объяснение
        science_title = Label(
            text='💡 Scientific Insight:',
            font_size='16sp',
            color=[0.4, 0.8, 1, 1],  # Синий
            size_hint_y=None,
            height=dp(30),
            halign='left'
        )
        science_title.bind(size=science_title.setter('text_size'))
        
        self.science_content = Label(
            text=self.tips[0]['science'],
            font_size='14sp',
            color=[0.8, 0.8, 0.8, 1],
            size_hint_y=None,
            text_size=(None, None),
            halign='left',
            valign='top',
            italic=True
        )
        self.science_content.bind(texture_size=self.science_content.setter('size'))
        
        content_layout.add_widget(self.tip_title)
        content_layout.add_widget(Widget(size_hint_y=None, height=dp(10)))  # Разделитель
        content_layout.add_widget(self.tip_content)
        content_layout.add_widget(Widget(size_hint_y=None, height=dp(15)))
        content_layout.add_widget(science_title)
        content_layout.add_widget(self.science_content)
        
        scroll.add_widget(content_layout)
        
        # Навигация между советами
        nav_layout = BoxLayout(size_hint_y=0.15, spacing=dp(10))
        
        prev_btn = NeumorphicButton(
            text='← Previous',
            font_size='14sp',
            color=[0.8, 0.4, 1, 1]  # Фиолетовый
        )
        prev_btn.bind(on_press=self.previous_tip)
        
        self.tip_counter = Label(
            text=f'1/{len(self.tips)}',
            font_size='16sp',
            color=[1, 0.8, 0.2, 1],
            size_hint_x=0.3
        )
        
        next_btn = NeumorphicButton(
            text='Next →',
            font_size='14sp',
            color=[0.8, 0.4, 1, 1]
        )
        next_btn.bind(on_press=self.next_tip)
        
        nav_layout.add_widget(prev_btn)
        nav_layout.add_widget(self.tip_counter)
        nav_layout.add_widget(next_btn)
        
        # Кнопка возврата
        back_btn = NeumorphicButton(
            text='← Back to Home',
            size_hint_y=0.1,
            font_size='16sp',
            color=[0.4, 0.8, 1, 1]
        )
        back_btn.bind(on_press=self.go_back)
        
        layout.add_widget(title)
        layout.add_widget(scroll)
        layout.add_widget(nav_layout)
        layout.add_widget(back_btn)
        
        # Фон
        with self.canvas.before:
            Color(0.05, 0.05, 0.1, 1)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_bg, size=self.update_bg)
        
        self.add_widget(layout)
        
        # Обновляем размеры текста после добавления в layout
        Clock.schedule_once(self.update_text_sizes, 0.1)
        
    def update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
        
    def update_text_sizes(self, dt):
        """Обновить размеры текстовых полей"""
        if self.width > 0:
            self.tip_content.text_size = (self.width - dp(40), None)
            self.science_content.text_size = (self.width - dp(40), None)
        
    def update_tip_content(self):
        """Обновить содержимое совета"""
        tip = self.tips[self.current_tip]
        
        # Обновляем содержимое
        self.tip_title.text = tip['title']
        self.tip_content.text = tip['content']
        self.science_content.text = tip['science']
        self.tip_counter.text = f'{self.current_tip + 1}/{len(self.tips)}'
        
        # Обновляем размеры
        Clock.schedule_once(self.update_text_sizes, 0.1)
        
        # Плавная анимация появления
        self.tip_content.opacity = 0
        self.science_content.opacity = 0
        
        anim1 = Animation(opacity=1, duration=0.5)
        anim2 = Animation(opacity=1, duration=0.5)
        
        anim1.start(self.tip_content)
        Clock.schedule_once(lambda dt: anim2.start(self.science_content), 0.3)
        
    def next_tip(self, instance):
        """Следующий совет"""
        self.current_tip = (self.current_tip + 1) % len(self.tips)
        self.update_tip_content()
        
    def previous_tip(self, instance):
        """Предыдущий совет"""
        self.current_tip = (self.current_tip - 1) % len(self.tips)
        self.update_tip_content()
        
    def go_back(self, instance):
        """Вернуться на главный экран"""
        self.app.root.transition = SlideTransition(direction='right')
        self.app.root.current = 'main'

class MindWellApp(App):
    """Основной класс приложения"""
    def build(self):
        # Инициализация менеджеров
        self.data_manager = DataManager()
        self.lang_manager = LanguageManager()
        
        # Создание менеджера экранов
        sm = ScreenManager()
        sm.transition = SlideTransition()
        
        # Добавление экранов
        sm.add_widget(MainScreen(self))
        sm.add_widget(MoodScreen(self))
        sm.add_widget(MeditationScreen(self))
        sm.add_widget(ConcentrationScreen(self))
        sm.add_widget(EmotionalIntelligenceScreen(self))
        
        return sm

# Запуск приложения
if __name__ == '__main__':
    MindWellApp().run()