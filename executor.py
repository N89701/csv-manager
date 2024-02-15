import csv
import pandas as pd

path = 'contacts.csv'


class Manager():
    """Class manager for working with csv-file"""
    string_attrs: tuple = (  # non-digit attributes of csv
            "last_name",
            "first_name",
            "middle_name",
            "organization",
    )
    digit_attrs: tuple = (  # digit attributes of csv
            "work_phone",
            "personal_phone"
    )

    @classmethod
    def collect_data(cls, number: str) -> dict:
        """
        This function is a utility for 'add' and 'redact' functions.
        It takes an argument number - a number of a next row in csv
        and then creates a dict and put number into it. Further,
        it adds an attributes of csv with a values using input
        and return a dict containing all contact data.
        """
        contact_data: dict = {"number": number}
        for attr in cls.string_attrs:
            contact_data[attr]: str = input(f"Enter contact {attr}: ")
        for attr in cls.digit_attrs:
            value: str = input(f"Enter contact {attr}: ")
            while value != 'None' and not (  # validation for both phones
                value.isdigit() and len(value) in range(11, 16)
            ):
                value = input(
                    f"Enter contact {attr} without '+' and other \
                    symbols, only numbers (11-15 symbols) or 'None': "
                )
            contact_data[attr] = value
        return contact_data  # return dict with all contact data

    @classmethod
    def add_contact(cls) -> None:
        """
        This function defines a number of the next row and then writes a row
        using a dict of data. If file doesn't exist, it will be created.
        """
        try:
            df: pd.DataFrame = pd.read_csv(path)
            number = str(int(df["number"].iloc[-1]) + 1)  # define a number
        except FileNotFoundError:
            with open(path, 'w', newline='', encoding="utf-8") as csvfile:
                filewriter = csv.writer(
                    csvfile, delimiter=',',
                    quotechar='|', quoting=csv.QUOTE_MINIMAL
                )
                filewriter.writerow((  # create a file if it doesn't exist
                    'number',
                    'first_name',
                    'last_name',
                    'middle_name',
                    'organization',
                    'work_phone',
                    'personal_phone'
                ))
            number = "1"
        with open(path, 'a', newline='', encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(cls.collect_data(number).values())  # write a row

    def read_contacts() -> None:
        """
        This function paginate a dataframe and displays a page by page.
        It have an options 'next', 'from_particular_row' and 'previous'.
        """
        rows_per_page: int = 5
        start: int = 0
        df: pd.DataFrame = pd.read_csv(path)
        rows_count: int = len(df)
        while start < rows_count:  # cycle for displaying paginated queryset
            end: int = min(start + rows_per_page, rows_count)
            print(df.loc[start:end-1])
            user_input: str = input(
                "Press 'Enter' for the next page, 'p' to display \
                previous list, number if you want start from  \
                particular row or whatever another key to exit "
            )
            if user_input == '':  # next
                start = end
            elif user_input == 'p':  # previous
                start -= rows_per_page
            elif user_input.isdigit() and int(user_input) < rows_count:
                # from particular row
                start = int(user_input) - 1
            else:  # quit from watching mode
                break

    @classmethod
    def redact_contact(cls) -> None:
        """
        This function filter a rows using an input for the last name,
        first name and second name. Further, if it's the only row with
        this values, user inputs a new data and this row overwrites. If it's
        a few rows, function suggests to pick a number of destinated row.
        Further the same thing with a one row - it is overwrites. If it is
        no any rows with this values, function quits.
        """
        df: pd.DataFrame = pd.read_csv(path)
        selected_row: pd.DataFrame = df[  # filtering using input
            (df['last_name'] == input("Enter the last name: ")) &
            (df['first_name'] == input("Enter the first name: ")) &
            (df['middle_name'] == input("Enter the middle name: "))
        ]
        if len(selected_row) == 1:  # the only row
            row_index: int = selected_row.index[0]
            number: int = row_index + 1
        elif len(selected_row) > 1:  # a few rows
            print("Multiple rows found:")
            print(selected_row)
            selected_list: list = selected_row['number'].tolist()
            number: int = int(input(
                "Enter the number of the row you want to redact: "
            ))
            if number in selected_list:
                row_index: int = number-1
            else:
                print("This number not in queryset")
                return
        else:  # no rows
            print(
                "No row found with the specified first name,\
                last name, and middle name."
            )
            return
        df.loc[row_index] = (cls.collect_data(number))  # rewrite a row
        df.to_csv(path, index=False)
        print("Row redacted successfully.")

    @classmethod
    def search_contact(cls) -> None:
        """
        This function suggests to input from one to three attributes and values
        for then. Further, it searchs a rows with this values and displays.
        """
        attrs: dict = {}
        while len(attrs) < 3:  # input an attribute
            attribute: str = input(
                "Choose from one to three attributes for filtration. To exit \
                press 'q', to start filtration press Enter "
            )
            if attribute in cls.string_attrs or attribute in cls.digit_attrs:
                attrs[attribute]: str = input(  # input a value of attribute
                    "Enter a value for this attribute "
                )
            elif attribute == "q":  # quit condition
                return
            elif attribute == "":  # start of searching with one or two attrs
                if len(attrs) == 0:
                    print('Choose at least 1 argument')
                else:
                    break
            else:
                print("This attribute doesn't exist")
        df: pd.DataFrame = pd.read_csv(path)
        for attr in attrs:
            df = df[(df[attr] == attrs[attr])]  # filtering a df with get data
        if len(df) == 0:
            print("No row found with your attributgetes")
        else:
            print(df)


# Commands for testing the app
Manager().add_contact()
Manager().redact_contact()
Manager().redact_contact()
Manager().redact_contact()
Manager().search_contact()
Manager.read_contacts()  # without a staples becase this method don't require a class
