import ipaddress


class InputValidation:

    @staticmethod
    def validate_ip(ip):
        try:
            ipaddress.ip_address(ip)
            return True
        except ValueError:
            return False

