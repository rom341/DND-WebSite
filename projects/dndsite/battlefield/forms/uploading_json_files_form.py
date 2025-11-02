# my_app/forms.py

from django import forms
import json

class JsonUploadForm(forms.Form):
    """Форма для загрузки JSON-файла."""
    
    # Поле для файла
    json_file = forms.FileField(
        label='Загрузите ваш JSON-файл',
        help_text='Допускаются только файлы с расширением .json'
    )

    def clean_json_file(self):
        """
        Пользовательская проверка (валидация) для нашего поля.
        Мы проверим расширение и попробуем прочитать JSON.
        """
        file = self.cleaned_data.get('json_file')

        if not file:
            # Если файл не загружен, валидация не пройдена
            raise forms.ValidationError("Файл не был загружен.")

        # 1. Проверяем расширение файла
        if not file.name.endswith('.json'):
            raise forms.ValidationError("Это не .json файл.")

        # 2. Проверяем, что это валидный JSON
        # Мы "перематываем" файл в начало, чтобы прочитать его
        file.seek(0)
        try:
            # Читаем файл и декодируем его как текст (utf-8)
            file_content = file.read().decode('utf-8')
            json.loads(file_content)
        except json.JSONDecodeError:
            # Если json.loads() выдает ошибку, значит JSON "битый"
            raise forms.ValidationError("Не удалось разобрать JSON. Файл поврежден или имеет неверный формат.")
        except UnicodeDecodeError:
            # Если файл не в UTF-8
            raise forms.ValidationError("Ошибка кодировки файла. Пожалуйста, используйте UTF-8.")

        # Не забываем перемотать файл обратно в начало,
        # чтобы его можно было прочитать в представлении (view)
        file.seek(0)
        
        # Обязательно возвращаем "очищенные" данные
        return file