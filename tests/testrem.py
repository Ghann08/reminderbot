import asyncio
import unittest
from datetime import datetime, timedelta
from unittest.mock import patch
from services.remindres import Reminders


class TestReminders(unittest.IsolatedAsyncioTestCase):
    async def test_initialization(self):
        """Тест инициализации напоминания"""
        text = "Тестовое напоминание"
        future_date = datetime.now() + timedelta(minutes=5)
        reminder = Reminders(text=text, date=future_date)

        self.assertEqual(reminder._text, text)
        self.assertEqual(reminder._date, future_date)
        self.assertIsNotNone(reminder._id_remind)
        self.assertFalse(reminder._remind.done())

    async def test_reminder_trigger(self):
        """Тест срабатывания напоминания"""
        text = "Срочное напоминание"
        past_date = datetime.now() - timedelta(seconds=1)  # Дата уже прошла

        with patch('builtins.print') as mock_print:
            reminder = Reminders(text=text, date=past_date)
            await asyncio.sleep(0.1)  # Даем время на выполнение

            mock_print.assert_called_once_with(f"Напоминание: {text}")
            self.assertTrue(reminder._remind.done())

    async def test_update_method(self):
        """Тест обновления напоминания"""
        original_text = "Старый текст"
        new_text = "Новый текст"
        original_date = datetime.now() + timedelta(minutes=10)
        new_date = datetime.now() + timedelta(minutes=20)

        reminder = Reminders(text=original_text, date=original_date)
        reminder._update(text=new_text, date=new_date)

        self.assertEqual(reminder._text, new_text)
        self.assertEqual(reminder._date, new_date)

    async def test_reminder_with_future_date(self):
        """Тест напоминания с будущей датой"""
        text = "Будущее напоминание"
        future_date = datetime.now() + timedelta(seconds=1)

        with patch('builtins.print') as mock_print:
            reminder = Reminders(text=text, date=future_date)
            self.assertFalse(reminder._remind.done())

            await asyncio.sleep(1.1)  # Ждем, когда дата наступит

            mock_print.assert_called_once_with(f"Напоминание: {text}")
            self.assertTrue(reminder._remind.done())

    async  def test_update_none(self):
        text = "Будущее напоминание"
        future_date = datetime.now() + timedelta(seconds=20)
        reminder = Reminders(text=text, date=future_date)
        reminder._update(text=None, date=None)
        self.assertEqual(reminder._text, text)
        self.assertEqual(reminder._date, future_date)

    async  def test_update_past(self):
        text = "Будущее напоминание"
        future_date = datetime.now() + timedelta(seconds=20)
        past_date = datetime.now() - timedelta(seconds=180)
        reminder = Reminders(text=text, date=future_date)
        reminder._update(date=past_date)
        self.assertEqual(reminder._text, text)
        self.assertEqual(reminder._date, future_date)

    if __name__ == '__main__':
        unittest.main()