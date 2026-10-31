"""Texto inicial da política de privacidade (/privacidade/), por seção.

RASCUNHO: precisa ser revisado pelo movimento (e de preferência por um advogado) antes de o
site ir para produção. Como as outras migrations de conteúdo, só cria o que não existe.
O bloco `priv_encarregado` nasce vazio: a página mostra "em breve" até alguém preencher.
"""

from django.db import migrations

BLOCOS = {
    "priv_intro": (
        "Política de privacidade",
        "Esta página explica quais dados pessoais o site do Habonim Dror Brasil trata, para "
        "quê, por quanto tempo e como você pode exercer seus direitos, de acordo com a Lei "
        "Geral de Proteção de Dados (Lei nº 13.709/2018, a LGPD).\n\n"
        "O responsável pelo tratamento (controlador) é o Habonim Dror Brasil. Para navegar e "
        "conhecer o movimento você não precisa criar conta nem informar nenhum dado.",
    ),
    "priv_dados": (
        "Quais dados tratamos e por quê",
        "Navegação: o site guarda só os cookies necessários para funcionar (sessão e proteção "
        "de formulários). Não usamos cookies de publicidade, ferramentas de análise de "
        "audiência nem rastreadores de terceiros.\n\n"
        "Conta (opcional): e-mail, nome e senha, guardada de forma criptografada. Servem para "
        "o login e para recursos como o histórico de doações. Base legal: execução do serviço "
        "que você pediu.\n\n"
        "Segurança: quando alguém tenta entrar, registramos o e-mail digitado, o endereço IP e "
        "o navegador, para bloquear tentativas de adivinhar senhas. Base legal: legítimo "
        "interesse em proteger as contas e o site.",
    ),
    "priv_fotos": (
        "Fotos e crianças e adolescentes",
        "Muitos chanichim e madrichim são menores de idade. Fotos de atividades, da galeria "
        "dos snifim e da Bagrut só são publicadas com autorização das pessoas que aparecem "
        "nelas ou, no caso de crianças e adolescentes, de pelo menos um dos pais ou "
        "responsáveis, como exige o artigo 14 da LGPD. Nomes de menores não são publicados "
        "por padrão.\n\n"
        "A autorização pode ser revogada a qualquer momento: basta pedir e a foto é retirada "
        "do site.",
    ),
    "priv_compartilhamento": (
        "Com quem compartilhamos",
        "Não vendemos nem alugamos dados pessoais. Os dados ficam em servidores contratados "
        "para hospedar o site. Quando as doações online estiverem disponíveis, o pagamento "
        "será feito diretamente no site do processador de pagamento: os dados do cartão não "
        "passam pelo nosso servidor.\n\n"
        "Os links para o Instagram dos snifim levam a um serviço de terceiros, que tem sua "
        "própria política de privacidade.",
    ),
    "priv_retencao": (
        "Por quanto tempo guardamos",
        "Os registros de segurança de login são apagados automaticamente depois de 90 dias. "
        "Cadastros nunca confirmados são apagados depois de 7 dias. As sessões expiram "
        "sozinhas. Os dados da conta ficam enquanto a conta existir; se você pedir a "
        "exclusão, eles são apagados, exceto o que a lei obrigar a guardar (por exemplo, "
        "registros de doações para fins fiscais).",
    ),
    "priv_direitos": (
        "Seus direitos",
        "Pela LGPD (artigo 18), você pode pedir a qualquer momento: confirmação de que "
        "tratamos seus dados; acesso a eles; correção de dados incompletos ou errados; "
        "anonimização, bloqueio ou eliminação de dados desnecessários; portabilidade; "
        "informação sobre com quem os compartilhamos; e a revogação de um consentimento, "
        "como a autorização de uma foto.\n\n"
        "Você também pode reclamar à Autoridade Nacional de Proteção de Dados (ANPD).",
    ),
    "priv_encarregado": ("Contato do encarregado (DPO)", ""),
}


def aplicar(apps, schema_editor):
    BlocoTexto = apps.get_model("core", "BlocoTexto")
    for chave, (titulo, texto) in BLOCOS.items():
        BlocoTexto.objects.get_or_create(chave=chave, defaults={"titulo": titulo, "texto": texto})


def desfazer(apps, schema_editor):
    apps.get_model("core", "BlocoTexto").objects.filter(chave__in=BLOCOS).delete()


class Migration(migrations.Migration):
    dependencies = [("core", "0007_idade_calculada")]

    operations = [migrations.RunPython(aplicar, desfazer)]
