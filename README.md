# Справочник по испанскому языку: грамматика и живая речь

Справочник на русском языке для изучающих испанский: образование и употребление времён, наклонения, местоимения, артикли, предлоги, согласование, разговорные конструкции, живая речь, сленг и различия между Испанией и Латинской Америкой. Правила сопровождаются таблицами, примерами и переводами.

Читать онлайн: **[spanish.f-y.name](https://spanish.f-y.name/)**

Справочник подготовлен с помощью искусственного интеллекта и может содержать ошибки: носитель языка текст не проверял. Если нашли ошибку, сообщите о ней в [issues](https://github.com/Forever-Young/spanish-reference/issues).

Справочник регулярно обновляется.<br>
Текущая версия и дата последнего обновления:
[![Версия](https://img.shields.io/github/v/release/Forever-Young/spanish-reference?label=версия)](https://github.com/Forever-Young/spanish-reference/releases/latest)
[![Обновлено](https://img.shields.io/github/last-commit/Forever-Young/spanish-reference?label=обновлено)](https://github.com/Forever-Young/spanish-reference/commits/main)

## Готовые книги

<p align="center">
  <a href="https://github.com/Forever-Young/spanish-reference/releases/latest/download/Spanish.reference.pdf"><img alt="Скачать PDF" src="https://img.shields.io/badge/%E2%AC%87%20%D0%A1%D0%BA%D0%B0%D1%87%D0%B0%D1%82%D1%8C-PDF-2ea44f?style=for-the-badge&labelColor=555" height="64"></a>
  &nbsp;&nbsp;
  <a href="https://github.com/Forever-Young/spanish-reference/releases/latest/download/Spanish.reference.epub"><img alt="Скачать EPUB" src="https://img.shields.io/badge/%E2%AC%87%20%D0%A1%D0%BA%D0%B0%D1%87%D0%B0%D1%82%D1%8C-EPUB-2ea44f?style=for-the-badge&labelColor=555" height="64"></a>
</p>

Скачайте **Spanish reference.pdf** и **Spanish reference.epub** в [последнем релизе](https://github.com/Forever-Young/spanish-reference/releases/latest). PDF включает кликабельное оглавление с номерами страниц; EPUB — навигационное оглавление. В книгах указано время сборки по Мадриду.

## Исходный текст

Исходный текст — [reference.md](reference.md). Его можно читать прямо на GitHub или собрать в PDF для печати и EPUB для электронной книги.

## Сборка вручную

Нужны Bash, Pandoc, Python 3.12 или новее и WeasyPrint. Для PDF установите шрифты Arial либо Liberation Sans / DejaVu Sans с поддержкой кириллицы.

На macOS зависимости можно установить через Homebrew:

```sh
brew install pandoc weasyprint
./build-pdf.sh
./build-epub.sh
python3 scripts/check-epub.py
```

На Ubuntu 24.04:

```sh
sudo apt-get update
sudo apt-get install -y pandoc python3-venv libpango-1.0-0 libpangoft2-1.0-0 fonts-liberation fonts-dejavu-core
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
./build-pdf.sh
./build-epub.sh
python3 scripts/check-epub.py
```

Книги появятся в корне проекта. Оформление PDF задаёт `reference.css`, EPUB — `epub.css`; Lua-фильтры добавляют дату, оглавление PDF и корректные переносы строк EPUB. Скрипты также принимают путь к исходнику и выходному файлу первым и вторым аргументами.

## Автоматическая сборка и релизы

GitHub Actions собирает и проверяет книги при изменениях `main`, в pull request и при ручном запуске. Результаты доступны как артефакт `spanish-reference` на странице запуска.

При отправке тега вида `v1.0.0` workflow создаёт GitHub Release и прикладывает обе книги. Сгенерированные файлы в Git не хранятся.

## Исправления

Предложения и исправления приветствуются через Issues и pull requests. Меняйте `reference.md` для правок текста и соответствующий CSS для оформления, затем проверяйте сборку.

## Лицензия и происхождение материалов

Текст справочника, скрипты, стили и конфигурация проекта распространяются по [MIT No Attribution (MIT-0)](LICENSE). Можно использовать, изменять и распространять материалы, в том числе коммерчески, без обязательного указания авторства. Лицензия распространяется и на PDF/EPUB, собранные из этих исходников.

Справочник и код подготовлены с помощью AI. При подготовке использовались сведения о грамматике испанского языка, в том числе из материалов Real Academia Española (RAE); полный перечень использованных источников не зафиксирован. Проект не является официальным изданием RAE. Лицензия проекта предоставляется в пределах прав его участников и не меняет условий использования сторонних материалов.

Материалы предоставляются «как есть», без гарантий; в объяснениях и примерах возможны ошибки.
