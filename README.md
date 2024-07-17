# Aplikacja do generowania kodów QR

## Założenia
Celem projektu jest stworzenie aplikacji umożliwiającej generowanie kodów QR z możliwością edycji wielu parametrów.

## Technologie
- Generowanie kodów QR za pomocą biblioteki SEGNO.
- Warstwa wizualna napisana w bibliotece Tkinter, z rozszerzeniem Tkinter Custom.

## Funkcjonalności
- **Konfiguracja kodu QR**:
  - Ustawienie wielkości generowanego kodu oraz ramki zewnętrznej.
  - Wybór stylu tła: kolor tła, przezroczyste tło lub tło w formie grafiki lub GIF-a.
  - Wybór koloru kodu QR.
  - Obrót kodu QR o określony kąt.
  - Możliwość zmiany wszystkich parametrów za pomocą przycisków, pól tekstowych itp.
  
- **Animowany QR**:
  - Generowanie animowanego QR z możliwością wyboru pliku z komputera.
  - Opcja rotacji QR w zakresie od 0 do 359 stopni, z walidacją liczbową.
  
- **Interakcja użytkownika**:
  - Wybór kolorów za pomocą color pickera.
  - Podgląd wygenerowanego kodu QR po podaniu parametrów.
  - Możliwość wyboru ścieżki zapisu wygenerowanego kodu lub skopiowania go do schowka.

- **Warstwa serwisowa**:
  - Projektowanie z myślą o przyszłym przeniesieniu aplikacji na stronę internetową.

## Podsumowanie
Aplikacja pozwala na szybkie i elastyczne generowanie kodów QR z różnorodnymi opcjami konfiguracyjnymi, odpowiadającymi potrzebom samorządu lokalnego. Dzięki intuicyjnemu interfejsowi użytkownika opartemu na Tkinter Custom, użytkownicy mogą łatwo dostosować parametry generowanego kodu QR oraz przeglądać jego podgląd przed zapisaniem lub skopiowaniem do schowka.

## Autorzy
Autorzy: ximi36, kryreneus
