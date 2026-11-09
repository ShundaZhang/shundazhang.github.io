"""Attribution and rendering for unmodified Wikimedia Commons diagrams."""

from html import escape
from urllib.parse import quote

CC = 'https://creativecommons.org/'
BY3 = ('CC BY 3.0', CC+'licenses/by/3.0/')
SA3 = ('CC BY-SA 3.0', CC+'licenses/by-sa/3.0/')
SA4 = ('CC BY-SA 4.0', CC+'licenses/by-sa/4.0/')
PD = ('Public domain', CC+'publicdomain/mark/1.0/')
BSD = ('BSD 3-Clause', 'assets/commons/NOTICE.txt')

IMAGES = {
    'cache-direct': ('Direct_Mapped_Cache.svg', 829, 515, 'Ferry24.Milan', SA4),
    'cache-four-way': ('4WaySetAssociativeCache.svg', 719, 585, 'ちぇす', SA3),
    'virtual-physical': ('Virtual_address_space_and_physical_address_space_relationship.svg', 773, 789, 'Dysprosia · SVG by Stannered', BSD),
    'page-tables-five-levels': ('Page_Tables_(5_levels).svg', 794, 631, 'Bellezzasolo', SA4),
    'numa': ('NUMA.svg', 385, 238, 'Moop2000', PD),
    'cpu-gpu': ('Cpu-gpu.svg', 2163, 816, 'NVIDIA · CUDA Programming Guide 3.0', BY3),
    'unified-system-memory': ('HSA-enabled_integrated_graphics.svg', 720, 405, 'ScotXW', SA4),
    'hbm': ('High_Bandwidth_Memory_schematic.svg', 960, 540, 'ScotXW', SA4),
}


def commons_figure(t, key, title, alt, note):
    filename, width, height, author, license_info = IMAGES[key]
    license_name, license_url = license_info
    if license_info == PD:
        license_name = t('Public domain', '公有领域')
    title, alt, note = (escape(t(*value), quote=True) for value in (title, alt, note))
    source = 'https://commons.wikimedia.org/wiki/File:' + quote(filename)
    asset = f'assets/commons/{key}.svg'
    return (
        f'<figure class="wiki-figure" id="figure-{key}"><figcaption><strong>{title}</strong></figcaption>'
        f'<a class="wiki-image" href="{asset}" target="_blank" rel="noopener"'
        f' aria-label="{t("Open original image","打开原图")} · {title}">'
        f'<img src="{asset}" width="{width}" height="{height}" loading="lazy" decoding="async" alt="{alt}"></a>'
        f'<p>{note}</p><small>{escape(author)} · <a href="{source}">Wikimedia Commons</a> · '
        f'<a href="{license_url}">{license_name}</a> · {t("Unmodified SVG","原始 SVG，未经修改")}</small></figure>'
    )
