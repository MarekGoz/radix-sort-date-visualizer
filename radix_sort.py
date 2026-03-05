import tkinter as tk
from collections import defaultdict
from datetime import datetime


def counting_sort(data, key_func,
                  max_value):  # Sortowanie przez zliczanie (sortuje wartości juz w ramach jednej składowej daty)
    count = [0] * (max_value + 1)
    output = [None] * len(data)

    # Policz wystąpienia każdego klucza
    for item in data:
        key = key_func(item)
        count[key] += 1

    # Zliczaj liczby, aby określić pozycję
    for i in range(1, len(count)):
        count[i] += count[i - 1]

    # Zbuduj tablicę wyjściową (sortowanie stabilne)
    for item in reversed(data):
        key = key_func(item)
        count[key] -= 1
        output[count[key]] = item

    return output


def radix_sort_dates(dates):  # Maksymalne wartości dla składowych daty, aby utworzyć odpowiednią liczbę komórek tablicy
    max_values = {
        "second": 99,
        "minute": 99,
        "hour": 99,
        "day": 99,
        "month": 99,
        "year": 9999
    }

    # Zdefiniuj kolejność sortowania (od pola najmniej znaczącego do najbardziej znaczącego)
    # Lecimy od najmniej znaczacego pola do najbardziej znaczącego (od sekund do lat)
    fields = [
        ("second", lambda x: x[5]),
        ("minute", lambda x: x[4]),
        ("hour", lambda x: x[3]),
        ("day", lambda x: x[2]),
        ("month", lambda x: x[1]),
        ("year", lambda x: x[0])
    ]

    # Wykonaj sortowanie zliczające dla każdego pola w określonej kolejności
    for field, key_func in fields:  # Iteruje sie po wartosciach w dacie
        max_value = max_values[field]
        dates = counting_sort(dates, key_func, max_value)

    return dates


data = [
    (1955, 5, 21, 14, 35, 42),
    (1987, 11, 3, 8, 20, 15),
    (1990, 5, 21, 14, 35, 20),
    (1987, 11, 3, 8, 20, 45),
    (2023, 1, 1, 0, 0, 0),
    (2010, 12, 31, 23, 59, 59),
    (2000, 2, 29, 12, 0, 0),  # Rok przestępny
    (1999, 7, 15, 6, 30, 45),
    (1980, 6, 5, 16, 45, 10),
    (1975, 4, 10, 9, 5, 5),
    (1965, 9, 30, 18, 50, 50),
    (1945, 3, 3, 3, 3, 3),
    (2020, 8, 20, 20, 20, 20),
    (2015, 10, 25, 10, 15, 0),
    (1995, 12, 15, 23, 0, 0),
    (1988, 2, 28, 23, 59, 59),  # Dzień przed przestępnym 29 lutego
    (2012, 2, 29, 14, 30, 30),  # Rok przestępny
    (1993, 3, 15, 7, 45, 30),
    (1970, 1, 1, 0, 0, 1),
    (2001, 9, 9, 1, 1, 1)
]


def GetNewData():  # Funkcja do sprawdzania i zapisywania daty do "bazy danych"
    try:
        year = int(year_entry.get())  # Pobieranie danych z entry w celu utworzenia nowego rekordu w "bazie danych"
        month = int(month_entry.get())
        day = int(day_entry.get())
        hour = int(hour_entry.get())
        minute = int(minute_entry.get())
        second = int(second_entry.get())

        # Walidacja miesiąca i dni (łącznie z rokiem przestępnym))
        if month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12:
            if day > 31 or day < 1:
                error_label.config(text="Błąd: Nieprawidłowa dzień dla tego miesiąca.", fg="red")
                return
        elif month == 4 or month == 6 or month == 9 or month == 11:
            if day > 30 or day < 1:
                error_label.config(text="Błąd: Nieprawidłowa dzień dla tego miesiąca.", fg="red")
                return
        elif month == 2:
            if year % 4 == 0 and year % 100 != 0 or year % 400 == 0:
                if day > 29 or day < 1:
                    error_label.config(text="Błąd: Nieprawidłowa dzień dla tego miesiąca (luty w roku przestępnym).",
                                       fg="red")
                    return
            else:
                if day > 28 or day < 1:
                    error_label.config(text="Błąd: Nieprawidłowa dzień dla tego miesiąca (luty w roku nieprzestępnym).",
                                       fg="red")
                    return
        elif month > 12:
            error_label.config(text="Błąd: Niewłaściwy miesiąc", fg="red")
            return

        # Walidacja godzin, minut i sekund
        if hour > 23 or hour < 0:
            error_label.config(text="Błąd: Nieprawidłowa godzina.", fg="red")
            return
        if minute > 59 or minute < 0:
            error_label.config(text="Błąd: Nieprawidłowa minuta.", fg="red")
            return
        if second > 59 or second < 0:
            error_label.config(text="Błąd: Nieprawidłowa sekunda.", fg="red")
            return

        # Tworzenie obiektu daty i sprawdzenie, czy jest w przyszłości
        temporaryData = datetime(year, month, day, hour, minute, second)
        now = datetime.now()
        if temporaryData > now:
            error_label.config(text="Błąd: Data z przyszłości.", fg="red")  # Wyrzucanie błędu o dacie z przyszłości
            return

        # Dodanie poprawnej daty do listy i wyświetlenie jej
        data.append((year, month, day, hour, minute, second))
        sorted_dates_text.delete("1.0", tk.END)  # Wyczyść poprzedni tekst
        sorted_dates_text.insert("1.0", "\n".join(map(str, radix_sort_dates(data))))  # Wyświetl posortowane daty
        error_label.config(text="Dodano poprawnie datę.", fg="green")

    except ValueError as e:  # Error z odpwoiednim komunikatem
        error_label.config(text=f"Błąd: {e}", fg="red")

    # GUI setup


