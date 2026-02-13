// Дожидаемся полной загрузки Telegram WebApp
document.addEventListener('DOMContentLoaded', () => {
  // Проверка: запущено ли приложение внутри Telegram
  if (!window.Telegram?.WebApp) {
    alert('Приложение должно быть запущено внутри Telegram!');
    return;
  }

  const WebApp = window.Telegram.WebApp;

  // Расширяем приложение на всю высоту
  WebApp.expand();

  // Включаем кнопку "Назад" в хедере Telegram
  WebApp.BackButton.show();
  WebApp.BackButton.onClick(() => WebApp.close());

  // Получаем данные пользователя
  const initDataUnsafe = WebApp.initDataUnsafe;
  const user = initDataUnsafe?.user;

  if (user) {
    document.getElementById('user-name').textContent = user.first_name;
    document.getElementById('user-id').textContent = user.id;
  }

  // Отображаем информацию о теме и платформе
  document.getElementById('theme').textContent = WebApp.colorScheme;
  document.getElementById('platform').textContent = WebApp.platform;

  // Счётчик
  let count = 0;
  const counterEl = document.getElementById('counter');
  document.getElementById('main-btn').addEventListener('click', () => {
    count++;
    counterEl.textContent = `Счётчик: ${count}`;

    // Показываем всплывающее уведомление в Telegram
    WebApp.showPopup({
      title: 'Успешно!',
      message: `Вы нажали ${count} раз`,
      buttons: [{ type: 'ok' }]
    });
  });

  // Кнопка закрытия
  document.getElementById('close-btn').addEventListener('click', () => {
    WebApp.close();
  });

  // Отправка данных обратно в бота (опционально)
  // WebApp.sendData('Данные от пользователя');
});