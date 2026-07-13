#!/usr/bin/env python3
# Сборка многостраничного сайта Eners Group из общих партиалов.
# Общие шапка/подвал/head → в один скрипт, страницы = контент во фрагментах ниже.
# Запуск:  python3 build.py   → генерирует html-файлы в корне проекта.
import os

ROOT = os.path.dirname(os.path.abspath(__file__))

def HEAD(title, desc):
    return f'''<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#ffffff">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/img/favicon-32.png">
<link rel="icon" type="image/png" sizes="16x16" href="/assets/img/favicon-16.png">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="stylesheet" href="/styles.css">
</head>
<body>'''

def HEADER(active=""):
    def a(href, key, label):
        cls = ' class="active"' if key == active else ''
        return f'<a href="{href}"{cls}>{label}</a>'
    return f'''
<header>
  <div class="wrap nav">
    <a class="logo" href="/"><img class="logo-img" src="/assets/img/logo-navy.png" alt="ЭНЕРС"><span class="logo-tag">Энергетика и<br>инженерные системы</span></a>
    <nav class="nav-links">
      {a("/uslugi/","uslugi","Услуги")}
      {a("/energoservis.html","energoservis","Энергосервис")}
      {a("/proekty/","proekty","Проекты")}
      {a("/o-kompanii.html","company","О компании")}
      {a("/kontakty.html","contacts","Контакты")}
    </nav>
    <div class="nav-cta">
      <a class="nav-mail" href="mailto:info@enersgroup.ru">info@enersgroup.ru</a>
      <a class="btn btn-primary" href="/kontakty.html">Оставить заявку</a>
      <button class="burger" aria-label="Меню">☰</button>
    </div>
  </div>
</header>'''

def CRUMB(items):
    # items: [(label, href|None)]
    parts = []
    for label, href in items:
        parts.append(f'<a href="{href}">{label}</a>' if href else f'<span>{label}</span>')
    return '<div class="crumbs wrap">' + '<i>/</i>'.join(parts) + '</div>'

FOOTER = '''
<footer>
  <div class="wrap">
    <div class="foot-grid">
      <div class="foot-col">
        <div class="logo"><img class="logo-img" src="/assets/img/logo-white.png" alt="ЭНЕРС ГРУПП"></div>
        <p class="foot-about">Распределённая энергетика и энергосервис для промышленных предприятий: энергоцентры, котельные, инженерные системы под ключ.</p>
      </div>
      <div class="foot-col">
        <h4>Услуги</h4>
        <a href="/uslugi/#energocentry">Энергоцентры на ГПУ</a>
        <a href="/uslugi/#kotelnye">Котельные</a>
        <a href="/uslugi/#btp">Тепловые пункты</a>
        <a href="/uslugi/#kompressornye">Компрессорные станции</a>
        <a href="/energoservis.html">Энергосервис</a>
      </div>
      <div class="foot-col">
        <h4>Компания</h4>
        <a href="/o-kompanii.html">О компании</a>
        <a href="/proekty/">Проекты</a>
        <a href="/kontakty.html">Контакты</a>
      </div>
      <div class="foot-col">
        <h4>Контакты</h4>
        <a href="mailto:info@enersgroup.ru">info@enersgroup.ru</a>
        <p>603016, г. Нижний Новгород,<br>ул. Героя Юрия Смирнова, д. 2</p>
        <p>Офисы: Нижний Новгород · Миасс</p>
      </div>
    </div>
    <div class="foot-bottom">
      <div>© 2026 ООО «ЭНЕРСГРУПП» · ОГРН 1225200005722 · ИНН 5256201227</div>
      <div><a href="/politika.html">Политика конфиденциальности</a> · Распределённая энергетика · ГПУ · Котельные</div>
    </div>
  </div>
</footer>'''

