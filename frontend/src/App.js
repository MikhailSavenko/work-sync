import React, { useState } from 'react';

// Основной компонент приложения
function App() {
  // Состояния для полей формы
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  // Состояние для отображения сообщений пользователю (успех/ошибка)
  const [message, setMessage] = useState('');
  const [messageType, setMessageType] = useState(''); // 'success' или 'error'

  // URL вашего Djoser API для регистрации
  // Убедитесь, что это правильный URL для вашего проекта
  // Например: 'http://localhost/auth/users/' если Nginx проксирует на Djoser
  const API_REGISTRATION_URL = 'http://localhost/api/v1/users/'; // Пример URL для Djoser /users/ endpoint

  // Обработчик отправки формы
  const handleSubmit = async (e) => {
    e.preventDefault(); // Предотвращаем стандартное поведение формы

    // Очищаем предыдущие сообщения
    setMessage('');
    setMessageType('');

    // Простая клиентская валидация
    if (!email || !password || !confirmPassword) {
      setMessage('Пожалуйста, заполните все поля.');
      setMessageType('error');
      return;
    }

    if (password !== confirmPassword) {
      setMessage('Пароли не совпадают.');
      setMessageType('error');
      return;
    }

    if (password.length < 8) { // Пример минимальной длины пароля
        setMessage('Пароль должен быть не менее 8 символов.');
        setMessageType('error');
        return;
    }

    try {
      const response = await fetch(API_REGISTRATION_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        // Отправляем данные в формате JSON.
        // Djoser обычно ожидает email и password.
        // Если ваша модель пользователя в Django использует 'username' как USERNAME_FIELD,
        // то Djoser может также ожидать поле 'username'.
        // В вашем случае email - USERNAME_FIELD, поэтому username не нужен,
        // но проверьте конфигурацию Djoser, если возникнут проблемы.
        body: JSON.stringify({
          email: email,
          password: password,
        // Если Djoser ожидает подтверждение пароля на бэкенде:
        // re_password: confirmPassword
        }),
      });

      // Проверяем статус ответа
      if (response.ok) {
        // Успешная регистрация
        const data = await response.json();
        setMessage('Регистрация прошла успешно! Теперь вы можете войти.');
        setMessageType('success');
        // Очищаем форму после успешной регистрации
        setEmail('');
        setPassword('');
        setConfirmPassword('');
      } else {
        // Ошибка регистрации
        const errorData = await response.json();
        // Djoser возвращает ошибки в формате JSON, например:
        // {"email": ["Пользователь с таким email уже существует."]}
        // {"password": ["Слишком простой пароль."]}
        let errorMessage = 'Ошибка регистрации.';
        if (errorData) {
          // Итерируемся по ошибкам и формируем сообщение
          errorMessage = Object.entries(errorData)
            .map(([field, errors]) => `${field}: ${errors.join(', ')}`)
            .join('; ');
        }
        setMessage(`Ошибка: ${errorMessage}`);
        setMessageType('error');
      }
    } catch (error) {
      // Ошибка сети или другая непредвиденная ошибка
      setMessage(`Произошла сетевая ошибка: ${error.message}. Пожалуйста, попробуйте еще раз.`);
      setMessageType('error');
      console.error('Сетевая ошибка:', error);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100 p-4 font-sans">
      <div className="bg-white p-8 rounded-lg shadow-xl w-full max-w-md">
        <h2 className="text-3xl font-bold text-center text-gray-800 mb-8">Регистрация</h2>

        {/* Контейнер для сообщений */}
        {message && (
          <div
            className={`p-3 mb-4 rounded-md text-sm ${
              messageType === 'success'
                ? 'bg-green-100 text-green-700'
                : 'bg-red-100 text-red-700'
            }`}
            role="alert"
          >
            {message}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label htmlFor="email" className="block text-sm font-medium text-gray-700">
              Email
            </label>
            <input
              type="email"
              id="email"
              className="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm transition duration-150 ease-in-out"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>

          <div>
            <label htmlFor="password" className="block text-sm font-medium text-gray-700">
              Пароль
            </label>
            <input
              type="password"
              id="password"
              className="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm transition duration-150 ease-in-out"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          <div>
            <label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-700">
              Подтверждение пароля
            </label>
            <input
              type="password"
              id="confirmPassword"
              className="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm transition duration-150 ease-in-out"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              required
            />
          </div>

          <button
            type="submit"
            className="w-full flex justify-center py-3 px-4 border border-transparent rounded-md shadow-sm text-lg font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition duration-200 ease-in-out transform hover:scale-105"
          >
            Зарегистрироваться
          </button>
        </form>

        <p className="mt-6 text-center text-sm text-gray-600">
          Уже есть аккаунт?{' '}
          <a href="#" className="font-medium text-blue-600 hover:text-blue-500">
            Войти
          </a>
        </p>
      </div>
    </div>
  );
}

export default App; // Экспортируем компонент App по умолчанию
