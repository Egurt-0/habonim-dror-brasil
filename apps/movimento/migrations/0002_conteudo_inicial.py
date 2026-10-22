"""Pilares, referências pedagógicas, tochniot e números, do Material HDBR (outubro de 2026)."""

from django.db import migrations

PILARES = [
    (
        "Judaísmo Cultural Humanista",
        "judaismo",
        "",
        "Uma vivência cultural e uma relação com a tradição judaica centradas na valorização "
        "do ser humano, abertas a diferentes formas de expressão e identificação com o "
        "judaísmo.",
        "O Judaísmo é um dos pilares fundamentais do Habonim Dror e constitui uma dimensão "
        "central de nossa identidade e de nossa prática educativa. Adotamos uma perspectiva de "
        "Judaísmo Cultural Humanista, que valoriza a cultura, a história, as tradições e as "
        "fontes judaicas, tendo o ser humano e os valores humanistas como centro.\n\n"
        "Entendemos o Judaísmo como uma experiência plural, que pode ser vivenciada de "
        "diferentes formas. Valorizamos tanto as tradições e fontes clássicas quanto suas "
        "releituras e ressignificações contemporâneas, buscando construir uma relação pessoal "
        "e coletiva significativa com a cultura judaica.\n\n"
        "Reconhecemos como legítimas diferentes formas de identificação e pertencimento ao "
        "povo e à cultura judaica, respeitando a diversidade existente dentro da comunidade "
        "judaica.",
    ),
    (
        "Sionismo Socialista",
        "sionismo-socialista",
        "",
        "A defesa do direito à autodeterminação do povo judeu no Estado de Israel, associada "
        "à construção de uma sociedade mais justa, igualitária e solidária.",
        "Somos sionistas porque reconhecemos o povo judeu como um povo e defendemos seu "
        "direito à autodeterminação, entendendo o Estado de Israel como expressão desse "
        "direito em um território de profunda relação histórica e espiritual com o povo "
        "judeu.\n\n"
        "Somos sionistas-socialistas porque entendemos que a autodeterminação nacional deve "
        "estar associada à construção de uma sociedade democrática, igualitária, solidária e "
        "socialmente justa.\n\n"
        "Buscamos uma sociedade na qual a cooperação, a igualdade e a responsabilidade "
        "coletiva tenham papel central, com garantia das necessidades básicas e redução das "
        "desigualdades socioeconômicas. Acreditamos que transformações sociais podem ser "
        "construídas democraticamente por meio da organização coletiva, de iniciativas "
        "populares e de experiências comunitárias.\n\n"
        "Nossa relação com Israel é, portanto, também uma relação de responsabilidade. Ser "
        "sionista significa participar criticamente da construção de uma sociedade israelense "
        "mais democrática, igualitária e coerente com nossos valores, reconhecendo suas "
        "contradições e desafios.",
    ),
    (
        "Chalutzianismo",
        "chalutzianismo",
        "ou Pioneirismo",
        "A disposição para agir antes de esperar, assumir responsabilidades e liderar pelo "
        "exemplo na construção de algo melhor.",
        "Ser chalutziano significa transformar valores em prática.\n\n"
        "O Chalutzianismo representa uma postura ativa diante da realidade: identificar aquilo "
        "que precisa ser transformado, assumir responsabilidade e construir alternativas "
        "coletivamente. Não se trata apenas de uma referência histórica aos pioneiros que "
        "participaram da construção do Estado de Israel, mas de uma forma de compreender a "
        "relação entre ideologia e ação.\n\n"
        "Acreditamos que a coerência ideológica não está na reprodução automática de modelos "
        "do passado, mas na capacidade de interpretar o presente, assumir responsabilidades e "
        "criar novas formas de intervenção social.",
    ),
    (
        "Kibutzianismo",
        "kibutzianismo",
        "ou Coletividade",
        "A valorização da vida em comunidade, da cooperação e do trabalho coletivo como "
        "princípios vividos na prática.",
        "Somos kibutzianos porque reconhecemos nos valores que constituíram o movimento "
        "kibutziano uma importante síntese de nossa visão de sociedade: igualdade, liberdade, "
        "cooperação, responsabilidade coletiva, trabalho e vida comunitária, sem abrir mão da "
        "individualidade.\n\n"
        "O kibutz é uma referência histórica e uma experiência concreta de construção "
        "coletiva, mas não é o único modelo possível de realização desses valores. Diante das "
        "transformações pelas quais passaram os kibutzim, entendemos o kibutzianismo como uma "
        "inspiração para diferentes formas de organização da vida.\n\n"
        "Assim, a Hagshamá pode acontecer por meio de diferentes experiências comunitárias, no "
        "campo ou na cidade, em Israel ou na diáspora, desde que estejam comprometidas com a "
        "construção de relações mais cooperativas, igualitárias e socialmente responsáveis.",
    ),
]