SCRIPT = '''
<script>
  document.querySelector('.burger')?.addEventListener('click',()=>{
    const n=document.querySelector('.nav-links');const open=n.style.display==='flex';
    n.style.display=open?'':'flex';
    if(!open){n.style.position='absolute';n.style.top='74px';n.style.left='0';n.style.right='0';
      n.style.flexDirection='column';n.style.background='#fff';n.style.padding='18px 24px';
      n.style.borderBottom='1px solid var(--line)';n.style.boxShadow='var(--shadow)';n.style.gap='16px'}
  });
  (function(){
    const form=document.getElementById('lead-form');if(!form)return;
    const note=form.querySelector('.form-note'),btn=form.querySelector('button[type=submit]');
    const nm=document.getElementById('lf-name'),ct=document.getElementById('lf-contact');
    form.addEventListener('submit',async(e)=>{e.preventDefault();
      if(!nm.value.trim()||!ct.value.trim()){note.textContent='Заполните имя и контакт для связи.';return;}
      const cons=form.querySelector('[name=consent]');if(cons&&!cons.checked){note.textContent='Подтвердите согласие на обработку персональных данных.';return;}
      const o=btn.textContent;btn.disabled=true;btn.textContent='Отправляем…';note.textContent='';
      try{const r=await fetch('/api/send.php',{method:'POST',body:new FormData(form)});
        const d=await r.json().catch(()=>({}));
        if(r.ok&&d.ok){form.reset();note.textContent='✓ Заявка отправлена. Мы свяжемся с вами.';}
        else{note.textContent=d.error||'Не удалось отправить. Напишите нам в Telegram или позвоните.';}
      }catch(err){note.textContent='Не удалось отправить. Проверьте соединение.';}
      finally{btn.disabled=false;btn.textContent=o;}
    });
  })();
  // калькулятор экономии ЭСК (только на странице с #c-load)
  (function(){
    const load=document.getElementById('c-load');if(!load)return;
    const ids=['c-load','c-hours','c-tariff','c-gas'].map(i=>document.getElementById(i));
    const eff=0.42,lhv=9.3,om=2.5;
    const ru=n=>n.toLocaleString('ru-RU',{maximumFractionDigits:0});
    const one=n=>n.toFixed(1).replace('.',',');
    function calc(){
      const [L,H,T,G]=ids.map(e=>parseFloat(e.value)||0);
      const cost=G/(eff*lhv)+om;
      const delta=Math.max(T-cost,0);
      const year=L*H*delta;
      document.getElementById('o-cost').textContent=one(cost)+' ₽/кВт·ч';
      document.getElementById('o-delta').textContent=one(delta)+' ₽/кВт·ч';
      document.getElementById('o-year').textContent=ru(year)+' ₽';
    }
    ids.forEach(e=>e.addEventListener('input',calc));calc();
  })();
</script>
</body></html>'''

LEAD_FORM = '''<form id="lead-form" class="lead" novalidate>
  <div><label for="lf-name">Имя</label><input id="lf-name" name="name" type="text" autocomplete="name" placeholder="Как к вам обращаться" required></div>
  <div><label for="lf-contact">Телефон или e-mail</label><input id="lf-contact" name="contact" type="text" autocomplete="tel" placeholder="Для связи" required></div>
  <div><label for="lf-task">Задача</label><textarea id="lf-task" name="task" rows="4" placeholder="Кратко об объекте, нагрузках, сроках"></textarea></div>
  <input type="text" name="company" tabindex="-1" autocomplete="off" aria-hidden="true" style="position:absolute;left:-9999px;width:1px;height:1px;opacity:0">
  <label class="consent"><input type="checkbox" name="consent" required> Я согласен(на) на обработку персональных данных согласно <a href="/politika.html" target="_blank" rel="noopener">Политике конфиденциальности</a></label>
  <button class="btn btn-primary btn-lg" type="submit">Отправить заявку →</button>
  <p class="form-note" role="status" aria-live="polite">Заявка уходит напрямую в Telegram — ответим в течение рабочего дня.</p>
</form>'''

# ---------- СТРАНИЦЫ ----------
PAGES = {}

PAGES["kontakty.html"] = dict(
  title="Контакты — Eners Group",
  desc="Контакты ООО «ЭНЕРСГРУПП»: офисы в Нижнем Новгороде и Миассе, e-mail info@enersgroup.ru. Оставьте заявку на энергопроект.",
  active="contacts",
  body=f'''
{CRUMB([("Главная","/"),("Контакты",None)])}
<section class="section page-head">
  <div class="wrap">
    <p class="eyebrow">Контакты</p>
    <h1 class="page-title">Обсудим ваш энергопроект</h1>
    <p class="page-lead">Оставьте заявку — рассчитаем мощность, сроки и экономию под ваш объект. Или свяжитесь напрямую.</p>
  </div>
</section>
<section class="section" style="padding-top:0">
  <div class="wrap contact-grid">
    <div class="contact-info-col">
      <div class="ci-block">
        <h3>E-mail</h3>
        <a href="mailto:info@enersgroup.ru" class="ci-big">info@enersgroup.ru</a>
      </div>
      <div class="ci-block">
        <h3>Офис · Нижний Новгород</h3>
        <p>603016, г. Нижний Новгород,<br>ул. Героя Юрия Смирнова, д. 2</p>
      </div>
      <div class="ci-block">
        <h3>Офис · Миасс</h3>
        <p>456304, Челябинская обл.,<br>г. Миасс, пр. Автозаводцев, д. 1</p>
      </div>
      <div class="ci-block">
        <h3>Реквизиты</h3>
        <p>ООО «ЭНЕРСГРУПП»<br>ОГРН 1225200005722 · ИНН 5256201227</p>
      </div>
    </div>
    <div class="form-card">
      <h3 style="margin-bottom:6px;color:var(--navy);font-size:22px">Оставить заявку</h3>
      <p style="color:var(--muted);margin:0 0 18px;font-size:15px">Заполните форму — заявка сразу уйдёт нам в Telegram.</p>
      {LEAD_FORM}
    </div>
  </div>
</section>''')


