import random

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from core.models import Bookmark, Comment, Link, Tag

User = get_user_model()

USERS = [
    ('admin', 'admin@kaydet.link', True),
    ('zeynep', 'zeynep@example.com', False),
    ('emre', 'emre@example.com', False),
    ('elif', 'elif@example.com', False),
    ('burak', 'burak@example.com', False),
    ('ada', 'ada@example.com', False),
    ('cem', 'cem@example.com', False),
]

LINKS = [
    # --- Oyunlar & Eğlence ---
    {
        'url': 'https://zty.pe/',
        'metadata': {'og:title': 'Z Type – A Typing Game', 'og:description': 'Shoot down enemies by typing words. The best typing game on the web.'},
        'tags': ['games', 'typing', 'browser-games'],
        'notes': {
            'zeynep': 'En iyi hızlı yazma oyunu. Her gün 10 dk oynuyorum.',
            'burak': 'İş yerinde herkes bağımlı oldu buna.',
        },
    },
    {
        'url': 'https://princejs.com/',
        'metadata': {'og:title': 'PrinceJS – Prince of Persia in the Browser', 'og:description': 'The legendary Prince of Persia game running in your browser.'},
        'tags': ['games', 'retro', 'browser-games'],
        'notes': {
            'emre': 'Çocukluğumun oyunu. Nostalji.',
            'cem': 'Kontroller orijinale çok sadık kalmış.',
        },
    },
    {
        'url': 'http://adarkroom.doublespeakgames.com/?lang=tr',
        'metadata': {'og:title': 'A Dark Room', 'og:description': 'An incremental text adventure game that starts simple and gets incredibly deep.'},
        'tags': ['games', 'text-adventure', 'browser-games'],
        'notes': {
            'elif': 'Basit başlıyor ama sonra inanılmaz derinleşiyor. Bitirmem 3 gün sürdü.',
        },
    },
    {
        'url': 'https://quickdraw.withgoogle.com/',
        'metadata': {'og:title': 'Quick, Draw!', 'og:description': 'Can a neural network learn to recognize doodling? Help teach it and have fun!'},
        'tags': ['ai', 'games', 'google'],
        'notes': {
            'ada': 'Yapay zeka çizimlerimi tanıyabiliyor mu diye test ettim. Güldüm.',
            'zeynep': 'Çocuklarla birlikte oynamak için harika.',
        },
    },
    {
        'url': 'https://flukeout.github.io/',
        'metadata': {'og:title': 'CSS Diner – A CSS Selector Game', 'og:description': 'A fun game to help you learn and practice CSS selectors.'},
        'tags': ['css', 'learning', 'games'],
        'notes': {
            'burak': 'CSS selector öğrenmek için en iyi yol.',
            'emre': 'Stajyerlere ilk gün bunu veriyorum.',
        },
    },
    {
        'url': 'http://play.elevatorsaga.com/',
        'metadata': {'og:title': 'Elevator Saga – The elevator programming game', 'og:description': 'Write JavaScript to control elevators and transport people efficiently.'},
        'tags': ['javascript', 'games', 'programming'],
        'notes': {
            'cem': 'Asansör algoritması yazmak düşündüğünüzden zor.',
        },
    },
    {
        'url': 'https://vim-adventures.com/',
        'metadata': {'og:title': 'Vim Adventures', 'og:description': 'Learn Vim commands while playing a game.'},
        'tags': ['vim', 'games', 'tools'],
        'notes': {
            'emre': 'Vim öğrenmek için en eğlenceli yol.',
        },
    },
    # --- Yazılım Geliştirme ---
    {
        'url': 'https://craftinginterpreters.com/',
        'metadata': {'og:title': 'Crafting Interpreters', 'og:description': 'A handbook for making programming languages. Free to read online.'},
        'tags': ['programming', 'compilers', 'books'],
        'notes': {
            'emre': 'Kendi betik dilini yazmak isteyenler için mükemmel kaynak.',
            'cem': 'Java ve C bölümleri ayrı ayrı yazılmış. İkisi de çok kaliteli.',
            'ada': 'Bölüm bölüm okudum, her biri kendi başına değerli.',
        },
    },
    {
        'url': 'https://explainshell.com/',
        'metadata': {'og:title': 'explainshell.com – match command-line arguments to their help text', 'og:description': 'Write down a command-line to see the help text that matches each argument.'},
        'tags': ['linux', 'terminal', 'tools'],
        'notes': {
            'burak': 'Karmaşık bash komutlarını anlamak için vazgeçilmez.',
            'zeynep': 'Stack Overflow yerine buna yapıştırıyorum komutu.',
        },
    },
    {
        'url': 'https://ohshitgit.com/tr',
        'metadata': {'og:title': 'Hasktir, Git!?!', 'og:description': 'Git kullanırken bir şeyleri batırdıysanız nasıl düzelteceğinizi bu siteden bulabilirsiniz.'},
        'tags': ['git', 'tools', 'turkce'],
        'notes': {
            'elif': 'Git force push yaptıktan sonra bu siteyi keşfettim. Keşke daha önce bilseydim.',
            'burak': 'Türkçe çevirisi de var, harika.',
        },
    },
    {
        'url': 'https://norvig.com/21-days.html',
        'metadata': {'og:title': 'Teach Yourself Programming in Ten Years', 'og:description': 'Why it takes ten years to learn programming, not 21 days. By Peter Norvig.'},
        'tags': ['programming', 'career', 'essays'],
        'notes': {
            'admin': 'Her yeni başlayan geliştiricinin okuması gereken yazı.',
            'cem': 'Yıllar sonra tekrar okudum, hala geçerli.',
        },
    },
    {
        'url': 'https://gitmoji.dev/',
        'metadata': {'og:title': 'gitmoji', 'og:description': 'An emoji guide for your commit messages.'},
        'tags': ['git', 'tools', 'emoji'],
        'notes': {
            'ada': 'Commit mesajlarına emoji eklemek artık standart olmalı.',
        },
    },
    {
        'url': 'https://devhints.io/',
        'metadata': {'og:title': "Rico's cheatsheets", 'og:description': 'A ridiculous collection of web development cheatsheets.'},
        'tags': ['cheatsheets', 'tools', 'web'],
        'notes': {
            'zeynep': 'Yeni bir teknoloji öğrenirken ilk baktığım yer.',
            'emre': 'Özellikle Bash ve Vim sayfaları çok iyi.',
        },
    },
    {
        'url': 'https://keepachangelog.com/en/1.0.0/',
        'metadata': {'og:title': 'Keep a Changelog', 'og:description': "Don't let your friends dump git logs into changelogs."},
        'tags': ['tools', 'best-practices', 'documentation'],
        'notes': {
            'cem': 'Her açık kaynak projede kullanılmalı.',
        },
    },
    # --- Önyüz & Tasarım ---
    {
        'url': 'https://www.webdesignmuseum.org/',
        'metadata': {'og:title': 'Web Design Museum', 'og:description': 'See how famous websites looked over the years.'},
        'tags': ['web-design', 'history', 'nostalgia'],
        'notes': {
            'elif': 'Google 1998 tasarımı ile bugünkü arasındaki fark inanılmaz.',
            'ada': 'İnternet kültürü müzesi. Saatlerce gezebilirsiniz.',
            'zeynep': 'GeoCities sayfaları beni güldürdü.',
        },
    },
    {
        'url': 'https://250kb.club/',
        'metadata': {'og:title': 'The 250kb Club', 'og:description': 'Web pages that are smaller than 250KB. Because not every page needs megabytes of JavaScript.'},
        'tags': ['web', 'performance', 'minimalism'],
        'notes': {
            'burak': 'E-posta okumak için 8MB JS indirmek yanlış.',
            'cem': 'Benim kişisel sitem 12KB. Gurur duyuyorum.',
        },
    },
    {
        'url': 'https://excalidraw.com/',
        'metadata': {'og:title': 'Excalidraw', 'og:description': 'Virtual whiteboard for sketching hand-drawn like diagrams.'},
        'tags': ['tools', 'design', 'diagrams'],
        'notes': {
            'zeynep': 'Toplantılarda beyaz tahta yerine bunu kullanıyoruz.',
            'emre': 'Figma çok ağır geldiğinde Excalidraw kurtarıyor.',
            'admin': 'Collaborative özelliği çok iyi çalışıyor.',
        },
    },
    {
        'url': 'https://fontjoy.com/',
        'metadata': {'og:title': 'Fontjoy – Font Pairing Made Simple', 'og:description': 'Generate font combinations with deep learning.'},
        'tags': ['typography', 'design', 'ai'],
        'notes': {
            'ada': 'Font seçimi konusunda kararssızlığıma son verdi.',
        },
    },
    {
        'url': 'https://coolors.co/',
        'metadata': {'og:title': 'Coolors – The super fast color palette generator', 'og:description': 'Generate or browse beautiful color combinations for your designs.'},
        'tags': ['colors', 'design', 'tools'],
        'notes': {
            'elif': 'Space tuşuna basarak yeni palet üretmek bağımlılık yapıyor.',
            'burak': 'Her projemde kullanıyorum.',
        },
    },
    {
        'url': 'https://web.dev/patterns/layout/',
        'metadata': {'og:title': 'Layout Patterns', 'og:description': 'A collection of common CSS layout patterns.'},
        'tags': ['css', 'layout', 'web'],
        'notes': {
            'zeynep': 'CSS grid sıkıştığımda mutlaka başvurduğum kaynak.',
        },
    },
    {
        'url': 'https://animista.net/',
        'metadata': {'og:title': 'Animista – CSS Animations on Demand', 'og:description': 'Play with a collection of ready-made CSS animations and generate only what you need.'},
        'tags': ['css', 'animation', 'tools'],
        'notes': {
            'ada': 'CSS animasyonlarını kod yazmadan oluşturmak mümkün.',
            'emre': 'Entrance animasyonları projelerime hayat verdi.',
        },
    },
    # --- Çalışma Düzeni ---
    {
        'url': 'https://musicforprogramming.net/',
        'metadata': {'og:title': 'musicForProgramming();', 'og:description': 'A series of mixes intended for listening while programming.'},
        'tags': ['music', 'productivity', 'focus'],
        'notes': {
            'cem': 'Kod yazarken en iyi arkadaşım.',
            'elif': 'Spotify yerine bunu açıyorum artık.',
            'admin': 'Episode 62 favorim.',
        },
    },
    {
        'url': 'https://obsidian.md/',
        'metadata': {'og:title': 'Obsidian – Sharpen your thinking', 'og:description': 'A powerful knowledge base that works on top of local Markdown files.'},
        'tags': ['notes', 'productivity', 'markdown'],
        'notes': {
            'burak': "Notion'dan geçtim, geri dönmem mümkün değil.",
            'zeynep': 'Zettelkasten metodu ile birlikte kullanınca müthiş.',
        },
    },
    {
        'url': 'https://typora.io/',
        'metadata': {'og:title': 'Typora – A Minimal Markdown Editor', 'og:description': 'A truly minimal markdown editor with live preview.'},
        'tags': ['markdown', 'writing', 'tools'],
        'notes': {
            'ada': "Notion'u bırakmama sebep olan uygulama.",
        },
    },
    # --- İnternet Kültürü ---
    {
        'url': 'https://useplaintext.email/',
        'metadata': {'og:title': 'Use Plaintext Email', 'og:description': 'Why you should use plain text email and how to do it.'},
        'tags': ['email', 'minimalism', 'internet-culture'],
        'notes': {
            'cem': 'HTML email göndermek kabalık. Düz metin yeterli.',
            'emre': 'Tartışmalı ama güzel argümanlar sunuyor.',
        },
    },
    {
        'url': 'https://pxlnv.com/blog/bullshit-web/',
        'metadata': {'og:title': 'The Bullshit Web', 'og:description': 'An honest look at the bloated state of the modern web.'},
        'tags': ['web', 'essays', 'internet-culture'],
        'notes': {
            'burak': 'Bir haber okumak için 14MB indirmek zorunda kalmak anormal.',
            'elif': 'Her web geliştiricisinin okuması gereken manifesto.',
        },
    },
    {
        'url': 'https://muto.ca/posts/web-design-practices-that-don-t-suck.html',
        'metadata': {'og:title': "Web Design Practices That Don't Suck", 'og:description': 'Practical web design principles that actually matter.'},
        'tags': ['web-design', 'best-practices', 'essays'],
        'notes': {
            'admin': 'Bu maddelerin hepsinin altına imzamı atarım.',
        },
    },
    # --- Girişimcilik ---
    {
        'url': 'https://www.failory.com/',
        'metadata': {'og:title': 'Failory – Learn from Failed Startups', 'og:description': 'Stories and lessons from failed startups.'},
        'tags': ['startups', 'business', 'lessons'],
        'notes': {
            'zeynep': 'Başarı hikayelerinden çok başarısızlık hikayeleri öğretiyor.',
            'cem': 'Her girişimcinin ego kontrolü için okuması lazım.',
        },
    },
    {
        'url': 'https://www.first1000.co/',
        'metadata': {'og:title': 'First 1000', 'og:description': 'How startups got their first 1000 users.'},
        'tags': ['startups', 'growth', 'marketing'],
        'notes': {
            'burak': 'Notion ve Figma hikayeleri çok ilginç.',
        },
    },
    {
        'url': 'https://alternativeto.net/',
        'metadata': {'og:title': 'AlternativeTo – Crowdsourced software recommendations', 'og:description': 'Find alternatives to any software, app or service.'},
        'tags': ['tools', 'software', 'alternatives'],
        'notes': {
            'elif': 'Ücretli bir yazılımın bedava alternatifini bulmak için birebir.',
            'admin': 'Yıllardır kullanıyorum, community çok aktif.',
        },
    },
    # --- Grafik & Araçlar ---
    {
        'url': 'https://squoosh.app/',
        'metadata': {'og:title': 'Squoosh', 'og:description': 'Compress and compare images with different codecs, right in your browser.'},
        'tags': ['images', 'performance', 'tools'],
        'notes': {
            'ada': "Google'ın yaptığı en iyi araçlardan biri.",
            'zeynep': 'Web için görsel optimize etmek artık 2 dakika.',
        },
    },
    {
        'url': 'https://tinypng.com/',
        'metadata': {'og:title': 'TinyPNG – Compress PNG and JPEG images', 'og:description': 'Smart lossy compression for your PNG and JPEG images.'},
        'tags': ['images', 'tools', 'optimization'],
        'notes': {
            'emre': 'Deploy öncesi mutlaka buradan geçiriyorum görselleri.',
        },
    },
    {
        'url': 'https://colorleap.app/',
        'metadata': {'og:title': 'Color Leap – Colors Through the Ages', 'og:description': 'Explore color palettes from different historical periods.'},
        'tags': ['colors', 'history', 'design'],
        'notes': {
            'elif': 'Rönesans dönemi renk paletleri gerçekten ilham verici.',
            'ada': 'Art Nouveau paleti ile bir site tasarladım, çok beğenildi.',
        },
    },
    # --- Eğitici & İlginç ---
    {
        'url': 'https://animagraffs.com/',
        'metadata': {'og:title': 'Animagraffs – Animated Infographics', 'og:description': 'How things work, explained with animated infographics.'},
        'tags': ['education', 'infographics', 'science'],
        'notes': {
            'cem': "Dikiş makinesinin nasıl çalıştığını nihayet anladım.",
            'burak': "Michael Jackson moonwalk açıklaması muhteşem.",
        },
    },
    {
        'url': 'https://www.howacarworks.com/',
        'metadata': {'og:title': 'How a Car Works', 'og:description': 'Every part of a car explained in detail with animations.'},
        'tags': ['education', 'cars', 'engineering'],
        'notes': {
            'emre': 'Debriyajdan elektrik aksamına kadar her şey var.',
        },
    },
    {
        'url': 'https://www.lightpollutionmap.info/',
        'metadata': {'og:title': 'Light Pollution Map', 'og:description': 'Interactive map showing light pollution across the world.'},
        'tags': ['maps', 'environment', 'science'],
        'notes': {
            'zeynep': 'Yıldız gözlemi yapacak yer bulmak için kullandım.',
            'elif': "İstanbul'dan neden yıldız göremediğimizi anlatan harita.",
        },
    },
    {
        'url': 'https://iss-sim.spacex.com/',
        'metadata': {'og:title': 'ISS Docking Simulator – SpaceX', 'og:description': 'Try docking with the International Space Station in this browser-based simulator.'},
        'tags': ['space', 'games', 'simulation'],
        'notes': {
            'burak': "SpaceX'in yaptığı simülasyonu denedim. Park etmesi çok zor.",
            'cem': '45 dakikada dock edebildim. Gerçek astronotlara saygım arttı.',
        },
    },
    {
        'url': 'https://onetimesecret.com/',
        'metadata': {'og:title': 'One-Time Secret', 'og:description': 'Share a secret link that only works once.'},
        'tags': ['security', 'privacy', 'tools'],
        'notes': {
            'admin': 'Şifre paylaşmak için Slack yerine bunu kullanıyorum.',
            'emre': 'Self-hosted versiyonu da var.',
        },
    },
    {
        'url': 'https://app.diagrams.net/',
        'metadata': {'og:title': 'diagrams.net', 'og:description': 'Free online diagram software for making flowcharts, UML, and more.'},
        'tags': ['diagrams', 'tools', 'free'],
        'notes': {
            'ada': 'Lucidchart ve Miro yerine bedava alternatif.',
            'zeynep': 'Git entegrasyonu ile diagram versiyonlama mümkün.',
        },
    },
    {
        'url': 'https://astro.build/',
        'metadata': {'og:title': 'Astro – Build faster websites', 'og:description': 'The web framework for content-driven websites. Ship less JavaScript.'},
        'tags': ['web', 'javascript', 'performance'],
        'notes': {
            'cem': "React'i Astro ile sardık. Sayfa hızımız 3x arttı.",
            'burak': 'Static site generator olarak en iyisi bence.',
        },
    },
    {
        'url': 'https://dbdiagram.io/home',
        'metadata': {'og:title': 'dbdiagram.io – Database Diagram Tool', 'og:description': 'A free, simple tool to draw ER diagrams by just writing code.'},
        'tags': ['database', 'tools', 'design'],
        'notes': {
            'admin': 'Her projeye başlamadan önce mutlaka uğradığım yer.',
            'elif': 'Kod yazarak diagram çizmek çok pratik.',
        },
    },
]

