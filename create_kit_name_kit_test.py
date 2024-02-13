import sender_stand_request
import data

# -----------Функции------------


# Значения для проверок с длинным параметром:

many_symbol_1 = "AbcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdAbcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabC"
many_symbol_2 = "AbcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdAbcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcD"


# функция получения токена
def get_new_user_token():
    user_response = sender_stand_request.post_new_user(data.user_body)
    # получаем токен
    auth_Token = user_response.json()["authToken"]
    return auth_Token


# функция, которая меняет содержимое тела запроса
def get_kit_body(name):
    # копируем из data в new_kit_body словаря с телом запроса
    new_kit_body = data.kit_body.copy()
    # Изменено значение ключа на переменную name
    new_kit_body['name'] = name
    # Возвращается новый словарь с требуемым значением имени
    return new_kit_body


# Функция позитивной проверки
def positive_assert(kit_body):
    new_kit_body_positive = get_kit_body(kit_body)  # в переменную сохраняем новое тело
    auth_token = get_new_user_token()  # передаем auth_Token
    # сохраняем результат запроса
    kit_response_positive = sender_stand_request.post_new_client_kit(new_kit_body_positive, auth_token)
    assert kit_response_positive.status_code == 201  # проверка кода ответа
    assert new_kit_body_positive["name"] == kit_response_positive.json()["name"]


# Функция негативной проверки:
def negative_assert_code_400(kit_body):
    new_kit_body_negative = get_kit_body(kit_body)  # в переменную сохраняем новое тело
    auth_token = get_new_user_token()  # передаем auth_Token
    # сохраняем результат запроса
    kit_response_negative = sender_stand_request.post_new_client_kit(new_kit_body_negative, auth_token)
    assert kit_response_negative.status_code == 400  # роверяем что код ответа 400


# Функция негативной проверки без имени:

def negative_assert_no_name(kit_body):
    # Передаётся auth_token
    auth_token = get_new_user_token()
    # В переменную response сохраняется результат
    kit_response_negative_no_name = sender_stand_request.post_new_client_kit(kit_body, auth_token)
    #  Проверяется, что код ответа = 400
    assert kit_response_negative_no_name.status_code == 400


# ---------------------Проверки------------------------
# Проверка 1 (Позитивная) - параметр name = 1 символ
def test_create_kit_1_letter_in_kit_name_get_success_response():
    positive_assert("a")


# Проверка 2 (Позитивная) - параметр name = 511 символов

def test_create_kit_511_letters_in_kit_name_get_success_response():
    positive_assert(many_symbol_1)


# Проверка 3 (Негативная) - параметр name = ""

def test_create_kit_0_letter_in_kit_name_get_error_response():
    negative_assert_code_400("")


# Проверка 4 (Негативная) - параметр name = 512 символов

def test_create_kit_512_letters_in_kit_name_get_error_response():
    negative_assert_code_400(many_symbol_2)


# Проверка 5 (Позитивная) - параметр name = "QWErty" - Английские буквы

def test_create_kit_english_letters_in_kit_name_get_success_response():
    positive_assert("QWErty")


# Проверка 6 (Позитивная) - параметр name = "Мария" - Русские буквы

def test_create_kit_russian_letters_in_kit_name_get_success_response():
    positive_assert("Мария")


# Проверка 7 (Позитивная) - параметр name = "\"№%@\"," - Спецсимволы

def test_create_kit_special_symbols_in_kit_name_get_success_response():
    positive_assert("\"№%@\",")


# Проверка 8 (Позитивная) - параметр name = " Человек и КО " - Разрешены пробелы

def test_create_kit_spaces_in_kit_name_get_success_response():
    positive_assert("Человек и КО")


# Проверка 9 (Позитивная) - параметр name = "123" - Разрешены цифры

def test_create_kit_numbers_in_kit_name_get_success_response():
    positive_assert("123")


# Проверка 10 (Негативная) - параметр name не передан

def test_create_kit_no_name_get_error_response():
    current_kit_body_no_name = data.kit_body.copy()  # копируем тело в переменную
    current_kit_body_no_name.pop("name")  # убираем параметр name
    negative_assert_no_name(current_kit_body_no_name)


# Проверка 11 (Негативная) - передан другой тип параметра - число

def test_create_kit_type_number_in_kit_name_get_error_response():
    negative_assert_code_400(1234)
