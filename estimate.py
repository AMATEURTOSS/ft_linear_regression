import csv
from sys import argv


def get_data() -> list[int]:
    ret = [0, 0]
    try:
        theta_file = open("theta.txt", "r")
        reader = csv.reader(theta_file)
        ret = reader.__next__()
    except FileNotFoundError:
        pass
    return ret


def original_data_to_normalized_data(target, max_val, min_val):
    return (target - min_val) / (max_val - min_val)


def normalized_data_to_original_data(target, max_val, min_val):
    return target * (max_val - min_val) + min_val


if __name__ == '__main__':
    data = get_data()
    normalized_theta0 = float(data[0])
    normalized_theta1 = float(data[1])
    mileage_max = float(data[2])
    mileage_min = float(data[3])
    price_max = float(data[4])
    price_min = float(data[5])
    mileage = int(argv[1])
    normalized_estimated_price = float(normalized_theta0) + float(normalized_theta1) \
                                 * original_data_to_normalized_data(mileage, mileage_max, mileage_min)
    estimated_price = normalized_data_to_original_data(normalized_estimated_price, price_max, price_min)
    print(f"Estimated price is {estimated_price}")
