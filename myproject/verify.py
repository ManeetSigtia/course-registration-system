import re
import datetime


class Validation:
    # function to validate format and authenticity of input dates
    def validate_date(self, year, month, day):
        self.boolean_date_verifier = True
        try:
            # checking if the date entered is valid i.e. if its a real date (e.g. 31/02/2021 is invalid)
            datetime.datetime(year, month, day)
        except ValueError:
            self.boolean_date_verifier = False

    # function to validate day of week based on date
    def validate_date_of_week(self, weekday, year, month, day):
        self.boolean_day_of_week_verifier = True
        # determining the index of the weekday based on the date entered
        self.predicted_day = datetime.date(year=year, month=month, day=day).weekday()
        self.days_array = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        # checking if the day of the week given matches with the predicted day
        if not weekday == self.days_array[self.predicted_day]:
            self.boolean_day_of_week_verifier = False

    # function to validate input from sessions field
    def validate_sessions(self, sessions):
        self.boolean_sessions_verifier = True
        self.sessions = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        for character in sessions:
            self.function_value = self.validate_character(self.sessions, 0, len(self.sessions) - 1, character)
            if not self.function_value:
                self.boolean_fees_verifier = False

    # function to validate input from fees field
    def validate_fees(self, fees):
        self.boolean_fees_verifier = True
        try:
            float(fees)
        except ValueError:
            self.boolean_fees_verifier = False
        return self.boolean_fees_verifier

    # function to validate input from phone number field
    def validate_phone(self, phone):
        # boolean to check whether the string passed is valid
        self.boolean_numbers_verifier = True
        # array containing all valid characters for 'phone' string
        self.phone_numbers = ['+', '-', '(', ')', ',', '.', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        # looping through each character in passed string
        for character in phone:
            # using binary search to determine if each character is present in the array
            self.function_value = self.validate_character(self.phone_numbers, 0, len(self.phone_numbers) - 1, character)
            if not self.function_value:
                # value has not been found
                self.boolean_numbers_verifier = False

    # function to validate input from email field
    def validate_email(self, email):
        self.boolean_emails_verifier = True
        # All email addresses should include:
        # 1 to 20 characters and/or uppercase letters, numbers, _ and - (1)
        # An @ symbol (2)
        # 2 to 20 lowercase and uppercase letters and numbers (3)
        # An . character (4)
        # 2 to 3 lowercase and uppercase letters (5)

        # 1. we need to use \w to validate the (1). \w includes characters, numbers, and underscore.
        # we need to add the - character to the pattern too. so the pattern for (1) should be [\w-]{1,20)
        # 2. we add @ symbol into the pattern for (2)
        # 3. we add \w{2,20} into the pattern for (3)
        # 4. we add \. into the pattern for (4)
        # 5. we add \w{2,3}$ into the pattern for (5). The $ says that after (5), there is no more character.

        if not re.match(r'[\w.-]{1,20}@[\w.]{2,20}\.\w{2,3}$', email):
            self.boolean_emails_verifier = False

    # function that performs classic binary search on sorted array
    def validate_character(self, array, low, high, character):
        # array is the sorted array of elements, character is the value to be found
        # initially, low is index position 0 and high is number of array elements - 1
        if high >= low:
            mid = (high + low) // 2  # mid is the average of high and low indices

            if array[mid] == character:
                return True  # The value has been found

            elif array[mid] > character:
                # recursively repeat binary search on the left side of the element
                return self.validate_character(array, low, mid - 1, character)

            else:
                # recursively repeat binary search on the ride side of the middle element
                return self.validate_character(array, mid + 1, high, character)
        else:
            return False  # value not found
