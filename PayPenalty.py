def pay_penalty(cursor, connection, email):
    cursor.execute('''
                    SELECT pid, amount, IFNULL(paid_amount, 0) as paid_amount
                    FROM penalties, borrowings
                    WHERE penalties.bid = borrowings.bid
                    AND borrowings.member LIKE :email
                    AND penalties.amount > IFNULL(penalties.paid_amount, 0)
                    ''', {"email": email})
    penalties = cursor.fetchall()

    print("\nUnpaid penalties:")
    for penalty in penalties:
        print(f"Penalty ID: {penalty['pid']}, Amount: {penalty['amount']}, Paid amount: {penalty['paid_amount']}")

    user_input = ""
    while penalties and user_input.lower() != "no":
        user_input = input("Would you like to pay for a penalty? ")
        if user_input.lower() == "yes":
            try:
                paid_pid = int(input("Enter pid to pay: "))
                cursor.execute('''
                            SELECT amount, IFNULL(paid_amount, 0) as paid_amount
                            FROM penalties, borrowings
                            WHERE penalties.pid = :paid_pid
                            AND penalties.bid = borrowings.bid
                            AND borrowings.member LIKE email;
                            ''', {"paid_pid": paid_pid, "email": email})
                penalty_amounts = cursor.fetchone()

                if penalty_amounts:
                    if penalty_amounts['paid_amount'] >= penalty_amounts['amount']:
                        print("You have already paid for this penalty")
                    else:
                        print("Penalty amount:", penalty_amounts[0]);
                        user_amount = int(input("Enter amount to pay: "))

                        if user_amount + penalty_amounts['paid_amount'] > penalty_amounts['amount']:
                            print("Penalty fully paid")
                        else:
                            print("Penalty partially paid")
                            
                        cursor.execute('''
                                        UPDATE penalties
                                        SET paid_amount = paid_amount + :user_amount
                                        WHERE penalties.pid = :paid_pid;
                                        ''', {"user_amount": user_amount, "paid_pid": paid_pid})
                        connection.commit()
                else:
                    print("Invalid pid")

            except Exception as e:
                print("Invalid input")
        elif user_input.lower() != "no":
            print("Invalid command")
        cursor.execute('''
                    SELECT pid, amount, IFNULL(paid_amount, 0) as paid_amount
                    FROM penalties, borrowings
                    WHERE penalties.bid = borrowings.bid
                    AND borrowings.member LIKE email
                    AND penalties.amount > IFNULL(penalties.paid_amount, 0)
                    ''', {"email": email})
        penalties = cursor.fetchall()
        print("\nUnpaid penalties:")
        for penalty in penalties:
            print(f"Penalty ID: {penalty['pid']}, Amount: {penalty['amount']}, Paid amount: {penalty['paid_amount']}")

    if not penalties:
        print("You have no penalties")

    print("")

    return
