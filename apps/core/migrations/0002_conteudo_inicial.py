"""Textos institucionais iniciais, tirados do Material HDBR (outubro de 2026).

Depois de aplicada, o conteúdo passa a ser editado pelo admin. Esta migration só cria blocos
que ainda não existem, então nunca sobrescreve edições.
"""

from django.db import migrations

BLOCOS = {
    "home_hero": (
        "Habonim Dror Brasil",
        "Uma rede nacional de educação judaica não formal, com 80 anos de história no Brasil.",
    ),
    "arg_capilaridade": (
        "Capilaridade nacional",
        "Não é uma tnuá local: é uma rede que conecta o Brasil inteiro, com 10 snifim de "
        "Manaus a Porto Alegre.",
    ),
    "arg_alcance": (
        "Alcance",
        "Chega a crianças que não têm escola judaica ou outras oportunidades de educação "
        "judaica.",
    ),
    "arg_impacto": (
        "Impacto comunitário",
        "Forma as lideranças que sustentam as pequenas comunidades e cria uma comunidade "
        "judaica nacional, e não apenas local.",
    ),
    "slogan": (
        "80 anos formando líderes, construindo comunidade e conectando gerações.",
        "",
    ),
    # Bases
    "quem_somos": (
        "Quem somos",
        "O Habonim Dror é um movimento juvenil judaico sionista socialista, chalutziano e "
        "kibutziano. Presente no Brasil desde 1945, é hoje a maior tnuá (movimento juvenil "
        "judaico) do país, com presença em 10 cidades e conexão com uma rede global presente "
        "em mais de 15 países.\n\n"
        "Nossa proposta é simples de enunciar e exigente de sustentar: formar líderes por meio "
        "da educação não formal, do exemplo pessoal e da vivência coletiva, de jovens para "
        "jovens.\n\n"
        "Isso significa que nossos educadores são os próprios madrichim. São bogrim que "
        "passaram pelo processo de formação da tnuá e escolheram assumir a responsabilidade de "
        "transmiti-lo à geração seguinte. É essa cadeia de formação, em que cada geração educa "
        "e prepara a próxima, que sustenta o movimento há oito décadas.",
    ),
    "pilares_intro": (
        "Ideologias: os quatro pilares",
        "Esses quatro pilares não são apenas conceitos apresentados aos nossos chaverim. Eles "
        "orientam a forma como o Habonim Dror pensa sua educação e são considerados na "
        "construção de cada peulá, machané e projeto da tnuá.",
    ),
    "ideologia_em_movimento": (
        "Uma ideologia em movimento",
        "O Habonim Dror entende sua ideologia como um horizonte de transformação. O Takanon "
        "explicita não apenas aquilo que somos hoje, mas também aquilo que buscamos construir. "
        "Por isso, nossa relação com a ideologia deve ser simultaneamente comprometida e "
        "crítica.\n\n"
        "Ser Dror significa conhecer nossa história e nossos princípios, questioná-los, "
        "atualizá-los diante da realidade e buscar formas concretas de colocá-los em prática."
        "\n\n"
        "Nossa ideologia é, portanto, um convite à construção: de uma vida judaica "
        "significativa, de uma sociedade mais justa, de uma relação responsável com Israel e "
        "com a diáspora e de comunidades baseadas na cooperação, na democracia, na igualdade "
        "e na responsabilidade coletiva.",
    ),
    "historia": (
        "História",
        "O Habonim Dror chegou ao Brasil em 1945 e, desde então, acompanhou diferentes "
        "momentos da formação e consolidação das comunidades judaicas do país. Os snifim, "
        "núcleos locais da tnuá, foram surgindo ao longo das décadas.\n\n"
        "Oitenta anos depois, a lógica que sustenta o movimento permanece a mesma: jovens que "
        "crescem na tnuá assumem responsabilidades, tornam-se madrichim e participam da "
        "formação da geração seguinte.",
    ),
    "tora_educativa": (
        "Torá Educativa",
        "A Torá Educativa é o documento que organiza nossa concepção pedagógica. Ela é "
        "revisada a cada dois anos, durante a veidá, e construída a partir do diálogo entre "
        "referências da educação e a experiência concreta dos próprios chaverim da tnuá.",
    ),
    "tora_educativa_objetivo": (
        "",
        "O objetivo não é formar jovens que simplesmente acumulem conteúdos. Buscamos formar "
        "pessoas críticas, com identidade judaica construída de maneira consciente e capazes "
        "de assumir responsabilidades e liderar pelo exemplo.",
    ),
    "dror_hoje": (
        "Dror no Brasil hoje",
        "O Habonim Dror não é uma iniciativa local que foi replicada em diferentes cidades. É "
        "uma rede construída para conectar diferentes comunidades. Um chanich de Fortaleza e "
        "um chanich de Porto Alegre percorrem uma mesma jornada educacional, encontram-se nas "
        "mesmas machanot centrais e fazem parte de uma mesma geração de liderança judaica "
        "nacional.",
    ),
    "rede_internacional": (
        "Rede internacional",
        "Presença em mais de 15 países, incluindo África do Sul, Alemanha, Argentina, "
        "Austrália, Bélgica, Brasil, Canadá, Estados Unidos, França, Holanda, Inglaterra, "
        "México, Nova Zelândia e Uruguai.",
    ),
    "parceiros": (
        "Parceiros: kehilot e CCHDs",
        "O Habonim Dror atua em parceria com as comunidades judaicas de cada cidade. Cada snif "
        "mantém uma relação direta com sua kehilá de referência.\n\n"
        "Essa relação é fundamental para o trabalho da tnuá. O Habonim Dror não forma jovens "
        "líderes de maneira isolada. Forma pessoas que participam da vida comunitária e que, "
        "ao longo do tempo, podem assumir responsabilidades e contribuir para a continuidade "
        "dessas próprias kehilot.",
    ),
    "cchds_parceiros": (
        "Casas de Cultura Habonim Dror",
        "No Rio de Janeiro, em São Paulo e em Porto Alegre, essa relação também se concretiza "
        "por meio das Casas de Cultura Habonim Dror, as CCHDs. Esses espaços funcionam como "
        "pontos de encontro entre a tnuá e a comunidade local e fortalecem a presença "
        "permanente do movimento em cada cidade.",
    ),
    # Shichavot Tzeirot
    "st_intro": (
        "As kvutzot mais jovens",
        "As Shichavot Tzeirot reúnem os chanichim mais novos da tnuá, de Chalutzim até "
        "Solelim Beit, em um processo educacional organizado por faixa etária. Cada snif "
        "possui autonomia para adaptar temas e atividades às características e necessidades "
        "de sua comunidade local.",
    ),
    "st_sabados": (
        "Sábados de atividade",
        "Todos os sábados, os snifim do Habonim Dror abrem suas portas para as peulot, criando "
        "um espaço contínuo de convivência, educação e pertencimento.\n\n"
        "Para muitas crianças e adolescentes em diferentes regiões do país, esse é o principal "
        "ou único espaço de educação judaica não formal ao qual têm acesso. É uma experiência "
        "que acontece fora do currículo de uma escola judaica e sem depender de mensalidade ou "
        "matrícula formal.\n\n"
        "Em média, 400 chaverim participam semanalmente dessas atividades em todo o Brasil.",
    ),
    "st_machanot_locais": (
        "Machanot locais",
        "Os acampamentos organizados por cada snif aprofundam, de maneira vivencial e "
        "intensiva, os processos trabalhados ao longo do ano.\n\n"
        "Além de ampliar as experiências educativas, as machanot fortalecem o vínculo entre o "
        "chanich, sua kvutzá e sua comunidade local. Para muitos jovens, também representam a "
        "primeira experiência de convivência coletiva prolongada fora de casa.",
    ),
    # Shichavot Bogrot
    "sb_intro": (
        "A liderança em formação",
        "A partir do 9º ano, o chaver começa a assumir responsabilidades diretas pela educação "
        "da geração seguinte. É nesse momento que uma das características mais importantes do "
        "Habonim Dror se torna especialmente evidente: formamos nossos próprios educadores.\n\n"
        "O jovem que foi educado pela tnuá passa progressivamente a participar de sua "
        "construção, assumindo tafkidim, planejando atividades, acompanhando chanichim e "
        "desenvolvendo sua própria capacidade de liderança.",
    ),
    "sb_hagshem": (
        "Projeto Hagshem",
        "O Hagshem é o projeto nacional que organiza e atualiza o processo educacional da tnuá "
        "a partir de Solelim Beit. Ele estrutura uma jornada progressiva, que começa com a "
        "construção do pertencimento nas Shichavot Tzeirot, avança para a formação em "
        "liderança e hadrachá nas Shichavot Bogrot, passa pela Shnat e culmina na Bagrut.\n\n"
        "Na Bagrut, o boguer atua como madrich e participa diretamente da gestão e da "
        "construção do snif.",
    ),
    "sb_tochniot": (
        "Temas das tochniot",
        "As tochniot, programações educacionais da tnuá, acompanham as diferentes etapas "
        "dessa jornada:",
    ),
    "sb_tochniot_fecho": (
        "",
        "Cada etapa prepara a seguinte. Um chanich que ingressa aos 13 anos constrói, ao longo "
        "dos anos, um repertório histórico, educacional, ideológico e crítico que servirá de "
        "base para sua experiência na Shnat e para sua atuação posterior na tnuá.",
    ),
    "sb_machanot_centrais": (
        "Machanot centrais",
        "Diferentemente das machanot locais, as machanot centrais reúnem chaverim de "
        "diferentes snifim em uma mesma experiência nacional.\n\n"
        "É nesses encontros que a dimensão nacional da tnuá se torna concreta. Um chanich do "
        "Recife acampa ao lado de um chanich de Porto Alegre, compartilha tzevet, participa "
        "das mesmas peulot e constrói vínculos com jovens de outras partes do país.\n\n"
        "As machanot centrais são, portanto, um dos principais espaços de encontro e "
        "construção de uma identidade nacional comum dentro do movimento.",
    ),
    "sb_shnat": (
        "Shnat Hachshará",
        "A Shnat é um ano de formação intensiva em Israel que dá continuidade ao processo "
        "educativo desenvolvido ao longo da trajetória na tnuá.\n\n"
        "A experiência aprofunda questões de identidade judaica e sionista, amplia a autonomia "
        "e a responsabilidade individual e coletiva e proporciona contato direto com "
        "diferentes dimensões da sociedade israelense.\n\n"
        "A Shnat também representa um importante momento de preparação para a continuidade da "
        "atuação dos jovens no Habonim Dror e para a construção de sua trajetória como "
        "líderes.\n\n"
        "Nos últimos 10 anos, a média anual de participantes da Kvutzá Shnat foi de 25 jovens.",
    ),
    # Kehilá HD
    "kh_lideranca": (
        "Formação de liderança",
        "O resultado de oito décadas de trabalho educativo não está apenas nas memórias "
        "construídas durante a infância e a juventude. Está também nas pessoas que, depois de "
        "passar pela tnuá, continuam contribuindo para suas comunidades.\n\n"
        "Ao longo de sua história, o Habonim Dror formou pessoas que hoje ocupam posições de "
        "liderança em federações, sociedades e diferentes organizações judaicas em todo o "
        "Brasil.",
    ),
    "kh_cchds": (
        "CCHDs: Casas de Cultura Habonim Dror",
        "Nos snifim do Rio de Janeiro, São Paulo e Porto Alegre, o Habonim Dror mantém espaços "
        "próprios, as Casas de Cultura Habonim Dror.\n\n"
        "Mais do que sedes administrativas, as CCHDs representam a presença permanente da tnuá "
        "na cidade. São espaços de encontro, convivência e realização de atividades que "
        "aproximam o movimento da comunidade judaica local.\n\n"
        "Também representam a continuidade de um projeto construído por diferentes gerações "
        "de chaverim e pela relação histórica entre a tnuá e as comunidades de cada cidade.",
    ),
    "kh_importancia": (
        "A importância do movimento juvenil",
        "Em cidades onde não há escola judaica, ou onde a escola existente não alcança todas "
        "as famílias, o movimento juvenil é muitas vezes uma das principais portas de entrada "
        "de uma criança para a vida comunitária judaica.\n\n"
        "Diferentemente de uma escola, a participação na tnuá não depende de mensalidade ou de "
        "matrícula formal. Depende de um sábado disponível, de um espaço de acolhimento e da "
        "possibilidade de construir vínculos.\n\n"
        "Por isso, o Habonim Dror não disputa espaço com as estruturas comunitárias. Ele "
        "amplia esse espaço. Cria comunidade onde ela ainda não existe e fortalece os vínculos "
        "onde ela já existe.\n\n"
        "Ao mesmo tempo em que constrói comunidades judaicas locais, o movimento conecta "
        "crianças, jovens e famílias de diferentes cidades em uma comunidade judaica nacional. "
        "Essa conexão acontece por meio das mesmas machanot, da mesma Torá Educativa, de uma "
        "trajetória educacional compartilhada e de valores comuns.\n\n"
        "É assim que uma atividade de sábado em um snif local se conecta a uma rede nacional e "
        "internacional e se transforma em parte de uma experiência judaica coletiva muito "
        "maior.",
    ),
    "kh_contribua": (
        "Contribua",
        "Sustentar essa rede de dez snifim, uma Shnat anual, machanot centrais e processos "
        "contínuos de formação de madrichim exige investimento permanente.\n\n"
        "As contribuições ajudam a garantir a continuidade das atividades e a ampliar o acesso "
        "dos jovens às experiências da tnuá, especialmente por meio de bolsas de participação. "
        "O objetivo é que nenhum jovem deixe de participar de uma machané ou da Shnat "
        "exclusivamente por uma questão financeira.",
    ),
    # Pendente: texto do Censo. Bloco vazio não aparece no site.
    "kh_censo": ("Censo", ""),
    "kh_vinho": (
        "Vinho Guefen",
        "A venda de vinho é uma das principais formas de arrecadação dos snifim do Habonim "
        "Dror em diferentes cidades do Brasil.\n\n"
        "O Vinho Guefen é Kasher Le Pessach e adequado para Kidush. Além de contribuir para a "
        "sustentabilidade financeira dos snifim, a iniciativa se tornou uma tradição que "
        "aproxima a comunidade do calendário judaico e fortalece o vínculo entre a kehilá e o "
        "movimento.\n\n"
        "Para encomendar, fale com o snif da sua cidade.",
    ),
    # Quero saber mais / glossário
    "saber_mais_intro": (
        "Quero saber mais",
        "Cada snif possui sua própria conta no Instagram. É uma das melhores formas de "
        "conhecer o cotidiano da tnuá em cada cidade e entrar em contato diretamente com o "
        "movimento local.",
    ),
    # Pendente: @ da conta nacional e link do site oficial. Bloco vazio não aparece.
    "conta_nacional": ("Habonim Dror Brasil", ""),
    "glossario_intro": (
        "Glossário",
        "O dia a dia da tnuá usa muitas palavras em hebraico. Aqui está o que cada uma "
        "significa. Ao longo do site, essas palavras aparecem sublinhadas: passe o mouse ou "
        "toque nelas para ver a definição.",
    ),
}


def criar_blocos(apps, schema_editor):
    BlocoTexto = apps.get_model("core", "BlocoTexto")
    for chave, (titulo, texto) in BLOCOS.items():
        BlocoTexto.objects.get_or_create(chave=chave, defaults={"titulo": titulo, "texto": texto})


class Migration(migrations.Migration):
    dependencies = [("core", "0001_initial")]

    operations = [migrations.RunPython(criar_blocos, migrations.RunPython.noop)]
