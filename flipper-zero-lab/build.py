"""Build a bilingual Flipper Zero hardware-hacking field guide. Python stdlib only."""
from pathlib import Path
from html import escape as e
import json
from hashlib import sha256
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
SOURCES = {
'docs': ('Flipper official documentation', 'https://docs.flipper.net/zero'),
'spec': ('Flipper hardware specifications', 'https://docs.flipper.net/zero/development/hardware/tech-specs'),
'update': ('Official firmware update', 'https://docs.flipper.net/zero/basics/firmware-update'),
'recovery': ('Official DFU recovery', 'https://docs.flipper.net/zero/basics/firmware-update/firmware-recovery'),
'fw': ('Official firmware source', 'https://github.com/flipperdevices/flipperzero-firmware'),
'fbt': ('Official fbt build targets', 'https://github.com/flipperdevices/flipperzero-firmware/blob/dev/documentation/fbt.md'),
'rf': ('Official Sub-GHz overview', 'https://docs.flipper.net/zero/sub-ghz'),
'freq': ('Supported RF bands and regional TX limits', 'https://docs.flipper.net/zero/sub-ghz/frequencies'),
'read': ('Read and emulate radio signals', 'https://docs.flipper.net/zero/sub-ghz/read'),
'raw': ('Read RAW and RSSI threshold', 'https://docs.flipper.net/zero/sub-ghz/read-raw'),
'nice': ('Supported vendors · Nice FLO / FLOR-S', 'https://docs.flipper.net/zero/sub-ghz/supported-vendors'),
'add': ('Add and enroll a new remote', 'https://docs.flipper.net/zero/sub-ghz/add-new-remote'),
'format': ('Official Sub-GHz file formats', 'https://github.com/flipperdevices/flipperzero-firmware/blob/dev/documentation/file_formats/SubGhzFileFormats.md'),
'nfc': ('Official NFC overview', 'https://docs.flipper.net/zero/nfc'),
'nfcread': ('Read NFC cards', 'https://docs.flipper.net/zero/nfc/read'),
'magic': ('Supported magic cards and writing', 'https://docs.flipper.net/zero/nfc/magic-cards'),
'mfkey': ('MIFARE Classic key recovery', 'https://docs.flipper.net/zero/nfc/mfkey32'),
'nxp': ('NXP MIFARE Classic EV1 1K datasheet', 'https://www.nxp.com/docs/en/data-sheet/MF1S50YYX_V1.pdf'),
'lf': ('Official 125 kHz RFID', 'https://docs.flipper.net/zero/rfid'),
'lfwrite': ('Writing LF RFID cards', 'https://docs.flipper.net/zero/rfid/write-data'),
'ib': ('Official iButton', 'https://docs.flipper.net/zero/ibutton'),
'ir': ('Official infrared', 'https://docs.flipper.net/zero/infrared'),
'irread': ('Learning infrared remotes', 'https://docs.flipper.net/zero/infrared/read'),
'usb': ('Official Bad USB and BLE HID', 'https://docs.flipper.net/zero/bad-usb'),
'gpio': ('Official GPIO pinout and electrical limits', 'https://docs.flipper.net/zero/gpio-and-modules'),
'marauder': ('ESP32 Marauder · Flipper integration', 'https://github.com/justcallmekoko/ESP32Marauder/wiki/Flipper-Zero'),
'marauderhw': ('Marauder hardware and firmware targets', 'https://github.com/justcallmekoko/ESP32Marauder/wiki/supported-hardware'),
'ufbt': ('Official uFBT', 'https://github.com/flipperdevices/flipperzero-ufbt'),
'fap': ('Official FAP and API compatibility', 'https://developer.flipper.net/flipperzero/doxygen/apps_on_sd_card.html'),
'manifest': ('Official application manifests', 'https://github.com/flipperdevices/flipperzero-firmware/blob/dev/documentation/AppManifests.md'),
'momentum': ('Momentum firmware · project source', 'https://github.com/Next-Flip/Momentum-Firmware'),
'unleashed': ('Unleashed firmware · project source', 'https://github.com/DarkFlippers/unleashed-firmware'),
'uber': ('UberGuidoZ · community laboratory resources', 'https://github.com/UberGuidoZ/Flipper'),
'derek': ('Derek Jamison · tutorials, apps and videos', 'https://github.com/jamisonderek/flipper-zero-tutorials'),
'lab': ('Flipper Lab · app catalog', 'https://lab.flipper.net/apps'),
'forum': ('Flipper community forum', 'https://forum.flipper.net/'),
}