root = tk.Tk()  # Tworzenie instancji okna GUI
root.title("Projekt AiSD")  # Tytuł okna

# Tytuł aplikacji w oknie
title = tk.Label(
    root,
    text="RADIX-SORT",
    font=("Helvetica", 40, "bold"),
    fg="#333333",
    padx=10,
    pady=20
)
title.pack()


def toggle_fullscreen(event=None):
    current_state = root.attributes('-fullscreen')  # Pobranie aktualnego stanu, czy aplikacja ma pełny ekran
    root.attributes('-fullscreen', not current_state)  # Zmiana stanu pełnego ekranu


# Zmianna fullscreen-okno po kliknięciu Escape
root.bind("<Escape>", toggle_fullscreen)

# Pola z datą do dodania, w ramach tabelki, z lewej nazwa, z prawej pola do wpisania daty
frame = tk.Frame(root, padx=50, pady=20)
frame.pack()

tk.Label(frame, text="Rok:", font=("Arial", 10, "bold")).grid(row=0, column=0)
year_entry = tk.Entry(frame)
year_entry.grid(row=0, column=1)

tk.Label(frame, text="Miesiąc:", font=("Arial", 10, "bold")).grid(row=1, column=0)
month_entry = tk.Entry(frame)
month_entry.grid(row=1, column=1)

tk.Label(frame, text="Dzień:", font=("Arial", 10, "bold")).grid(row=2, column=0)
day_entry = tk.Entry(frame)
day_entry.grid(row=2, column=1)

tk.Label(frame, text="Godzina:", font=("Arial", 10, "bold")).grid(row=3, column=0)
hour_entry = tk.Entry(frame)
hour_entry.grid(row=3, column=1)

tk.Label(frame, text="Minuta:", font=("Arial", 10, "bold")).grid(row=4, column=0)
minute_entry = tk.Entry(frame)
minute_entry.grid(row=4, column=1)

tk.Label(frame, text="Sekunda:", font=("Arial", 10, "bold")).grid(row=5, column=0)
second_entry = tk.Entry(frame)
second_entry.grid(row=5, column=1)

# Przycisk dodawania
add_button = tk.Button(
    frame,
    text="Dodaj datę",
    command=GetNewData,
    bg="#4CAF50",
    fg="white",
    font=("Arial", 12, "bold"),
    bd=5  # Szerokość obramowania
)
add_button.grid(row=6, column=0, columnspan=2, pady=10)

# Komunikat błędu
error_label = tk.Label(root, text="", font=("Arial", 12), fg="red")  # Dodanie label do okna
error_label.pack()  # Umieszczenie label na oknie

# Dodanie scrollbara do danych
sorted_dates_frame = tk.Frame(root)  # Dodanie frame na posortowane dane
sorted_dates_frame.pack(fill="both",
                        expand=True)  # Umieszczenie frame na oknie z wypełnieniem wysokości i szerokości oraz rozciąganiem

sorted_dates_text = tk.Text(sorted_dates_frame, wrap="none", padx=10, pady=10)  # Wyświetlenie posortowanych danych
sorted_dates_text.pack(side="left", fill="both",
                       expand=True)  # Umieszczenie text na frame z ułożeniem na lewo, z wypełnieniem wysokości i szerokości oraz rozciąganiem

scrollbar = tk.Scrollbar(sorted_dates_frame, command=sorted_dates_text.yview)  # Dodanie scrollbara
scrollbar.pack(side="right", fill="y")  # Ustawienie z prawej strony, wypełnienie wysokości
sorted_dates_text.config(yscrollcommand=scrollbar.set)  # Ustawienie scrollbara na text

# Początkowe wyświetlanie danych
sorted_dates_text.insert("1.0", "\n".join(map(str, radix_sort_dates(
    data))))  # 1.0 dodaje na początek frame; dodawanie do jednego tekstu, gdzie każdy rekord to nowa linijka

# Włączenie GUI
root.mainloop()

"""
Podział pracy:

    Kamil Homziuk:
        -Pobranie danych (metoda GetNewData)
        -Walidacja danych
        -GUI

    Marek Gozdalski:
        -Sortowanie countingSort, radixSort
        -alerty do GUI
        -dodanie scrollbara do danych

"""
# Użytkownik musi podać datę przynajmniej w poprawnym formacie pod względem liczby cyfr, aby dostać nasz komunikat błędu
# Błędy systemowe wynikają z próby tworzenia zmiennej typu data do porównania, czy nie jest to data z przyszłości