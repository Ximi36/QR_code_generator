import requests
import re
import time
import hashlib
import urllib.parse
import base64

# Podstawowy adres URL
base_url = "https://task.zostansecurity.ninja/"

# Pobranie zawartości podstawowej strony
response = requests.get(base_url)
content = response.text

# Wyszukiwanie ciągu znaków zaczynającego się od "/?step=1&challenge" i kończącego się na wartości timestamp
pattern = r"(/\?step=1&challenge=[^&]+&timestamp=\d+)"
match = re.search(pattern, content)

if match:
    # Pobranie znalezionego ciągu znaków
    challenge_url = match.group(1)

    # Aktualny timestamp
    current_timestamp = int(time.time())

    # Aktualizacja ciągu znaków z aktualnym timestampem
    updated_challenge_url = re.sub(r'timestamp=\d+', f'timestamp={current_timestamp}', challenge_url)

    # Utworzenie pełnego URL do zapytania GET
    full_url = base_url + updated_challenge_url

    # Wysłanie zapytania GET na nowy adres
    first_response = requests.get(full_url)

    # Wyświetlenie odpowiedzi
    print(first_response.text)

    # Sprawdzenie, czy odpowiedź zawiera instrukcje dla następnego etapu
    if "Very good! Next stage:" in first_response.text:
        # Pobranie X-challenge z odpowiedzi
        challenge_pattern = r"X-challenge: ([a-f0-9]{64})"
        challenge_match = re.search(challenge_pattern, first_response.text)

        if challenge_match:
            x_challenge = challenge_match.group(1)

            # Drugi etap: wysłanie zapytania GET do /?step=2 z odpowiednimi nagłówkami
            second_stage_url = base_url + "/?step=2"

            # Nagłówki do drugiego etapu
            headers = {
                "X-challenge": x_challenge,
                "X-timestamp": str(int(time.time()))  # Aktualny timestamp
            }

            # Wysłanie zapytania GET z nagłówkami
            second_response = requests.get(second_stage_url, headers=headers)

            # Wyświetlenie odpowiedzi
            print(second_response.text)

            # Sprawdzenie, czy odpowiedź zawiera instrukcje dla trzeciego etapu
            if "Very good! Next stage:" in second_response.text:
                # Pobranie challenge, timestamp i słownika do trzeciego etapu
                third_stage_challenge_pattern = r"challenge: ([a-f0-9]{64})"
                third_stage_timestamp_pattern = r"timestamp: (\d+)"
                dictionary_pattern = r"\{([^\}]+)\}"

                third_stage_challenge_match = re.search(third_stage_challenge_pattern, second_response.text)
                third_stage_timestamp_match = re.search(third_stage_timestamp_pattern, second_response.text)
                dictionary_match = re.search(dictionary_pattern, second_response.text)

                if third_stage_challenge_match and third_stage_timestamp_match and dictionary_match:
                    challenge_value = third_stage_challenge_match.group(1)
                    timestamp_value = third_stage_timestamp_match.group(1)

                    # Przetwarzanie słownika
                    dictionary_str = dictionary_match.group(1)
                    # Podział ciągu na pary klucz-wartość
                    dictionary_items = re.findall(r'"([^"]+)": "([^"]+)"', dictionary_str)
                    data_dict = {key: value for key, value in dictionary_items}

                    # Sortowanie kluczy słownika i tworzenie sparametryzowanego stringa
                    sorted_items = sorted(data_dict.items())
                    encoded_str = urllib.parse.urlencode(sorted_items)

                    # Obliczanie hash SHA256
                    hash_value = hashlib.sha256(encoded_str.encode()).hexdigest()

                    # Parametry POST do trzeciego etapu
                    post_data = {
                        "challenge": challenge_value,
                        "timestamp": timestamp_value,
                        "hash": hash_value
                    }

                    # Wysłanie zapytania POST do trzeciego etapu
                    third_stage_url = base_url + "/?step=3"
                    third_response = requests.post(third_stage_url, data=post_data)

                    # Wyświetlenie odpowiedzi
                    print(third_response.text)

                    # Pobranie zakodowanego emaila
                    encoded_email_pattern = r"Vm0w.*"
                    encoded_email_match = re.search(encoded_email_pattern, third_response.text)

                    if encoded_email_match:
                        encoded_email = encoded_email_match.group(0)

                        # Dekodowanie wielokrotne base64
                        decoded_email = encoded_email
                        while True:
                            try:
                                decoded_email = base64.b64decode(decoded_email).decode('utf-8')
                            except Exception as e:
                                break

                        # Wyświetlenie zdekodowanego emaila
                        print("Zdekodowany email:", decoded_email)
                    else:
                        print("Nie znaleziono zakodowanego emaila.")
                else:
                    print("Nie znaleziono wartości challenge, timestamp lub słownika w odpowiedzi drugiego etapu.")
            else:
                print("Drugi etap nie zakończył się sukcesem.")
        else:
            print("Nie znaleziono nagłówka X-challenge w odpowiedzi.")
    else:
        print("Pierwszy etap nie zakończył się sukcesem.")
else:
    print("Nie znaleziono odpowiedniego ciągu znaków.")