REFERENCIAS = [
    (
        "Paulo Freire",
        "A práxis, entendida como ação acompanhada de reflexão, e a educação como ato político "
        "e problematizador.",
    ),
    (
        "Janusz Korczak",
        "O respeito profundo à criança e a construção de uma relação de confiança e "
        "reciprocidade entre educador e educando.",
    ),
    (
        "Jean Piaget e Lev Vygotsky",
        "A compreensão de que a educação deve considerar cada etapa do desenvolvimento e "
        "acontece na relação entre o indivíduo e seu meio.",
    ),
    (
        "Autogestão",
        "A compreensão de que o chanich é sujeito de sua formação, capaz de decidir, "
        "questionar, participar e assumir responsabilidade por suas escolhas.",
    ),
]

TOCHNIOT = [
    ("Solelim Beit", "Introdução à tnuá e construção do pertencimento coletivo."),
    ("Bonim", "Juventude, identidade judaica, introdução ao socialismo e história do povo judeu."),
    ("Mordim", "Chinuch e hadrachá, judaísmo cultural humanista e introdução ao sionismo."),
    ("Maapilim", "Correntes sionistas, sionismo socialista, kibutz e formação do Estado de Israel."),
    ("Magshimim", "Sociedade israelense, caminhos para a paz e preparação para a Shnat."),
]

NUMEROS = [
    # (valor, prefixo, rótulo, aparece na home)
    ("80", "", "anos de história no Brasil", True),
    ("10", "", "snifim ativos, de Manaus a Porto Alegre", True),
    ("400", "Cerca de", "chaverim nas atividades de sábado, toda semana", True),
    ("15", "Mais de", "países na rede internacional", True),
    ("200", "Cerca de", "chaverim, em média, em cada machané central", False),
    ("60", "", "aliot de chaverim nos últimos 10 anos", False),
    ("25", "", "jovens por ano na Shnat, em média, nos últimos 10 anos", False),
]


def criar_conteudo(apps, schema_editor):
    Pilar = apps.get_model("movimento", "Pilar")
    ReferenciaPedagogica = apps.get_model("movimento", "ReferenciaPedagogica")
    Tochnit = apps.get_model("movimento", "Tochnit")
    Numero = apps.get_model("movimento", "Numero")

    for ordem, (nome, slug, subtitulo, resumo, texto) in enumerate(PILARES):
        Pilar.objects.get_or_create(
            slug=slug,
            defaults={
                "nome": nome,
                "subtitulo": subtitulo,
                "resumo": resumo,
                "texto": texto,
                "ordem": ordem,
            },
        )
    if not ReferenciaPedagogica.objects.exists():
        for ordem, (nome, descricao) in enumerate(REFERENCIAS):
            ReferenciaPedagogica.objects.create(nome=nome, descricao=descricao, ordem=ordem)
    if not Tochnit.objects.exists():
        for ordem, (nome, temas) in enumerate(TOCHNIOT):
            Tochnit.objects.create(nome=nome, temas=temas, ordem=ordem)
    if not Numero.objects.exists():
        for ordem, (valor, prefixo, rotulo, destaque) in enumerate(NUMEROS):
            Numero.objects.create(
                valor=valor, prefixo=prefixo, rotulo=rotulo, destaque=destaque, ordem=ordem
            )


class Migration(migrations.Migration):
    dependencies = [("movimento", "0001_initial")]

    operations = [migrations.RunPython(criar_conteudo, migrations.RunPython.noop)]
