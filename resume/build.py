"""Build the public, bilingual technical résumé from curated publishable text."""
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parent
TALK='https://archive.fosdem.org/2022/schedule/event/tee_sgx_analysis/'
def build(lang):
    t=lambda en,zh:zh if lang=='zh' else en
    home='/index.zh.html' if lang=='zh' else '/'
    ctf='/ctf/index.zh.html' if lang=='zh' else '/ctf/'
    labels=[('experience',t('Experience','工作经历')),('projects',t('Selected projects','项目经历')),('talks',t('Talks & teaching','演讲与教学')),('background',t('Technical background','技术背景'))]
    body=f'''<header class="profile"><p class="kicker">{t('TECHNICAL RÉSUMÉ','技术履历')}</p><h1>ShundaZhang</h1><p class="specialty">{t('Systems & hardware security · Confidential computing · Cryptography','系统与硬件安全 · 机密计算 · 密码学')}</p>
<p>{t('I work on hardware and systems security at ByteDance, with a focus on cryptography, chip security, trusted execution and platform trust. Previously at Intel, I worked as a technical lead, security researcher and cloud security engineer on SGX, TDX and their software stacks. My experience combines security architecture review, hands-on validation and low-level software engineering.','我目前在字节跳动从事硬件与系统安全工作，关注密码学、芯片安全、可信执行及平台信任。此前在 Intel 担任技术负责人、安全研究员和云安全工程师，长期参与 SGX、TDX 及其软件栈的工作，结合安全架构审查、实战验证与底层软件工程。')}</p>
<nav class="profile-links" aria-label="{t('Profile links','个人页面')}"><a href="https://github.com/ShundaZhang">GitHub</a><a href="{ctf}">{t('CTF record','CTF 记录')}</a><a href="{home}">{t('Projects & learning notes','项目与学习笔记')}</a></nav></header>
<nav class="contents" aria-label="{t('On this page','本页目录')}">{''.join(f'<a href="#{ident}">{label}</a>' for ident,label in labels)}</nav>
<section id="experience"><h2>{labels[0][1]}</h2>
<article class="experience" id="bytedance"><h3>ByteDance <span>{t('Hardware & systems security · 2024–present','硬件与系统安全 · 2024–至今')}</span></h3>
<p>{t('GM/SM cryptography, post-quantum cryptography (PQC), chip security architecture and security testing, side-channel security testing, TEE architecture, trusted boot and remote attestation.','国密、抗量子密码（PQC）、芯片安全架构与安全测试、侧信道安全测试、TEE 架构、可信启动与远程证明。')}</p>
<p class="confidential">{t('Further details are not publicly available at this time because they involve company-confidential information.','具体细节涉及公司机密，目前不便公开。')}</p></article>
<article class="experience"><h3>Intel <span>{t('Technical lead · Security researcher · Cloud security engineer · 2007–2024','技术负责人 · 安全研究员 · 云安全工程师 · 2007–2024')}</span></h3>
<p>{t('Led security validation for SGX SDK, Platform Software (PSW) and Data Center Attestation Primitives (DCAP), including TDX attestation software. Responsibilities included security development lifecycle (SDL), architecture review, threat modeling, penetration testing, fuzzing, code review and vulnerability remediation across Windows and Linux. Supported cloud adoption of SGX and TDX and translated deployment requirements into software work.','负责 SGX SDK、平台软件（PSW）及数据中心认证原语（DCAP）的安全验证，包括 TDX 认证软件。工作涵盖安全开发生命周期（SDL）、架构审查、威胁建模、渗透测试、模糊测试、代码审查及漏洞修复，覆盖 Windows 与 Linux。支持 SGX/TDX 的云端部署，并将部署需求转化为软件开发工作。')}</p></article>
<article class="experience compact"><h3>ZTE <span>{t('Software engineer · 2006–2007','软件开发工程师 · 2006–2007')}</span></h3><p>{t('Software development at the Shanghai R&D center, before joining Intel in 2007.','在上海研发中心从事软件开发，随后于 2007 年加入 Intel。')}</p></article></section>
<section id="projects"><h2>{labels[1][1]}</h2><p class="section-note">{t('Selected work from my Intel experience','Intel 经历中的部分项目')}</p>
<ul class="project-list">
<li><strong>{t('SGX / TDX security validation','SGX / TDX 安全验证')}</strong> — {t('Led a security engineering team in validating enclave and attestation software. Developed validation tools and reproducible attack proofs of concept, reviewed security boundaries and worked with developers on mitigations.','带领安全工程团队验证 Enclave 与认证软件，开发安全验证工具和可复现攻击 PoC，审查安全边界，并与开发团队协作完成缓解与修复。')}</li>
<li><strong>{t('SGX SDK and systems software','SGX SDK 与系统软件')}</strong> — {t('Development and testing of SDK/driver components, cryptographic integration including OpenSSL and GM/SM, protected file access and dynamic memory management. Helped deliver trusted-library capabilities for networking, I/O, filesystems and threading.','参与 SDK/驱动组件开发与测试，涵盖 OpenSSL 与国密集成、安全文件访问和动态内存管理；支持网络、I/O、文件系统及线程等可信库能力的交付。')}</li>
<li><strong>{t('Cloud confidential computing','云端机密计算')}</strong> — {t('Supported Chinese cloud providers in deploying Intel SGX and TDX, including attestation integration, security assessment and SDK requirements for enclave-based application runtimes.','支持国内云计算厂商部署 Intel SGX 与 TDX，涉及认证集成、安全评估，以及基于 Enclave 的应用运行时所需 SDK 能力。')}</li>
</ul></section>
<section id="talks"><h2>{labels[2][1]}</h2><ul>
<li><a href="{TALK}">SGX Enclave Exploit Analysis and Considerations for Defensive SGX Programming</a> <span class="meta">· FOSDEM 2022</span><br><span class="detail">{t('Enclave attack analysis and defensive programming; the conference page includes slides and recordings.','Enclave 攻击分析与防御编程；会议页面包含演示文稿及录像。')}</span></li>
<li>{t('Instructor for advanced exploitation (SANS SEC660 / GXPN preparation), advanced secure coding and applied cryptography; contributed to security training and CTF activities at Intel.','担任高级漏洞利用（SANS SEC660 / GXPN 备考）、高级安全编码及应用密码学课程讲师，参与 Intel 安全培训与 CTF 活动建设。')}</li>
<li>{t('Contributed to the Anolis confidential computing SIG and TEE-related security and patent review.','参与龙蜥（Anolis）机密计算 SIG，以及 TEE 相关安全与专利审查。')}</li>
</ul></section>
<section id="background"><h2>{labels[3][1]}</h2>
<p><strong>{t('Engineering','工程能力')}</strong> — {t('C/C++, Python and x86 assembly; Intel architecture, low-level software, security testing and cryptographic implementation review.','C/C++、Python 与 x86 汇编；Intel 架构、底层软件、安全测试及密码实现审查。')}</p>
<p><strong>{t('Security domains','安全方向')}</strong> — {t('SGX / TDX, attestation and confidential computing; familiarity with AMD SEV, Arm TrustZone and RISC-V Keystone. Cryptography, threat modeling, penetration testing, fuzzing and secure code review.','SGX / TDX、认证与机密计算；熟悉 AMD SEV、Arm TrustZone 及 RISC-V Keystone。密码学、威胁建模、渗透测试、模糊测试与安全代码审查。')}</p>
<p><strong>{t('Professional credentials','专业资质')}</strong> — GXPN; Intel Product Security Expert; Intel Security Brown Belt.</p>
<p><strong>{t('Security practice','攻防实践')}</strong> — {t('HTB Labs Grandmaster, with a particular focus on Crypto and OSINT; captain of 59x101. My CTF page documents team results, including All blue’s 12th-place finish at HTB Business CTF 2024.','HTB Labs Grandmaster，重点关注 Crypto 与 OSINT，担任 59x101 队长。CTF 页面整理团队战绩，包括 All blue 在 HTB Business CTF 2024 的全球第 12 名。')} <a href="{ctf}">{t('Competition record →','竞赛记录 →')}</a></p>
<h3 class="education-title">{t('Education','教育背景')}</h3><ul class="education">
<li>{t('Master’s in Computer Architecture','计算机系统结构硕士')} · {t('Huazhong University of Science and Technology','华中科技大学')} <span class="meta">· 2006</span></li>
<li>{t('Second bachelor’s degree in Computer Science and Technology','计算机科学与技术第二学士学位')} · {t('Huazhong University of Science and Technology','华中科技大学')} <span class="meta">· 2002</span></li>
<li>{t('Bachelor’s in Materials Science and Engineering','材料科学与工程学士')} · {t('Wuhan University of Technology','武汉理工大学')} <span class="meta">· 2003</span></li>
</ul></section>'''
    html=f'''<!doctype html>
<html lang="{'zh-CN' if lang=='zh' else 'en'}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#ffffff"><meta name="description" content="{t('Technical résumé of ShundaZhang: systems and hardware security, SGX/TDX, confidential computing, cryptography and security validation.','ShundaZhang 技术履历：系统与硬件安全、SGX/TDX、机密计算、密码学及安全验证。')}"><title>{t('Résumé','技术履历')} · ShundaZhang</title><link rel="icon" href="../favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="style.css"><script src="../language.js"></script></head>
<body><a class="skip" href="#main">{t('Skip to content','跳至正文')}</a><div class="topbar"><div class="wrap"><a class="back" href="{home}">← {t('Personal home','个人主页')}</a><nav aria-label="{t('Language selection','语言选择')}" class="languages"><a href="index.html" data-atlas-lang="en" {'aria-current="page"' if lang=='en' else ''}>EN</a><a href="index.zh.html" data-atlas-lang="zh" {'aria-current="page"' if lang=='zh' else ''}>中文</a></nav></div></div><main class="wrap" id="main">{body}</main><footer class="wrap"><span>© 2026 ShundaZhang</span><span>{t('Updated 1 Oct 2026','更新于 2026 年 10 月 1 日')}</span></footer></body></html>'''
    html=re.sub(r'&(?!#\d+;|#x[0-9a-fA-F]+;|[A-Za-z]+;)', '&amp;', html)
    (ROOT/('index.zh.html' if lang=='zh' else 'index.html')).write_text(html,encoding='utf-8')
if __name__=='__main__':
    for language in ('en','zh'):build(language)
    print('Built 2 bilingual résumé pages from curated public content')
