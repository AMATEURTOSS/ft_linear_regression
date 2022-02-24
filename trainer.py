import csv
import sys
import matplotlib.pyplot as plt


def is_valid_parameter():
    if (len(sys.argv) != 2 and len(sys.argv) != 3) or\
            (len(sys.argv) == 3 and sys.argv[2] != "-cw" and sys.argv[2] != "-cb"):
        print("ERROR: Invalid parameter")
        print("USAGE: python trainer.py <file_name> [-option]")
        print("OPTIONS:")
        print("        -cw: graph the cost for w(gradient")
        print("        -cb: graph the cost for b(y-intercept")
        exit(1)
    try:
        file = open(sys.argv[1], "r")
        file.close()
    except FileNotFoundError:
        print("ERROR: File not found")
        exit(1)


def read_data() -> list:
    data = []
    data_file = open(file_name, "r")
    reader = csv.reader(data_file)
    for mileage, price in reader:
        data.append({"mileage": int(mileage), "price": int(price)})
    data_file.close()
    return data


class Trainer:
    __theta: list = [0.0, 0.0]
    __data: list
    __option: str
    __normalized_data: list = []
    __mileage_max: int
    __mileage_min: int
    __price_max: int
    __price_min: int

    def __init__(self, data: list, option: str):
        self.__data = data
        self.__option = option
        self.__normalization()

    def __normalization(self) -> None:
        self.__mileage_max = max(self.__data, key=lambda el: el["mileage"])["mileage"]
        self.__mileage_min = min(self.__data, key=lambda el: el["mileage"])["mileage"]
        self.__price_max = max(self.__data, key=lambda el: el["price"])["price"]
        self.__price_min = min(self.__data, key=lambda el: el["price"])["price"]
        for element in self.__data:
            mileage = element["mileage"]
            price = element["price"]
            normalized_mileage = (mileage - self.__mileage_min) / (self.__mileage_max - self.__mileage_min)
            normalized_price = (price - self.__price_min) / (self.__price_max - self.__price_min)
            self.__normalized_data.append({"mileage": normalized_mileage, "price": normalized_price})
            if self.__option is None:
                plt.scatter(normalized_mileage, normalized_price)

    def __get_estimate_price(self, mileage: int):
        return self.__theta[0] + self.__theta[1] * mileage

    def __calc_theta_0(self) -> float:
        new_theta = 0
        for element in self.__normalized_data:
            mileage = element["mileage"]
            price = element["price"]
            new_theta += (self.__get_estimate_price(mileage) - price)
        new_theta = ((new_theta / len(self.__normalized_data)) * 0.1)
        return new_theta

    def __calc_theta_1(self) -> float:
        new_theta = 0
        for element in self.__normalized_data:
            mileage = element["mileage"]
            price = element["price"]
            new_theta += ((self.__get_estimate_price(mileage) - price) * mileage)
        new_theta = ((new_theta / len(self.__normalized_data)) * 0.1)
        return new_theta

    def __calc_cost(self) -> float:
        cost_sum = 0
        for element in self.__normalized_data:
            mileage = int(element["mileage"])
            price = int(element["price"])
            cost_sum += ((self.__get_estimate_price(mileage) - price) ** 2)
        return cost_sum / len(self.__normalized_data)

    def __write_to_file(self) -> None:
        theta_file = open("theta.txt", "w+")
        theta_file.write(f"{self.__theta[0]},"
                         f"{self.__theta[1]},"
                         f"{self.__mileage_max},"
                         f"{self.__mileage_min},"
                         f"{self.__price_max},"
                         f"{self.__price_min}")

    def training(self):
        for i in range(10000):
            if self.__option == "-cb" or self.__option is None:
                self.__theta[0] -= self.__calc_theta_0()  # b - b_grad
            if self.__option == "-cw" or self.__option is None:
                self.__theta[1] -= self.__calc_theta_1()  # w - w_grad
            if self.__option is not None:
                plt.scatter(self.__theta[1], self.__calc_cost())
        print(f"w: {self.__theta[1]}")
        print(f"b: {self.__theta[0]}")
        if self.__option is None:
            plt.plot([0, 1], [self.__get_estimate_price(0), self.__get_estimate_price(1)])
        self.__write_to_file()


if __name__ == '__main__':
    is_valid_parameter()
    file_name = sys.argv[1]
    option = sys.argv[2] if len(sys.argv) == 3 else None
    data = read_data()
    tr = Trainer(data, option)
    tr.training()
    plt.show()