def build(zh):
    def t(en, cn): return cn if zh else en
    def p(en, cn): return '<p>'+t(en,cn)+'</p>'
    def h(en, cn): return '<h3>'+t(en,cn)+'</h3>'
    def ul(items): return '<ul>'+''.join('<li>'+t(*x)+'</li>' for x in items)+'</ul>'
    def steps(items): return '<ol class="steps">'+''.join('<li>'+t(*x)+'</li>' for x in items)+'</ol>'
    def code(s): return '<pre><code>'+e(s.strip())+'</code></pre>'
    def refs(*keys):
        return '<div class="refs">'+t('Read the source','原始资料')+' · '+ ' · '.join(f'<a href="{SOURCES[k][1]}" target="_blank" rel="noopener noreferrer">{e(SOURCES[k][0])}</a>' for k in keys)+'</div>'
    def table(head, rows):
        return '<div class="table-scroll" tabindex="0" role="region" aria-label="'+t('Scrollable comparison','可横向滚动的对照表')+'"><table><thead><tr>'+''.join('<th scope="col">'+t(*c)+'</th>' for c in head)+'</tr></thead><tbody>'+''.join('<tr>'+''.join(('<th scope="row">' if i==0 else '<td>')+t(*c)+('</th>' if i==0 else '</td>') for i,c in enumerate(r))+'</tr>' for r in rows)+'</tbody></table></div>'
    def note(en,cn): return '<aside class="note">'+t(en,cn)+'</aside>'
    def diagram(name,title,caption):
        fn=f'assets/{name}{".zh" if zh else ""}.svg'
        if name == 'map':
            fn += '?v=' + sha256((ROOT/fn).read_bytes()).hexdigest()[:12]
        return f'<figure class="diagram"><a href="{fn}" target="_blank" rel="noopener" aria-label="{e(t("Open diagram", "打开完整示意图"))}"><img src="{fn}" alt="{e(t(*title))}" loading="lazy"/></a><figcaption><strong>{t(*title)}</strong> — {t(*caption)} <span>{t("Original teaching diagram · open full size", "本站教学示意图 · 点击查看完整大图")}</span></figcaption></figure>'
    def photo(name,title,key):
        return f'<figure class="official"><a href="assets/{name}.webp" target="_blank" rel="noopener"><img src="assets/{name}.webp" alt="{e(t(*title))}" loading="lazy"/></a><figcaption>{t(*title)} · <a href="{SOURCES[key][1]}" target="_blank" rel="noopener">Flipper Devices · {t("official illustration", "官方原图")}</a> · {t("Click for original size", "点击查看原始尺寸")}</figcaption></figure>'

    sections=[]
    def section(id,title,body): sections.append((id,t(*title),body))
    section('map',('The hardware-hacking map','硬件 Hacking 全景'),
      p('Start with a question about a real interface. What identifies a device? Which bytes change? What prevents replay? Capture a baseline, change one variable, and verify the receiver’s behavior. This field guide emphasizes radio, cards, USB and hardware exploration. App development supports those experiments.',
        '从真实接口上的问题入手。设备凭什么识别身份？哪些字节在变化？什么机制防止重放？先采集基线，再改变一个变量，最后验证接收端行为。本站以无线、卡片、USB 与硬件探索为主，开发内容用于辅助实验。')+
      diagram('map',('One device, several different interfaces','一台设备，多种不同接口'),('Each interface has its own physical layer and security assumptions. Wi-Fi requires an expansion board.','每种接口有独立的物理层与安全假设。Wi-Fi 需要扩展板。'))+
      table([('Interface','接口'),('What to investigate','研究问题'),('Bench equipment','实验装备')],[
       [('Sub-GHz','Sub-GHz'),('Pulse encoding, fixed code, stateful rolling code','脉冲编码、固定码、有状态滚动码'),('Owned remote + disconnected test receiver / LED','自有遥控器 + 与执行机构断开的测试接收板 / LED')],
       [('NFC / M1','NFC / M1'),('UID, sectors, authentication and reader decisions','UID、扇区、认证和读卡器的判定逻辑'),('Classic test card + compatible blank + lab reader','Classic 测试卡 + 兼容空白卡 + 实验读卡器')],
       [('LF RFID / iButton','低频 RFID / iButton'),('Identifier-only designs and compatible media','仅标识符设计与介质兼容性'),('Test tags / keys and a desktop reader','测试标签 / 钥匙与桌面读头')],
       [('IR / USB','红外 / USB'),('Command structure and implicit input trust','指令结构与隐式输入信任'),('Your remote, TV and an offline test computer','自有遥控器、电视及离线测试电脑')],
       [('GPIO / Wi-Fi expansion','GPIO / Wi-Fi 扩展'),('UART logs, buses, board firmware and RF metadata','UART 日志、总线、板载固件与无线元数据'),('3.3 V development board, meter, compatible ESP32','3.3 V 开发板、万用表、兼容 ESP32 扩展板')]])+
      note('Use owned equipment or a defined authorized test bench. Disconnect gate motors and other actuators during RF experiments. Keep local card dumps and RF identifiers out of public repositories. This site publishes procedures and synthetic examples; it does not claim hardware tests have been completed.',
       '使用自有设备或明确授权的测试台。无线实验先断开门机等执行机构。真实卡片 dump、密钥和遥控器标识符不要上传公开仓库。本站提供方法与合成示例，不将文档核验写成已完成硬件实测。')+refs('docs','spec'))

    section('firmware',('Firmware, customization and recovery','刷机、固件定制与恢复'),
      p('A firmware image, SD resources and an external app are separate artifacts. Record the firmware version and source commit before comparing experiments. Back up the SD card and use a USB data cable. Establish a working official release baseline before trying a community build.',
        '设备固件、SD 卡资源和外部 App 是三个不同产物。对比实验前记录固件版本与源码提交，备份 SD 卡并使用可传数据的 USB 线。先用官方稳定版本建立可工作的基线，再测试社区版本。')+
      diagram('firmware',('Keep a reversible firmware path','保留可逆的固件路径'),('A firmware rollback also needs matching SD resources and app API compatibility.','回退固件时，还需要匹配 SD 资源与 App API。'))+
      steps([('Back up card data, saved remotes and app settings with qFlipper / a card reader. Note the current version.','通过 qFlipper 或读卡器备份卡片数据、遥控器与 App 配置，记录当前版本。'),
       ('With a microSD card inserted, connect qFlipper or the official mobile app, choose the Release channel and complete the update without disconnecting power.','插入 microSD，连接 qFlipper 或官方手机 App，选择 Release 通道，更新时保持供电。'),
       ('Reopen a saved test file and run one known-good app. For a custom package, follow that project’s release instructions and verify its origin and available checksums.','打开一个已保存的测试文件、运行一个已知可用的 App。社区安装包按项目发布说明安装，核对来源及其提供的校验值。'),
       ('For corruption, enter Settings / Power / Reboot / Firmware Upgrade on a responsive device and use qFlipper Repair. If unresponsive, follow the official recovery button sequence linked below. Restore the official release before restoring compatible backups.','若固件损坏且界面仍可操作，通过 Settings / Power / Reboot / Firmware Upgrade 进入恢复模式，使用 qFlipper Repair。无响应时按下方官方文档的按键步骤进入 DFU。先恢复官方版本，再恢复兼容的备份。')])+
      h('Build a small, reviewable firmware change','从一个可审查的小改动开始')+
      code('''git clone --recursive https://github.com/flipperdevices/flipperzero-firmware.git
cd flipperzero-firmware
git rev-parse HEAD                 # record the exact source revision
./fbt                             # builds distribution artifacts
# Make a small change, inspect git diff, then rebuild
./fbt COMPACT=1 DEBUG=0 updater_package copro_dist
# Optional, only with your device connected and backed up
# ./fbt flash_usb_full''')+
      table([('Choice','选择'),('Role','定位'),('Before installing','安装前关注')],[
       [('Official Release','官方 Release'),('Baseline for documented menus and SDK behavior','文档菜单与 SDK 行为的基线'),('Version, SD assets, release notes','版本、SD 资源、发布说明')],
       [('Momentum','Momentum'),('Community customization, UI and bundled apps','社区定制、界面与配套 App'),('Project release guide, app bundle and configuration changes','项目发布指南、配套 App 与配置变化')],
       [('Unleashed','Unleashed'),('Community firmware with protocol and application extensions','扩展协议与应用的社区固件'),('Hardware target, firmware-specific features and regional TX rules','硬件目标、固件专属能力与当地发射规定')],
       [('Your source build','自行构建'),('Inspect one decoder, setting or UI component at a time','一次研究一个解码器、配置或界面模块'),('Pinned commit, diff, build log and a stock recovery package','固定提交、差异、构建日志与官方恢复包')]])+
      p('Keep RF transmission within local spectrum rules even when firmware exposes additional settings. Installing a different firmware cannot add a missing radio chip or solve an unsupported cryptographic protocol by itself.',
        '即使固件显示更多选项，发射仍需遵守当地频谱规定。更换固件无法凭空增加射频芯片，也不会自动解决不支持的密码协议。')+refs('update','recovery','fbt','momentum','unleashed'))

    section('radio',('Sub-GHz capture and signal analysis','Sub-GHz 捕获与信号分析'),
      p('The CC1101 receives selected bands, not a continuous 0–1 GHz spectrum. Official operational bands are 300–348, 387–464 and 779–928 MHz; transmission is region-limited. Match frequency, modulation and receive bandwidth before interpreting a capture.',
        'CC1101 工作在指定频段，并非连续覆盖 0–1 GHz。官方工作频段为 300–348、387–464、779–928 MHz，发射还受地区限制。先匹配频率、调制与接收带宽，再解释捕获结果。')+
      photo('subghz-menu',('Sub-GHz menu and capture modes','Sub-GHz 菜单与捕获方式'),'rf')+
      table([('Setting / mode','设置 / 模式'),('Meaning','含义'),('Typical mistake','常见误区')],[
       [('Frequency Analyzer','Frequency Analyzer'),('Find a strong nearby carrier; identify its protocol separately','定位附近强信号的载波，协议需另行识别'),('A frequency peak alone does not reveal the code','发现频率峰值就认为已经识别遥控码')],
       [('Read','Read'),('Run supported decoders and show structured fields','运行已有解码器并显示结构化字段'),('Assume every decoded dynamic protocol can be saved','认为能解码的动态协议都能保存')],
       [('Read RAW','Read RAW'),('Record demodulated level durations for timing analysis','记录解调后的电平持续时间，用于时序分析'),('Treat pulse timings as SDR I/Q samples','将脉冲时长当成 SDR 的 I/Q 采样')],
       [('RSSI threshold','RSSI 阈值'),('Gate weak activity; choose it from the idle and target levels','根据空闲和目标信号强度过滤弱活动'),('Raise it so far that the frame edges disappear','阈值过高，反而丢失有效帧边缘')]])+
      diagram('capture',('Capture → compare → explain','捕获 → 对比 → 解释'),('Repeat the same button, compare another button, then check timing and changing fields.','重复同一按键，再换按键，对比时序和变化字段。'))+
      h('A repeatable RF bench session','一次可重复的无线实验')+
      steps([('Place your remote near Flipper without pressing it against the antenna. Run Frequency Analyzer, press one button briefly, and note the detected band.','遥控器靠近 Flipper，但避免紧贴天线。运行 Frequency Analyzer，短按一次，记录检测频段。'),
       ('Open Read, configure the measured frequency and a suitable preset, and capture several presses. Save a supported static protocol with a descriptive test name.','进入 Read，选择测得的频率和合适 preset，多次按键。可保存的静态协议使用清晰的测试名称保存。'),
       ('For unknown timing, open Read RAW, start recording, make three separated presses and stop. Keep an idle sample. Compare RSSI, modulation and distance if it is noisy.','需要分析未知时序时，使用 Read RAW，开始录制后间隔按三次，再停止。保留空闲样本。噪声多时分别对比 RSSI、调制与距离。'),
       ('Export the .sub file through qFlipper. Compare at least two captures and annotate frequency, preset, frame gaps and pulse ratios. Test replay only on your isolated fixed-code receiver.','通过 qFlipper 导出 .sub，至少比较两份捕获，标注频率、preset、帧间隔及脉宽比例。仅在隔离的自有固定码接收板上验证重放。')])+
      diagram('pulses',('Read a pulse train','读懂一段脉冲'),('Synthetic 300 / 900 µs symbols illustrate timing ratios. They are not a Nice protocol definition.','合成的 300 / 900 µs 符号用于解释脉宽比例，不代表 Nice 协议定义。'))+
      p('In a RAW .sub record, positive durations represent high level and negative durations low level, in microseconds. A long low gap is a candidate frame boundary. Cluster short and long timings, normalize drift, then inspect repeated frames. A histogram alone cannot identify encryption or establish a bit mapping.',
        'RAW .sub 中，正时长表示高电平，负时长表示低电平，单位为微秒。长低电平间隔可以作为候选帧边界。先对短 / 长时长聚类、归一化漂移，再比较重复帧。仅凭直方图无法判断加密，也不能自动确定比特映射。')+
      '<p><a class="download" href="downloads/pulse_inspect.py" download>'+t('Download the offline pulse inspector','下载离线脉冲分析脚本')+'</a> <a href="downloads/synthetic.sub" download>'+t('Synthetic .sub example','合成 .sub 示例')+'</a></p>'+
      code('python3 pulse_inspect.py synthetic.sub --svg pulses.svg\n# For a real capture, adjust the frame-gap threshold to that protocol\npython3 pulse_inspect.py your_capture.sub --gap-us 5000 --svg capture.svg')+
      refs('freq','read','raw','format'))

    section('nice',('Nice remote-control experiments','Nice 遥控器实战'),
      p('Check the exact remote and receiver model before transmitting. The official compatibility table identifies Nice FLO 12/24-bit as static at 433.92 MHz AM, and FLOR-S as dynamic at 433.92 MHz AM. Model labels and the decoded protocol matter more than a similar-looking case.',
        '发射前确认遥控器与接收器的准确型号。官方兼容表将 Nice FLO 12/24-bit 列为 433.92 MHz AM 静态协议，将 FLOR-S 列为同频 AM 动态协议。应以型号与解码协议为准，不能仅凭外壳相似判断。')+
      diagram('nice',('Fixed code and rolling state','固定码与滚动状态'),('A stateful receiver evaluates freshness as well as identity. This is a conceptual model, not a FLOR-S frame specification.','有状态接收器既判断身份，也判断新鲜度。图为概念模型，并非 FLOR-S 帧规格。'))+
      h('FLO fixed-code lab','FLO 固定码实验')+
      steps([('Use a spare FLO remote and matching bench receiver. Disconnect the receiver from the door or gate motor and observe an LED or relay indicator.','使用备用 FLO 遥控器和匹配的桌面接收板，断开门机 / 闸机，观察 LED 或继电器指示。'),
       ('Use Sub-GHz / Read at the confirmed frequency. Capture the same button several times, confirm the displayed static protocol, and save it.','在确认的频率使用 Sub-GHz / Read。多次捕获同一按键，确认显示静态协议后保存。'),
       ('Open Saved, choose the test capture, select Emulate and send once. Compare the receiver indication with the original remote, then check another button.','进入 Saved，选择测试捕获，使用 Emulate 单次发送。将接收板反应与原遥控器对照，再比较另一个按键。'),
       ('Log successes / trials, distance and preset. If it fails, investigate protocol variant, bit length, modulation and receiver pairing independently.','记录成功次数 / 总次数、距离与 preset。失败时分别排查协议变体、位长、调制及接收端配对。')])+
      h('FLOR-S and enrollment','FLOR-S 与接收器注册')+
      p('A rolling-code design maintains transmitter and receiver state. A previously accepted message may be rejected as stale; consuming codes away from the receiver can also affect synchronization. Official firmware decodes listed dynamic protocols with saving disabled. Use the receiver manufacturer’s authorized enrollment procedure for a new transmitter. Flipper’s Add Manually path is useful only where the current firmware explicitly supports that protocol and the receiver supports enrollment.',
        '滚动码设计维护发射端与接收端状态。已经接受过的消息可能因过期而被拒绝，在接收器范围外消耗码值也可能影响同步。官方固件对表中动态协议允许解码，但禁用保存。新发射器按接收器厂商的授权注册流程处理；Flipper 的 Add Manually 仅适用于当前固件明确支持且接收器支持注册的协议。')+
      note('Do not diagnose a failed rolling-code experiment by repeatedly pressing a live vehicle or gate remote. Record the state and consult the receiver’s pairing / resynchronization instructions. Keep RAW replay practice on the fixed-code bench.',
        '滚动码实验失败时，不要反复按真实车辆或门机遥控器“试运气”。先记录状态，再查接收端的注册 / 重同步说明。RAW 重放练习放在固定码实验台上完成。')+refs('nice','add'))

    section('nfc',('M1 / MIFARE Classic cards','M1 / MIFARE Classic 卡片'),
      p('“M1” commonly refers to MIFARE Classic. Identify the card family before choosing a workflow. Classic, DESFire, Ultralight and LF RFID have different memory and authentication models. Displaying a UID is only one observation; determine what the reader actually authenticates.',
        '“M1”通常指 MIFARE Classic。先确认卡片家族再选择流程，Classic、DESFire、Ultralight 与低频 RFID 的存储和认证模型不同。显示 UID 只是一个观察结果，还应确认读卡器实际验证什么。')+
      photo('dual-antenna',('13.56 MHz NFC and 125 kHz LF antennas','13.56 MHz NFC 与 125 kHz 低频天线'),'nfc')+
      diagram('sectors',('Inside a Classic 1K card','Classic 1K 卡片的内部结构'),('16 sectors × 4 blocks × 16 bytes. Sector 0 block 0 is manufacturer data; a trailer controls each sector.','16 扇区 × 4 块 × 16 字节。扇区 0 的块 0 为厂商数据，每个扇区由尾块管理。'))+
      p('Each sector trailer contains a 6-byte Key A, access-control bytes and a 6-byte Key B field. The access bytes determine block permissions and how Key B is used. Trailer data needs careful handling: readable dump bytes do not necessarily expose the actual secret keys. Classic uses Crypto1; a UID-only reader introduces a separate system-design weakness.',
        '每个扇区尾块包含 6 字节 Key A、访问控制字节及 6 字节 Key B 字段。访问位决定各块权限及 Key B 用法。尾块要谨慎处理，dump 中可读出的字节不一定就是实际秘密密钥。Classic 使用 Crypto1；仅读 UID 的读卡器还存在独立的系统设计弱点。')+
      diagram('cardflow',('Read, emulate, write and verify','读取、模拟、写卡与验证'),('Check dump completeness and card behavior separately. Treat keys and dumps as credentials.','分别验证 dump 完整性与卡片行为，将密钥和 dump 当作凭据管理。'))+
      h('Clone a known-key test card','复制已知密钥的测试卡')+
      steps([('Prepare a spare Classic card with known test keys and a lab reader. In NFC / Read, scan and save it. Record UID, type and sectors successfully read.','准备一张密钥已知的备用 Classic 测试卡与实验读头，使用 NFC / Read 扫描并保存，记录 UID、类型与读取成功的扇区。'),
       ('Resolve missing sectors before writing. Test emulation against the lab reader and note whether it authenticates data or only checks the UID.','写卡前处理未读取的扇区。先在实验读头测试模拟，记录它验证数据认证还是仅检查 UID。'),
       ('Open Apps / NFC / NFC Magic and use Check Magic Tag on a compatible blank. Supported generations and capacities must match the current app’s documentation.','进入 Apps / NFC / NFC Magic，使用 Check Magic Tag 检查兼容空白卡，代际与容量以当前 App 文档为准。'),
       ('Choose Write and the saved complete test image. Keep the blank in place, then reread it and compare UID and application data. Test the original, Flipper emulation and blank separately on the lab reader.','选择 Write 和完整测试镜像，写入时保持空白卡位置。重新读取并对比 UID 和应用数据，分别测试原卡、Flipper 模拟及空白卡。')])+
      table([('Result','结果'),('What it means','含义'),('Next check','下一步')],[
       [('UID read','读取 UID'),('Selection and identification worked','选卡与标识读取成功'),('Sector authentication and data coverage','扇区认证与数据覆盖率')],
       [('Complete Classic dump','完整 Classic dump'),('Required data and usable keys have been collected','所需数据与可用密钥已取得'),('Access bits, dynamic state and reader policy','访问位、动态状态及读头策略')],
       [('Emulation works','模拟成功'),('The tested reader accepted that interaction','该读头接受了本次交互'),('Physical blank behavior and timing may differ','实体空白卡的行为和时序可能不同')],
       [('Ordinary Classic blank','普通 Classic 空白卡'),('Data may be writable with the right keys','具备正确密钥时可写部分数据'),('Manufacturer UID is not normally rewritable','厂商 UID 通常不可改写')]])+
      h('When a test dump is incomplete','测试 dump 不完整时')+
      p('The official key-recovery guide documents dictionary attempts, MFKey32 and card-only attacks. MFKey32 uses suitable reader authentication nonce transcripts to recover Crypto1 state. On an authorized lab reader, follow Extract MF Keys, compute the candidate keys with the documented tool, then reread the test card and verify coverage. Collecting nonces alone does not prove key recovery. Keep transcripts private and distinguish card-only prerequisites from reader-assisted ones.',
        '官方密钥恢复指南记录了字典尝试、MFKey32 及仅卡攻击。MFKey32 利用合适的读头认证 nonce 记录恢复 Crypto1 状态。在获授权的实验读头上按 Extract MF Keys 流程采集，用文档工具计算候选密钥，再回读测试卡核验覆盖率。采到 nonce 不等于已经恢复密钥，并应区分仅卡攻击与借助读头的前提。认证记录保持私有。')+refs('nfcread','nxp','magic','mfkey'))

    section('rfid',('LF RFID and contact keys','低频 RFID 与接触式钥匙'),
      p('A card’s shape does not identify its radio technology. Start with the LF RFID and NFC read modes separately. A 125 kHz identifier badge and an authenticated 13.56 MHz card can look identical while relying on very different security assumptions.',
        '卡片外形不能判断无线技术。分别用低频 RFID 和 NFC 读取模式识别。125 kHz 标识符卡与经过认证的 13.56 MHz 卡，外形可能完全一致，安全假设却不同。')+
      diagram('identifiers',('Where does identity become trust?','身份在哪里变成了信任？'),('Compare an identifier lookup with an authenticated exchange. A checksum detects errors; it does not establish authenticity.','比较标识符查询与认证交互。校验和用于检错，不能证明真实性。'))+
      table([('Medium','介质'),('Lab workflow','实验流程'),('Boundary','边界')],[
       [('125 kHz RFID','125 kHz RFID'),('Read a spare tag → save → emulate on your reader → write a compatible rewritable test tag → reread','读取备用标签 → 保存 → 自有读头上模拟 → 写入兼容可改写测试标签 → 回读'),('T5577-class media need protocol / encoding compatibility; not every LF tag is writable','T5577 类介质也需匹配协议 / 编码，不是所有低频卡都可写')],
       [('iButton','iButton'),('Read a test key through the contact pad → save → emulate → compare a compatible writable blank','通过接触点读取测试钥匙 → 保存 → 模拟 → 对比兼容可写空白钥匙'),('Dallas, Cyfral and Metakom differ; a secure authenticator is not equivalent to a simple serial-number key','Dallas、Cyfral 与 Metakom 不同，安全认证芯片不能等同于简单序列号钥匙')]])+
      p('A useful finding is a precise statement such as “this bench reader accepts the duplicated identifier without another challenge.” Avoid generalizing that result to every badge or every reader from the same vendor. Store protocol, ID, reader model and observed decisions in your notebook.',
        '有价值的结论应具体，例如“这个实验读头接受相同标识符，没有额外挑战”。不要将它推广为同厂商所有卡片或读头的结论。实验记录需保留协议、ID、读头型号及实际判定结果。')+refs('lf','lfwrite','ib'))

    section('infrared',('Infrared remote reverse engineering','红外遥控逆向'),
      photo('infrared-menu',('Official infrared learning menu','官方红外学习菜单'),'ir')+
      p('IR separates a carrier from its command envelope. A receiver demodulates the carrier into marks and spaces. A decoded protocol may expose address, command and repeat information; a RAW capture preserves the envelope timing. Devices with stateful remotes, especially air conditioners, may send an entire state rather than a simple button code.',
        '红外信号包含载波与指令包络。接收器把载波解调成 mark 与 space。已解码协议可能显示地址、命令与重复信息，RAW 保留包络时序。空调等有状态遥控器可能发送完整状态，而非简单按键编号。')+
      diagram('ir',('Carrier → envelope → command','载波 → 包络 → 命令'),('Compare short presses, long presses and repeated frames on your own appliance.','在自有电器上比较短按、长按和重复帧。'))+
      steps([('Open Infrared / Learn New Remote, aim your remote at Flipper’s IR window, press one harmless button and save it with a meaningful name.','进入 Infrared / Learn New Remote，将遥控器对准红外窗口，按一个无害功能键，使用有含义的名称保存。'),
       ('Learn two other buttons and inspect the .ir file in qFlipper. Compare decoded address / command fields or RAW timing arrays.','再学习两个按键，通过 qFlipper 查看 .ir，比较地址 / 命令字段或 RAW 时序数组。'),
       ('Replay once at the owned appliance and observe its state. For a toggle command, log the starting state; for AC controls, compare complete state changes.','对自有电器单次发送，观察状态变化。对于 toggle，记录起始状态；对于空调，比较完整状态切换。')])+
      p('Use a single-device learning exercise before testing universal dictionaries. A failed send can be caused by aim, distance, a missing repeat frame or the wrong state, even when the pulse capture looks clean.',
        '先完成单设备学习，再尝试通用码库。即使脉冲看似干净，方向、距离、缺少重复帧或状态不匹配，都可能导致发送失败。')+refs('ir','irread'))

    section('usb',('BadUSB and BLE HID experiments','BadUSB 与 BLE HID 实验'),
      p('USB HID is a trust-boundary experiment: a computer accepts input from a peripheral as if a person typed it. Flipper can send scripted keyboard input over supported USB / BLE HID paths. Focus on visible actions in a test editor to understand enumeration, focus, layout and timing.',
        'USB HID 的核心是输入信任边界，电脑把外设输入视作人在打字。Flipper 可通过支持的 USB / BLE HID 路径发送脚本化键盘输入。先在测试编辑器中观察可见操作，理解枚举、焦点、布局与时序。')+
      diagram('hid',('From peripheral to trusted input','外设如何变成受信输入'),('The host executes the input in the active application and user context.','输入作用于当前前台应用与用户上下文。'))+
      code('''REM Open an empty text editor on your own computer first
DELAY 1500
STRING Flipper lab - visible keyboard input only
ENTER
STRING Verify keyboard layout, focus and timing''')+
      p('Save this as visible-hid.txt under SD Card / badusb. Open a blank editor yourself, connect Flipper, select the script in Bad USB and run it. This example opens no shell and reads no files. Compare US and non-US layouts and log missed characters. For BLE, pair only with your test host and remove the pairing afterward.',
        '保存为 SD Card / badusb 下的 visible-hid.txt。自行打开空白编辑器，连接 Flipper，在 Bad USB 中选择并运行。示例不打开 shell，也不读取文件。对比不同键盘布局并记录漏字。BLE 仅与测试主机配对，实验后移除配对。')+
      '<p><a href="downloads/visible-hid.txt" download>'+t('Download the visible HID example','下载可见输入示例')+'</a></p>'+
      p('For a security assessment, measure whether unknown HID devices are allowed, whether an unlocked session is required and whether device-control policies are enforced. VID/PID strings identify a device claim; they are not cryptographic proof of its identity.',
        '安全评估可以测量未知 HID 是否被允许、是否需要已解锁会话、设备管控策略是否生效。VID/PID 字符串仅代表设备自报标识，并非密码学身份证明。')+refs('usb'))

    section('gpio',('GPIO, UART and Wi-Fi expansion','GPIO、UART 与 Wi-Fi 扩展'),
      p('A good hardware-hacking workflow starts with a meter and the board documentation. Identify ground, logic voltage and bus direction before connecting wires. Use 3.3 V logic for the labs below; a 5 V power pin is a separate supply rail. Never assume a pin is safe at 5 V in every configuration.',
        '硬件 Hacking 先从万用表和板卡文档开始。接线前确认地线、逻辑电平与总线方向。下述实验使用 3.3 V 逻辑，5 V 供电脚是独立电源轨，不能认为所有配置下 GPIO 都耐 5 V。')+
      photo('gpio-pinout',('Official full GPIO pinout','官方完整 GPIO 引脚图'),'gpio')+
      diagram('uart',('UART bridge with a safe starting point','UART 桥接的安全起点'),('Start receive-only: board TX → Flipper RX, common GND, no VCC wire. Confirm the selected UART mapping in the app.','先只接收，板 TX 接 Flipper RX，共地，不接 VCC。引脚映射以 App 选中的 UART 为准。'))+
      steps([('Use a documented 3.3 V development board. Power it separately. Connect its GND to Flipper GND and its TX to the selected Flipper RX. Leave Flipper TX disconnected initially.','使用有文档的 3.3 V 开发板，独立供电。连接共地，板 TX 接所选 Flipper RX，开始时不连接 Flipper TX。'),
       ('Open GPIO / USB-UART Bridge, match the UART configuration, and select the Flipper serial port in your terminal. Compare the board’s documented baud rate and framing.','进入 GPIO / USB-UART Bridge，匹配 UART 配置，在电脑终端选择 Flipper 串口，按板卡说明设置波特率与帧格式。'),
       ('Capture boot messages and timestamps without sending commands. Later, connect the opposite direction only for a defined test. Keep firmware consoles and logs private if they contain secrets.','先只采集启动消息和时间戳，不发送命令。之后仅针对明确测试连接反向通道，日志含秘密时保持私有。')])+
      table([('Bus / extension','总线 / 扩展'),('Investigation','研究内容'),('Required detail','必要条件')],[
       [('SPI / I²C','SPI / I²C'),('Read a test sensor or inspect a known bus transaction','读取测试传感器或观察已知总线事务'),('Correct bus app, pull-ups, chip-select and voltage; never drive an active bus blindly','匹配总线 App、上拉、片选与电平，不盲目驱动正在工作的总线')],
       [('SWD / debugging','SWD / 调试'),('Breakpoints and firmware tracing on an owned dev board','自有开发板断点与固件跟踪'),('A supported debug probe; UART bridge alone is not an SWD probe','支持的调试探针，UART 桥本身不等于 SWD 探针')],
       [('ESP32 + Marauder','ESP32 + Marauder'),('RF discovery / metadata on an isolated Wi-Fi lab network','隔离 Wi-Fi 实验网的无线发现与元数据'),('Separate board firmware, matching hardware target and a compatible Flipper UART app','独立板载固件、匹配硬件目标与兼容 Flipper UART App')]])+
      diagram('wifi',('Two processors, two firmware images','两个处理器，两套固件'),('Flipper provides the UI; the external ESP32 supplies Wi-Fi functionality.','Flipper 提供操作界面，外部 ESP32 提供 Wi-Fi 能力。'))+
      p('For a Wi-Fi lab, use an isolated AP with a test SSID. Match the expansion board’s exact model to Marauder’s supported-hardware table before flashing. Compare channel and beacon metadata with the AP configuration. Record which actions are passive scans and which emit frames. Save the original board firmware so you can restore its debugging role.',
        'Wi-Fi 实验使用隔离 AP 与测试 SSID。刷机前将扩展板准确型号与 Marauder 的硬件兼容表匹配。将信道、beacon 元数据与 AP 配置对照，分别标记被动接收与会主动发送帧的操作。保留板载原固件，便于恢复调试用途。')+refs('gpio','marauder','marauderhw'))

    section('workbench',('Build experiments that teach something','把实验做成可复核的研究'),
      table([('Experiment','实验'),('Hypothesis and method','假设与方法'),('Evidence to keep','保留证据')],[
       [('Fixed-code replay','固定码重放'),('The test receiver accepts an identical command. Compare original vs emulation at the same distance.','测试接收板会接受相同指令。在相同距离比较原遥控器与模拟。'),('Preset, decoded type, trials and receiver LED log','preset、解码类型、次数与接收板 LED 记录')],
       [('Stateful rejection','有状态拒绝'),('A previously accepted message is rejected by a stateful test receiver. Use a toy receiver or documented dev kit.','有状态测试接收器拒绝已接受过的消息，使用玩具接收程序或有文档的开发套件。'),('Counter transitions and acceptance log, no real receiver secrets','计数器迁移与接受日志，不公开真实接收器秘密')],
       [('Card reader policy','卡片验证策略'),('Does the lab reader need authenticated sector data, or only an identifier? Compare explicit reader configurations.','实验读头需要认证扇区数据还是仅 ID？对比读头明确配置。'),('Reader configuration, successful sector coverage and decisions','读头配置、扇区读取覆盖率与判定')],
       [('Hardware observability','硬件可观察性'),('Boot logs expose a protocol or configuration error. Capture the same reset sequence several times.','启动日志揭示协议或配置错误，多次记录相同复位序列。'),('Wiring diagram, voltage, baud rate and timestamped logs','接线图、电平、波特率与带时间戳日志')]])+
      diagram('evidence',('A compact research loop','简洁的研究闭环'),('Separate observation, interpretation and verified outcome. Use controls to challenge your explanation.','区分观察、解释与验证结论，使用对照实验检验假设。'))+
      '<p><a href="downloads/lab-notebook.md" download>'+t('Download the bilingual experiment template','下载中英文实验记录模板')+'</a></p>'+
      h('Troubleshooting by layer','按层定位失败原因')+
      ul([('No RF capture — check the supported band, battery, modulation, bandwidth and antenna distance before changing decoders.','抓不到无线信号，先检查支持频段、电池、调制、带宽与天线距离，再考虑解码器。'),
       ('A capture exists but the receiver ignores it — check static / rolling classification, pairing, repeat timing and receiver state.','有捕获但接收器无反应，检查静态 / 滚动码分类、注册、重复帧时序与接收器状态。'),
       ('A card UID reads but a dump is incomplete — investigate sector keys and permissions; a different firmware does not guarantee data recovery.','能读 UID 但 dump 不完整，排查扇区密钥与权限，更换固件不保证恢复数据。'),
       ('UART text is garbled — check ground, logic levels, baud rate and framing. An output-voltage conflict is an electrical problem.','UART 乱码，检查共地、电平、波特率与帧格式。输出电压冲突属于电气问题。'),
       ('An app will not load — compare its hardware target and required API with your firmware, then rebuild against the correct SDK.','App 无法加载，核对硬件目标、API 与固件版本，再用匹配 SDK 重建。')]))

    section('development',('Supporting apps and a tiny game','辅助 App 与小游戏开发'),
      p('Use a small FAP app for a custom visualizer, input tool or game. Build the full firmware only when changing firmware internals. The included “Bit Lab” game lets you match an 8-bit pattern with the D-pad; it demonstrates input events, a message queue, locked state and Canvas rendering without accessing radios or cards.',
        '自定义可视化、输入工具或小游戏可以用小型 FAP App 实现。修改固件内部功能时再构建完整固件。附带的 Bit Lab 用方向键匹配 8 位图案，演示输入事件、消息队列、加锁状态与 Canvas 绘制，不访问射频或卡片。')+
      diagram('app',('Input → state → pixels','输入 → 状态 → 像素'),('Keep callbacks short and release the viewport, queue, mutex and GUI record when leaving.','回调保持简短，退出时释放 viewport、队列、互斥锁与 GUI record。'))+
      code('''python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade ufbt
# Extract bit-lab-source.zip and enter the bit_lab folder
cd bit_lab
ufbt                         # builds the .fap in dist/
# Optional, with a Flipper connected over USB
# ufbt launch''')+
      '<p><a class="download" href="downloads/bit-lab-source.zip" download>'+t('Download Bit Lab source','下载 Bit Lab 源码')+'</a> <a href="downloads/bit_lab.fap" download>'+t('Compiled FAP','已编译 FAP')+'</a> · <a href="downloads/bit_lab/bit_lab.c">'+t('Read the C source','阅读 C 源码')+'</a> · <a href="downloads/bit_lab/application.fam">application.fam</a></p>'+
      note('Bit Lab was compiled with official uFBT 0.2.6 and release SDK 1.5.1, target f7 / API 88.2. The FAP package check passed. No physical-device runtime test was performed.', 'Bit Lab 已使用官方 uFBT 0.2.6 与 Release SDK 1.5.1 编译，目标为 f7 / API 88.2，FAP 包检查通过。尚未进行实体设备运行测试。')+
      p('The manifest declares appid, entry point and EXTERNAL app type. The SDK supplies the API and toolchain. Record the SDK version used for your build; a community firmware may require its own compatible SDK. A successful build verifies compilation, while input, display and resource cleanup still need a device test.',
        'manifest 声明 appid、入口函数与 EXTERNAL 应用类型，SDK 提供 API 和工具链。记录构建使用的 SDK 版本，社区固件可能需要匹配 SDK。编译成功只能证明构建通过，输入、显示和资源释放仍需设备验证。')+refs('ufbt','fap','manifest','derek'))

    section('resources',('Official sources and community routes','官方资料与社区进阶路线'),
      p('Read protocol and electrical facts in official documentation, then inspect community implementations and issues. The table below is a curated navigation guide, not a bulk mirror of someone else’s repository. Versions and app availability change; check the project’s current release and hardware target.',
        '协议与电气规格以官方文档为起点，再阅读社区实现和 issue。下表为精选导航，不是对他人仓库的批量镜像。版本和 App 可用性会变化，使用前查看项目当前发布与硬件目标。')+
      table([('Resource','资源'),('Best use','适合用途'),('How to study it','建议读法')],[
       [('<a href="https://docs.flipper.net/zero">Official docs</a>','<a href="https://docs.flipper.net/zero">官方文档</a>'),('Menus, compatibility, recovery and electrical limits','菜单、兼容性、恢复与电气限制'),('Start with the chapter source links, compare the installed version','先读各章资料链接，对照设备版本')],
       [('<a href="https://github.com/flipperdevices/flipperzero-firmware">Firmware source</a>','<a href="https://github.com/flipperdevices/flipperzero-firmware">官方固件源码</a>'),('Decode state machines, file formats and peripheral services','解码状态机、文件格式与外设服务'),('Trace capture → decoder → saved file → transmitter','追踪捕获 → 解码 → 文件 → 发送的调用链')],
       [('<a href="https://lab.flipper.net/apps">Flipper Lab</a>','<a href="https://lab.flipper.net/apps">Flipper Lab</a>'),('Find external tools and inspect their source links','查找外部工具并追溯源码'),('Compare API compatibility and permissions before installing','安装前比较 API 兼容性与访问能力')],
       [('<a href="https://github.com/UberGuidoZ/Flipper">UberGuidoZ</a>','<a href="https://github.com/UberGuidoZ/Flipper">UberGuidoZ</a>'),('Community notes, IR resources and hardware references','社区笔记、红外资源与硬件参考'),('Choose a small sample and inspect it; do not import opaque payload bundles','挑选小样本审阅，不盲目导入不透明脚本包')],
       [('<a href="https://github.com/jamisonderek/flipper-zero-tutorials">Derek Jamison</a>','<a href="https://github.com/jamisonderek/flipper-zero-tutorials">Derek Jamison</a>'),('Walkthroughs, videos, app and game patterns','实战教程、视频、App 与游戏开发模式'),('Follow the tutorial repository to its current video and source','从教程仓库进入当前视频与源码')],
       [('<a href="https://github.com/Next-Flip/Momentum-Firmware">Momentum</a> / <a href="https://github.com/DarkFlippers/unleashed-firmware">Unleashed</a>','<a href="https://github.com/Next-Flip/Momentum-Firmware">Momentum</a> / <a href="https://github.com/DarkFlippers/unleashed-firmware">Unleashed</a>'),('Compare community features and implementations','比较社区功能与实现'),('Read release notes and diff one feature against stock firmware','读发布说明，对比一个功能与官方源码的差异')],
       [('<a href="https://github.com/justcallmekoko/ESP32Marauder/wiki">ESP32 Marauder</a>','<a href="https://github.com/justcallmekoko/ESP32Marauder/wiki">ESP32 Marauder</a>'),('External Wi-Fi tooling and board compatibility','外部 Wi-Fi 工具与板卡兼容性'),('Begin with supported hardware and Flipper UART integration','从硬件支持表与 Flipper UART 集成入手')],
       [('<a href="https://forum.flipper.net/">Flipper forum</a>','<a href="https://forum.flipper.net/">Flipper 论坛</a>'),('Protocol-specific discussion and reproduction reports','协议讨论与复现记录'),('Search exact model + firmware + symptoms; verify claims against code','搜索准确型号 + 固件 + 现象，对照代码核实说法')]])+
      h('Further hardware-hacking directions','其他值得继续探索的 Hacking 方向')+
      ul([('Wireless sensors and weather stations — study packet framing and checksum behavior on your own transmitter; support may live in a separate community app.','无线传感器与气象站，研究自有发射器的帧结构和校验行为，支持可能位于独立社区 App。'),
       ('Protocol implementation review — compare a decoder’s state transitions with captured edge timings, then add a regression test using synthetic input.','协议实现审查，将解码器状态迁移与边沿时序对照，再用合成输入添加回归测试。'),
       ('Hardware test automation — turn a known UART / I²C experiment into a reproducible script and save wiring and supply assumptions with it.','硬件测试自动化，把已知 UART / I²C 实验做成可重复脚本，同时保存接线与供电假设。'),
       ('Radio beyond Flipper — use an SDR for I/Q and spectrum work, a logic analyzer for digital buses, and a specialized NFC instrument when raw protocol tracing is needed.','超出 Flipper 能力时，频谱与 I/Q 用 SDR，数字总线用逻辑分析仪，底层 NFC 跟踪用专门仪器。')])+
      note('Illustrations from Flipper Devices are attributed next to each image and retain their original ownership. Teaching diagrams and synthetic lab files are local to this site. Source review date: 23 November 2026. UI labels can differ by firmware.',
        'Flipper Devices 图片在图旁标注出处，版权归原权利人。本站教学图与合成实验文件保存在本地。资料核验日期为 2026 年 11 月 23 日，菜单名称可能随固件变化。'))

    toc=''.join(f'<a href="#{id}"><span>{i:02}</span>{title}</a>' for i,(id,title,_) in enumerate(sections,1))
    article=''.join(f'<section id="{id}" class="chapter"><div class="chapter-label">FIELD NOTES / {i:02}</div><h2>{title}</h2>{body}</section>' for i,(id,title,body) in enumerate(sections,1))
    html=f'''<!DOCTYPE html>
<html lang="{'zh-CN' if zh else 'en'}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{t('Flipper Zero Hacking Lab','Flipper Zero Hacking 实战')} · ShundaZhang</title><meta name="description" content="{t('A visual field guide to Flipper Zero firmware, Sub-GHz, Nice remotes, NFC, RFID, IR, USB and hardware hacking.','以实战和图解学习 Flipper Zero 固件、Sub-GHz、Nice 遥控器、NFC、RFID、红外、USB 与硬件 Hacking。')}"><link rel="icon" href="../favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="style.css"><script src="../language.js"></script></head>
<body><a class="skip" href="#main">{t('Skip to content','跳转到正文')}</a><header><a class="brand" href="{'../index.zh.html' if zh else '../'}">ShundaZhang <span>/ {t('Security','安全')}</span></a><nav aria-label="{t('Language','语言')}"><a href="index.html" data-atlas-lang="en" {'aria-current="page"' if not zh else ''}>EN</a><a href="index.zh.html" data-atlas-lang="zh" {'aria-current="page"' if zh else ''}>中文</a></nav></header>
<div class="hero"><div><div class="eyebrow">HARDWARE HACKING / FIELD GUIDE</div><h1>Flipper Zero<br><em>{t('Hacking Lab','Hacking 实战')}</em></h1><p>{t('Understand the interface. Capture the evidence. Test the assumption.','理解接口，捕获证据，检验假设')}<br>{t('A hands-on route through radios, cards and hardware.','从无线、卡片到硬件的实战路线')}</p><div class="tags"><span>Sub-GHz</span><span>NFC / RFID</span><span>USB / GPIO</span></div><a class="start" href="#radio">{t('Start with a signal','从一段信号开始')}</a></div><figure class="hero-figure"><img src="assets/hero.svg" alt="{t('Flipper Zero teaching illustration with waveform, antenna and interface labels','Flipper Zero 教学示意图，展示波形、天线与接口')}"><figcaption>{t('Capture / understand / verify','捕获 / 理解 / 验证')}</figcaption></figure></div>
<div class="layout"><aside class="toc"><h2>{t('On the workbench','实验台目录')}</h2><nav aria-label="{t('Chapters','章节')}">{toc}</nav></aside><main id="main">{article}</main></div><footer><a href="{'../index.zh.html#security' if zh else '../#security'}">{t('Back to the knowledge map','返回知识体系')}</a><span>ShundaZhang · 2026</span><a href="https://github.com/ShundaZhang/shundazhang.github.io/tree/main/flipper-zero-lab">{t('Site source','站点源码')}</a></footer></body></html>'''
    def image_dimensions(match):
        src=match.group(1)
        file_src=src.split('?',1)[0]
        if file_src.endswith('.svg'):
            v=ET.parse(ROOT/file_src).getroot().attrib['viewBox'].split()
            w,height=int(v[2]),int(v[3])
        else:
            w,height={'subghz-menu':(2526,832),'dual-antenna':(1482,754),'gpio-pinout':(4359,3670),'infrared-menu':(1610,572)}[Path(src).stem]
        return f'<img src="{src}" width="{w}" height="{height}"'
    html=re.sub(r'<img src="([^"]+)"',image_dimensions,html)
    (ROOT/('index.zh.html' if zh else 'index.html')).write_text(html)


if __name__ == '__main__':
    from diagrams import build_diagrams
    build_diagrams(ROOT/'assets')
    build(False)
    build(True)
    print('Built Flipper Zero Hacking Lab · EN / 中文 · 12 chapters')
