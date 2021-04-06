<h1> Справочник по синтаксису Markdown и расширений </h1>

Данная статья демонстрирует возможности языка разметки [Markdown](https://daringfireball.net/projects/markdown) с использованием расширений: [markdown extra](https://belousovv.ru/php/MarkdownExtra), [mathjax 3](https://www.mathjax.org), [admonitions](https://docutils.sourceforge.io/docs/ref/rst/directives.html#admonitions), [table of contents](https://python-markdown.github.io/extensions/toc), [wikilinks](https://python-markdown.github.io/extensions/wikilinks), [mermaid][].

[mermaid]: https://mermaid-js.github.io

Статья на языке Markdown должна иметь расширение **.md**.

# Оглавление

[TOC]

# Markdown разметка

► Обычный текст (как этот) считается параграфом. Для жёсткого разрыва используется пустая строка. Для мягкого разрыва (например, в многострочном элементе списка) используется двойной пробел в конце строки.

```markdown
Обычный текст (как этот) считается параграфом. Для жёсткого разрыва используется пустая строка. Для мягкого разрыва (например, в многострочном элементе списка) используется двойной пробел в конце строки.
```

► В качестве блочных можно встраивать блочные HTML элементы. Пример встроенной HTML таблицы:

<table border="1">
    <tr>
        <td>Foo</td>
    </tr>
</table>

```html
<table border="1">
    <tr>
        <td>Foo</td>
    </tr>
</table>
```

► В качестве строчных можно встраивать строчные HTML элементы, например <del>del</del>.

```markdown
В качестве строчных можно встраивать строчные HTML элементы, например <del>del</del>.
```

##### ► Заголовки помечаются символами "#...# " (с пробелом) в начале строки. Количество символов равняется уровню заголовка. {data-toc-label='Пример заголовка 5 уровня'}

```markdown
##### Заголовки помечаются символами "#...# " (с пробелом) в начале строки. Количество символов равняется уровню заголовка.
```

> ► Цитаты начинаются с символа ">" в начале строки

```markdown
> Цитаты начинаются с символа ">" в начале строки
```

► Маркированные списки начинаются со следующих символов в начале строке:
- "-"
* "*"
+ "+"

```markdown
Маркированные списки начинаются со следующих символов в начале строке:
- "-"
* "*"
+ "+"
```

► Нумерованные списки начинаются с цифры (далее следует автонумерация) с точкой:
2. два
1. один
1. один

```markdown
Нумерованные списки начинаются с цифры (далее следует автонумерация) с точкой:
2. два
1. один
1. один
```

► Блоки кода обозначаются отступом в 4 пробела (табуляция):

    #include <stdio.h>
    
    int main(void)
    {
      printf("Hello World\n");
      return 0;
    }

```markdown
    #include <stdio.h>
    
    int main(void)
    {
      printf("Hello World\n");
      return 0;
    }
```

► Строки кода можно встроить в обычную строку, обрамляя символами тильда (`printf("Hello World\n");`).

```markdown
Строки кода можно встроить в обычную строку, обрамляя символами тильда (`printf("Hello World\n");`).
```

► Строки, состоящие из повторяющихся три и более раза подряд символов "*" или "-" образуют горизонтальную линию:

---

```markdown
---
```

► [Ссылки](# "Подсказка") обозначаются следующим образом (между скобками возможен один пробел):

    [Текст](url "Опциональная подсказка")

```markdown
[Ссылки](# "Подсказка") обозначаются ...
```

[Длинные ссылки][long_link_id] можно раскрывать где-нибудь в удобном месте документа (например, в конце).

    [Текст][id ссылки]
    ...
    [id ссылки]: url "Опциональная подсказка"

[long_link_id]: # "Подсказка длинной ссылки"

Если название [ссылки][] является одним словом, id ссылки можно опустить.

    [Слово][]
    ...
    [Слово]: url "Опциональная подсказка"

[ссылки]: # "Сокращённая длинная ссылка"

► Текст можно *выделять* и **сильно выделять**, обрамляя одним или парой символов "*" или "_".

```markdown
Текст можно *выделять* и **сильно выделять**, обрамляя одним или парой символов "*" или "_".
```

► Специальные символы (\\\`\*\_\{\}\[\]\(\)\#\+\-\.\!) можно вставлять в текст через слэш в начале \\<символ>.

```markdown
Специальные символы (\\\`\*\_\{\}\[\]\(\)\#\+\-\.\!) можно вставлять текст через слэш в начале \\<символ>.
```

► В текст и ссылки можно встраивать изображения аналогично ссылкам (включая длинные ссылки с id):

    ![Альтернативный текст](url "Опциональная подсказка")

![Альтернативный текст][base64image]

```markdown
![Альтернативный текст][base64image]
...
[base64image]: data:image/png;base64,iVBOR....Y= "Пример изображения" 
```

► Ссылки, обрамлённые в угловые кавычки, автоматически генерируются прямо в тексте (например, <http://example.com/> или <address@example.com>).

```markdown
Ссылки, обрамлённые в угловые кавычки, автоматически генерируются прямо в тексте (например, <http://example.com/> или <address@example.com>).
```



# Markdown extra разметка

<table border="1" markdown="1">  
	<tr>
		<td>
			► *Markdown-текст* можно встраивать прямо в блочные HTML элементы, указав аттрибут *markdown="1"*.
		</td>
	</tr>
</table>

```html
<table border="1" markdown="1">  
	<tr>
		<td>
			*Markdown-текст* можно встраивать прямо в блочные HTML элементы, указав аттрибут *markdown="1"*.
		</td>
	</tr>
</table>
```

► В фигурных скобках можно указать класс (через точку) или id (через решётку) элемента (например, класс кода используется для правильной подсветки `printf("Hello World\n");`{.cpp}).

##### Заголовок с id *test-id* и классами *a* и *b*. {.a #test-id .b data-toc-label='Пример заголовка с аттрибутами'}

[Ссылка на заголовок test-id](#test-id)

```markdown
В фигурных скобках можно указать класс (через точку) или id (через решётку) элемента (например, класс кода используется для правильной подсветки `printf("Hello World\n");`{.cpp}).

##### Заголовок с id *test-id* и классами *a* и *b*. {.a #test-id .b}

[Ссылка на заголовок test-id](#test-id)
```

► Код можно указать в специальном блоке без отступов следующим синтаксисом:

~~~.markdown
```название_языка
код
```
~~~

или

```markdown
~~~.название_языка
код
~~~
```

или

```markdown
~~~ {.название_языка .класс1 .класс2 #id}
код
~~~
```

Пример C++ "Hello, world":

```cpp
#include <stdio.h>

int main(void)
{
  printf("Hello World\n");
  return 0;
}
```

~~~.markdown
```cpp
#include <stdio.h>

int main(void)
{
  printf("Hello World\n");
  return 0;
}
```
~~~


► Таблицы можно записывать упрощённым способом. Пример:

Колонка 1 |Колонка 2
----------------- | -----------------
Содержимое Ячейки | Содержимое Ячейки
Содержимое Ячейки | Содержимое Ячейки

```markdown
Колонка 1 |Колонка 2
----------------- | -----------------
Содержимое Ячейки | Содержимое Ячейки
Содержимое Ячейки | Содержимое Ячейки
```

Для красоты можно выставить символы "|" в начале и конце каждой строки. Также можно задать выравнивание в колонках через двоеточие слева или справа:

| Предмет   | Цена  |
| --------- | -----:|
| Компьютер | $1600 |
| Телефон   |   $12 |
| Трубка    |    $1 |

```markdown
| Предмет   | Цена  |
| --------- | -----:|
| Компьютер | $1600 |
| Телефон   |   $12 |
| Трубка    |    $1 |
```

►  Списки определения создаются с помощью специального синтаксиса.

```markdown
Термин 1
:	определение 1
Термин 2
:	определение 2
```

Можно указывать несколько терминов с новой строки и несколько определений, включаяя многострочные, с новой строки с двоеточием. Для отступа у определения достаточно поставить пустую строку перед ним.

Яблоко
Apple
:   Плод яблони, который употребляется в пищу в свежем
    виде, служит сырьём в кулинарии и для приготовления
    напитков.
:   Официально зарегистрированная социал-либеральная 
политическая партия современной России.

Апельсин

:   Плод апельсинного дерева, родом из Китая.

```markdown
Яблоко
Apple
:   Плод яблони, который употребляется в пищу в свежем
    виде, служит сырьём в кулинарии и для приготовления
    напитков.
:   Официально зарегистрированная социал-либеральная 
политическая партия современной России.


Апельсин

:   Плод апельсинного дерева, родом из Китая.
```

►  Сноски позволяют вынести уточняющий текст в другой место статьи.[^1]

```markdown
Сноски позволяют вынести уточняющий текст в другой место статьи.[^1]
...
[^1]: 
	Сноска позволяет вернуться назад к тексту. 
	
	Сноска может содержать несколько абзацев, но также может умещаться в одну строку.
```

►  Аббревиатуры указываются в любом месте документа, а затем раскрывают встречающиеся в статье термины (например, TerminID, HTML).

*[TerminID]: раскрытие термина.
*[HTML]: Hyper Text Markup Language.

```markdown
Аббревиатуры указываются в любом месте документа, а затем раскрывают встречающиеся в статье термины (например, TerminID, HTML).

*[TerminID]: раскрытие термина
*[HTML]: Hyper Text Markup Language
```


►  "Нижнее_подчёркивание_в_кавычках" теперь не обозначает выделение.

```markdown
"Нижнее_подчёркивание_в_кавычках" теперь не обозначает выделение.
```

►  Новые символы (:\|) подлежат экранированию (в местах, где возможна двузначная трактовка).

```markdown
Новые символы (:\|) подлежат экранированию (в местах, где возможна двузначная трактовка).
```



# Mathjax формулы

►  Строчные формулы [TeX/LaTeX][] вставляются через "\$...\$", например $ax^2 + bx + c = 0 | a \ne 0$.

[TeX/LaTeX]: https://en.wikibooks.org/wiki/LaTeX

```markdown
Строчные формулы [TeX/LaTeX][] вставляются через "\$...\$", например $ax^2 + bx + c = 0 | a \ne 0$.
```

►  Блоки формул [TeX/LaTeX][] обозначаются через "\$\$...\$\$".

$$
x_{1,2} = {-b \pm \sqrt{b^2-4ac} \over 2a}.
$$

```markdown
$$
x_{1,2} = {-b \pm \sqrt{b^2-4ac} \over 2a}.
$$
```

!!! tip ""
	Формулы [TeX/LaTeX][] являются интерактивными, имеют собственное контекстное меню, позволяющее задать различные настройки отображения и получить другую информацию о формуле.

►  Формулы [MathML](https://www.w3.org/Math) вставляются через HTML теги "math".

<math>
	<msubsup>
		<mo>∫</mo>
		<mn>0</mn>
		<mn>1</mn>
	</msubsup>
	<mi>x</mi>
	<mrow>
	  <mo> ⅆ </mo>
	  <mi> x </mi>
	</mrow>
</math>

```html
<math>
	<msubsup>
		<mo>∫</mo>
		<mn>0</mn>
		<mn>1</mn>
	</msubsup>
	<mi>x</mi>
	<mrow>
	  <mo> ⅆ </mo>
	  <mi> x </mi>
	</mrow>
</math>
```

►  Новый символ (\$) подлежит экранированию.

```markdown
Новый символ (\$) подлежит экранированию.
```



# Admonitions заметки

►  Обычные заметки выносят текст в рамку.

!!! tip "Обычная заметка"
	Данный тип заметок позволяет добавить слабо относящийся к контексту текст.

```markdown
!!! tip "Обычная заметка"
	Данный тип заметок позволяет добавить слабо относящийся к контексту текст.
```

►  Информационные заметки выделяют блок на фоне остального текста.

!!! hint "Информационная заметка"
	Данный тип заметок позволяет добавить дополнительную информацию, которая

	* обычно не обязательна к прочтению,
	* может содержать другие элементы, например списки.

```markdown
!!! hint "Информационная заметка"
	Данный тип заметок позволяет добавить дополнительную информацию, которая

	* обычно не обязательна к прочтению,
	* может содержать другие элементы, например списки.
```

►  Важные заметки привлекают внимание читателя.

!!! alert "Важная заметка"
	Данный тип заметок позволяет обратить внимание читателя на важную информацию или предупредить его.

```markdown
!!! alert "Важная заметка"
	Данный тип заметок позволяет обратить внимание читателя на важную информацию.
```

►  Критические заметки требуют исключительного внимания.

!!! danger "Критическая заметка"
	Данный тип заметок позволяет сообщить читателю об ошибке или критически важной информации.

```markdown
!!! danger "Критическая заметка"
	Данный тип заметок позволяет сообщить читателю об ошибке или критически важной информации.
```

►  Полный синтаксис заметок выглядит следующим образом:

```markdown
!!! type optional-class1 optional-class2 "Note title"
	Content like simple text or
	markdown.
```

Заметка может иметь любой тип и любое количество дополнительных классов, но рекомендуется использовать следующие типы в порядке возрастания важности: **tip, hint, alert, danger**.

►  Название заметки можно опустить, задав пустую строку.

!!! tip ""
	Заметка без названия.

```markdown
!!! tip ""
	Заметка без названия.
```

►  Название заметки можно сократить до её типа.

!!! tip additional-class
	Заметка с автоматическим названием.

```markdown
!!! tip additional-class
	Заметка с автоматическим названием.
```


# Автособираемое оглавление

►  В любое место документа можно вставить автоматически собираемое из заголовков оглавление с помощью "\\[TOC\\]".

[TOC]

```markdown
В любое место документа можно вставить автоматически собираемое из заголовков оглавление с помощью "\\[TOC\\]".

[TOC]
```

►  По умолчанию заголовки копируются в оглавление, однако их можно переименовать с помощью аттрибута "data-toc-label". Достаточно задать аттрибут через синтаксис [markdown extra](#markdown-extra). 

##### У этого заголовка другое название в оглавлении {data-toc-label='Пример переименованного заголовка'}

```markdown
##### У этого заголовка другое название в оглавлении {data-toc-label='Пример переименованного заголовка'}
```

►  По умолчанию ID заголовков формируются автоматически на основе текста через символ "-" с добавлением уникального номера в конец через символ "_", если ID уже не был [определён](#custom-header-id) через синтаксис [markdown extra](#markdown-extra).

##### Заголовок с ID "custom-header-id" {#custom-header-id data-toc-label='Пример заголовка с ID'}

```markdown
По умолчанию ID заголовков формируются автоматически на основе текста через символ "-" с опциональным добавлением номера в конец через символ "_" для уникальности, если ID уже не был [определён](#custom-header-id) через синтаксис [markdown extra](#markdown-extra).

##### Заголовок с ID "custom-header-id" {#custom-header-id data-toc-label='Пример заголовка с ID'}
```



# Внутренние ссылки { #internal-links }

►  Внутренние ссылки, например [[Markdown]], обращаются к другим статьям или разделам по их названию.

```markdown
Внутренние ссылки, например [[Markdown]], обращаются к другим статьям или разделам по их названию.
```

!!! tip ""
	Если существует несколько одноимённых статей или разделов, ссылка выбирается **случайным образом**.

►  Вложенные внутренние ссылки, например [[Simple Wiki / Markdown]], позволяют устранить неоднозначность имён. Они создаются путём разделения уровней символом "/" (допускается использовать любое количество уровней и пробелов с каждой стороны).

```markdown
Вложенные внутренние ссылки, например [[Simple Wiki / Markdown]], позволяют устранить неоднозначность имён. Они создаются путём разделения уровней символом "/"...
```

►  Якорные внутренние ссылки, например [[Simple Wiki / Markdown # internal-links]], позволяют ссылаться на отдельную часть статьи. Для этого в конец ссылке необходимо добавить соответствующий ID через символ "#" (допускается использовать любое количество уровней и пробелов с каждой стороны).

```markdown
Якорные внутренние ссылки, например [[Simple Wiki / Markdown # internal-links]], позволяют ссылаться на отдельную часть статьи. Для этого в конец ссылки необходимо добавить соответствующий ID через символ "#"...
```

# Mermaid диаграммы

►  Диаграммы вставляются как блок кода на языке "mermaid". Подробнее синтаксис диаграмм можно изучить на официальном сайте [mermaid][].

~~~markdown
```mermaid
Код диаграммы
```
~~~

```mermaid
graph TD
	a --> b
```

~~~markdown
```mermaid
graph TD
	a --> b
```
~~~

►  Пример блок-схемы.

```mermaid
graph TB
    sq[Square shape] --> ci((Circle shape))

    subgraph A
        od>Odd shape]-- Two line<br/>edge comment --> ro
        di{Diamond with <br/> line break} -.-> ro(Rounded<br>square<br>shape)
        di==>ro2(Rounded square shape)
    end

    %% Notice that no text in shape are added here instead that is appended further down
    e --> od3>Really long text with linebreak<br>in an Odd shape]

    %% Comments after double percent signs
    e((Inner / circle<br>and some odd <br>special characters)) --> f(,.?!+-*ز)

    cyr[Cyrillic]-->cyr2((Circle shape Начало));

     classDef green fill:#9f6,stroke:#333,stroke-width:2px;
     classDef orange fill:#f96,stroke:#333,stroke-width:4px;
     class sq,e green
     class di orange
```

~~~markdown
```mermaid
graph TB
    sq[Square shape] --> ci((Circle shape))

    subgraph A
        od>Odd shape]-- Two line<br/>edge comment --> ro
        di{Diamond with <br/> line break} -.-> ro(Rounded<br>square<br>shape)
        di==>ro2(Rounded square shape)
    end

    %% Notice that no text in shape are added here instead that is appended further down
    e --> od3>Really long text with linebreak<br>in an Odd shape]

    %% Comments after double percent signs
    e((Inner / circle<br>and some odd <br>special characters)) --> f(,.?!+-*ز)

    cyr[Cyrillic]-->cyr2((Circle shape Начало));

     classDef green fill:#9f6,stroke:#333,stroke-width:2px;
     classDef orange fill:#f96,stroke:#333,stroke-width:4px;
     class sq,e green
     class di orange
```
~~~

►  Пример диаграммы последовательности.

```mermaid
sequenceDiagram
    participant Alice
    participant Bob
    Alice->>John: Hello John, how are you?
    loop Healthcheck
        John->>John: Fight against hypochondria
    end
    Note right of John: Rational thoughts <br/>prevail!
    John-->>Alice: Great!
    John->>Bob: How about you?
    Bob-->>John: Jolly good!
```

~~~markdown
```mermaid
sequenceDiagram
    participant Alice
    participant Bob
    Alice->>John: Hello John, how are you?
    loop Healthcheck
        John->>John: Fight against hypochondria
    end
    Note right of John: Rational thoughts <br/>prevail!
    John-->>Alice: Great!
    John->>Bob: How about you?
    Bob-->>John: Jolly good!
```
~~~

►  Пример диаграммы Ганта.

```mermaid
gantt
    dateFormat  YYYY-MM-DD
    title       Adding GANTT diagram functionality to mermaid
    excludes    weekends
    %% (`excludes` accepts specific dates in YYYY-MM-DD format, days of the week ("sunday") or "weekends", but not the word "weekdays".)

    section A section
    Completed task            :done,    des1, 2014-01-06,2014-01-08
    Active task               :active,  des2, 2014-01-09, 3d
    Future task               :         des3, after des2, 5d
    Future task2              :         des4, after des3, 5d

    section Critical tasks
    Completed task in the critical line :crit, done, 2014-01-06,24h
    Implement parser and jison          :crit, done, after des1, 2d
    Create tests for parser             :crit, active, 3d
    Future task in critical line        :crit, 5d
    Create tests for renderer           :2d
    Add to mermaid                      :1d

    section Documentation
    Describe gantt syntax               :active, a1, after des1, 3d
    Add gantt diagram to demo page      :after a1  , 20h
    Add another diagram to demo page    :doc1, after a1  , 48h

    section Last section
    Describe gantt syntax               :after doc1, 3d
    Add gantt diagram to demo page      :20h
    Add another diagram to demo page    :48h
```

~~~markdown
```mermaid
gantt
    dateFormat  YYYY-MM-DD
    title       Adding GANTT diagram functionality to mermaid
    excludes    weekends
    %% (`excludes` accepts specific dates in YYYY-MM-DD format, days of the week ("sunday") or "weekends", but not the word "weekdays".)

    section A section
    Completed task            :done,    des1, 2014-01-06,2014-01-08
    Active task               :active,  des2, 2014-01-09, 3d
    Future task               :         des3, after des2, 5d
    Future task2              :         des4, after des3, 5d

    section Critical tasks
    Completed task in the critical line :crit, done, 2014-01-06,24h
    Implement parser and jison          :crit, done, after des1, 2d
    Create tests for parser             :crit, active, 3d
    Future task in critical line        :crit, 5d
    Create tests for renderer           :2d
    Add to mermaid                      :1d

    section Documentation
    Describe gantt syntax               :active, a1, after des1, 3d
    Add gantt diagram to demo page      :after a1  , 20h
    Add another diagram to demo page    :doc1, after a1  , 48h

    section Last section
    Describe gantt syntax               :after doc1, 3d
    Add gantt diagram to demo page      :20h
    Add another diagram to demo page    :48h
```
~~~

►  Пример диаграммы состояний.

```mermaid
stateDiagram
        [*] --> Active

        state Active {
            [*] --> NumLockOff
            NumLockOff --> NumLockOn : EvNumLockPressed
            NumLockOn --> NumLockOff : EvNumLockPressed
            --
            [*] --> CapsLockOff
            CapsLockOff --> CapsLockOn : EvCapsLockPressed
            CapsLockOn --> CapsLockOff : EvCapsLockPressed
            --
            [*] --> ScrollLockOff
            ScrollLockOff --> ScrollLockOn : EvCapsLockPressed
            ScrollLockOn --> ScrollLockOff : EvCapsLockPressed
        }
        state SomethingElse {
          A --> B
          B --> A
        }

        Active --> SomethingElse
        note right of SomethingElse : This is the note to the right.

        SomethingElse --> [*]
```

~~~markdown
```mermaid
stateDiagram
        [*] --> Active

        state Active {
            [*] --> NumLockOff
            NumLockOff --> NumLockOn : EvNumLockPressed
            NumLockOn --> NumLockOff : EvNumLockPressed
            --
            [*] --> CapsLockOff
            CapsLockOff --> CapsLockOn : EvCapsLockPressed
            CapsLockOn --> CapsLockOff : EvCapsLockPressed
            --
            [*] --> ScrollLockOff
            ScrollLockOff --> ScrollLockOn : EvCapsLockPressed
            ScrollLockOn --> ScrollLockOff : EvCapsLockPressed
        }
        state SomethingElse {
          A --> B
          B --> A
        }

        Active --> SomethingElse
        note right of SomethingElse : This is the note to the right.

        SomethingElse --> [*]
```
~~~

►  Пример диаграммы классов.

```mermaid
classDiagram
Class01 <|-- AveryLongClass : Cool
Class03 *-- Class04
Class05 o-- Class06
Class07 .. Class08
Class09 --> C2 : Where am i?
Class09 --* C3
Class09 --|> Class07
Class07 : equals()
Class07 : Object[] elementData
Class01 : size()
Class01 : int chimp
Class01 : int gorilla
Class08 <--> C2: Cool label
```

~~~markdown
```mermaid
classDiagram
Class01 <|-- AveryLongClass : Cool
Class03 *-- Class04
Class05 o-- Class06
Class07 .. Class08
Class09 --> C2 : Where am i?
Class09 --* C3
Class09 --|> Class07
Class07 : equals()
Class07 : Object[] elementData
Class01 : size()
Class01 : int chimp
Class01 : int gorilla
Class08 <--> C2: Cool label
```
~~~

►  Пример диаграммы [git](https://git-scm.com).

```mermaid
gitGraph:
options
{
    "nodeSpacing": 150,
    "nodeRadius": 10
}
end
commit
branch newbranch
checkout newbranch
commit
commit
checkout master
commit
commit
merge newbranch
```

~~~markdown
```mermaid
gitGraph:
options
{
    "nodeSpacing": 150,
    "nodeRadius": 10
}
end
commit
branch newbranch
checkout newbranch
commit
commit
checkout master
commit
commit
merge newbranch
```
~~~

►  Пример диаграммы "сущность-связь".

```mermaid
erDiagram
    CAR ||--o{ NAMED-DRIVER : allows
    CAR {
        string registrationNumber
        string make
        string model
    }
    PERSON ||--o{ NAMED-DRIVER : is
    PERSON {
        string firstName
        string lastName
        int age
    }
```

~~~markdown
```mermaid
erDiagram
    CAR ||--o{ NAMED-DRIVER : allows
    CAR {
        string registrationNumber
        string make
        string model
    }
    PERSON ||--o{ NAMED-DRIVER : is
    PERSON {
        string firstName
        string lastName
        int age
    }
```
~~~

►  Пример диаграммы путевого журнала.

```mermaid
journey
    title My working day
    section Go to work
      Make tea: 5: Me
      Go upstairs: 3: Me
      Do work: 1: Me, Cat
    section Go home
      Go downstairs: 5: Me
      Sit down: 5: Me
```

~~~markdown
```mermaid
journey
    title My working day
    section Go to work
      Make tea: 5: Me
      Go upstairs: 3: Me
      Do work: 1: Me, Cat
    section Go home
      Go downstairs: 5: Me
      Sit down: 5: Me
```
~~~

►  Пример круговой диаграммы.

```mermaid
pie
    title Key elements in Product X
    "Calcium" : 42.96
    "Potassium" : 50.05
    "Magnesium" : 10.01
    "Iron" :  5
```

~~~markdown
```mermaid
pie
    title Key elements in Product X
    "Calcium" : 42.96
    "Potassium" : 50.05
    "Magnesium" : 10.01
    "Iron" :  5
```
~~~












[^1]: 
	Сноска позволяет вернуться назад к тексту.
	
	Сноска может содержать несколько абзацев.



[base64image]: data:image/png;base64,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 "Пример изображения"