COMMENTS = [
    ('https://craftinginterpreters.com/', 'burak', 'Tree-walk interpreter bölümü tek başına bir kurs değerinde.'),
    ('https://craftinginterpreters.com/', 'elif', "Ben Lua bölümünden başladım, sonra Java'ya döndüm. İkisi de çok iyi."),
    ('https://musicforprogramming.net/', 'zeynep', 'Spotify Focus playlist lerinden çok daha iyi. Reklam yok, algoritma yok.'),
    ('https://musicforprogramming.net/', 'burak', 'Arayüzü bile kod yazma hissi veriyor.'),
    ('https://250kb.club/', 'admin', 'kaydet.link da 250kb altında. Gururla katılabiliriz.'),
    ('https://250kb.club/', 'emre', 'Medium bile 4MB. Düşünün artık.'),
    ('https://excalidraw.com/', 'elif', "Figma'ya gerek kalmadan hızlıca wireframe çiziyorum."),
    ('https://excalidraw.com/', 'cem', 'Collaborative modu toplantılarda çok işe yarıyor.'),
    ('https://ohshitgit.com/tr', 'admin', 'git reflog hayat kurtarır. Bu siteden öğrendim.'),
    ('https://ohshitgit.com/tr', 'ada', 'Türkçe çeviri kalitesi çok iyi.'),
    ('https://www.webdesignmuseum.org/', 'emre', "Apple.com'un 1997 versiyonunu görünce şok oldum."),
    ('https://www.webdesignmuseum.org/', 'burak', "Flash'lı siteler dönemi... Ne günlerdi."),
    ('https://obsidian.md/', 'admin', 'Plugin ekosistemi inanılmaz zengin.'),
    ('https://obsidian.md/', 'elif', 'Dataview plugin ile veritabanı gibi kullanabiliyorsunuz.'),
    ('https://pxlnv.com/blog/bullshit-web/', 'cem', "2017'de yazılmış ama her yıl daha geçerli."),
    ('https://pxlnv.com/blog/bullshit-web/', 'zeynep', 'Cookie banner ları da ekleseydi keşke.'),
    ('https://iss-sim.spacex.com/', 'ada', 'Fizik dersinde öğretmen olsam bunu ödev olarak verirdim.'),
    ('https://quickdraw.withgoogle.com/', 'cem', 'Kedimi tanıyamadı ama bisikleti ilk çizgide bildi.'),
    ('https://astro.build/', 'zeynep', 'Blog sitem Astro ile 5 dakikada ayağa kalktı.'),
    ('https://astro.build/', 'elif', "Next.js'den geçtim, pişman değilim."),
    ('https://www.failory.com/', 'admin', "Survivor bias'a karşı en iyi ilaç."),
    ('https://alternativeto.net/', 'emre', "Notion alternatifi ararken AppFlowy'yi burada buldum."),
    ('https://norvig.com/21-days.html', 'elif', 'Her sene bir kere okurum. Her seferinde farklı bir şey öğrenirim.'),
    ('https://animagraffs.com/', 'zeynep', 'Motor çalışma prensibi animasyonu muhteşem.'),
]


