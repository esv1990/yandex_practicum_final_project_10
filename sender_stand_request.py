import configuration
import data
import requests

# Создаем пользователя
def post_new_user(body):
    return requests.post(configuration.URL_SERVICE + configuration.CREATE_USER_PATH,  # подставляем полный url
                         json=body,  # тут тело
                         headers=data.headers)  # а здесь заголовки




def get_auth_token():
    auth_token = requests.post(configuration.URL_SERVICE + configuration.CREATE_USER_PATH,
                               headers=data.headers)
    return auth_token


# создаем новый набор
def post_new_client_kit(kit_body, auth_Token):
    headers = data.headers.copy()
    headers["Authorization"] = "Bearer " + auth_Token
    return requests.post(configuration.URL_SERVICE + configuration.CREATE_PRODUCTS_KIT_PATH, json=kit_body,
                         headers=headers)
