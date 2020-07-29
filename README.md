# py_sms2oik
 <h3>Описание.</h3> <br>
 Программа предназначена для считывания смс сообщений от сигнализатора КЗ на ВЛ Linetroll R400D и дальнейшая их интергация в ПТК "ОИК Диспетчер".
 
 <h3>Алгоритм работы. </h3> <br>
 Сигнализаторы КЗ на ВЛ должны быть настроены на передачу сообщений сим-карте, установленной в модеме. GSM модем подключен к компьютеру через USB. 
 Программа обращается к модему посредством виртуального интерфеса RS-232 и АТ комманд. 
 При постеплении сообщения на сим карту, программа ее интерпретирует и делает специальный http запрос к серверу ОИК, воздейтсвуя на данные.  
 
 <h3>Конфигурационные файлы. </h3> <br>
 В папке с программой находится файл settings.ini. В нем задается соответствие абонентского номера сим-карты, установленной в Linetroll и адресу БД ОИК диспетчер. 
 +79826103571;106:1:;ВЛ-110 кВ Арти-Манчаж
 Внимание! Адрес в структуре должен заканчиваться на двоеточие, например "106:1:", номер телефона задается в формате "+79005229999"
 Каждая новая запись должна начинаться с начала строки. 

 <h3>Описание в структуре ОИК Диспетчер. </h3> <br>
 В структуре БД ОИК Диспетчера необходимо создать КП на каждый Лайнтролл, следующей структуры: 
 Канал (Лайнтролы)
	КП "Место установки лайнтрола"
		Телесигналы
			1 ТС Неустойчивое повреждение
			2 ТС Устойчивое повреждение
			3 ТС Низкий заряд батареи
			4 ТС Потеря напряжения,
		Телеизмерения
			1 ТИ Уровень сети GSM 
 
 <h3>Параметры запуска из командной строки.</h3> <br>
 python sms2oik.py <br>
 -s адрес сервера <br>
 -p COM порт комьютера через который идет опрос модема <br>
 -cc ключ для воздействия на данные ОИК Диспетчер. Задается при запуске oik_http_gate.exe <br>
 -cs скорость обмена с модемом на COM порту <br>
 
