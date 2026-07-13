<?php
// Шаблон конфига. Скопировать в config.php и подставить реальные значения.
// config.php в git НЕ попадает (см. .gitignore) — это защита токена.
return [
    'bot_token' => 'ВСТАВЬ_ТОКЕН_ОТ_BOTFATHER',

    // Telegram user_id получателей заявок (те, кто нажал Start у бота).
    'chat_ids' => [
        0, // заменить на реальный user_id
    ],
];
