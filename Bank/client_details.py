import random as r
import secrets
import hashlib
import json
import os


class Client:
    """
    A class to represent a bank client

    Attributes
    ----------
        - name: str
        - surname: str
        - email: str
        - password: str
        - account_number: int

    Methods
    -------
        - hash_pass
        - verify_pass
        - get_pass
        - get_email
        - save_user
        - save_to_file
        - find_user
    """
    
    def __init__(self, name, surname, email, password, account_number=None):
        """
        Constructs all the necessary attributes for the client object.

        Parameters
        ----------
        name: str
            The name of the client.
        surname: str
            The last name of the client.
        email: str
            The email address of the client.
        """
        self.name = name
        self.surname = surname
        self.__email = email
        self.__password = password
        self.account_number = account_number if account_number is not None else 1620000 + r.randint(10000, 99999)
    

    @staticmethod
    def hash_pass(password):
        """
        Parameter
        ---------
        password: str
            user's password to be hashed
        Returns a hashed password and salt. """

        salt = secrets.token_hex(16)
        encoded_password = password.encode('utf-8')
        encoded_salt = salt.encode('utf-8')
        hash_object = hashlib.sha256(encoded_password + encoded_salt)
        hashed_pass = hash_object.hexdigest()

        return salt, hashed_pass


    @staticmethod
    def verify_pass(password, salt):
        """
        Parameters
        ----------
        password: str
            user's password 
        salt: str
            random salt for hashing

        Returns a hashed password
        """
        encoded_password = password.encode('utf-8')
        encoded_salt = salt.encode('utf-8')
        hash_object = hashlib.sha256(encoded_password + encoded_salt)
        hashed_pass = hash_object.hexdigest()

        return hashed_pass


    # getter for the password and email
    def get_email(self):
        """ Returns the email of the client. """
        return self.__email
    

    def get_pass(self):
        """ Returns the password of the client. """
        password = self.hash_pass(self.__password)
        return password


    # method for displaying
    def __str__(self):
        """ Returns readable client data. """
        return (
                f'Name: {self.name}\n'
                f'Surname: {self.surname}\n'
                f'Email: {self.get_email()}\n'
                f'Account Number: {self.account_number}'
                )
    

    def save_user(self):
        """ Saves confidencial user info to json. """

        filename = 'user.json'
        users = [{self.get_email():[self.account_number, self.get_pass()]}]
        file_exists = os.path.exists(filename)

        if file_exists:
            user = {self.get_email():[self.account_number, self.get_pass()]}
            try:
                with open(filename, 'r') as file:
                    content = file.read()
                    existing_users = json.loads(content)
                    existing_users.append(user)

                with open(filename, 'w') as file:
                    file.write(json.dumps(existing_users))

            except FileNotFoundError:
                print(f"the file {filename} was not found")
        else:
            try:
                with open(filename, 'a+') as file:
                    save_data = json.dumps(users)
                    file.write(save_data)
            except FileNotFoundError:
                print(f"the file {filename} was not found")
    

    def save_to_file(self):
        """ Keeps track of current clients. """

        filename = "user_list.txt"
        try:
            with open(filename, "a") as file:
                file.write(self.__str__() + ("\n" + "_" * 30) + '\n')
        except Exception as e:
            print(f'An error has occurred while saving file: {e}')
    

    @staticmethod
    def find_user(email):
        """
        Parameter
        ---------
        email: str
            user's email to search for
        
        Returns user info or None
        """

        filename = 'user.json'
        try:
            with open(filename, "r") as file:
                for line in file:
                    users = json.loads(line)

        except FileNotFoundError:
            print(f'The file {filename} does not exist.')
            return None
        
        except Exception as e:
            print(f'An error occurred while reading from file: {e}')
            return None
        
        for user in users:
            if email in user:
                return user
        print("Error: User not found")
        return None


