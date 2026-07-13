<?php
// Приём заявки с сайта → отправка в Telegram через бота @EnersGroupBot.
// Токен и получатели берутся из config.php (не в git, не во фронтенде).

header('Content-Type: application/json; charset=utf-8');

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['ok' => false, 'error' => 'Method not allowed'], JSON_UNESCAPED_UNICODE);
    exit;
}

$configFile = __DIR__ . '/config.php';
if (!is_file($configFile)) {
    http_response_code(500);
    echo json_encode(['ok' => false, 'error' => 'Сервер не настроен'], JSON_UNESCAPED_UNICODE);
    exit;
}
$config = require $configFile;

// Антиспам: скрытое поле-ловушка (honeypot). Боты его заполняют — люди нет.
if (trim($_POST['company'] ?? '') !== '') {
    echo json_encode(['ok' => true], JSON_UNESCAPED_UNICODE); // делаем вид, что успех
    exit;
}

$name    = trim($_POST['name'] ?? '');
$contact = trim($_POST['contact'] ?? '');
$task    = trim($_POST['task'] ?? '');

if ($name === '' || $contact === '') {
    http_response_code(422);
    echo json_encode(['ok' => false, 'error' => 'Заполните имя и контакт'], JSON_UNESCAPED_UNICODE);
    exit;
}

// Ограничения длины
$name    = mb_substr($name, 0, 100);
$contact = mb_substr($contact, 0, 100);
$task    = mb_substr($task, 0, 2000);

$esc  = fn($s) => htmlspecialchars($s, ENT_QUOTES, 'UTF-8');
$text = "🔔 <b>Новая заявка с сайта enersgroup.ru</b>\n\n"
      . "👤 <b>Имя:</b> " . $esc($name) . "\n"
      . "📞 <b>Контакт:</b> " . $esc($contact) . "\n"
      . "📝 <b>Задача:</b> " . ($task !== '' ? $esc($task) : '—');

$sentAny = false;
foreach ($config['chat_ids'] as $chatId) {
    if (tg_send($config['bot_token'], $chatId, $text)) {
        $sentAny = true;
    }
}

if ($sentAny) {
    echo json_encode(['ok' => true], JSON_UNESCAPED_UNICODE);
} else {
    http_response_code(502);
    echo json_encode(['ok' => false, 'error' => 'Не удалось отправить заявку'], JSON_UNESCAPED_UNICODE);
}

function tg_send(string $token, $chatId, string $text): bool {
    $url = "https://api.telegram.org/bot{$token}/sendMessage";
    $payload = http_build_query([
        'chat_id'                  => $chatId,
        'text'                     => $text,
        'parse_mode'               => 'HTML',
        'disable_web_page_preview' => true,
    ]);
    $ch = curl_init($url);
    curl_setopt_array($ch, [
        CURLOPT_POST           => true,
        CURLOPT_POSTFIELDS     => $payload,
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_TIMEOUT        => 15,
    ]);
    $res  = curl_exec($ch);
    $code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);
    if ($res === false || $code !== 200) {
        return false;
    }
    $data = json_decode($res, true);
    return isset($data['ok']) && $data['ok'] === true;
}