SERVICES = [
 dict(k="energocentry", p="M13 2 3 14 12 14 11 22 21 10 12 10 13 2", kind="polygon",
  title="Энергоцентры на ГПУ",
  lead="Автономная электростанция на площадке предприятия — электроэнергия, тепло и холод из одного источника.",
  body="Проектируем и строим энергоцентры на газопоршневых установках единичной мощностью от 1 до 25 МВт. За счёт когенерации (одновременная выработка электроэнергии и тепла), а при необходимости тригенерации (плюс холод через абсорбционную машину) коэффициент использования топлива достигает 80–90 %, а себестоимость собственной энергии в 2–3 раза ниже сетевых тарифов. Работаем на природном, попутном нефтяном и других горючих газах — в параллели с сетью или в островном режиме.",
  incl=["ТЭО, расчёт нагрузок и подбор мощности","ГПУ Weichai и Jichai под топливо и режим","Когенерация — утилизация тепла выхлопа и рубашки","Тригенерация — холод через АБХМ","Синхронизация с сетью, РЗА, распредустройство","АСУ ТП, диспетчеризация, учёт","Здание/укрытие, градирни, обвязка"],
  apply="Промышленные предприятия с постоянной электрической и тепловой нагрузкой, площадки с дефицитом или дорогим сетевым питанием.",
  img="energocentr-3d.jpg",
  spec='''<div class="spec"><h4>Линейки ГПУ (единичная мощность)</h4>
        <div class="spec-row"><b>Weichai</b><span>0,3–1,5 МВт</span></div>
        <div class="spec-row"><b>Jichai (CNPC), серии 190 / 6000</b><span>0,5–2,0 МВт</span></div>
        <div class="spec-row"><b>Энергоцентр из нескольких ГПУ</b><span>до 25 МВт</span></div></div>'''),
 dict(k="kotelnye", p="M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.38-.5-2-1-3-1.07-2.14-.22-4.05 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.15.43-2.29 1-3a2.5 2.5 0 0 0 2.5 2.5Z", kind="path",
  title="Котельные",
  lead="Пар, горячая вода и термомасло для технологии и отопления.",
  body="Проектируем и строим паровые, водогрейные котельные и установки на термическом масле — блочно-модульные и стационарные. Полный цикл: ТЭО и проект, поставка котлов и вспомогательного оборудования, строительство, пусконаладка и сервис. Реконструируем действующие котельные с ростом КПД и переводом на автоматическую работу без постоянного персонала.",
  incl=["Паровые котельные — насыщенный и перегретый пар","Водогрейные котельные для отопления и ГВС","Термомасляные установки для технологии","Блочно-модульные котельные (БМК) заводской готовности","ХВО, деаэрация, насосные группы, обвязка","Автоматика и диспетчеризация"],
  apply="Технологический пар, отопление и горячее водоснабжение промышленных площадок.",
  img="kotelnaya-6mvt.jpg", spec=None),
 dict(k="btp", p="M14 4v10.54a4 4 0 1 1-4 0V4a2 2 0 0 1 4 0Z", kind="path",
  title="Блочные тепловые пункты",
  lead="Узел, который распределяет тепло по объекту и держит параметры под контролем.",
  body="Блочные и индивидуальные тепловые пункты (БТП/ИТП) полной заводской готовности для отопления, вентиляции и ГВС. Собираем на раме, испытываем на заводе и привозим готовый модуль — на площадке остаётся минимум монтажа. Погодозависимая автоматика и частотное регулирование насосов снижают потребление, узлы учёта дают прозрачную картину расхода.",
  incl=["Теплообменники отопления, ГВС, вентиляции","Насосные группы с частотным регулированием","Погодозависимая автоматика","Узлы коммерческого учёта тепла","Диспетчеризация и удалённый мониторинг"],
  apply="Производственные, административные и жилые объекты любого масштаба.",
  img="btp.jpg", spec=None),
 dict(k="kompressornye", p="M12 14l4-4|M3.34 19a10 10 0 1 1 17.32 0", kind="path",
  title="Компрессорные станции",
  lead="Сжатый воздух нужного качества и давления — без перебоев.",
  body="Проектируем, поставляем, монтируем и обслуживаем компрессорные станции сжатого воздуха. Подбираем винтовые и центробежные компрессоры под фактический расход и давление, проектируем осушку, фильтрацию, ресиверы и разводку. Настраиваем управление по нагрузке (каскад, частотный привод) — это заметно снижает затраты на электроэнергию при переменном потреблении.",
  incl=["Винтовые и центробежные компрессоры","Осушители, фильтры, ресиверы","Трубопроводная разводка сжатого воздуха","Система управления и учёта потребления","Сервис, ремонт, аудит пневмосети"],
  apply="Любое производство, где используется сжатый воздух в технологии.",
  img="real/ks-1.jpg", spec=None),
 dict(k="nasosnye", p="M12 22a7 7 0 0 0 7-7c0-2-1-3.9-3-5.5s-3.5-4-4-6.5c-.5 2.5-2 4.9-4 6.5C6 11.1 5 13 5 15a7 7 0 0 0 7 7z", kind="path",
  title="Насосные станции",
  lead="Надёжная подача воды и технологических сред под нужным давлением.",
  body="Насосные станции водоснабжения, пожаротушения и технологических сред. Подбираем насосное оборудование, проектируем станции повышения давления с частотным регулированием, автоматику и диспетчеризацию. Блочно-модульное исполнение полной заводской готовности сокращает сроки ввода.",
  incl=["Станции хозпитьевого и технического водоснабжения","Станции пожаротушения","Повышение давления с частотным регулированием","Автоматика и диспетчеризация","Блочно-модульные решения «под ключ»"],
  apply="Промышленные площадки, объекты водоснабжения и пожарной безопасности.",
  img="real/ks-2.jpg", spec=None),
 dict(k="co2", p="M17.7 7.7a2.5 2.5 0 1 1 1.8 4.3H2|M9.6 4.6A2 2 0 1 1 11 8H2|M12.6 19.4A2 2 0 1 0 14 16H2", kind="path",
  title="Извлечение CO₂ из дымовых газов",
  lead="Товарный диоксид углерода из собственных дымовых газов.",
  body="Установки улавливания и очистки CO₂ из дымовых газов котельных и газопоршневых генераторов. Углекислота, которая раньше уходила в атмосферу, становится товарным продуктом (пищевой или технический CO₂) либо используется в собственной технологии — при одновременном снижении углеродного следа предприятия. Хорошо дополняет энергоцентр или котельную как источник дополнительной выручки.",
  incl=["Улавливание CO₂ из дымовых газов","Очистка и осушка газа","Сжижение и хранение","Интеграция с энергоцентром или котельной"],
  apply="Производства с дымовыми газами и потребностью в CO₂: пищепром, тепличные комплексы, сварочные производства.",
  img=None, spec=None),
 dict(k="gazoluchistoe", p="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4", kind="sun",
  title="Газолучистое отопление и освещение",
  lead="Обогрев больших цехов там, где греть весь объём воздуха дорого.",
  body="Системы газолучистого (инфракрасного) отопления нагревают не воздух, а поверхности, оборудование и людей — это эффективно для высоких и просторных производственных помещений, где воздушное отопление избыточно и дорого. Проектируем светлые и тёмные инфракрасные обогреватели, зональное управление под геометрию цеха, а также промышленное освещение.",
  incl=["Инфракрасные газовые обогреватели (светлые/тёмные)","Зональное управление по участкам","Расчёт и проект под геометрию помещения","Промышленное освещение цехов"],
  apply="Цеха, склады, ангары, СТО, логистические комплексы с большой площадью.",
  img=None, spec=None),
 dict(k="askue", p="M22 12h-4l-3 9L9 3l-3 9H2", kind="path",
  title="АСКУЭ и диспетчеризация",
  lead="Видеть, где уходит энергия, и управлять оборудованием удалённо.",
  body="Автоматизированные системы коммерческого и технического учёта энергоресурсов (АСКУЭ) и диспетчеризация инженерного оборудования. Собираем данные по электроэнергии, теплу, газу и воде; разворачиваем SCADA, удалённый мониторинг и управление, интеграцию с ERP и верхним уровнем. Это же — основа для честного подтверждения экономии по энергосервисному контракту.",
  incl=["Узлы учёта электроэнергии, тепла, газа, воды","SCADA и диспетчерский пункт","Удалённый мониторинг и управление 24/7","Отчётность и интеграция с ERP","База для подтверждения экономии по ЭСК"],
  apply="Предприятия, которым нужен прозрачный учёт ресурсов и удалённое управление инженерными системами.",
  img=None, spec=None),
]
def svc_icon(paths, kind):
    if kind=="polygon":
        inner='<polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>'
    elif kind=="sun":
        inner=f'<circle cx="12" cy="12" r="4"/><path d="{paths}"/>'
    else:
        inner="".join(f'<path d="{p}"/>' for p in paths.split("|"))
    return f'<svg viewBox="0 0 24 24">{inner}</svg>'

