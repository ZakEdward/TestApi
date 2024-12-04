# Реферальная система

Это простая реферальная система, реализованная с использованием Django, Django REST Framework и PostgreSQL.

## Установка

1. Клонируйте репозиторий:

    ```bash
    git clone <repository_url>
    cd referral_system
    ```

2. Создайте и активируйте виртуальное окружение:

    ```bash
    python -m venv venv
    source venv/bin/activate  # На Windows: venv\Scripts\activate
    ```

3. Установите зависимости:

    ```bash
    pip install -r requirements.txt
    ```

4. Настройте базу данных PostgreSQL в `settings.py`:

    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'referral_system',
            'USER': 'your_db_user',
            'PASSWORD': 'your_db_password',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }
    ```

5. Примените миграции:

    ```bash
    python manage.py migrate
    ```

6. Запустите сервер разработки:

    ```bash
    python manage.py runserver
    ```

## API

### Авторизация по номеру телефона

1. **Отправка номера телефона**

    ```http
    POST /api/auth/phone/
    ```

    **Запрос:**

    ```json
    {
        "phone_number": "1234567890"
    }
    ```

    **Ответ:**

    ```json
    {
        "message": "Code sent",
        "code": "1234"
    }
    ```

2. **Ввод кода авторизации**

    ```http
    POST /api/auth/verify/
    ```

    **Запрос:**

    ```json
    {
        "phone_number": "1234567890",
        "code": "1234"
    }
    ```

    **Ответ:**

    ```json
    {
        "message": "User authenticated",
        "user_id": 1
    }
    ```

### Профиль пользователя

1. **Получение профиля пользователя**

    ```http
    GET /api/profile/<int:user_id>/
    ```

    **Ответ:**

    ```json
    {
        "phone_number": "1234567890",
        "invite_code": "ABC123",
        "referred_by": null,
        "referred_users": []
    }
    ```

2. **Активация инвайт-кода**

    ```http
    POST /api/profile/<int:user_id>/
    ```

    **Запрос:**

    ```json
    {
        "invite_code": "XYZ789"
    }
    ```

    **Ответ:**

    ```json
    {
        "message": "Invite code activated"
    }
    ```