class Command(BaseCommand):
    help = 'Seed database with rich sample data from curated link collection'

    def handle(self, *args, **options):
        # Create users
        users = {}
        for username, email, is_admin in USERS:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': email,
                    'is_staff': is_admin,
                    'is_superuser': is_admin,
                },
            )
            if created:
                user.set_password(f'{username}123' if not is_admin else 'admin')
                user.save()
                self.stdout.write(self.style.SUCCESS(f'Created user: {username}'))
            users[username] = user

        # Create tags
        all_tag_names = set()
        for link_data in LINKS:
            all_tag_names.update(link_data.get('tags', []))

        tags = {}
        for name in all_tag_names:
            tag, _ = Tag.objects.get_or_create(
                slug=slugify(name),
                defaults={'name': name},
            )
            tags[name] = tag

        # Create links and bookmarks
        user_list = [u for u in users.values()]
        for link_data in LINKS:
            link, created = Link.objects.get_or_create(
                url=link_data['url'],
                defaults={'metadata': link_data.get('metadata', {})},
            )
            if created:
                self.stdout.write(f'  Link: {link.title}')

            link_tags = [tags[t] for t in link_data.get('tags', [])]

            # Create bookmarks from explicit notes
            notes = link_data.get('notes', {})
            first_bm = None
            for username, note in notes.items():
                user = users.get(username)
                if not user:
                    continue
                bm, bm_created = Bookmark.objects.get_or_create(
                    user=user,
                    link=link,
                    defaults={
                        'note': note,
                        'is_private': False,
                        'parent': first_bm,
                    },
                )
                if bm_created:
                    bm.tags.set(link_tags)
                if first_bm is None:
                    first_bm = bm

            # Random additional saves from other users (no note)
            noted_users = set(notes.keys())
            for user in user_list:
                if user.username in noted_users:
                    continue
                if random.random() < 0.25:  # noqa: S311
                    bm, bm_created = Bookmark.objects.get_or_create(
                        user=user,
                        link=link,
                        defaults={
                            'is_private': False,
                            'parent': first_bm,
                        },
                    )
                    if bm_created:
                        bm.tags.set(link_tags)

        # Create comments
        comment_count = 0
        for url, username, body in COMMENTS:
            user = users.get(username)
            link = Link.objects.filter(url=url).first()
            if not user or not link:
                continue
            _, created = Comment.objects.get_or_create(
                link=link,
                posted_by=user,
                body=body,
            )
            if created:
                comment_count += 1

        # Fetch real OG metadata for all links
        self.stdout.write('\nFetching OG metadata...')
        from core.services.link import LinkService

        for link in Link.objects.all():
            if link.metadata.get('og:image'):
                continue  # already has image, skip
            try:
                result = LinkService.scrape_url(link.url)
                scraped = result.get('metadata', {})
                if scraped:
                    link.metadata = scraped
                    link.save(update_fields=['metadata'])
                    self.stdout.write(f'  OK: {link.title}')
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'  SKIP: {link.url} ({e})'))

        self.stdout.write(self.style.SUCCESS(
            f'\nSeed complete: {Link.objects.count()} links, '
            f'{Bookmark.objects.count()} bookmarks, '
            f'{Comment.objects.count()} comments, '
            f'{Tag.objects.count()} tags'
        ))