# ---- УСЛУГИ (обзор с якорями на каждое направление) ----
svc_cards="".join(f'''
      <a class="svc reveal" href="/uslugi/#{s['k']}">
        <div class="ic">{svc_icon(s['p'],s['kind'])}</div>
        <h3>{s['title']}</h3><p>{s['lead']}</p><span class="more">Подробнее</span>
      </a>''' for s in SERVICES)

def svc_block(i, s):
    incl="".join(f'<li>{x}</li>' for x in s['incl'])
    media=f'<div class="usluga-media"><img src="/assets/img/{s["img"]}" alt="{s["title"]} — Eners Group" loading="lazy"></div>' if s['img'] else ''
    cls="usluga"+("" if s['img'] else " no-media")+(" rev" if (s['img'] and i%2) else "")
    return f'''
  <section class="section{' soft' if i%2 else ''}" id="{s['k']}">
    <div class="wrap {cls}">
      {media}
      <div class="usluga-body reveal">
        <div class="ic">{svc_icon(s['p'],s['kind'])}</div>
        <h2>{s['title']}</h2>
        <p class="usluga-lead">{s['lead']}</p>
        <p>{s['body']}</p>
        <div class="usluga-cols">
          <div><h4>Что входит</h4><ul>{incl}</ul></div>
          <div><h4>Где применяется</h4><p>{s['apply']}</p>{s['spec'] or ''}</div>
        </div>
        <a class="btn btn-primary" href="/kontakty.html">Обсудить проект →</a>
      </div>
    </div>
  </section>'''
