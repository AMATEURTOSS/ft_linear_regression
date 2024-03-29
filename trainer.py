import csv
import sys
import matplotlib.pyplot as plt


def is_valid_parameter():
    if len(sys.argv) != 2:
        print("ERROR: Invalid parameter")
        print("USAGE: python trainer.py [file_name]")
        exit(1)
    try:
        file = open(sys.argv[1], "r")
        file.close()
    except FileNotFoundError:
        print("ERROR: File not found")
        exit(1)


class Trainer:
    __theta: list = [0.0, 0.0]
    __data: list = []
    __normalized_data: list = []
    __mileage_max: int
    __mileage_min: int
    __price_max: int
    __price_min: int
    __x = []  # x value for cost graph (bios)
    __y = []  # y value for cost graph (weight)
    __z = []  # z value for cost graph (cost)

    def __init__(self, data_file_name: str):
        data_file = open(data_file_name, "r")
        reader = csv.reader(data_file)
        for mileage, price in reader:
            self.__data.append({"mileage": int(mileage), "price": int(price)})
        self.__normalization()
        data_file.close()

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
            mileage = float(element["mileage"])
            price = float(element["price"])
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

    def __draw_linear_regression_graph(self) -> None:
        plt.figure()
        ax = plt.axes()
        ax.set_title('ft_linear_regression')
        ax.set_ylabel('price')
        ax.set_xlabel('mileage')
        for element in self.__normalized_data:
            plt.scatter(element["mileage"], element["price"])
        plt.plot([0, 1], [self.__get_estimate_price(0), self.__get_estimate_price(1)])

    def __draw_cost_graph(self) -> None:
        plt.figure()
        ax = plt.axes(projection='3d')
        ax.set_title('cost according to W and B')
        ax.set_xlabel('bios')
        ax.set_ylabel('weight')
        ax.set_zlabel('cost')
        ax.plot3D(self.__x, self.__y, self.__z, 'green')

    def training(self):
        for i in range(10000):
            self.__x.append(self.__theta[0])
            self.__y.append(self.__theta[1])
            self.__z.append(self.__calc_cost())
            self.__theta[0] -= self.__calc_theta_0()  # b - b_grad
            self.__theta[1] -= self.__calc_theta_1()  # w - w_grad
        print(f"w: {self.__theta[1]}")
        print(f"b: {self.__theta[0]}")
        print(f"e: {self.__calc_cost()}")
        self.__draw_linear_regression_graph()
        self.__draw_cost_graph()
        self.__write_to_file()


if __name__ == '__main__':
    is_valid_parameter()
    tr = Trainer(sys.argv[1])
    tr.training()
    plt.show()
