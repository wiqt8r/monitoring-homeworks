# Домашнее задание к занятию 14 «Средство визуализации Grafana»

## Задание повышенной сложности

**При решении задания 1** не используйте директорию [help](./help) для сборки проекта. Самостоятельно разверните grafana, где в роли источника данных будет выступать prometheus, а сборщиком данных будет node-exporter:

- grafana;
- prometheus-server;
- prometheus node-exporter.

За дополнительными материалами можете обратиться в официальную документацию grafana и prometheus.

В решении к домашнему заданию также приведите все конфигурации, скрипты, манифесты, которые вы 
использовали в процессе решения задания.

**При решении задания 3** вы должны самостоятельно завести удобный для вас канал нотификации, например, Telegram или email, и отправить туда тестовые события.

В решении приведите скриншоты тестовых событий из каналов нотификаций.

## Обязательные задания

### Задание 1

скриншот веб-интерфейса grafana со списком подключенных Datasource.

<img width="1565" height="974" alt="image" src="https://github.com/user-attachments/assets/c9ec5d0f-1366-4d13-989c-3f234221ca31" />


## Задание 2

- утилизация CPU для nodeexporter (в процентах, 100-idle):
```
100 - (avg by (instance) (rate(node_cpu_seconds_total{job="nodeexporter",mode="idle"}[5m])) * 100)
```
- CPULA 1/5/15 - три запроса на одной панельке:
```
node_load1{job="nodeexporter"}
node_load5{job="nodeexporter"}
node_load15{job="nodeexporter"}
```
- количество свободной оперативной памяти:
```
node_memory_MemAvailable_bytes{job="nodeexporter"}
```
- количество места на файловой системе:
```
(
  node_filesystem_avail_bytes{
    job="nodeexporter",
    fstype!~"tmpfs|overlay|squashfs|ramfs",
    mountpoint!~"/run/credentials/.*"
  }
/
  node_filesystem_size_bytes{
    job="nodeexporter",
    fstype!~"tmpfs|overlay|squashfs|ramfs",
    mountpoint!~"/run/credentials/.*"
  }
) * 100
```

Dashboard:

<img width="2560" height="1229" alt="image" src="https://github.com/user-attachments/assets/09008764-993b-4bfa-9c0d-14cab700d3f2" />


## Задание 3

Пришлось поменять визуальное отображение на Graph, потому что графана не давала создавать алерты для других визуализаций:

<img width="1329" height="1039" alt="image" src="https://github.com/user-attachments/assets/8254921a-2f27-40a2-99eb-16d85057ed9f" />

искусственно нагрузил память, алерт в телегу пришёл:

<img width="560" height="233" alt="image" src="https://github.com/user-attachments/assets/85bee440-6eaf-497a-ba09-9c4a19a644be" />


## Задание 4

1. Сохраните ваш Dashboard.Для этого перейдите в настройки Dashboard, выберите в боковом меню «JSON MODEL». Далее скопируйте отображаемое json-содержимое в отдельный файл и сохраните его.
1. В качестве решения задания приведите листинг этого файла.

---

### Как оформить решение задания

Выполненное домашнее задание пришлите в виде ссылки на .md-файл в вашем репозитории.

---
