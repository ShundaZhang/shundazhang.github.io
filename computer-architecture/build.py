"""Regenerate the bilingual Computer Architecture Atlas with Python 3."""

from html import escape
from pathlib import Path

from chapters import SOURCES, chapters

ROOT = Path(__file__).parent
NAV = (
    ('index', 'Overview', '总览'),
    ('isa', 'ISA', '指令集'),
    ('cpu', 'CPU', 'CPU 微架构'),
    ('cache', 'Cache', '缓存'),
    ('memory', 'Memory', '内存'),
    ('io', 'I/O', 'I/O'),
    ('parallel', 'Multicore', '多核'),
    ('performance', 'Performance', '性能'),
    ('ai', 'AI Systems', 'AI 体系结构'),
    ('labs', 'Labs', '实验'),
)


def render(lang):
    def t(en, zh):
        return zh if lang == 'zh' else en

    def filename(name, language=lang):
        return f'{name}{".zh" if language == "zh" else ""}.html'

    def title(name):
        return next(t(en, zh) for key, en, zh in NAV if key == name)

    def link(name, label=None, anchor=''):
        return f'<a href="{filename(name)}{anchor}">{escape(label or title(name))}</a>'

    def paragraph(*texts):
        return ''.join(f'<p>{escape(s)}</p>' for s in texts)

    def code(text):
        return f'<pre tabindex="0"><code>{escape(text)}</code></pre>'

    def table(headers, rows, label):
        head = ''.join(f'<th scope="col">{escape(h)}</th>' for h in headers)
        body = ''.join(
            f'<tr><th scope="row">{escape(row[0])}</th>'
            + ''.join(f'<td>{escape(value)}</td>' for value in row[1:]) + '</tr>'
            for row in rows
        )
        return (f'<div class="table-wrap" tabindex="0" role="region" aria-label="{escape(label)}">'
                f'<table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>')

    def flow(label, steps, caption):
        cells = ''.join(f'<li><strong>{escape(head)}</strong><span>{escape(detail)}</span></li>'
                        for head, detail in steps)
        return (f'<figure class="flow"><figcaption>{escape(label)}</figcaption>'
                f'<ol>{cells}</ol><p>{escape(caption)}</p></figure>')

    def references(keys):
        items = ''.join(f'<li><a href="{SOURCES[key][0]}">{escape(t(*SOURCES[key][1:]))} ↗</a></li>'
                        for key in keys)
        return f'<ul class="sources" aria-label="{t("Primary sources","一手资料")}">{items}</ul>'

    def section(ident, label, body):
        return f'<section id="{ident}" class="chapter-section"><h2>{escape(label)}</h2>{body}</section>'

    def shell(name, intro, body, parts=()):
        nav = ''.join(
            f'<a href="{filename(slug)}"'+(' aria-current="page"' if slug == name else '')+f'>{t(en, zh)}</a>'
            for slug, en, zh in NAV
        )
        langs = ''.join(
            f'<a href="{filename(name, choice)}" data-atlas-lang="{choice}"'
            + (' aria-current="page"' if lang == choice else '') + f'>{label}</a>'
            for choice, label in [('en','EN'),('zh','中文')]
        )
        toc = ''.join(f'<a href="#{ident}">{escape(label)}</a>' for ident, label, _ in parts)
        toc = f'<nav class="jumps" aria-label="{t("On this page","本页目录")}">{toc}</nav>' if toc else ''
        name_on_page = t('Computer Architecture','计算机体系结构') if name == 'index' else title(name)
        tag, headline, description = intro
        idx = next(i for i, item in enumerate(NAV) if item[0] == name)
        pager = ''
        if name != 'index':
            prev = link(NAV[idx-1][0], '← '+title(NAV[idx-1][0]))
            next_ = link(NAV[idx+1][0], title(NAV[idx+1][0])+' →') if idx+1 < len(NAV) else ''
            pager = f'<nav class="pager" aria-label="{t("Adjacent chapters","相邻章节")}">{prev}{next_}</nav>'
        scripts = '<script src="labs.js" defer></script>' if name == 'labs' else ''
        hero = (f'<section class="hero"><div class="wrap hero-inner{" hero-home" if name=="index" else ""}">'
                f'<div><span class="eyebrow">{escape(tag)}</span><h1>{escape(headline)}</h1>'
                f'<p>{escape(description)}</p>{toc}'
                +(f'<div class="actions">{link("isa",t("Start with instructions →","从指令开始 →"))}{link("labs",t("Open the labs","打开实验"))}</div>' if name=='index' else '')
                +'</div>'+ (overview_map if name=='index' else '') +'</div></section>')
        return f'''<!doctype html>
<html lang="{t("en","zh-CN")}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#132739">
<meta name="description" content="{escape(description, quote=True)}">
<title>{escape(name_on_page)} · Architecture Atlas</title>
<link rel="icon" href="../favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="style.css">
<script src="../language.js"></script>{scripts}
</head>
<body>
<a class="skip" href="#main">{t("Skip to content","跳至正文")}</a>
<div class="top"><div class="wrap"><a href="../{filename('index')}">← {t("Personal home","个人主页")}</a><nav class="lang" aria-label="{t('Language','语言')}">{langs}</nav></div></div>
<header class="wrap site-header"><a class="brand" href="{filename('index')}"><span aria-hidden="true">μ</span> {t('Architecture Atlas','计算机体系结构')}</a>
<nav class="site-nav" aria-label="{t('Chapters','章节')}">{nav}</nav></header>
<main id="main">{hero}
<div class="wrap reading">{body}{pager}</div></main>
<footer><div class="wrap"><a href="../{filename('index')}">{t("ShundaZhang · Personal home","ShundaZhang · 个人主页")}</a><span>x86-64 / RISC-V</span></div></footer>
</body>
</html>
'''

    overview_map = flow(t('Trace a memory-mapped workload','跟踪一条系统路径'), [
        ('01 / ISA', t('A load names a virtual address','加载指令给出虚拟地址')),
        ('02 / CORE', t('The core translates and issues it','核心翻译地址并发射加载')),
        ('03 / MEMORY', t('Caches and DRAM return data','缓存与 DRAM 返回数据')),
        ('04 / I/O', t('Devices transfer data over a bus','设备通过总线传输数据')),
    ], t('One instruction set can support many core and platform designs.','同一种指令集可以对应多种核心和平台设计。'))
    lessons = chapters(t, paragraph, code, table, flow, link, references)
    cards = []
    for index, (name, info, _) in enumerate(lessons, 1):
        slug = filename(name)
        cards.append(f'<a class="topic" href="{slug}"><span class="eyebrow">{index:02} / {escape(info[0])}</span>'
                     f'<h3>{escape(title(name))}</h3><p>{escape(info[2])}</p><span class="topic-arrow" aria-hidden="true">→</span></a>')
    cards.append(f'<a class="topic" href="{filename("labs")}"><span class="eyebrow">09 / PRACTICE</span><h3>{t("Labs","实验")}</h3><p>{t("Decode an address, exercise a cache, and estimate CPI and KV memory.","拆解地址，试算缓存映射、CPI 和 KV 容量。")}</p><span class="topic-arrow" aria-hidden="true">→</span></a>')
    intro = ('SYSTEMS / FIELD GUIDE', t('Computer Architecture','计算机体系结构'),
             t('Follow instructions, addresses and bytes through a computer. Compare x86-64 and RISC-V at the ISA, core and platform levels.',
               '沿指令、地址与数据理解计算机如何工作，用 x86-64 和 RISC-V 对照指令集、核心与平台三个层次。'))
    body = section('route',t('A route through the course','课程学习路线'),
                   paragraph(t('Start with C, pointers, hexadecimal and basic Boolean logic. Work through chapters 01–05 in order, then study multicore, performance and AI systems. Use the exercises to check whether you can explain an observation before opening a manual.',
                               '先具备 C、指针、十六进制和基本布尔逻辑知识。按顺序读完 01–05 章，再学习多核、性能与 AI 体系结构。遇到观测结果，先用实验检查自己的解释，再查手册。'))
                   + '<div class="topic-grid">'+''.join(cards)+'</div>')
    body += section('reading',t('Courses and manuals','课程与手册'),
                    paragraph(t('Berkeley CS61C pairs lecture notes and labs with RISC-V assembly and datapath design. MIT Computation Structures builds from logic and state to pipelines, caches and virtual memory. The ISA manuals define exact behavior, and Linux driver documentation explains how the OS uses platform interfaces.',
                                'Berkeley CS61C 用讲义与实验串起 RISC-V 汇编和数据通路。MIT Computation Structures 从逻辑与状态讲到流水线、缓存和虚拟内存。ISA 手册用来核对准确语义，Linux 驱动文档则说明操作系统如何使用平台接口。'))
                    + references(('cs61c','mit','intel','rv','linux-dma')))
    (ROOT/filename('index')).write_text(shell('index',intro,body),encoding='utf-8')

    for name, info, parts in lessons:
        content = ''.join(section(ident,label,html) for ident,label,html in parts)
        (ROOT/filename(name)).write_text(shell(name,info,content,parts),encoding='utf-8')

    def lab_input(ident, label, value, kind='text', attrs=''):
        return f'<label for="{ident}">{escape(label)}<input id="{ident}" type="{kind}" value="{value}" {attrs}></label>'

    def lab(ident, fields, explain):
        return (f'<div class="lab"><div class="lab-controls">{fields}</div><output id="{ident}-result" '
                f'class="lab-result" aria-live="polite"></output>{paragraph(explain)}</div>')

    inputs = lab_input('cache-address',t('Address (hexadecimal)','地址（十六进制）'),'0x1234')
    inputs += lab_input('cache-ways',t('Associativity (1, 2, 4 or 8)','相联度（1、2、4 或 8）'),'4','number','min="1" max="8"')
    cache_lab = lab('cache',inputs,t('The model uses a 32 KiB cache with 64-byte lines. The address is a toy physical address with simple indexing. Change the ways while keeping capacity fixed, and observe how the number of sets and the tag change.',
                                    '模型采用 32 KiB、64 字节行的缓存，输入是按简单位索引映射的教学物理地址。保持容量不变，改变路数，观察组数和 tag 如何变化。'))
    memory_lab = lab('sv39',lab_input('sv39-address',t('Virtual address (hexadecimal)','虚拟地址（十六进制）'),'0x40123456'),
                     t('Split a canonical 64-bit Sv39 virtual address into three 9-bit indices and a 12-bit offset. Enter 0x0000004000000000 to see a noncanonical address. A translation also needs page tables and permission checks.',
                       '把规范的 64 位 Sv39 虚拟地址拆成三个 9 位索引和一个 12 位偏移。输入 0x0000004000000000 可观察非规范地址。完成翻译还需要页表和权限检查。'))
    fields = lab_input('cpi-branch',t('Branch instructions (%)','分支指令比例（%）'),'20','number','min="0" max="100"')
    fields += lab_input('cpi-miss',t('Misprediction rate among branches (%)','分支中误预测比例（%）'),'5','number','min="0" max="100"')
    fields += lab_input('cpi-penalty',t('Cycles per misprediction','每次误预测代价（周期）'),'15','number','min="0" max="1000"')
    cpi_lab = lab('cpi',fields,t('The model starts with base CPI 1 and adds branch frequency × misprediction rate × penalty. It assumes the added work does not overlap. Real out-of-order cores require measurement.',
                                '模型从基础 CPI 1 开始，加上分支频率 × 误预测率 × 代价，并假设开销没有重叠。真实乱序核心需要实测。'))
    kv_fields = ''.join(
        lab_input('kv-'+key,t(en,zh),default,'number',f'min="1" max="{maximum}"')
        for key, en, zh, default, maximum in [
            ('layers','Layers','层数','32',512),
            ('heads','KV heads','KV 头数','8',256),
            ('dimension','Head dimension','每头维度','128',1024),
            ('bytes','Bytes per element','每元素字节数','2',8),
            ('tokens','Cached tokens per sequence','每序列缓存 token 数','32768',1048576),
            ('sequences','Active sequences','并发序列数','8',1024),
        ]
    )
    kv_lab = lab('kv',kv_fields,t(
        'This payload assumes equal-length sequences, standard K and V tensors and fixed bytes per element. It excludes model weights, runtime buffers and allocator overhead.',
        '有效载荷假设序列等长、采用标准 K 与 V 张量且每元素字节数固定。权重、运行时缓冲和分配器开销需要另算。'))
    labs = [
        ('cache-mapping',t('Map an address to a cache set','把地址映射到缓存组'),cache_lab),
        ('sv39',t('Split a Sv39 address','拆解 Sv39 地址'),memory_lab),
        ('cpi',t('Budget branch stalls','估算分支带来的停顿'),cpi_lab),
        ('kv-capacity',t('Budget KV cache capacity','估算 KV cache 容量'),kv_lab),
        ('inspect',t('Inspect an actual platform','观察实际平台'),paragraph(t(
            'On Linux, compare lscpu, /proc/cpuinfo, /sys/devices/system/cpu/cpu0/cache/index*/ and /proc/interrupts. For each cache, inspect level, type, coherency_line_size and shared_cpu_list. Tool and field availability depends on the kernel and hardware. In QEMU, inspect the guest ISA and device model. Collect cache latency and PMU measurements on real hardware or a model that explicitly simulates timing.',
            '在 Linux 上对照 lscpu、/proc/cpuinfo、/sys/devices/system/cpu/cpu0/cache/index*/ 与 /proc/interrupts。对每级缓存查看 level、type、coherency_line_size 和 shared_cpu_list。工具与字段可用性取决于内核和硬件。在 QEMU 中观察客体 ISA 与设备模型，缓存延迟和 PMU 测量用实机或明确模拟时序的模型完成。'))
         +references(('qemu','perf','cs61c'))),
    ]
    lab_intro = ('09 / PRACTICE',t('Test the model','动手验证模型'),
                 t('Try four small calculations in the browser, then compare the model with a real platform.',
                   '先在浏览器内做四个小实验，再回到实际平台检验模型的适用范围。'))
    (ROOT/filename('labs')).write_text(shell('labs',lab_intro,''.join(section(*part) for part in labs),labs),encoding='utf-8')


if __name__ == '__main__':
    for language in ('en', 'zh'):
        render(language)
    print('Built 20 bilingual architecture pages')
