## Миграция базы данных с помощью Alembic

**Миграция** баз данных необходима при разработке схемы базы данных с течением времени без потери существующих данных. По мере роста и изменения веб-приложений схема базы данных может нуждаться в обновлениях для соответствия новым функциям или требованиям к данным.

Если вы даже не слышали об этом термине (что вряд ли, но вдруг), то можно прочитать вводную часть этой статьи (не обязательно читать до конца):

https://habr.com/ru/articles/121265/

Простыми словами, миграции БД - это аналог гитхаба, но для баз данных (хранится история изменений и можно откатиться назад, если что-то сломалось). В данном уроке мы рассмотрим эту проблематику, а не переезд БД из одного дата центра в другой или переход с MySQL на MongoDB (если кто так подумал). 

**Alembic** - это мощный инструмент миграции баз данных, который легко работает с FastAPI, позволяя вам управлять изменениями схемы базы данных контролируемым и версионным образом. Стоит отметить, что автором этого инструмента является автор SQLAlchemy, которая является **одной из самых** популярных ORM-ок в питоне. Поэтому покажем на примере этой ORM-ки.

В зависимости от выбранной вами базы данных или ORM-ки к ней, рекомендуем поискать подходящий инструмент для работы, например `peewee-migrations`. **В PonyORM миграции** вышли между релизами 0.7.9 и 0.7.10, и они теперь идут "из коробки" (и довольно удобны).