svc_sections="".join(svc_block(i,s) for i,s in enumerate(SERVICES))

INDUSTRIES=[
 ("Пищевая промышленность","Стабильные электро- и тепловые нагрузки, потребность в паре, холоде и пищевом CO₂."),
 ("Тепличные комплексы","Электроэнергия, тепло и CO₂ для досветки и подкормки — из одного энергоцентра."),
 ("Целлюлозно-бумажные производства","Большие объёмы пара и электроэнергии в непрерывном режиме работы."),
 ("Машиностроение и металлообработка","Сжатый воздух, тепло и надёжное электроснабжение производственных цехов."),
 ("Нефтегаз и добыча","Автономная генерация на попутном газе, энергоснабжение удалённых площадок."),
 ("Логистика и склады","Отопление больших площадей, освещение и резервное электроснабжение."),
]
industries="".join(f'''
      <div class="ind reveal"><h3>{n}</h3><p>{d}</p></div>''' for (n,d) in INDUSTRIES)

PAGES["uslugi/index.html"]=dict(title="Услуги — Eners Group",
  desc="Направления Eners Group: энергоцентры на ГПУ, котельные, тепловые пункты, компрессорные и насосные станции, извлечение CO₂, газолучистое отопление, АСКУЭ и диспетчеризация.",
  active="uslugi", body=f'''
{CRUMB([("Главная","/"),("Услуги",None)])}
<section class="section page-head"><div class="wrap">
  <p class="eyebrow">Направления</p>
  <h1 class="page-title">Инженерные системы энергоснабжения под ключ</h1>
  <p class="page-lead">Полный цикл — проект, поставка, строительство и сервис. Всё по модели энергосервиса, с оплатой из вашей экономии.</p>
</div></section>
<section class="section" style="padding-top:0"><div class="wrap"><div class="grid g-4">{svc_cards}</div></div></section>
{svc_sections}
<section class="section"><div class="wrap">
  <div class="section-head reveal"><p class="eyebrow">Отрасли применения</p>
    <h2>Где мы решаем задачи энергоснабжения</h2>
    <p>Подбираем состав энергетической инфраструктуры под режим работы и нагрузки конкретного производства.</p></div>
  <div class="grid g-3">{industries}</div>
</div></section>
<section class="section soft"><div class="wrap"><div class="cta reveal">
  <h2>Не нашли нужное направление?</h2><p>Мы закрываем весь спектр энергетических и инженерных систем предприятия. Опишите задачу — предложим решение.</p>
  <a class="btn btn-primary btn-lg" href="/kontakty.html">Оставить заявку →</a></div></div></section>''')

# ---- ПРОЕКТЫ ----
PROJECTS=[
 ("real/ural-gpu-2.jpg","Энергоцентр на ГПУ","Урал","6 МВт · энергосервис 6 лет","3 рабочих ГПУ + 1 резервная, параллель с сетью, трубный газ. Оплата из экономии."),
 ("real/atmosfera-1.jpg","Энергоцентр","Атмосфера","Стальные конструкции · градирни","Компоновка энергоцентра с градирнями и системой оборотного водоснабжения."),
 ("real/ks-1.jpg","Компрессорная станция","—","Винтовые компрессоры","Станция сжатого воздуха: компрессоры, ресиверы, осушка, обвязка."),
 ("real/miass-1.jpg","Энергоцентр · Миасс","Миасс","Строительство и монтаж","Возведение энергоцентра: металлоконструкции, градирни, обвязка."),
 ("real/ks-2.jpg","Машинное отделение","—","Насосно-компрессорное оборудование","Монтаж технологического оборудования и трубопроводной обвязки."),
 ("real/ural-gpu-3.jpg","Машинный зал ГПУ","Урал","Когенерация","Газопоршневые двигатели с утилизацией тепла в машинном зале."),
]
def proj_card(img,t,client,sub,desc):
    params="".join(f'<span>{x.strip()}</span>' for x in sub.split('·') if x.strip())
    loc=f'<em>{client}</em>' if client and client!='—' else ''
    return f'''
      <article class="proj reveal">
        <div class="proj-img"><img src="/assets/img/{img}" alt="{t}" loading="lazy"></div>
        <div class="proj-body">
          <div class="proj-head"><b>{t}</b>{loc}</div>
          <div class="proj-params">{params}</div>
          <p class="proj-desc">{desc}</p>
        </div>
      </article>'''
