import json
import logging

# логирование
logging.basicConfig(
    filename='shelter.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

# ===== Базовый класс =====
class Animal:
    def __init__(self, name, age, weight, health="good"):
        self.name = name
        self.age = age
        self.weight = weight
        self.__health = health

    def speak(self):
        return "..."

    def eat(self, food):
        logging.info(f"{self.name} ест {food}")

    def info(self):
        return f"Имя: {self.name}, возраст: {self.age}, вес: {self.weight}"

    def __str__(self):
        return self.info()


# ===== Наследники =====
class Dog(Animal):
    def speak(self):
        return "Гав!"

    def fetch(self):
        return f"{self.name} приносит палку!"


class Cat(Animal):
    def speak(self):
        return "Мяу!"

    def purr(self):
        return f"{self.name} мурчит..."


class Parrot(Animal):
    def speak(self):
        return "Привет!"

    def repeat(self, phrase):
        return f"{self.name} повторяет: {phrase}"


# ===== Менеджер приюта =====
class Shelter:
    def __init__(self):
        self.animals = []

    def add_animal(self, animal):
        self.animals.append(animal)
        logging.info(f"Добавлено животное {animal.name}, возраст {animal.age}")

    def remove_animal(self, name):
        for a in self.animals:
            if a.name == name:
                self.animals.remove(a)
                logging.info(f"Удалено животное {name}")
                return
        logging.error(f"Животное {name} не найдено")

    def find_by_name(self, name):
        for a in self.animals:
            if a.name == name:
                logging.info(f"Найдено животное {name}")
                return a
        logging.error(f"Поиск: животное {name} не найдено")
        return None

    def show_all(self):
        for a in self.animals:
            print(a)

    def save_to_file(self):
        data = []
        for a in self.animals:
            data.append({
                "type": a.__class__.__name__,
                "name": a.name,
                "age": a.age,
                "weight": a.weight
            })

        with open("animals.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        logging.info("Данные сохранены в файл")

    def load_from_file(self):
        try:
            with open("animals.json", "r", encoding="utf-8") as f:
                data = json.load(f)

            self.animals = []

            for item in data:
                if item["type"] == "Dog":
                    a = Dog(item["name"], item["age"], item["weight"])
                elif item["type"] == "Cat":
                    a = Cat(item["name"], item["age"], item["weight"])
                elif item["type"] == "Parrot":
                    a = Parrot(item["name"], item["age"], item["weight"])
                else:
                    continue

                self.animals.append(a)

            logging.info("Данные загружены из файла")

        except FileNotFoundError:
            logging.error("Файл animals.json не найден")


# ===== Консольное меню =====
def main():
    shelter = Shelter()

    while True:
        print("\n1 Добавить животное")
        print("2 Удалить животное")
        print("3 Найти животное")
        print("4 Показать всех")
        print("5 Сохранить")
        print("6 Загрузить")
        print("0 Выход")

        choice = input("Выбор: ")

        if choice == "1":
            t = input("Тип (dog/cat/parrot): ")
            name = input("Имя: ")
            age = int(input("Возраст: "))
            weight = float(input("Вес: "))

            if t == "dog":
                shelter.add_animal(Dog(name, age, weight))
            elif t == "cat":
                shelter.add_animal(Cat(name, age, weight))
            elif t == "parrot":
                shelter.add_animal(Parrot(name, age, weight))

        elif choice == "2":
            name = input("Имя: ")
            shelter.remove_animal(name)

        elif choice == "3":
            name = input("Имя: ")
            a = shelter.find_by_name(name)
            if a:
                print(a.info())

        elif choice == "4":
            shelter.show_all()

        elif choice == "5":
            shelter.save_to_file()

        elif choice == "6":
            shelter.load_from_file()

        elif choice == "0":
            break


if __name__ == "__main__":
    main()
