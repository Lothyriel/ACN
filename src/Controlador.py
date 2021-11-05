import json

from datetime import date
path_configs = 'utils\\configs.json'
path_contas = 'utils\\contas.json'
path_coins = 'utils\\coins.json'
path_log = 'Logs\\log-{}.txt'


def save_log(new_log):
    with open(path_log.format(date.today()), 'a+') as f:
        f.write(new_log + "\n")


class Controlador:
    def __init__(self):
        with open(path_contas, "r") as f:
            self.contas = json.load(f)

        with open(path_coins, "r") as f:
            self.coins = json.load(f)

    def save_coins(self):
        with open(path_coins, "w") as cf:
            json.dump(self.coins, cf)

    def save_contas(self):
        with open(path_contas, "w") as cf:
            json.dump(self.contas, cf)

    def cadastrar_planta(self, user, alias, id_planta):
        if len(id_planta) != 24:
            return " Id da planta inválido"

        user_id = str(user.id)
        data = {"user": str(user), "configs": {"regar": "1", "landPobre": "1"}}

        aliases = dict()
        enderecos_alias = list()
        if self.usuario_cadastrado(user_id):
            data = self.contas[user_id]
            aliases = data["aliases"]
            enderecos = aliases.get(alias)
            enderecos_alias = enderecos if enderecos else list()

        if id_planta in enderecos_alias:
            return " Já está Cadastrado!"

        enderecos_alias.append(id_planta)
        aliases[alias] = enderecos_alias
        data["aliases"] = aliases
        self.contas[user_id] = data
        self.save_contas()
        return " Cadastrado!"

    def excluir_planta(self, user_id, alias, id_planta=None):
        conta = self.contas.get(user_id)

        def resultado_exclusao():
            if not conta:
                return "Sem aliases cadastrados"

            if alias == "all":
                self.contas.pop(user_id)
                return "Todas as plantas removidas!"

            aliases = conta["aliases"]
            if not id_planta:
                removido = aliases.pop(alias)
                return "Conta: {} ".format(alias) + "removida" if removido else "não está cadastrada"

            plantas_alias = self.get_plantas_alias(user_id, alias)
            if plantas_alias == "Sem plantas cadastradas":
                return plantas_alias

            if id_planta not in plantas_alias:
                return "Planta {} não está cadastrada".format(id_planta)

            plantas_alias.remove(id_planta)
            if len(plantas_alias) == 0:
                self.excluir_planta(user_id, alias)

            if len(aliases) == 0:
                self.excluir_planta(user_id, alias)
            return "Planta {} foi removida do {}".format(id_planta, alias)

        self.save_contas()
        return resultado_exclusao()

    def get_plantas_alias(self, user_id, alias):
        alias = self.contas.get(user_id).get("aliases").get(alias)
        return alias if alias else "Sem plantas cadastradas nesta conta"

    def usuario_cadastrado(self, user_id):
        return user_id in self.contas.keys()

    def get_conta(self, user):
        return self.contas.get(str(user.id))
