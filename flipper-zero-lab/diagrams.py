"""Original SVG teaching diagrams, bilingual labels, no external runtime."""
from html import escape
from pathlib import Path
import textwrap

INK='#183044'; MUTED='#526779'; ORANGE='#d65716'; BLUE='#236a80'; GREEN='#196854'

def build_diagrams(root):
 root.mkdir(exist_ok=True)
 for zh in (False,True):
  def t(a,b):return b if zh else a
  def text(x,y,s,size=20,fill=INK,anchor='start',bold=False):
   return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}"'+(' font-weight="700"' if bold else '')+'>'+escape(s)+'</text>'
  def box(x,y,w,h,label,detail='',color=BLUE,single_line=False):
   r=f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="#fff" stroke="{color}" stroke-width="2"/>'
   lines=[label] if single_line else textwrap.wrap(label,12 if zh else int(w/11))
   for i,s in enumerate(lines):r+=text(x+w/2,y+30+i*25,s,19,color,'middle',True)
   if detail:
    lines=textwrap.wrap(detail,14 if zh else int(w/9.5))
    for i,s in enumerate(lines):r+=text(x+w/2,y+h-20-(len(lines)-1-i)*22,s,16,MUTED,'middle')
   return r
  def arrow(x1,y1,x2,y2,label=''):
   r=f'<path d="M{x1},{y1} L{x2},{y2}" fill="none" stroke="{MUTED}" stroke-width="2" marker-end="url(#a)"/>'
   if label:r+=text((x1+x2)/2,(y1+y2)/2-12,label,17,MUTED,'middle')
   return r
  def save(name,title,body,height=360):
   svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 {height}" role="img" aria-labelledby="title desc"><title id="title">{escape(title)}</title><desc id="desc">{escape(t("Original educational diagram. Labels describe components and data flow.","本站原创教学图，标注组件与数据流。"))}</desc><defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10Z" fill="{MUTED}"/></marker></defs><rect width="1000" height="{height}" fill="#f4f8fa"/><g font-family="system-ui, sans-serif">{text(30,40,title,23,INK,bold=True)}{body}</g></svg>'
   (root/(name+('.zh' if zh else '')+'.svg')).write_text(svg)
  def flow(name,title,items,foot):
   body=''
   n=len(items);w=(940-(n-1)*40)/n
   for i,item in enumerate(items):
    x=30+i*(w+40);body+=box(x,100,w,135,t(*item[0]),t(*item[1]))
    if i<n-1:body+=arrow(x+w+5,167,x+w+35,167)
   body+=text(30,287,t(*foot),18,MUTED)
   save(name,t(*title),body,320)
  # Give the hub clear routing corridors above and below. Connector tips stop
  # eight units outside each card so arrowheads never overlap its border.
  body=''
  for a in [(263,166,377,305),(500,208,500,267),(737,166,623,305),
            (263,510,377,355),(500,457,500,393),(737,510,623,355)]:
   body+=arrow(*a)
  body+=box(385,275,230,110,'Flipper Zero',t('UI + files + tools','界面 + 文件 + 工具'),ORANGE,single_line=True)
  for x,y,title,desc in [(25,90,'Sub-GHz',t('CC1101 / pulse timing','CC1101 / 脉冲时序')),
                         (385,90,'NFC / LF RFID','13.56 MHz / 125 kHz'),
                         (745,90,'USB / BLE','HID + RPC'),
                         (25,465,'Infrared',t('Carrier + envelope','载波 + 包络')),
                         (385,465,'iButton',t('Contact interface','接触式接口')),
                         (745,465,'GPIO / ESP32',t('Buses / Wi-Fi expansion','总线 / Wi-Fi 扩展'))]:
   body+=box(x,y,230,110,title,desc,single_line=True)
  save('map',t('Follow the physical interface','从物理接口出发'),body,610)
  flow('firmware',('A reversible update','可逆更新路径'),[(('Back up','备份'),('SD + settings + version','SD + 配置 + 版本')),(('Install','安装'),('Trusted release / build','可信发布 / 自行构建')),(('Validate','验证'),('Known-good test','已知正常的测试')),(('Recover','恢复'),('DFU + stock release','DFU + 官方版本'))],('Also match app APIs and SD resources','同时匹配 App API 与 SD 资源'))
  flow('capture',('An RF experiment in four stages','无线实验的四个阶段'),[(('Locate','定位'),('Band + frequency','频段 + 频率')),(('Capture','捕获'),('Read / Read RAW','Read / Read RAW')),(('Compare','比较'),('Timings + fields','时序 + 字段')),(('Verify','验证'),('Bench receiver result','实验接收器结果'))],('Repeat captures; change only one variable at a time','重复采集，每次只改变一个变量'))
  body=text(35,90,t('Demodulated envelope','解调后的包络'),19)
  pts=[(40,185)];x=40
  for hi,lo in [(30,90),(90,30),(30,90),(90,30)]:
   pts.extend([(x,125),(x+hi,125),(x+hi,185),(x+hi+lo,185)]);x+=hi+lo
  body+=f'<polyline points="'+ ' '.join(f'{a},{b}' for a,b in pts)+'" fill="none" stroke="'+ORANGE+'" stroke-width="4"/>'
  body+=arrow(40,205,890,205,t('time / µs','时间 / µs'))
  body+=text(40,250,'+300  −900      +900  −300      +300  −900      +900  −300',20)
  body+=text(40,295,t('High / low durations → compare ratios → inspect repeated frames','高 / 低电平时长 → 比较比例 → 观察重复帧'),20)
  body+=box(665,90,280,95,t('RAW ≠ I/Q','RAW ≠ I/Q'),t('No carrier phase samples','不保留载波相位采样'))
  save('pulses',t('Synthetic pulse timing','合成脉冲时序'),body,335)
  body=text(35,90,t('Fixed-code conceptual model','固定码概念模型'),20,ORANGE,bold=True)
  body+=box(35,115,260,95,'ID + button',t('Same command','相同指令'))+arrow(305,160,380,160)+box(390,115,260,95,'ID + button',t('Same command','相同指令'))+arrow(660,160,710,160)+box(720,115,245,95,t('Compare value','比较码值'),t('No freshness check','没有新鲜度检查'))
  body+=text(35,270,t('Rolling-code conceptual model','滚动码概念模型'),20,GREEN,bold=True)
  body+=box(35,295,260,115,'ID + n + code(n)',t('Transmitter state','发射端状态'),GREEN)+arrow(305,350,380,350)+box(390,295,260,115,t('Verify + window','验证 + 接受窗口'),t('Receiver state n₀','接收端状态 n₀'),GREEN)+arrow(660,350,710,350)+box(720,295,245,115,t('Accept → update','接受后更新'),t('Old code → reject','旧码 → 拒绝'),GREEN)
  body+=text(35,455,t('This diagram does not specify the Nice FLOR-S packet format','本图不定义 Nice FLOR-S 的报文格式'),18,MUTED)
  save('nice',t('Identity and freshness are different checks','身份与新鲜度是不同的检查'),body,490)
  body=''
  for r in range(4):
   title=['Sector 0','Sector 1','…','Sector 15'][r]
   body+=text(25,105+r*78,title,20)
   for b in range(4):
    label=(t('Manufacturer','厂商数据') if r==0 and b==0 else t('Trailer','扇区尾块') if b==3 else f'Block {b}')
    body+=box(165+b*198,65+r*78,180,64,label,color=ORANGE if b==3 else BLUE)
  body+=text(35,420,t('Sector trailer · 16 bytes','扇区尾块 · 16 字节'),20,INK,bold=True)
  body+=box(35,443,330,75,'Key A','6 bytes',GREEN)+box(375,443,250,75,t('Access + GPB','访问位 + GPB'),'4 bytes',ORANGE)+box(635,443,330,75,'Key B','6 bytes',GREEN)
  save('sectors',t('MIFARE Classic 1K · 1024 bytes','MIFARE Classic 1K · 1024 字节'),body,555)
  flow('cardflow',('Card data and reader behavior','卡片数据与读头行为'),[(('Read','读取'),('UID + sectors + keys','UID + 扇区 + 密钥')),(('Check','检查'),('Complete test image','完整测试镜像')),(('Emulate / write','模拟 / 写入'),('Compatible test media','兼容测试介质')),(('Verify','验证'),('Reread + lab reader','回读 + 实验读头'))],('A matching UID alone does not establish a complete clone','UID 相同不等于完整复制'))
  body=text(35,95,t('Identifier lookup','标识符查询'),21,ORANGE,bold=True)+box(35,120,270,90,'ID',t('Static identifier','静态标识符'))+arrow(315,165,410,165)+box(425,120,530,90,t('Reader checks allowlist','读头查询允许列表'),t('Same ID may produce the same decision','相同 ID 可能得到相同判定'))
  body+=text(35,275,t('Authenticated exchange','认证交互'),21,GREEN,bold=True)+box(35,300,270,105,t('Challenge','挑战'),t('Fresh random value','新鲜随机数'),GREEN)+arrow(315,350,365,350)+box(380,300,270,105,t('Response','响应'),t('Uses a secret key','使用秘密密钥'),GREEN)+arrow(660,350,705,350)+box(720,300,235,105,t('Verify','验证'),t('Policy + freshness','策略 + 新鲜度'),GREEN)
  save('identifiers',t('An identifier is one input to a security decision','标识符是安全判定的一个输入'),body,450)
  body=box(35,95,270,110,t('IR transmitter','红外发射端'),t('Carrier bursts','成串载波脉冲'))+arrow(315,150,355,150)+box(370,95,270,110,t('IR receiver','红外接收端'),t('Demodulated envelope','解调后的包络'))+arrow(650,150,695,150)+box(710,95,255,110,t('Decoder','解码器'),t('Address + command','地址 + 命令'))
  for x in range(45,290,10):body+=f'<path d="M{x},265v-30h5v30h5" fill="none" stroke="{ORANGE}" stroke-width="2"/>'
  body+=f'<path d="M380,270v-35h65v35h65v-35h65v35h50" fill="none" stroke="{BLUE}" stroke-width="4"/>'
  body+=text(720,260,'Protocol / RAW',21)+text(720,292,t('Repeat / state','重复帧 / 状态'),18,MUTED)
  save('ir',t('Two time scales in an infrared signal','红外信号的两个时间尺度'),body,330)
  flow('hid',('USB / BLE HID trust boundary','USB / BLE HID 信任边界'),[(('Script','脚本'),('Visible text','可见文本')),(('HID reports','HID 报告'),('Keyboard events','键盘事件')),(('Host input','主机输入'),('Layout + focus','布局 + 焦点')),(('Application','应用'),('Active user context','当前用户上下文'))],('Observe in a blank editor; no shell or file access needed','在空白编辑器中观察，无需 shell 或文件访问'))
  body=box(45,100,300,200,'Flipper Zero',t('Selected UART','选定的 UART'))+box(655,100,300,200,t('3.3 V test board','3.3 V 测试板'),t('Separate power','独立供电'))
  body+=arrow(655,175,345,175,t('Board TX → Flipper RX','板 TX → Flipper RX'))+arrow(345,260,655,260,'GND ↔ GND')
  body+=text(500,335,t('Start with VCC and Flipper TX disconnected','开始时不接 VCC 和 Flipper TX'),21,ORANGE,'middle',True)
  body+=text(500,378,t('Confirm pin numbering and logic level before wiring','接线前确认引脚编号与逻辑电平'),19,MUTED,'middle')
  save('uart',t('Receive-only UART first','先进行只接收 UART 实验'),body,415)
  flow('wifi',('Wi-Fi requires external hardware','Wi-Fi 需要外部硬件'),[(('Flipper','Flipper'),('UI + matching app','界面 + 配套 App')),(('UART','UART'),('Commands + results','命令 + 结果')),(('ESP32 board','ESP32 扩展板'),('Board firmware','板载固件')),(('Lab AP','实验 AP'),('Test SSID / channel','测试 SSID / 信道'))],('Restore the board’s original firmware when returning to debugging','恢复调试用途时还原扩展板原固件'))
  flow('evidence',('A finding needs a control experiment','结论需要对照实验'),[(('Hypothesis','假设'),('Expected behavior','预期行为')),(('Baseline','基线'),('Known-good control','已知正常对照')),(('One change','一个改动'),('Repeat + record','重复 + 记录')),(('Conclusion','结论'),('Evidence + limits','证据 + 局限'))],('Record failures and negative results as carefully as successes','认真记录失败与阴性结果'))
  flow('app',('Small app architecture','小型 App 架构'),[(('Input callback','输入回调'),('Queue event','事件入队')),(('Main loop','主循环'),('Consume event','消费事件')),(('State','状态'),('Mutex protection','互斥保护')),(('Draw callback','绘图回调'),('Canvas / viewport','Canvas / viewport'))],('Exit → remove viewport → free resources → close GUI record','退出 → 移除视图 → 释放资源 → 关闭 GUI record'))
 # Decorative technical teaching illustration, same neutral labels for both languages.
 (root/'hero.svg').write_text('''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 460" role="img"><title>Flipper Zero teaching illustration</title><rect x="75" y="100" width="450" height="265" rx="60" fill="#fff" stroke="#183044" stroke-width="4"/><rect x="109" y="140" width="244" height="145" rx="10" fill="#ffb967" stroke="#d65716" stroke-width="3"/><text x="130" y="174" font-family="monospace" font-size="19" fill="#183044">SUB-GHZ / LAB</text><path d="M130 240h20v-33h23v33h28v-33h45v33h25v-33h23v33h36" fill="none" stroke="#183044" stroke-width="4"/><circle cx="438" cy="216" r="45" fill="#f3f6f8" stroke="#183044" stroke-width="3"/><path d="M426 183h24l-12-16zM426 249h24l-12 16zM405 204v24l-16-12zM471 204v24l16-12z" fill="#d65716"/><circle cx="438" cy="216" r="15" fill="#d65716"/><circle cx="493" cy="288" r="10" fill="#183044"/><rect x="371" y="323" width="103" height="13" rx="4" fill="#d65716"/><path d="M135 100V73h110v27M272 100V73h110v27" fill="none" stroke="#183044" stroke-width="4"/><path d="M129 356v27h169v-27" fill="none" stroke="#236a80" stroke-width="3"/><g font-family="monospace" font-size="17" fill="#526779"><text x="129" y="56">GPIO / UART</text><text x="125" y="412">NFC / RFID ANTENNA</text><text x="368" y="399">USB / HID</text><text x="358" y="43">RF • IR • I/O</text></g><path d="M487 80q25 10 25 30M500 61q38 13 38 46" fill="none" stroke="#d65716" stroke-width="4"/></svg>''')