proj_cards="".join(proj_card(*p) for p in PROJECTS)
PAGES["proekty/index.html"]=dict(title="Проекты — Eners Group",
  desc="Реализованные объекты Eners Group: энергоцентры на ГПУ, котельные, компрессорные станции. Реальные фотографии объектов.",
  active="proekty", body=f'''
{CRUMB([("Главная","/"),("Проекты",None)])}
<section class="section page-head"><div class="wrap">
  <p class="eyebrow">Проекты</p>
  <h1 class="page-title">Реализованные объекты</h1>
  <p class="page-lead">Энергоцентры, котельные и инженерные системы, построенные и обслуживаемые нашей командой. Более 100 МВт и 30+ объектов.</p>
</div></section>
<section class="section" style="padding-top:0"><div class="wrap"><div class="grid g-3">{proj_cards}</div>
  <p style="text-align:center;color:var(--muted);margin-top:32px;font-size:15px">Подписи и характеристики объектов уточняются. По части проектов действует NDA.</p>
</div></section>
<section class="stats-band"><div class="wrap">
  <div class="stat reveal"><b>100+ МВт</b><span>реализованной мощности</span></div>
  <div class="stat reveal"><b>30+</b><span>объектов под ключ</span></div>
  <div class="stat reveal"><b>10+ лет</b><span>опыт команды</span></div>
  <div class="stat reveal"><b>24/7</b><span>сервис и мониторинг</span></div>
</div></section>''')

# ---- ЭНЕРГОСЕРВИС ----
PAGES["energoservis.html"]=dict(title="Энергосервис (ЭСК) — Eners Group",
  desc="Энергосервисный контракт: своя генерация без капитальных затрат. Мы строим и обслуживаем энергоцентр за свой счёт, вы платите из экономии.",
  active="energoservis", body=f'''
{CRUMB([("Главная","/"),("Энергосервис",None)])}
<section class="section page-head"><div class="wrap">
  <p class="eyebrow">Энергосервисный контракт</p>
  <h1 class="page-title">Своя генерация без капитальных затрат</h1>
  <p class="page-lead">Мы проектируем, строим и обслуживаем энергоцентр за свой счёт. Вы платите из фактической экономии на энергоресурсах — и получаете один центр ответственности за результат.</p>
  <div class="hero-actions" style="margin-top:26px"><a class="btn btn-primary btn-lg" href="/kontakty.html">Рассчитать экономию →</a></div>
</div></section>
<section class="section" style="padding-top:0"><div class="wrap">
  <div class="grid g-3">
    <div class="svc reveal"><div class="ic"><svg viewBox="0 0 24 24"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg></div><h3>0 ₽ капзатрат</h3><p>Инвестиции в оборудование и строительство берём на себя.</p></div>
    <div class="svc reveal"><div class="ic"><svg viewBox="0 0 24 24"><path d="M3 3v18h18"/><path d="m19 9-5 5-4-4-3 3"/></svg></div><h3>Оплата из экономии</h3><p>Платите частью экономии на энергоресурсах после ввода в работу.</p></div>
    <div class="svc reveal"><div class="ic"><svg viewBox="0 0 24 24"><path d="M9 12l2 2 4-4"/><circle cx="12" cy="12" r="9"/></svg></div><h3>Один ответственный</h3><p>Проект, стройка, оборудование и сервис — в одних руках.</p></div>
  </div>
</div></section>
<section class="section soft"><div class="wrap">
  <div class="section-head reveal"><p class="eyebrow">Как это работает</p><h2>Прозрачный путь от заявки до генерации</h2></div>
  <div class="steps">
    <div class="step reveal"><h3>Аудит и ТЭО</h3><p>Обследуем площадку, считаем нагрузки и экономику.</p></div>
    <div class="step reveal"><h3>Проект и модель</h3><p>Проект, BIM-модель, финансовая модель ЭСК.</p></div>
    <div class="step reveal"><h3>Стройка и ПНР</h3><p>Поставка, строительство, пусконаладка за наш счёт.</p></div>
    <div class="step reveal"><h3>Эксплуатация</h3><p>Обслуживаем и держим под мониторингом 24/7.</p></div>
    <div class="step reveal"><h3>Оплата из экономии</h3><p>Вы платите из фактической экономии по договору.</p></div>
  </div>
</div></section>
<section class="section" id="calc"><div class="wrap">
  <div class="section-head reveal"><p class="eyebrow">Калькулятор экономии</p>
    <h2>Оцените экономию от собственной генерации</h2>
    <p>Предварительный расчёт по модели энергосервиса. Точные цифры считаем после аудита площадки.</p></div>
  <div class="calc reveal">
    <div class="calc-inputs">
      <label>Средняя электрическая нагрузка, кВт<input type="number" id="c-load" value="1000" min="0" step="50"></label>
      <label>Часов работы в год<input type="number" id="c-hours" value="8000" min="0" max="8760" step="100"></label>
      <label>Текущий тариф на электроэнергию, ₽/кВт·ч<input type="number" id="c-tariff" value="8" min="0" step="0.1"></label>
      <label>Цена газа, ₽/м³<input type="number" id="c-gas" value="7" min="0" step="0.1"></label>
    </div>
    <div class="calc-out">
      <div class="calc-row"><span>Себестоимость собственной э/э</span><b id="o-cost">—</b></div>
      <div class="calc-row"><span>Экономия на каждом кВт·ч</span><b id="o-delta">—</b></div>
      <div class="calc-row big"><span>Экономия в год</span><b id="o-year">—</b></div>
      <p class="calc-note">Ориентировочно, по типовым параметрам ГПУ (электрический КПД ~42 %, теплотворность газа ~9,3 кВт·ч/м³, эксплуатация ~2,5 ₽/кВт·ч). Без учёта дополнительного эффекта от утилизации тепла (когенерация) — он увеличивает экономию.</p>
      <a class="btn btn-primary" href="/kontakty.html">Точный расчёт по вашему объекту →</a>
    </div>
  </div>
</div></section>
<section class="section soft"><div class="wrap"><div class="cta reveal">
  <h2>Посчитаем экономию под ваш объект</h2><p>Оставьте параметры — оценим мощность, capex/opex и потенциальную экономию по модели энергосервиса.</p>
  <a class="btn btn-primary btn-lg" href="/kontakty.html">Оставить заявку →</a></div></div></section>''')

