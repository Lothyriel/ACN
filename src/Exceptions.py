class CancelaVarredura(Exception):
    pass


class TokenExpired(CancelaVarredura):
    pass


class Manutencao(CancelaVarredura):
    pass


class ServerError(CancelaVarredura):
    pass
