import csv
from sys import argv


def get_theta() -> list[int]:
    ret = [0, 0]
    try:
        theta_file = open("theta.txt", "r")
        reader = csv.reader(theta_file)
        ret = reader.__next__()
    except FileNotFoundError:
        pass
    return ret


if __name__ == '__main__':
    theta = get_theta()
    mileage = int(argv[1])
    print(f"Estimated price is {float(theta[0]) + float(theta[1]) * mileage}")
