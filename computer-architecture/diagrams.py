"""Small, readable schematics for the cache and memory worked examples."""

from html import escape


def figure(title, body, note):
    return (f'<figure class="schematic"><figcaption>{escape(title)}</figcaption>'
            f'{body}<p>{escape(note)}</p></figure>')


def fields(title, items, note):
    cells = ''.join(
        f'<li><strong>{escape(label)}</strong><code>{escape(value)}</code><span>{escape(detail)}</span></li>'
        for label, value, detail in items
    )
    return figure(title, f'<ol class="bit-fields">{cells}</ol>', note)


def cache_schematics(t):
    bit_split = fields(t('Split physical address 0x1234', '拆开物理地址 0x1234'), [
        (t('Tag','Tag 标记'), '0x0', t('Bits above bit 12 distinguish lines in a set.','第 13 位及以上区分同组的不同行。')),
        (t('Set index','组索引'), '1001000₂ = 72', t('Bits 12–6 select one row.','第 12–6 位选中一组。')),
        (t('Byte offset','行内偏移'), '110100₂ = 52', t('Bits 5–0 select a byte in that line.','第 5–0 位选中该行中的字节。')),
    ], t('32 KiB ÷ (4 ways × 64 bytes) = 128 sets. The drawing follows a simple physically indexed cache.',
         '32 KiB ÷（4 路 × 64 字节）= 128 组。图中使用简单的物理地址索引。'))

    head = ''.join(f'<th scope="col">{t("Way","路位")} {i}</th>' for i in range(4))
    cells = [
        (71, ('tag 0','tag 3','tag 5','—')),
        (72, ('tag 0 ✓','tag 3','tag 6','—')),
        (73, ('tag 0','tag 2','—','—')),
    ]
    rows = ''.join(
        f'<tr{" class=selected-set" if index == 72 else ""}><th scope="row">{index}</th>'
        + ''.join(f'<td{" class=hit-way" if tag.endswith("✓") else ""}>{tag}</td>' for tag in tags)+'</tr>'
        for index, tags in cells
    )
    grid = (f'<table class="cache-grid"><thead><tr><th scope="col">{t("Set","组")}</th>{head}</tr></thead>'
            f'<tbody>{rows}</tbody></table>')
    ways = figure(t('Select set 72, then match tag 0 across its ways','选中第 72 组，再在四路中匹配 tag 0'),
        grid, t('Each populated cell represents a full line plus metadata. Tag 0 in set 71 is irrelevant to this lookup. A dash indicates an invalid slot.',
                '有内容的格子代表一整条缓存行及元数据。第 71 组的 tag 0 不参与本次匹配，横杠表示无效路位。'))
    byte_line = fields(t('Inside the matched 64-byte line','打开命中的 64 字节缓存行'), [
        (t('Earlier bytes','前面的字节'), '0…51', '0x1200…0x1233'),
        (t('Selected byte','选中的字节'), '52', '0x1234'),
        (t('Later bytes','后面的字节'), '53…63', '0x1235…0x123f'),
    ], t('The line starts at 0x1200. Address 0x1238 hits the same line at offset 56. Address 0x3234 selects the same set and offset but has tag 1, so it misses in the snapshot above.',
         '行首地址是 0x1200。0x1238 仍落在同一行，偏移为 56。0x3234 的组索引与偏移相同，但 tag 为 1，在上图中未命中。'))
    return bit_split + ways + byte_line


def sv39_fields(t):
    return fields(t('Decode the canonical Sv39 address 0x40123456','拆解 Sv39 规范地址 0x40123456'), [
        ('VPN[2]', '0x001', t('Bits 38–30 · root index','第 38–30 位 · 根表索引')),
        ('VPN[1]', '0x000', t('Bits 29–21 · middle index','第 29–21 位 · 中间级索引')),
        ('VPN[0]', '0x123', t('Bits 20–12 · lowest index','第 20–12 位 · 最低级索引')),
        (t('Offset','页内偏移'), '0x456', t('Bits 11–0 · unchanged in PA','第 11–0 位 · 在物理地址中保留')),
    ], t('Bits 63–39 copy bit 38. For an ordinary 4 KiB leaf the walker uses all three indices.',
         '第 63–39 位复制第 38 位。普通 4 KiB 叶项会用到三个索引。'))


def address_spaces(t):
    def box(label, value):
        return f'<div><strong>{escape(label)}</strong><code>{escape(value)}</code></div>'

    a = box(t('Process A','进程 A'), 'VA 0x4000')
    b = box(t('Process B','进程 B'), 'VA 0x4000')
    shared = box(t('Shared backing page','共享后备页'), 'PA 0x81001000')
    private = box(t('New private page','新私有页'), 'PA 0x81002000')
    return figure(t('The same virtual address can resolve differently after COW','写时复制后，相同虚拟地址可落在不同物理页'),
        '<div class="address-rows">'
        f'<div class="address-row"><strong>{t("Before a write","写入前")}</strong>{a}<span aria-hidden="true">→</span>{shared}</div>'
        f'<div class="address-row"><strong>{t("Before a write","写入前")}</strong>{b}<span aria-hidden="true">→</span>{shared}</div>'
        f'<div class="address-row changed"><strong>{t("After B writes","B 写入后")}</strong>{b}<span aria-hidden="true">→</span>{private}</div>'
        '</div>', t('A and B have separate page tables. Before the write both refer to the same backing page. After the copy, A keeps its old mapping and B sees its private copy.',
                    'A 与 B 有各自的页表，写入前指向同一后备页。复制后，A 保留旧映射，B 看到自己的副本。'))
