import csv

def process_transactions(input_file):
    credit_file = "credit.csv"
    debit_file = "debit.csv"
    error_file = "error.csv"

    balances = {}

    with open(input_file, "r") as infile, \
         open(credit_file, "w", newline="") as credit_out, \
         open(debit_file, "w", newline="") as debit_out, \
         open(error_file, "w", newline="") as error_out:

        reader = csv.DictReader(infile)
        credit_writer = csv.DictWriter(credit_out, fieldnames=reader.fieldnames)
        debit_writer = csv.DictWriter(debit_out, fieldnames=reader.fieldnames)
        error_writer = csv.DictWriter(error_out, fieldnames=reader.fieldnames + ["reason"])

        credit_writer.writeheader()
        debit_writer.writeheader()
        error_writer.writeheader()

        for row in reader:
            try:
                tid = row["tid"]
                acc = row["acc"]
                ttype = row["type"].upper()
                amount = float(row["amount"])
                timestamp = row["time"]

                if ttype not in ["CREDIT", "DEBIT"]:
                    raise ValueError("Invalid transaction type")

                if amount <= 0:
                    raise ValueError("Amount must be positive")

                # Write to appropriate file
                if ttype == "CREDIT":
                    credit_writer.writerow(row)
                    balances[acc] = balances.get(acc, 0) + amount
                else:
                    debit_writer.writerow(row)
                    balances[acc] = balances.get(acc, 0) - amount

            except Exception as e:
                row["reason"] = str(e)
                error_writer.writerow(row)

    # Print account-wise balances
    print("\nAccount-wise balances:")
    for acc, bal in sorted(balances.items(), key=lambda x: abs(x[1]), reverse=True):
        print(f"{acc} {bal}")


# ---------------- SAMPLE INPUT FILE ----------------
# Save this as "new_transactions.csv" before running
"""
tid,acc,type,amount,time
T10,A1,CREDIT,1000,2026-09-30T09:00:00
T11,A2,DEBIT,500,2026-09-30T09:30:00
T12,A3,CREDIT,-200,2026-09-30T10:00:00
T13,A1,TRANSFER,300,2026-09-30T10:15:00
T14,A2,DEBIT,abc,2026-09-30T10:30:00
T15,A3,CREDIT,700,2026-09-30T11:00:00
"""

# Run the function
process_transactions("new_transactions.csv")
