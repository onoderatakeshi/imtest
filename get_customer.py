import json
import sys



class Customer:
    def __init__(self, customer_dict):
        self.customer_dict = customer_dict
   
        self.customer_id = customer_dict["customer"]
        self.meters = customer_dict["meters"]
    
    def output(self):
        for meter in self.meters:
            if meter["mac"] != "":
                print(self.customer_id, meter["mac"])
            else:
                print(self.customer_id)


def test(json_dict):
    total = json_dict["total"]
    print("total=", total)

    for customer in json_dict["customers"]:
        cust = Customer(customer)
        cust.output()

#   print(json_dict["customers"][1])


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Help:")
        print(sys.argv[0], "[filename]")
        quit()

    filename = sys.argv[1]
    fp = open(filename, "r")
    json_dict = json.load(fp)
    test(json_dict)



