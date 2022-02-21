import csv
import matplotlib.pyplot as plt


class Trainer:
    theta: list[float] = [0.0, 0.0]
    data: list[dict] = []
    data_row_count: int = 0

    def __init__(self, data_file_name: str):
        data_file = open(data_file_name, "r")
        reader = csv.reader(data_file)
        i = 0
        for mileage, price in reader:
            self.data.append({"mileage": int(mileage), "price": int(price)})
            plt.scatter(int(mileage), int(price))
            i += 1
        self.data_row_count = i
        data_file.close()

    def get_estimate_price(self, theta: list[float], mileage: int):
        return theta[0] + theta[1] * mileage

    def calc_theta_0(self, theta: list[float]) -> float:
        new_theta = 0
        for element in self.data:
            mileage = int(element["mileage"])
            price = int(element["price"])
            new_theta += (self.get_estimate_price(theta, mileage) - price)
        new_theta = ((new_theta / self.data_row_count) * 0.01)
        return new_theta

    def calc_theta_1(self, theta: list[float]) -> float:
        new_theta = 0
        for element in self.data:
            mileage = int(element["mileage"])
            price = int(element["price"])
            new_theta += ((self.get_estimate_price(theta, mileage) - price) * mileage)
        new_theta = ((new_theta / self.data_row_count) * 0.00000000015)
        return new_theta

    def calc_cost(self, theta) -> int:
        cost_sum = 0
        for element in self.data:
            mileage = int(element["mileage"])
            price = int(element["price"])
            cost_sum += ((self.get_estimate_price(theta, mileage) - price) ** 2) / self.data_row_count
        return cost_sum

    def write_to_file(self) -> None:
        theta_file = open("theta.txt", "w+")
        theta_file.write(f"{self.theta[0]},{self.theta[1]}")

    def training(self):
        for i in range(10000):
            prev = self.theta.copy()
            self.theta[0] = prev[0] - self.calc_theta_0(prev) # b - b_grad
            self.theta[1] = prev[1] - self.calc_theta_1(prev) # w - w_grad
            print("{0:2} w = {1:.5f}, b = {2:.5f} error = {3:.5f}"
                  .format(i, self.theta[1], self.theta[0], self.calc_cost(self.theta)))
        plt.plot([0, 250000], [self.get_estimate_price(self.theta, 0), self.get_estimate_price(self.theta, 250000)])
        self.write_to_file()


if __name__ == '__main__':
    tr = Trainer("data.csv")
    tr.training()
    plt.show()
