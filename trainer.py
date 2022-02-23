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
    theta: list = [0.0, 0.0]
    data: list = []
    normalized_data: list = []
    mileage_max: int
    mileage_min: int
    price_max: int
    price_min: int

    def __init__(self, data_file_name: str):
        data_file = open(data_file_name, "r")
        reader = csv.reader(data_file)
        for mileage, price in reader:
            self.data.append({"mileage": int(mileage), "price": int(price)})
        self.normalization()
        data_file.close()

    def normalization(self) -> None:
        self.mileage_max = max(self.data, key=lambda el: el["mileage"])["mileage"]
        self.mileage_min = min(self.data, key=lambda el: el["mileage"])["mileage"]
        self.price_max = max(self.data, key=lambda el: el["price"])["price"]
        self.price_min = min(self.data, key=lambda el: el["price"])["price"]
        for element in self.data:
            mileage = element["mileage"]
            price = element["price"]
            normalized_mileage = (mileage - self.mileage_min) / (self.mileage_max - self.mileage_min)
            normalized_price = (price - self.price_min) / (self.price_max - self.price_min)
            self.normalized_data.append({"mileage": normalized_mileage, "price": normalized_price})
            plt.scatter(normalized_mileage, normalized_price)

    def get_estimate_price(self, mileage: int):
        return self.theta[0] + self.theta[1] * mileage

    def calc_theta_0(self) -> float:
        new_theta = 0
        for element in self.normalized_data:
            mileage = element["mileage"]
            price = element["price"]
            new_theta += (self.get_estimate_price(mileage) - price)
        new_theta = ((new_theta / len(self.normalized_data)) * 0.1)
        return new_theta

    def calc_theta_1(self) -> float:
        new_theta = 0
        for element in self.normalized_data:
            mileage = element["mileage"]
            price = element["price"]
            new_theta += ((self.get_estimate_price(mileage) - price) * mileage)
        new_theta = ((new_theta / len(self.normalized_data)) * 0.1)
        return new_theta

    def calc_cost(self) -> int:
        cost_sum = 0
        for element in self.normalized_data:
            mileage = int(element["mileage"])
            price = int(element["price"])
            cost_sum += ((self.get_estimate_price(mileage) - price) ** 2) / len(self.normalized_data)
        return cost_sum

    def write_to_file(self) -> None:
        theta_file = open("theta.txt", "w+")
        theta_file.write(f"{self.theta[0]},"
                         f"{self.theta[1]},"
                         f"{self.mileage_max},"
                         f"{self.mileage_min},"
                         f"{self.price_max},"
                         f"{self.price_min}")

    def training(self):
        for i in range(10000):
            self.theta[0] -= self.calc_theta_0()  # b - b_grad
            self.theta[1] -= self.calc_theta_1()  # w - w_grad
            print(f"e: {self.calc_cost()}")
        print(f"w: {self.theta[1]}")
        print(f"b: {self.theta[0]}")
        plt.plot([0, 1], [self.get_estimate_price(0), self.get_estimate_price(1)])
        self.write_to_file()


if __name__ == '__main__':
    is_valid_parameter()
    tr = Trainer(sys.argv[1])
    tr.training()
    plt.show()
