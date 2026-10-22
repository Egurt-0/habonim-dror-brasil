import pytest

from apps.glossario.models import Termo
from apps.glossario.services import texto_com_glossario


@pytest.mark.django_db
class TestTextoComGlossario:
    def test_liga_termo_ao_glossario(self):
        html = texto_com_glossario("Todo snif tem madrichim.")
        assert 'href="/glossario/#snif"' in html
        assert 'href="/glossario/#madrich"' in html
        assert 'data-definicao="Núcleo local do movimento em uma cidade."' in html

    def test_so_a_primeira_ocorrencia_e_ligada(self):
        html = texto_com_glossario("O snif e os snifim.")
        assert html.count('class="termo"') == 1

    def test_nao_liga_pedaco_de_palavra(self):
        Termo.objects.create(termo="Ama", slug="ama", definicao="x", variantes="ama")
        assert 'href="/glossario/#ama"' not in texto_com_glossario("Ele amava a tnuá.")

    def test_ignora_maiusculas(self):
        assert 'href="/glossario/#shnat"' in texto_com_glossario("A SHNAT é em Israel.")

    def test_prefere_a_forma_mais_longa(self):
        html = texto_com_glossario("A Shnat Hachshará dura um ano.")
        assert ">Shnat Hachshará</a>" in html

    def test_escapa_html_do_banco(self):
        html = texto_com_glossario('<script>alert("x")</script> snif')
        assert "<script>" not in html
        assert "&lt;script&gt;" in html

    def test_quebra_paragrafos(self):
        html = texto_com_glossario("Primeiro.\n\nSegundo.")
        assert html.count("<p>") == 2

    def test_termo_com_apostrofo_e_reconhecido(self):
        Termo.objects.create(
            termo="Rosh Ha'shaná", slug="rosh", definicao="x", variantes="ha'shaná"
        )
        html = texto_com_glossario("Festa de Ha'shaná.")
        assert 'href="/glossario/#rosh"' in html
        assert "Ha&#x27;shaná</a>" in html

    def test_nao_casa_dentro_de_entidade_html(self):
        Termo.objects.create(termo="Amp", slug="amp", definicao="x", variantes="amp, quot")
        html = texto_com_glossario('Pão & "vinho"')
        assert "&amp;" in html and "&quot;vinho&quot;" in html
        assert 'class="termo"' not in html

    def test_inline_nao_cria_paragrafo(self):
        html = texto_com_glossario("Solelim e snif.", paragrafos=False)
        assert "<p>" not in html
        assert 'href="/glossario/#snif"' in html

    def test_novo_termo_aparece_sem_reiniciar(self):
        texto_com_glossario("aquecer o cache")
        Termo.objects.create(termo="Sicha", slug="sicha", definicao="Conversa.", variantes="sicha")
        assert 'href="/glossario/#sicha"' in texto_com_glossario("Depois da sicha.")