# ---- О КОМПАНИИ ----
PAGES["o-kompanii.html"]=dict(title="О компании — Eners Group",
  desc="ООО «ЭНЕРСГРУПП» — распределённая энергетика и энергосервис для промышленных предприятий. Офисы в Нижнем Новгороде и Миассе.",
  active="company", body=f'''
{CRUMB([("Главная","/"),("О компании",None)])}
<section class="section page-head"><div class="wrap">
  <p class="eyebrow">О компании</p>
  <h1 class="page-title">Инженерная команда, которая доводит энергообъект до результата</h1>
  <p class="page-lead">ООО «ЭНЕРСГРУПП» создаёт энергетическую инфраструктуру и инженерные системы для промышленных предприятий — от собственной генерации до котельных, тепловых пунктов, компрессорных и насосных станций, учёта и диспетчеризации. Объединяем проектирование, поставку, строительство и сервис — заказчик получает предсказуемый результат и единую ответственность.</p>
</div></section>
<section class="section soft"><div class="wrap">
  <div class="mission reveal">
    <p class="eyebrow">Наша миссия</p>
    <p class="mission-text">Создавать для промышленных предприятий <b>надёжную энергетическую инфраструктуру и инженерные системы под ключ</b> — от собственной генерации электроэнергии, тепла и холода до котельных, тепловых пунктов, компрессорных, насосных станций, учёта и диспетчеризации — чтобы заказчики снижали издержки и развивали производство, не отвлекаясь на инженерное обеспечение.</p>
  </div>
</div></section>
<section class="section"><div class="wrap">
  <div class="section-head reveal"><p class="eyebrow">Подход</p>
    <h2>Отвечаем за результат, а не продаём оборудование</h2>
    <p>Комплексный подход: сопровождаем предприятие от аудита до подтверждённого эффекта. Заказчик видит и измеряет экономию, а не получает набор «железа».</p></div>
  <div class="steps">
    <div class="step reveal"><h3>Аудит и ТЭО</h3><p>Обследуем площадку, считаем нагрузки и экономику проекта.</p></div>
    <div class="step reveal"><h3>Проект и реализация</h3><p>Проектируем, поставляем, строим и вводим в эксплуатацию.</p></div>
    <div class="step reveal"><h3>Эксплуатация</h3><p>Обслуживаем оборудование под мониторингом 24/7.</p></div>
    <div class="step reveal"><h3>Подтверждённый результат</h3><p>Фиксируем и подтверждаем фактическую экономию.</p></div>
  </div>
</div></section>
<section class="stats-band"><div class="wrap">
  <div class="stat reveal"><b>100+ МВт</b><span>реализованной мощности</span></div>
  <div class="stat reveal"><b>30+</b><span>объектов под ключ</span></div>
  <div class="stat reveal"><b>10+ лет</b><span>опыт команды</span></div>
  <div class="stat reveal"><b>24/7</b><span>сервис и мониторинг</span></div>
</div></section>
<section class="section soft"><div class="wrap">
  <div class="section-head reveal"><p class="eyebrow">Оборудование и партнёры</p><h2>Работаем с проверенными производителями</h2></div>
  <div class="equip reveal">
    <span class="chip">Weichai · газопоршневые двигатели</span>
    <span class="chip">Jichai · серия 26/32</span>
    <span class="chip">Ingersoll Rand · компрессоры</span>
    <span class="chip">Когенерация · утилизация тепла</span>
  </div>
</div></section>
<section class="section"><div class="wrap">
  <div class="section-head reveal"><p class="eyebrow">Офисы</p><h2>Нижний Новгород и Миасс</h2></div>
  <div class="grid g-3">
    <div class="svc reveal"><h3>Нижний Новгород</h3><p>603016, ул. Героя Юрия Смирнова, д. 2<br>пр. Ленина, д. 88</p></div>
    <div class="svc reveal"><h3>Миасс</h3><p>456304, Челябинская обл.,<br>г. Миасс, пр. Автозаводцев, д. 1</p></div>
    <div class="svc reveal"><h3>Реквизиты</h3><p>ООО «ЭНЕРСГРУПП»<br>ОГРН 1225200005722<br>ИНН 5256201227</p></div>
  </div>
</div></section>
<section class="section soft"><div class="wrap"><div class="cta reveal">
  <h2>Обсудим ваш энергопроект</h2><p>Расскажите о задаче — предложим решение и рассчитаем экономику.</p>
  <a class="btn btn-primary btn-lg" href="/kontakty.html">Связаться →</a></div></div></section>''')


