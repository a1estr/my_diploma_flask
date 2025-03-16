import requests



# Данный код не является тестом!!! он создан для демонстарации того какой адресс внутри контейнера
def test_example_api():

  url = "http://localhost:5000/"

  headers = {
      "accept": "application/json",
      "Content-Type": "application/json"
  }

  data = {
      "username": "test",
      "password": "test"
  }

  response = requests.post(url, json=data, headers=headers)

  if response.status_code == 200:
      print("Успешный вход в систему:")
      print(response.json())
  elif response.status_code == 401:
      print("Ошибка авторизации: Неверное имя пользователя или пароль.")
  else:
      print(f"Ошибка запроса: {response.status_code}")
      print(response.text)

  response = requests.post(f'{url}/register', json=data, headers=headers)

  # Вывод статуса и ответа
  print("Статус код:", response.status_code)
  print("Ответ:", response.json())

  response = requests.post(f'{url}/register', json=data, headers=headers)

  print("Статус код:", response.status_code)
  print("Ответ:", response.json())  

  response = requests.post(url, json=data, headers=headers)

  if response.status_code == 200:
      print("Успешный вход в систему:")
      print(response.json())
  elif response.status_code == 401:
      print("Ошибка авторизации: Неверное имя пользователя или пароль.")
  else:
      print(f"Ошибка запроса: {response.status_code}")
      print(response.text)





