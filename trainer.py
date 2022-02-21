import csv
import matplotlib.pyplot as plt


class Trainer:
    theta: list[float] = [0.0, 0.0]
    data: list[dict] = []

    def __init__(self, data_file_name: str):
        data_file = open(data_file_name, "r")
        reader = csv.reader(data_file)
        for mileage, price in reader:
            self.data.append({"mileage": int(mileage), "price": int(price)})
            plt.scatter(int(mileage), int(price))
        data_file.close()

    def get_estimate_price(self, mileage: int):
        return self.theta[0] + self.theta[1] * mileage

    def calc_theta_0(self) -> float:
        new_theta = 0
        for element in self.data:
            mileage = int(element["mileage"])
            price = int(element["price"])
            new_theta += (self.get_estimate_price(mileage) - price)
        new_theta = ((new_theta / len(self.data)) * 0.01)
        return new_theta

    def calc_theta_1(self) -> float:
        new_theta = 0
        for element in self.data:
            mileage = int(element["mileage"])
            price = int(element["price"])
            new_theta += ((self.get_estimate_price(mileage) - price) * mileage)
        new_theta = ((new_theta / len(self.data)) * 0.00000000015)
        return new_theta

    def calc_cost(self) -> int:
        cost_sum = 0
        for element in self.data:
            mileage = int(element["mileage"])
            price = int(element["price"])
            cost_sum += ((self.get_estimate_price(mileage) - price) ** 2) / len(self.data)
        return cost_sum

    def write_to_file(self) -> None:
        theta_file = open("theta.txt", "w+")
        theta_file.write(f"{self.theta[0]},{self.theta[1]}")

    def training(self):
        for i in range(10000):
            self.theta[0] -= self.calc_theta_0()  # b - b_grad
            self.theta[1] -= self.calc_theta_1()  # w - w_grad
            print("{0:2} w = {1:.5f}, b = {2:.5f} error = {3:.5f}"
                  .format(i, self.theta[1], self.theta[0], self.calc_cost()))
        plt.plot([0, 250000], [self.get_estimate_price(0), self.get_estimate_price(250000)])
        self.write_to_file()


if __name__ == '__main__':
    tr = Trainer("data.csv")
    tr.training()
    plt.show()
