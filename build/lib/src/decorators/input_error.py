
def input_error(func):
    def wrapper(*args):
        try:
            return func(*args)
        except KeyError:
            return "Contact not found."
        except IndexError:
            return "Data is already set for this contact"
        except TypeError:
            return "Invalid input. Please check your input."
        except ValueError:
            return "Invalid input. Please check your input."

    return wrapper

