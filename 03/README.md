# Домашнее задание к занятию 15 «Система сбора логов Elastic Stack»

## Дополнительные ссылки

При выполнении задания используйте дополнительные ресурсы:

- [поднимаем elk в docker](https://www.elastic.co/guide/en/elastic-stack-get-started/current/get-started-docker.html);
- [поднимаем elk в docker с filebeat и docker-логами](https://www.sarulabs.com/post/5/2019-08-12/sending-docker-logs-to-elasticsearch-and-kibana-with-filebeat.html);
- [конфигурируем logstash](https://www.elastic.co/guide/en/logstash/current/configuration.html);
- [плагины filter для logstash](https://www.elastic.co/guide/en/logstash/current/filter-plugins.html);
- [конфигурируем filebeat](https://www.elastic.co/guide/en/beats/libbeat/5.3/config-file-format.html);
- [привязываем индексы из elastic в kibana](https://www.elastic.co/guide/en/kibana/current/index-patterns.html);
- [как просматривать логи в kibana](https://www.elastic.co/guide/en/kibana/current/discover.html);
- [решение ошибки increase vm.max_map_count elasticsearch](https://stackoverflow.com/questions/42889241/how-to-increase-vm-max-map-count).

В процессе выполнения в зависимости от системы могут также возникнуть не указанные здесь проблемы.

Используйте output stdout filebeat/kibana и api elasticsearch для изучения корня проблемы и её устранения.

## Задание 1
> скриншот `docker ps` через 5 минут после старта всех контейнеров (их должно быть 5);
Поднято 5 контейнеров Elasticstack и приложение some_app из композа

<img width="1989" height="417" alt="image" src="https://github.com/user-attachments/assets/d784f50a-7386-4345-a0ef-65ed9a688879" />

> скриншот интерфейса kibana;

<img width="2560" height="1229" alt="image" src="https://github.com/user-attachments/assets/237e061e-97fc-4574-b130-11f56f588649" />


## Задание 2

Кибана запущена, index-patterns есть, поиск работает:

<img width="2560" height="1229" alt="image" src="https://github.com/user-attachments/assets/47d3552a-c201-49b3-a644-f1254e7179b2" />

 
---
