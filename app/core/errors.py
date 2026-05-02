class AppException(Exception):
    """Базовое исключение приложения"""
    pass

class ConflictError(AppException):
    """Конфликт (например, email уже занят)"""
    pass

class UnauthorizedError(AppException):
    """Неверный логин, пароль или токен"""
    pass

class ForbiddenError(AppException):
    """Нет прав доступа"""
    pass

class NotFoundError(AppException):
    """Объект не найден"""
    pass

class ExternalServiceError(AppException):
    """Ошибка при обращении к внешнему API"""
    pass
