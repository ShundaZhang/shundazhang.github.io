"""Original bilingual process illustrations; not screenshots or hardware traces."""
from html import escape as e

def build_case_diagrams(root):
    for zh in (False, True):
        def t(en, cn): return cn if zh else en
        def text(x,y,label,size=24,color='#183044',bold=False):
            return f'<text x="{x}" y="{y}" text-anchor="middle" font-size="{size}" fill="{color}"'+(' font-weight="700"' if bold else '')+'>'+e(label)+'</text>'
        def box(x,y,w,title,detail,accent=False):
            color='#c74c0b' if accent else '#236a80'
            return f'<rect x="{x}" y="{y}" width="{w}" height="100" rx="12" fill="white" stroke="{color}" stroke-width="2"/>'+text(x+w/2,y+39,title,25,color,True)+text(x+w/2,y+74,detail,21)
        def arrow(x1,y1,x2,y2):
            return f'<path d="M{x1} {y1} L{x2} {y2}" fill="none" stroke="#526779" stroke-width="2.5" marker-end="url(#arrow)"/>'
        def save(name,title,body,height):
            svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 680 {height}" role="img" aria-labelledby="title desc"><title id="title">{e(title)}</title><desc id="desc">{e(t("Original teaching workflow, not a hardware test result.","原创教学流程图，不是硬件实测结果。"))}</desc><defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto"><path d="M0 0L10 5L0 10Z" fill="#526779"/></marker></defs><rect width="680" height="{height}" fill="#f3f7fa"/><g font-family="system-ui,sans-serif">{body}</g></svg>'
            (root/(name+('.zh' if zh else '')+'.svg')).write_text(svg)
        title=t('Nice FLOR-S: capture → encode → verify','Nice FLOR-S：捕获 → 编码 → 验证')
        body=text(340,48,title,25,bold=True)
        items=[(t('Back up → install Unleashed','备份 → 安装 Unleashed'),t('Release + matching SD assets','Release + 匹配的 SD 资源')),
               (t('Sub-GHz → Read → Save','Sub-GHz → Read → Save'),t('433.92 MHz · matching AM/OOK','433.92 MHz · 匹配 AM/OOK')),
               (t('Decoded private capture','私有解码捕获'),t('Serial · Button · Counter','Serial · Button · Counter')),
               (t('Saved → Emulate → Send','Saved → Emulate → Send'),t('Encoder + counter-state policy','编码器 + 计数器状态策略')),
               (t('Your receiver: accept or reject?','自有接收器：接受还是拒绝？'),t('Identity + freshness + enrollment','身份 + 新鲜度 + 注册状态'))]
        for i,(a,b) in enumerate(items):
            y=85+i*145
            body+=box(45,y,590,a,b,accent=i==3)
            if i<4:body+=arrow(340,y+107,340,y+137)
        body+=text(340,823,t('RAW playback ≠ a new rolling-code frame','RAW 重放 ≠ 生成新的滚动码帧'),22,'#c74c0b',True)
        body+=text(340,864,t('Failure? Stop TX; check receiver synchronization','失败？停止发射，检查接收端同步'),22)
        save('nice-worked',title,body,900)
        title=t('M1 / Classic: emulation vs physical copy','M1 / Classic：模拟与实体复制')
        body=text(340,48,title,25,bold=True)
        body+=box(45,85,590,t('Read your Classic 1K card','读取自有 Classic 1K 卡'),t('NFC → Read · 16 sectors · known keys','NFC → Read · 16 扇区 · 已知密钥'))
        body+=arrow(340,192,340,222)
        body+=box(45,230,590,t('Save the complete private image','私有保存完整镜像'),t('More → Save · preserve .nfc baseline','More → Save · 保留 .nfc 基线'))
        body+=f'<path d="M340 337V365H180V391M340 365H500V391" fill="none" stroke="#526779" stroke-width="2.5"/>'
        body+=arrow(180,373,180,393)+arrow(500,373,500,393)
        body+=box(30,405,300,t('Flipper emulation','Flipper 模拟'),t('Saved → Emulate','Saved → Emulate'))
        body+=box(350,405,300,t('Magic blank','Magic 空白卡'),t('Check Magic Tag','Check Magic Tag'))
        body+=arrow(180,512,180,542)+arrow(500,512,500,542)
        body+=box(30,550,300,t('Hold at lab reader','贴近实验读头'),t('Inspect .shd changes','检查 .shd 变化'))
        body+=box(350,550,300,t('More → Write','More → Write'),t('Image → blank → reread','镜像 → 空白卡 → 回读'))
        body+=f'<path d="M180 657V685H500V657" fill="none" stroke="#526779" stroke-width="2.5"/>'+arrow(340,685,340,715)
        body+=box(45,725,590,t('Verify on the authorized reader','在授权读头独立验证'),t('UID + authentication + application data','UID + 认证 + 应用数据'),True)
        body+=text(340,875,t('UID only ≠ complete copy','只有 UID ≠ 完整复制'),23,'#c74c0b',True)
        body+=text(340,915,t('Write to Initial Card ≠ write a new blank','Write to Initial Card ≠ 写入新空白卡'),21)
        save('m1-worked',title,body,950)