PAGES["politika.html"]=dict(title="Политика конфиденциальности — Eners Group",
  desc="Политика ООО «ЭНЕРСГРУПП» в отношении обработки персональных данных в соответствии с 152-ФЗ.",
  active="", body=f'''
{CRUMB([("Главная","/"),("Политика конфиденциальности",None)])}
<section class="section page-head"><div class="wrap">
  <p class="eyebrow">Правовая информация</p>
  <h1 class="page-title" style="font-size:clamp(26px,3.6vw,40px)">Политика в отношении обработки персональных данных</h1>
</div></section>
<section class="section" style="padding-top:0"><div class="wrap legal">
  <h3>1. Общие положения</h3>
  <p>Настоящая Политика определяет порядок обработки и защиты персональных данных физических лиц (далее — Пользователи) Оператором — <b>ООО «ЭНЕРСГРУПП»</b> (ОГРН 1225200005722, ИНН 5256201227, адрес: 603016, г. Нижний Новгород, ул. Героя Юрия Смирнова, д. 2) и разработана в соответствии с Федеральным законом от 27.07.2006 № 152-ФЗ «О персональных данных».</p>
  <p>Используя сайт enersgroup.ru и отправляя данные через формы обратной связи, Пользователь выражает согласие с условиями настоящей Политики.</p>
  <h3>2. Какие данные обрабатываются</h3>
  <p>Оператор обрабатывает персональные данные, которые Пользователь предоставляет добровольно при заполнении форм на сайте: имя, контактные данные (телефон и/или адрес электронной почты), а также текст обращения. Дополнительно могут автоматически собираться технические данные (IP-адрес, cookie-файлы, сведения о браузере) в целях функционирования сайта.</p>
  <h3>3. Цели обработки</h3>
  <p>Обработка осуществляется в целях обработки заявок и обращений Пользователя, предоставления обратной связи, подготовки коммерческих предложений и информирования о ходе рассмотрения обращения.</p>
  <h3>4. Правовые основания</h3>
  <p>Правовым основанием обработки является согласие Пользователя на обработку персональных данных, выражаемое при отправке формы, а также положения 152-ФЗ и иных нормативных актов РФ.</p>
  <h3>5. Порядок и сроки обработки</h3>
  <p>Персональные данные обрабатываются с использованием средств автоматизации и без таковых. Оператор не передаёт данные третьим лицам, за исключением случаев, предусмотренных законодательством РФ. Данные хранятся в течение срока, необходимого для достижения целей обработки, либо до отзыва согласия.</p>
  <h3>6. Права пользователя</h3>
  <p>Пользователь вправе получать сведения об обработке своих данных, требовать их уточнения, блокирования или удаления, а также отозвать согласие на обработку, направив обращение на e-mail <a href="mailto:info@enersgroup.ru">info@enersgroup.ru</a>.</p>
  <h3>7. Файлы cookie</h3>
  <p>Сайт может использовать cookie-файлы для корректной работы и анализа посещаемости. Пользователь может отключить cookie в настройках браузера; это может повлиять на работу отдельных функций сайта.</p>
  <h3>8. Контакты</h3>
  <p>По вопросам обработки персональных данных: ООО «ЭНЕРСГРУПП», e-mail <a href="mailto:info@enersgroup.ru">info@enersgroup.ru</a>.</p>
  <p class="legal-note">Актуальная редакция Политики размещена на данной странице.</p>
</div></section>''')


def build():
    for path, p in PAGES.items():
        html = HEAD(p["title"], p["desc"]) + HEADER(p["active"]) + p["body"] + FOOTER + SCRIPT
        full = os.path.join(ROOT, path)
        os.makedirs(os.path.dirname(full), exist_ok=True) if os.path.dirname(path) else None
        with open(full, "w", encoding="utf-8") as f:
            f.write(html)
        print("built", path)

if __name__ == "__main__":
    build()
