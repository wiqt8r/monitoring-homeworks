# Домашнее задание к занятию 14 «Средство визуализации Grafana»

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

<img width="564" height="370" alt="image" src="https://github.com/user-attachments/assets/67e76464-4d2e-4ac7-91c3-fa5c3c4e9904" />



## Задание 4

[Листинг файла Dashboard.](./Dashboard.json)

---

