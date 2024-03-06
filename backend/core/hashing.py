from bcrypt import checkpw, hashpw, gensalt


class Hasher:
    @staticmethod
    def get_password_hash(value: str) -> str:
        return hashpw(value.encode(), gensalt()).decode()

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return checkpw(plain_password.encode(), hashed_password.encode())
