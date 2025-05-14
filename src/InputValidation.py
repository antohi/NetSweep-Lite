import ipaddress


class InputValidation:

    # Validates IP before continuing process
    @staticmethod
    def validate_ip(ip):
        try:
            ipaddress.ip_address(ip)
            return True
        except ValueError:
            return False

