class Musica:
    def __init__(self, titulo, url, local_file=False):
        self.url = url
        self.titulo = titulo
        self.local_file = local_file
        self.audio = None
