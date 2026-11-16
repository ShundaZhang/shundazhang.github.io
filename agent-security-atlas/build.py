"""Build the bilingual static Agent Security Atlas."""
from html import escape
from pathlib import Path

from figures import (
    architecture_references,
    attestation_exchange,
    context_flow,
    deployment_architecture,
    identity_exchange,
    kata_stack,
    runtime_boundaries,
    sandbox_lifecycle,
    support_request,
    tool_exchange,
)

ROOT = Path(__file__).resolve().parent


def build(zh):
    def t(en, cn):
        return cn if zh else en

    def paragraph(en, cn):
        return f'<p>{t(en, cn)}</p>'

    def source(url, name):
        return f'<a href="{url}" target="_blank" rel="noopener noreferrer">{name} ↗</a>'

    def refs(*items):
        return '<p class="refs">' + ' · '.join(source(*item) for item in items) + '</p>'

    def table(headings, rows):
        head = ''.join(f'<th scope="col">{t(*name)}</th>' for name in headings)
        body = ''.join(
            '<tr>' + ''.join(
                f'<{"th" if i == 0 else "td"}{" scope=row" if i == 0 else ""}>{t(*cell)}</{"th" if i == 0 else "td"}>'
                for i, cell in enumerate(row)
            ) + '</tr>' for row in rows
        )
        return f'<div class="table-scroll" tabindex="0" role="region" aria-label="{t("Scrollable comparison", "可滚动的对照表")}"><table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'

    def list_items(items):
        return '<ul class="explain">' + ''.join(
            f'<li><strong>{t(*name)}</strong> {t(*body)}</li>' for name, body in items
        ) + '</ul>'

    def code(value):
        return f'<pre><code>{escape(value)}</code></pre>'

    sections = [
        ('threats', 'Threat model', '威胁模型'),
        ('isolation', 'Runtime isolation', '运行隔离'),
        ('identity', 'Agent identity', 'Agent 身份与管理'),
        ('permissions', 'Tools & credentials', '工具与凭据'),
        ('data', 'Obfuscation & data', '混淆与数据'),
        ('products', 'Product practices', '产品做法'),
        ('design', 'Deployment', '部署设计'),
        ('lab', 'Policy lab', '策略实验'),
    ]

    def section(index, lead, body):
        ident, en, cn = sections[index]
        return f'<section class="chapter" id="{ident}"><header><h2>{t(en, cn)}</h2><p>{t(*lead)}</p></header>{body}</section>'

    title = t('AI Agent Security', 'AI Agent 安全')
    nav = ''.join(f'<a href="#{ident}">{t(en, cn)}</a>' for ident, en, cn in sections)
    hero = f'''<section class="hero">
      <div class="hero-copy">
        <p class="updated"><span></span>{t('TECHNICAL SURVEY · 15 NOV 2026', '技术调研 · 2026 年 11 月 15 日')}</p>
        <h1>{t('AI Agent<br>Security', 'AI Agent<br>安全与隔离')}</h1>
        <p>{t('Control what an agent can read, run, and send. A guide to workload identity, cloud sandboxes, tool authorization, and protecting sensitive context.', '控制 Agent 能读什么、运行什么、向哪里发送数据。系统整理工作负载身份、云端沙箱、工具授权与敏感上下文保护。')}</p>
        <div class="actions"><a href="#isolation">{t('Explore isolation', '查看隔离技术')} ↓</a><a href="#products">{t('Compare products', '对照业界产品')} ↓</a></div>
      </div>
      <figure class="boundary">
        <figcaption>{t('TRUST BOUNDARIES', '信任边界')}</figcaption>
        <ol>
          <li><span>01</span><div><strong>{t('Untrusted content', '不可信内容')}</strong><small>{t('Web · files · tool responses', '网页 · 文件 · 工具返回值')}</small></div></li>
          <li><span>02</span><div><strong>{t('Agent harness', 'Agent Harness')}</strong><small>{t('Context assembly · proposed actions', '组装上下文 · 提出操作')}</small></div></li>
          <li><span>03</span><div><strong>{t('Policy broker', '授权网关')}</strong><small>{t('Identity · scope · approval · audit', '身份 · 权限范围 · 审批 · 审计')}</small></div></li>
          <li><span>04</span><div><strong>{t('Isolated execution', '隔离执行')}</strong><small>{t('Sandbox · egress proxy · scoped tools', '沙箱 · 出口代理 · 受限工具')}</small></div></li>
        </ol>
        <a class="drawing-link" href="#agent-system-diagram">{t('See the full architecture', '查看完整架构图')} ↓</a>
      </figure>
    </section>'''

    threats = section(0, (
        'A cloud agent crosses trust boundaries whenever it reads a document, reuses state, runs code, or acts under a user’s identity.',
        '云端 Agent 读文档、复用状态、执行代码或代用户操作时，都会跨越不同的信任边界。',
    ), table(
        [('Entry point', '入口'), ('Example failure', '失效示例'), ('Where to enforce', '在哪里拦截')],
        [
            [('Documents / web / RAG', '文档 / 网页 / RAG'), ('A webpage tells a support agent to paste a private order into a search query.', '网页诱导客服 Agent 把私有订单写进搜索请求。'), ('Tag origins and constrain data sent to public search.', '标记来源，并限制可发送到公开搜索的数据。')],
            [('Tools / MCP / subagents', '工具 / MCP / 子 Agent'), ('A tool response requests a second call with broader permissions.', '工具返回值诱导 Agent 发起权限更大的第二次调用。'), ('Authorize each action independently with identity, resource and argument checks.', '为每次操作独立检查身份、目标资源和参数。')],
            [('Code and browser', '代码与浏览器'), ('A dependency reads mounted secrets or a logged-in browser transfers data.', '依赖读取挂载的秘密，或已登录浏览器将数据传出。'), ('Separate code and browser profiles, restrict files and network, keep secrets in a broker.', '分离代码沙箱与浏览器会话，限制文件和网络，凭据由网关保管。')],
            [('Memory / snapshots', '记忆 / 快照'), ('Poisoned memory persists or a restored image exposes another tenant’s state.', '被污染的记忆跨会话保留，或恢复快照时暴露其他租户状态。'), ('Enforce tenant ACLs on retrieval, writes, snapshot restore and deletion.', '在检索、写入、快照恢复与删除时执行租户 ACL。')],
            [('Supply chain / runaway loops', '供应链 / 失控循环'), ('A new skill adds an executable or a retry loop repeats a costly write.', '新技能携带可执行程序，或重试循环反复提交高成本写操作。'), ('Pin and review packages, bound depth/cost, and make writes idempotent.', '固定并审查依赖版本，限制深度与成本，让写操作具备幂等性。')],
        ],
    ) + refs(
        ('https://genai.owasp.org/risk-maps-supported/top-10-for-agentic-apps-2026/', 'OWASP Agentic Top 10'),
        ('https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html', 'OWASP AI Agent Security'),
    ))

    adoption = '<div class="adoption" id="tee-adoption"><h3>' + t(
        'How widely are TEEs used?', 'TEE 的采用有多广？',
    ) + '</h3>' + paragraph(
        'Confidential computing is already used in commercial AI, but it was less common than network and access isolation, containers in VMs, and microVM sandboxes in the Linux Foundation’s November 2026 survey.',
        '机密计算已经用于商用 AI。Linux Foundation 2026 年 11 月发布的调查显示，其采用范围仍小于网络与访问隔离、VM 内的容器和 microVM 沙箱。',
    ) + table(
        [('AI workload isolation', 'AI 工作负载的隔离措施'), ('In use', '已使用'), ('Planned', '计划使用')],
        [
            [('Network and access isolation', '网络与访问隔离'), ('57%', '57%'), ('55%', '55%')],
            [('Containers inside VMs', '在 VM 内运行容器'), ('40%', '40%'), ('41%', '41%')],
            [('Hardware-level VM isolation', '硬件级 VM 隔离'), ('35%', '35%'), ('31%', '31%')],
            [('Namespace containers on bare metal', '裸机上的 Namespace 容器隔离'), ('33%', '33%'), ('34%', '34%')],
            [('MicroVM sandboxing', 'MicroVM 沙箱'), ('20%', '20%'), ('30%', '30%')],
            [('Confidential computing', '机密计算（TEE 类方案）'),
             ('<strong>12%</strong>', '<strong>12%</strong>'), ('<strong>26%</strong>', '<strong>26%</strong>')],
        ],
    ) + paragraph(
        'The survey covers organizations’ AI workloads, including workloads beyond agents. Respondents could select multiple measures. After excluding “don’t know” responses, 435 answered the current-use question and 381 answered the planning question. The 26% reflects intent for the following year. The 12% describes this sample, while the global share of agent deployments using a TEE remains unknown.',
        '调查覆盖组织的 AI 工作负载，范围比 Agent 更广。答卷者可以多选。排除“不确定”后，已使用题有 435 份有效答卷，计划使用题有 381 份。26% 反映未来一年的使用意向，12% 是该样本中报告已经使用的比例。全球 Agent 部署的 TEE 采用率仍未知。',
    ) + refs((
        'https://www.cncf.io/wp-content/uploads/2026/11/Virtual-Machines_Report_2026.pdf#page=11',
        t('Linux Foundation survey · Figure 5', 'Linux Foundation 调查 · 图 5'),
    )) + paragraph(
        'In a separate Agent security survey by NeuralTrust, 164 respondents reported activity monitoring (42%), role-based access control (38%), data loss prevention (31%), and prompt-injection filtering (27%). These figures describe a different sample and question.',
        'NeuralTrust 另一项针对 Agent 安全的调查中，164 名答卷者报告的措施包括活动监控（42%）、基于角色的访问控制（38%）、数据防泄漏（31%）和提示注入过滤（27%）。这组结果来自不同的样本与题目。',
    ) + refs((
        'https://a.storyblok.com/f/322249/x/8af0a54178/the-state-of-ai-agent-security-2026.pdf#page=16',
        t('NeuralTrust Agent security survey · Q9', 'NeuralTrust Agent 安全调查 · 第 9 题'),
    )) + paragraph(
        'Tool permissions, approvals and egress checks govern what an agent can do. If a webpage persuades a TDX-protected agent to send customer data to an unapproved destination, the egress policy must still block that request. A TEE addresses a separate threat: privileged infrastructure reading plaintext or keys in use. Remote attestation can make data and key delivery conditional on a verified workload, which is why confidential inference, sensitive data processing and key custody are useful early applications.',
        '工具权限、审批与出口策略控制 Agent 能做什么。即使 Agent 跑在 TDX 中，恶意网页诱导它向未经授权的地址发送客户数据时，仍需出口策略拦截请求。TEE 的额外用途是约束有特权的基础设施读取正在处理的明文或密钥，并通过远程证明把数据与密钥交付绑定到通过验证的工作负载。因此，机密推理、敏感数据处理和密钥托管是典型应用。',
    ) + refs(
        ('https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html', 'OWASP AI Agent Security'),
        ('https://security.apple.com/blog/expanding-pcc', 'Apple PCC'),
    ) + '</div>'

    def implementation(en, cn, *links):
        references = ' · '.join(source(url, t(*label)) for url, label in links)
        return en + '<br>' + references, cn + '<br>' + references

    tee_cases = '<div class="tee-cases" id="tee-products"><h3>' + t(
        'Where commercial products use TEEs', '哪些商用产品用了 TEE',
    ) + '</h3>' + paragraph(
        'Code sandboxes protect the host from agent-generated code. Confidential computing adds a different protection: it limits what privileged infrastructure can see of the workload’s data while it is running. Check which component is protected and whether the evidence is bound to the endpoint receiving plaintext.',
        '代码沙箱保护宿主免受 Agent 生成代码的影响。机密计算还提供另一方向的保护，限制具有基础设施特权的一方在运行期间能看到的工作负载数据。选型时要查清哪个组件受保护，以及证明是否绑定到接收明文的端点。',
    ) + table(
        [('Product', '产品'), ('Scope and maturity', '保护范围与状态'), ('Published implementation', '公开实现')],
        [
            [
                ('Apple Intelligence · PCC', 'Apple Intelligence · PCC'),
                ('Selected cloud inference workflows in Apple Intelligence.', 'Apple Intelligence 的特定云端推理任务。'),
                implementation(
                    'Apple silicon PCC nodes use Secure Enclave and Secure Boot as roots of trust. The device verifies node credentials and encrypts to the verified nodes. The June 2026 Google Cloud expansion uses Intel TDX, NVIDIA Confidential Computing and Titan. Apple documents separate confidential VMs for attested keys.',
                    'Apple silicon PCC 节点以 Secure Enclave 和 Secure Boot 为信任基础。设备验证节点凭据，再把请求加密给已验证的节点。2026 年 6 月公布的 Google Cloud 扩展采用 Intel TDX、NVIDIA Confidential Computing 和 Titan，并用独立机密 VM 保存经过证明的密钥。',
                    ('https://security.apple.com/blog/private-cloud-compute/', ('Apple PCC', 'Apple PCC')),
                    ('https://security.apple.com/blog/expanding-pcc', ('Google Cloud expansion', 'Google Cloud 扩展')),
                ),
            ],
            [
                ('Google Private AI Compute', 'Google Private AI Compute'),
                ('Selected Pixel features such as Magic Cue and Recorder summaries. This is Google’s own serving system.', 'Pixel 的部分功能，例如 Magic Cue 与 Recorder 摘要。这里指 Google 自己的推理服务。'),
                implementation(
                    'Google documents an AMD-based CPU TEE and a hardened Cloud TPU path based on Titanium Intelligence Enclave. Trusted nodes attest peers and encrypt traffic across the inference pipeline.',
                    'Google 文档说明 CPU 侧采用基于 AMD 的 TEE，TPU 侧采用基于 Titanium Intelligence Enclave 的加固链路。可信节点相互证明并加密传输推理数据。',
                    ('https://blog.google/innovation-and-ai/products/google-private-ai-compute/', ('Pixel features', 'Pixel 功能')),
                    ('https://services.google.com/fh/files/misc/private_ai_compute_technical_brief.pdf', ('Technical brief', '技术简报')),
                ),
            ],
            [
                ('OpenAI Private Inference', 'OpenAI Private Inference'),
                ('API preview for eligible inference workflows.', '面向符合条件的推理工作流，处于 API 预览。'),
                implementation(
                    'OpenAI describes confidential computing for prompts and responses during model processing. Its public overview leaves CPU/GPU details and client attestation unspecified. The scope described is inference.',
                    'OpenAI 公开说明用机密计算保护模型处理中的提示和响应。公开概述未列出 CPU / GPU 和客户端证明细节，所述范围是推理链路。',
                    ('https://openai.com/business/private-intelligence/', ('Private Intelligence', 'Private Intelligence')),
                ),
            ],
            [
                ('Phala Cloud / dstack', 'Phala Cloud / dstack'),
                ('Deployable platform for confidential Agent applications.', '可部署机密 Agent 应用的平台。'),
                implementation(
                    'Run the Agent workload in a measured TDX confidential VM. dstack can release application keys after attestation. Any remote model API or SaaS that receives plaintext sits in its own trust domain.',
                    '将 Agent 应用放入受度量的 TDX 机密 VM，dstack 可在证明通过后发放应用密钥。收到明文的远端模型 API 或 SaaS 处于各自的信任域。',
                    ('https://github.com/dstack-TEE/dstack', ('dstack', 'dstack')),
                    ('https://phala.com/solutions/ai-agents', ('Agent deployment', 'Agent 部署')),
                ),
            ],
            [
                ('Agents on NEAR Intents', 'Agents on NEAR Intents'),
                ('An Agent API with a documented, publicly verifiable TEE endpoint.', '提供公开验证端点的 Agent API。'),
                implementation(
                    'The API, database and TLS termination run inside an Intel TDX VM. Its attestation endpoint binds the client nonce and the API TLS key to the quote. The application documents its separate wallet and policy boundary.',
                    'API、数据库和 TLS 终止都在 Intel TDX VM 内。证明端点把客户端 nonce 和 API TLS 密钥绑定到 Quote。钱包及授权策略有独立的边界。',
                    ('https://docs.agentsonintents.com/integration/agent-api/tee', ('Verify the TDX quote', '验证 TDX Quote')),
                ),
            ],
            [
                ('Microsoft Azure Confidential AI', 'Microsoft Azure Confidential AI'),
                ('Infrastructure for customer-deployed confidential AI.', '供客户部署机密 AI 的基础设施。'),
                implementation(
                    'Azure documents SEV-SNP or TDX confidential VMs, confidential containers and NVIDIA confidential GPUs. Verify what the selected workload actually puts inside its TEE, including where TLS terminates.',
                    'Azure 提供 SEV-SNP 或 TDX 机密 VM、机密容器和 NVIDIA 机密 GPU。需要核对所选部署实际将哪些组件放进 TEE，以及 TLS 在哪里终止。',
                    ('https://learn.microsoft.com/en-us/azure/confidential-computing/confidential-ai', ('Azure Confidential AI', 'Azure Confidential AI')),
                ),
            ],
        ],
    )
    tee_cases += paragraph(
        'The AgentCore Firecracker, Vercel microVM and GKE gVisor examples in Product Practices document execution isolation. Verify TEE coverage separately from their sandbox descriptions. For an attested deployment, check hardware endorsements, accepted measurements and TCB status, freshness, and the binding to the TLS or key-release public key. Tool authorization and egress controls still govern what measured code can send.',
        '「产品做法」里的 AgentCore Firecracker、Vercel microVM 和 GKE gVisor 是公开文档中的执行隔离做法。TEE 覆盖范围需要单独核对。验证部署时，应检查硬件背书、允许的度量和 TCB 状态、证明新鲜度，以及证据是否绑定 TLS 或密钥发放的公钥。经度量的代码仍需工具授权和出口控制。',
    ) + attestation_exchange(zh) + '<p><a href="#tee-adoption">' + t(
        'See how TEE adoption compares with other controls', '查看 TEE 与其他防护措施的采用率对照',
    ) + ' ↓</a></p></div>'

    runtime_background = '<div class="runtime-background" id="microvm-kata"><h3>' + t(
        'Background: microVM and Kata Containers', '背景知识：microVM 与 Kata Containers',
    ) + '</h3>' + list_items([
        (('MicroVM is a lightweight virtual machine.', 'microVM 是轻量虚拟机。'),
         ('It boots its own guest kernel. A virtual machine monitor (VMM) configures the guest’s virtual CPUs, memory and devices. Firecracker is one implementation: it uses KVM and keeps the device model small, with virtio network, block and vsock devices. Trimming the device model helps reduce startup overhead and the amount of device code exposed to the guest.',
          '它会启动独立的 Guest 内核。虚拟机监控器（VMM）配置 Guest 的虚拟 CPU、内存和设备。Firecracker 是一个实现，使用 KVM，并提供精简的 virtio 网络、块设备和 vsock。精简设备模型有助于降低启动开销并缩小 Guest 可触及的设备代码范围。')),
        (('Kata Containers is a container runtime.', 'Kata Containers 是容器运行时。'),
         ('It brings the VM boundary to Kubernetes Pods. A Pod’s <code>runtimeClassName</code> can select a configured Kata runtime handler. In a typical Kubernetes deployment, each Kata Pod gets one VM, and its containers run inside that VM. Kata supports VMM backends such as QEMU, Cloud Hypervisor and Firecracker, subject to the installed configuration and feature support.',
          '它把 VM 隔离接入 Kubernetes Pod。Pod 的 <code>runtimeClassName</code> 可以选择已配置的 Kata 运行时。在典型 Kubernetes 部署中，一个 Kata Pod 对应一台 VM，容器在该 VM 内运行。Kata 可使用 QEMU、Cloud Hypervisor、Firecracker 等 VMM，具体组合取决于已安装的运行时和功能支持。')),
    ]) + runtime_boundaries(zh) + '<div class="runtime-comparison">' + table(
        [('Deployment', '部署方式'), ('Kernel used by the workload', '工作负载使用的内核'), ('Typical management unit', '典型管理单位')],
        [
            [('Conventional container', '普通容器'), ('Shared host kernel', '共享宿主内核'),
             ('A container, optionally inside a Pod', '容器，也可由 Pod 编排')],
            [('Direct microVM', '直接运行 microVM'), ('Independent kernel per VM', '每台 VM 有独立内核'),
             ('A VM, e.g. one per Agent job', 'VM，例如每个 Agent 任务分配一台')],
            [('Kata Containers', 'Kata Containers'), ('Guest kernel shared by containers in the same Pod VM', '同一 Pod VM 内的容器共享 Guest 内核'),
             ('Typically one VM per Kubernetes Pod', '典型部署中每个 Kubernetes Pod 对应一台 VM')],
        ],
    ) + '</div>' + paragraph(
        'A <strong>microVM</strong> is a lightweight VM. <strong>Kata</strong> is the runtime that places a Pod inside a VM. A supported Kata deployment can use Firecracker to run that VM.',
        '<strong>microVM</strong> 是轻量虚拟机。<strong>Kata</strong> 是把 Pod 放进虚拟机运行的容器运行时。在支持的部署中，Kata 可以用 Firecracker 启动这台 VM。',
    ) + kata_stack(zh) + paragraph(
        'For a threat model that includes privileged host access to guest data, select a supported confidential VM configuration and verify its attestation separately.',
        '如果威胁模型包含宿主特权方读取 Guest 数据，还需选择支持机密计算的 VM 配置，并单独验证远程证明。',
    ) + refs(
        ('https://github.com/kata-containers/kata-containers/blob/main/docs/hypervisors.md', 'Kata VMM Backends'),
        ('https://shundazhang.github.io/tee-tdx-sgx/' + ('coco.zh.html' if zh else 'coco.html'), 'CoCo / TEE'),
    ) + '</div>'

    isolation = section(1, (
        'Start by deciding which code runs, who can supply it, and whose secrets and state it could reach.',
        '先确定运行什么代码、谁能提供代码，以及代码可能接触哪些租户的秘密和运行状态。',
    ), runtime_background + table(
        [('Boundary', '隔离边界'), ('Mechanism and fit', '机制与适用场景'), ('What to configure', '必须检查的配置')],
        [
            [('Process / Linux container', '进程 / Linux 容器'), ('Namespaces isolate views, cgroups bound resources, and seccomp plus an LSM constrain kernel access. Suitable for controlled workloads with a shared host kernel.', 'Namespace 隔离资源视图，cgroups 限定配额，seccomp 与 LSM 收窄内核访问。适合可控且接受共享宿主内核的负载。'), ('Run without privilege, drop capabilities, restrict mounts and block access to the container runtime socket.', '非特权运行，收紧 capabilities 和挂载，禁止访问容器运行时 socket。')],
            [('gVisor', 'gVisor'), ('Sentry implements a Linux syscall interface in userspace and mediates host operations. Gofer is used for filesystem access in applicable configurations.', 'Sentry 在用户态实现 Linux syscall 接口并代理宿主操作，适用配置下由 Gofer 协助访问文件系统。'), ('Test syscall and filesystem compatibility. Apply external egress controls and check direct filesystem access settings.', '测试 syscall 与文件系统兼容性，并检查外部网络策略和直接文件访问配置。')],
            [('MicroVM / Kata', 'MicroVM / Kata'), ('A guest kernel separates untrusted native code and browsers from the host. Firecracker and Cloud Hypervisor use hardware virtualization. Kata integrates VM boundaries with container workflows.', '独立 Guest 内核隔离不可信原生代码和浏览器。Firecracker 与 Cloud Hypervisor 使用硬件虚拟化，Kata 将 VM 边界接入容器工作流。'), ('Review the VMM API, shared devices, filesystem bridges, host patching, and teardown. Benchmark cold starts, memory and I/O.', '检查 VMM API、共享设备、文件系统桥接、宿主补丁及销毁流程，并测量冷启动、内存和 I/O。')],
            [('V8 isolate / WASM', 'V8 Isolate / WASM'), ('A language runtime confines supported code to a memory and API boundary. Expose typed functions or capability-scoped WASI handles for short jobs.', '语言运行时用内存和 API 边界限制所支持的代码，适合短任务，可只开放类型化函数或受限的 WASI 句柄。'), ('Constrain host imports, preopened directories, outbound fetch, execution budgets and runtime versions. Confirm which boundaries the provider adds.', '检查宿主 imports、预开放目录、网络 fetch、执行预算与运行时版本，确认厂商叠加的隔离边界。')],
            [('Confidential VM / TEE', '机密 VM / TEE'), ('TDX and SEV-SNP protect private guest state against parts of the host threat model. Attestation can gate key delivery to a measured workload.', 'TDX 和 SEV-SNP 在其威胁模型内保护 Guest 私有状态。远程证明可用于向符合度量策略的工作负载发放密钥。'), ('Verify the full CPU/GPU trust path if required. Apply tool policy, constrain shared I/O, and model any provider receiving plaintext.', '按需验证 CPU / GPU 证明链，继续限制工具权限与共享 I/O，并明确哪些服务仍接触明文。')],
        ],
    ) + tee_cases + adoption + sandbox_lifecycle(zh) + paragraph(
        'Use a separate boundary for each mutually untrusted tenant or job. Bind the session ID to an authenticated owner, make base images read-only, give the job a writable scratch layer, then revoke credentials and destroy it. A warm pool should assign clean instances. For hibernation, protect snapshots like live memory and scope the restore operation to the same tenant and policy version.',
        '按相互不信任的租户或任务划分边界。将会话 ID 绑定认证主体，用只读基础镜像和独立可写层运行任务，结束后撤销凭据并销毁实例。预热池应只分配干净实例。休眠快照应按运行内存的敏感度保护，恢复操作须检查租户和策略版本。',
    ) + refs(
        ('https://gvisor.dev/docs/architecture_guide/intro/', 'gVisor security'),
        ('https://github.com/firecracker-microvm/firecracker/blob/main/docs/prod-host-setup.md', 'Firecracker Jailer'),
        ('https://github.com/kata-containers/kata-containers', 'Kata Containers'),
        ('https://docs.wasmtime.dev/security.html', 'Wasmtime / WASI'),
        ('https://shundazhang.github.io/tee-tdx-sgx/' + ('coco.zh.html' if zh else 'coco.html'), 'CoCo / TEE'),
    ))

    identity = section(2, (
        'Identify who requested the work, which deployed Agent is acting, and whose permissions apply to each tool call.',
        '识别谁发起任务、哪个已部署的 Agent 在执行，以及每次工具调用使用谁的权限。',
    ), table(
        [('Identity or credential', '身份或凭据'), ('Mainstream implementation', '主流实现'), ('What to verify', '校验要点')],
        [
            [('User identity', '用户身份'),
             ('Enterprise SSO with OpenID Connect (OIDC) establishes the user session. An OAuth access token authorizes calls to the application API.',
              '用 OpenID Connect（OIDC）接入企业单点登录并建立会话。调用应用 API 时使用 OAuth 访问令牌。'),
             ('Validate the issuer and sign-in token, then resolve the user and tenant from verified claims and directory membership.',
              '验证签发方和登录令牌，再依据经过验证的声明和目录成员关系解析用户及租户。')],
            [('Agent workload identity', 'Agent 工作负载身份'),
             ('Give each independently authorized workload a cloud IAM role, managed identity, or service account. The platform issues short-lived credentials, including via workload identity federation on Kubernetes.',
              '为需要独立授权的工作负载绑定云 IAM 角色、托管身份或服务账号，由平台发放短期凭据。Kubernetes 部署可使用工作负载身份联合。'),
             ('Map the deployed Agent to the authenticated principal on the server. Treat names and IDs supplied in prompts or tool arguments as input data.',
              '服务端将已部署的 Agent 映射到经过认证的主体。提示词和工具参数提供的名称或 ID 按输入数据处理。')],
            [('Tool access token', '工具访问令牌'),
             ('Use delegated OAuth for user-scoped access. Use application credentials or a cloud role for unattended jobs with their own permissions.',
              '代用户访问时使用 OAuth 委托。无人值守任务使用应用凭据或云角色，按该主体自身的权限执行。'),
             ('For JWT access tokens, verify signature, issuer, audience and expiry. Check scopes or roles, then enforce tenant and object-level access at the resource.',
              'JWT 访问令牌须检查签名、签发方、受众和有效期。校验 scope 或角色，并在资源端检查租户归属和对象级权限。')],
        ],
    ) + identity_exchange(zh) + paragraph(
        'For delegated access, use an on-behalf-of exchange if the provider supports it, or a separate OAuth authorization-code flow with user consent as required by the tool. Each remote MCP server receives a token issued for that server. Calls from it to another API use a credential for that upstream resource.',
        '代用户访问时，可用身份提供方支持的 On-Behalf-Of（OBO）令牌交换，或按工具要求通过独立的 OAuth 授权码流程取得用户授权。远程 MCP 服务接收面向自身签发的令牌，访问上游 API 时另用面向该资源的凭据。',
    ) + refs(
        ('https://openid.net/specs/openid-connect-core-1_0.html', 'OpenID Connect Core'),
        ('https://www.rfc-editor.org/rfc/rfc9700', 'OAuth 2.0 Security BCP'),
        ('https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization', 'MCP Authorization'),
    ) + '<h3>' + t('Managing identities in production', '生产环境中的身份管理') + '</h3>' + list_items([
        (('Inventory and ownership.', '登记与负责人。'),
         ('Record the Agent’s owner, deployment and environment, workload principal, tool connections and permission grants. Separate production from test identities.',
          '登记 Agent 的负责人、部署与环境、工作负载主体、工具连接和授权项。生产与测试使用独立身份。')),
        (('Grant and revoke.', '授权与撤销。'),
         ('Grant roles at the narrowest resource scope and review them when tools change. When retiring an Agent, disable its principal or remove its grants and delegated connections. Block new requests at the gateway while outstanding tokens expire or are revoked.',
          '按最小资源范围授予角色，接入或变更工具时复核权限。下线时禁用主体或移除授权和委托连接，由网关阻止新请求，等待已签发令牌到期或在支持时主动吊销。')),
        (('Trace each call.', '追踪每次调用。'),
         ('Log the user when present, the Agent workload principal, the deployment version, the target, the decision and a request ID. Keep tokens and secrets out of logs and model context.',
          '记录用户（如有）、Agent 工作负载主体、部署版本、目标资源、策略决定及请求 ID。令牌和秘密留在凭据管理层，避免出现在日志和模型上下文中。')),
    ]) + '<h3>' + t('How platforms implement it', '主流平台如何实现') + '</h3>' + table(
        [('Platform', '平台'), ('Workload identity', '工作负载身份'), ('Concrete implementation', '具体实现')],
        [
            [('AWS Bedrock AgentCore', 'AWS Bedrock AgentCore'),
             ('AgentCore workload identity and IAM roles', 'AgentCore 工作负载身份与 IAM 角色'),
             ('Runtime supports IAM SigV4 or a configured JWT authorizer. For a user’s Google Drive, a credential provider obtains the user’s OAuth grant and the Token Vault associates it with the Agent workload and user. ' + source('https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-oauth.html', 'AgentCore inbound/outbound auth'),
              'Runtime 支持 IAM SigV4 或已配置的 JWT 授权器。代用户读 Google Drive 时，凭据提供方取得用户的 OAuth 授权，Token Vault 将其与 Agent 工作负载及用户关联。 ' + source('https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-oauth.html', 'AgentCore 入站与出站认证'))],
            [('Microsoft Foundry / Entra ID', 'Microsoft Foundry / Entra ID'),
             ('Entra Agent ID or a project managed identity, depending on the connection', '按连接配置使用 Entra Agent ID 或项目托管身份'),
             ('A supported tool connection can obtain a downstream token on behalf of the user. For app-only access to Azure resources, assign the selected identity an Azure RBAC role scoped to the resource. ' + source('https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/user-delegation', 'Foundry tool delegation'),
              '支持委托的工具连接可代用户取得下游令牌。以应用身份访问 Azure 资源时，可给选用的身份授予限定资源范围的 Azure RBAC 角色。 ' + source('https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/user-delegation', 'Foundry 工具委托'))],
            [('Google Cloud', 'Google Cloud'),
             ('Custom service accounts or GKE Workload Identity Federation', '自定义服务账号或 GKE 工作负载身份联合'),
             ('Agent Runtime supports a custom service account scoped by IAM. For an Agent deployed on GKE, bind IAM access to its Kubernetes service account and obtain short-lived Google Cloud credentials without distributing a service account key. ' + source('https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/runtime/setup', 'Agent Runtime setup') + ' · ' + source('https://docs.cloud.google.com/kubernetes-engine/docs/concepts/workload-identity', 'GKE federation'),
              'Agent Runtime 可指定按 IAM 限权的自定义服务账号。部署在 GKE 时，可给 Agent 的 Kubernetes 服务账号绑定 IAM 权限，获取短期 Google Cloud 凭据，省去分发服务账号密钥。 ' + source('https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/runtime/setup', 'Agent Runtime 配置') + ' · ' + source('https://docs.cloud.google.com/kubernetes-engine/docs/concepts/workload-identity', 'GKE 身份联合'))],
        ],
    ))

    permissions = section(3, (
        'Have the harness send proposed actions to a broker that checks the current user, agent, destination, operation and data class.',
        'Harness 把拟执行的动作交给网关，由网关检查当前用户、Agent、目标、操作和数据类别。',
    ), tool_exchange(zh) + list_items([
        (('Capabilities.', '最小权限。'), ('Resolve targets server-side. Authorize reads and writes separately, including object ownership and tenant. For a write or export, bind the approval to the normalized destination, parameters, user, expiry and an idempotency key.', '在服务端解析资源，对读写分别授权，并核对对象归属和租户。写操作和导出审批绑定规范化后的目标、参数、用户、有效期及幂等键。')),
        (('Egress.', '网络出口。'), ('Default to deny. Route allowed traffic through a proxy that can enforce host, port, path and method where visible. Revalidate redirects and resolved IPv4/IPv6 addresses. Block metadata, private or link-local destinations except named private services. Test UDP, alternate DNS and browser side channels.', '默认拒绝。允许的流量经代理转发，在可见时检查主机、端口、路径和方法。重定向与解析后的 IPv4 / IPv6 地址逐跳复核，阻断元数据服务、私网及链路本地地址，按需单独开放指定私有服务。测试 UDP、替代 DNS 和浏览器间接外联。')),
        (('Credential broker.', '凭据代理。'), ('Mint a short-lived, audience-bound token after authorization, then inject it into the approved upstream request. Keep it out of the shell environment and transcripts. Filter echoed headers and signed links from responses, and remove credentials on cross-origin redirects.', '授权后签发短时、绑定接收方的令牌，由代理注入获准的上游请求。凭据不进入 Shell 环境和对话。过滤响应中回显的请求头与签名链接，跨源重定向时剥离凭据。')),
        (('MCP.', 'MCP。'), ('Review and pin servers and tool definitions, validate token audiences, and get separate upstream OAuth authorization. Deny token passthrough. Run local stdio servers under constrained privileges and authorize remote calls outside the model.', '审查并固定服务器和工具定义，验证 token audience，并为上游 API 单独获取 OAuth 授权。禁止透传客户端令牌。本地 stdio 服务器以受限权限运行，远端调用由模型之外的策略授权。')),
        (('Browser sessions.', '浏览器会话。'), ('Use separate profiles for public research and authenticated work. Restrict uploads and downloads, check the destination after redirects, and put login input and state-changing actions under controlled user interaction.', '公开检索与已登录操作使用独立浏览器配置。限制上传下载，重定向后检查目标，登录输入和改变外部状态的操作由受控交互处理。')),
    ]) + refs(
        ('https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices', 'MCP security guidance'),
        ('https://openai.com/index/designing-agents-to-resist-prompt-injection/', 'OpenAI prompt-injection defenses'),
    ))

    data = section(4, (
        'The term obfuscation spans several techniques. Their security properties depend on what is transformed, who can reverse it and where policy is enforced.',
        '混淆可以指多类机制。安全属性取决于变换的对象、谁可以还原，以及策略由哪一层执行。',
    ), table(
        [('Technique', '技术'), ('Use', '用途'), ('Limit', '局限')],
        [
            [('Delimiters / spotlighting', '分隔与 Spotlighting'), ('Tag source boundaries and mark untrusted tokens, or encode document text for a trained/instructed model to read as data. Microsoft documents a base64 variant.', '标记外部文本来源和边界，或编码文档，让配套模型按数据处理。Microsoft 记录了一种采用 Base64 的做法。'), ('Model-facing hint. Encoding is reversible, consumes context and can affect utility. Enforce permissions externally.', '它是面向模型的提示信号。编码可逆、消耗上下文并可能影响任务效果，操作权限仍需外部执行。')],
            [('Redaction / pseudonyms', '脱敏 / 假名化'), ('Remove irrelevant fields and replace needed identifiers with tenant- or task-scoped aliases. Keep the alias map in the broker. Resolve only after authorization.', '剔除不需要的字段，对需要关联的标识符使用租户或任务级代号，将映射保存在网关，授权后再解析。'), ('Context and repeated aliases can re-identify people. A regex alone misses OCR, code and multilingual variants. Test log and tool-result handling too.', '上下文和重复代号仍可能重新识别身份。单一正则容易漏过 OCR、代码或多语言变体，还要检查日志与工具结果。')],
            [('Secret placeholders', '秘密占位符'), ('Pass a handle or placeholder into the sandbox. An external proxy exchanges it for a credential only on the permitted request.', '把句柄或占位符交给沙箱。外部代理只为获准的请求替换成真实凭据。'), ('Scope remote operations as well as hosts. A valid token can still enable unwanted writes, and a response could echo a real secret.', '还要限制远端操作。有效令牌仍可能被用于非预期写入，响应也可能回显真实凭据。')],
            [('Information-flow control', '信息流控制'), ('Track provenance and taint across transformations. Separate untrusted parsing from privileged tool planning, and authorize data flows at sinks. CaMeL explores capability-backed data flows.', '跟踪来源与污点在变换中的传播。分离不可信解析和有权工具规划，在数据出口授权。CaMeL 研究用 capability 将这些约束绑定到数据流。'), ('Research guarantees apply to the studied runtime and policy model. Untracked paths, declassification and model-derived data need explicit treatment.', '研究中的保证依赖受测运行时和策略模型。需明确处理未追踪路径、解密级和模型派生数据。')],
            [('Cryptographic confidentiality', '密码学机密性'), ('Use TLS for transport, envelope encryption for persisted state, and attested key release when the workload must be protected from the host.', '传输用 TLS，持久状态用封装加密。需要抵御宿主时，使用经证明的密钥发放。'), ('A model or tool receiving plaintext can still leak it through writes or network calls. Apply destination policy to every plaintext sink.', '收到明文的模型和工具仍可能经写操作或网络泄露。对所有明文出口执行目标策略。')],
        ],
    ) + context_flow(zh) + paragraph(
        'Normalize Unicode, HTML, Markdown, URL encoding and OCR before policy evaluation, while retaining the original source and classification. Attackers can hide instructions that way too. Avoid treating base64, rephrasing, hidden system prompts or encrypted storage as authority checks.',
        '策略评估前可归一化 Unicode、HTML、Markdown、URL 编码和 OCR，并保留原始来源及分类。攻击者也会用这些形式隐藏指令。Base64、改写提示词、隐藏系统提示和存储加密各自需要独立的权限校验配合。',
    ) + refs(
        ('https://arxiv.org/abs/2403.14720', 'Spotlighting paper'),
        ('https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/content-filter-prompt-shields', 'Microsoft Prompt Shields'),
        ('https://arxiv.org/abs/2503.18813', 'CaMeL paper'),
        ('https://presidio.dataprivacystack.org/anonymizer/', 'Presidio Anonymizer'),
        ('https://cdn.openai.com/pdf/dd8e7875-e606-42b4-80a1-f824e4e11cf4/prevent-url-data-exfil.pdf', 'URL-based exfiltration'),
    ))

    def product(name, approach, check, *links, recipe=None, recipe_note=None):
        snippet = code(recipe) + paragraph(*recipe_note) if recipe else ''
        return f'<article class="product"><h3>{name}</h3>{paragraph(*approach)}{snippet}{paragraph(*check)}{refs(*links)}</article>'

    recent = '<div class="recent"><h3>' + t('What changed in late 2026', '2026 年下半年的进展') + '</h3>' + list_items([
        (('12 November · AWS.', '11 月 12 日 · AWS。'),
         ('The next-generation AgentCore Runtime announcement describes faster startup and larger workloads within the per-session Firecracker boundary. AWS also documents filesystem persistence separately.',
          '新一代 AgentCore Runtime 公告介绍了按会话隔离的 Firecracker 如何支持更快启动与更大负载。文件系统持久化仍由独立配置控制。')),
        (('October · Google Cloud.', '10 月 · Google Cloud。'),
         ('Agent Compute Engine and Agent Substrate document per-agent identity and network mediation. The GKE docs compare suspend, resume and identity semantics across deployment models.',
          'Agent Compute Engine 与 Agent Substrate 把独立身份和网络代理纳入运行时设计。GKE 文档对比了不同部署模型在休眠、恢复和身份管理上的差异。')),
        (('September · OWASP.', '9 月 · OWASP。'),
         ('The GenAI Security Project added the Agent Control Standard alongside existing risk guidance, reflecting growing attention to enforcement at runtime.',
          'GenAI Security Project 在已有风险指引之外引入 Agent Control Standard，重点转向运行时如何实际执行规则。')),
    ]) + refs(
        ('https://aws.amazon.com/blogs/machine-learning/run-agents-securely-and-efficiently-with-the-next-generation-agentcore-runtime/', 'AWS November announcement'),
        ('https://cloud.google.com/blog/topics/ai-infrastructure/introducing-agent-compute-engine-and-expanded-agent-governance/', 'Google Cloud announcement'),
        ('https://genai.owasp.org/2026/09/01/owasp-genai-security-project-unveils-2026-top-10-for-llm-applications-new-agent-control-standard-and-sponsors-as-community-tops-30000-members/', 'OWASP announcement'),
    ) + '</div>'

    products = section(5, (
        'The controls below come from public product documentation reviewed on 15 November 2026. Hosted features and availability depend on compute mode, region, plan and release.',
        '以下依据截至 2026 年 11 月 15 日查阅的公开产品文档。功能可用性取决于计算模式、区域、套餐和版本。',
    ), '<p><a href="#tee-products">' + t(
        'See products using TEEs in Runtime Isolation', '查看「运行隔离」中的 TEE 产品案例',
    ) + ' ↑</a></p><div class="product-grid">' + ''.join([
        product('Amazon Bedrock AgentCore', (
            'Serverless Runtime microVMs isolate CPU, memory and filesystem per session. Gateway Policy can evaluate Cedar rules for tool calls. Use IAM or JWT authentication and bind session IDs to the invoking tenant.',
            'Serverless Runtime microVM 按会话隔离 CPU、内存和文件系统。Gateway Policy 可用 Cedar 策略判断工具调用。使用 IAM 或 JWT 认证，并将会话 ID 绑定到调用租户。',
        ), (
            'AWS also documents an Instances compute type that can host multiple collaborating agents with a shared filesystem. Check the chosen compute type and whether persistent filesystem configuration retains state after termination.',
            'AWS 也提供 Instances 计算模式，可让多个协作 Agent 共享文件系统。选型时检查计算模式，并确认启用持久文件系统后哪些数据会在会话结束后保留。',
        ),
            ('https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-how-it-works.html', 'microVMs'),
            ('https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-instances-how-it-works.html', 'Instances'),
            ('https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy-permissions.html', 'Gateway Policy'),
            ('https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-filesystem-configurations.html', 'Filesystem lifecycle'),
        ),
        product('Google Cloud', (
            'Gemini Enterprise Agent Platform executes code in a separate Google-managed gVisor sandbox without inheriting the parent Agent Runtime credentials. On GKE, Agent Substrate uses per-actor SPIFFE identity and an egress gateway that can inject credentials. Agent Sandbox uses Kubernetes-native controllers and workload network policy.',
            'Gemini Enterprise Agent Platform 在独立的 Google 托管 gVisor 沙箱中执行代码，沙箱不继承父 Agent Runtime 的凭据。GKE 的 Agent Substrate 为每个 Actor 分配 SPIFFE 身份，并可在出口网关注入凭据。Agent Sandbox 则使用 Kubernetes 原生控制器与工作负载网络策略。',
        ), (
            'For the Kubernetes path, check the requested RuntimeClass and the actual node runtime. Compare microVM versus gVisor, and test who can read or restore persisted state.',
            'Kubernetes 部署需核对请求的 RuntimeClass 与节点实际运行时。比较 microVM 和 gVisor，并验证哪些身份可读取或恢复持久状态。',
        ),
            ('https://docs.cloud.google.com/gemini-enterprise-agent-platform/scale/sandbox', 'Managed sandboxes'),
            ('https://docs.cloud.google.com/kubernetes-engine/docs/concepts/machine-learning/agent-workloads', 'GKE runtime comparison'),
            ('https://cloud.google.com/blog/topics/ai-infrastructure/introducing-agent-compute-engine-and-expanded-agent-governance/', 'Agent Compute Engine announcement'),
        ),
        product('Cloudflare Agents / Code Mode', (
            'Dynamic Workers run generated JavaScript with a restricted set of bindings. A separate container option supports Linux tools and packages. The dynamic Worker can have its own outbound behavior.',
            'Dynamic Workers 运行生成的 JavaScript，按需提供受限 bindings。需要 Linux 工具和依赖时可选容器。Dynamic Worker 可单独配置网络出口。',
        ), (
            'Set <code>globalOutbound</code> explicitly. With <code>null</code>, give the worker access only through approved bindings. Review those bindings for write, export and delegation capabilities.',
            '显式设置 <code>globalOutbound</code>。设为 <code>null</code> 时，通过批准的 bindings 提供所需能力，并逐一核对它们能否写入、导出或转授。',
        ),
            ('https://developers.cloudflare.com/agents/tools/sandbox/', 'Sandbox choices'),
            ('https://developers.cloudflare.com/dynamic-workers/usage/egress-control/', 'Egress configuration'),
            recipe='globalOutbound: null',
            recipe_note=('This is a Worker Loader option. Omission inherits the parent Worker’s outbound access.', '这是 Worker Loader 的配置项。省略会继承父 Worker 的网络出口权限。'),
        ),
        product('Claude Managed Agents', (
            'Cloud environments accept limited networking and an explicit host list. Vault credentials can be restricted to HTTPS request headers for specific hosts, with placeholders visible to sandbox code.',
            '云端环境支持有限网络和显式主机列表。Vault 凭据可以仅注入指定主机的 HTTPS 请求头，沙箱代码只看到占位符。',
        ), (
            'Review remote MCP, web search and web fetch settings separately. Allowed hosts can still accept uploads. Put sensitive reads and writes behind application tools that enforce operation-level rules.',
            '分别检查远端 MCP、网页搜索和抓取设置。允许的主机仍可能接受上传。敏感读写应经过可校验具体操作的应用工具。',
        ),
            ('https://platform.claude.com/docs/en/managed-agents/secure-deployment', 'Secure deployment'),
            recipe='networking:\n  type: limited\n  allowed_hosts:\n    - help.example.com',
            recipe_note=('Place this fragment under the cloud environment’s config. The hostname is illustrative.', '将片段放在云端环境的 config 下。域名为示例。'),
        ),
        product('OpenAI Agents API / ChatGPT Agent', (
            'An OpenAI-hosted Agents API sandbox supports restricted networking and vault-backed credential injection. Self-hosted sandbox owners maintain their execution and network boundaries. ChatGPT Agent separately documents user confirmations and observation controls for its product workflows.',
            'OpenAI 托管的 Agents API 沙箱支持受限网络与 Vault 凭据注入。自管沙箱由部署方维护执行和网络边界。ChatGPT Agent 的产品工作流另外提供用户确认与监督控制。',
        ), (
            'Keep network rules and credential restrictions in place when enabling automatic review. Audit sandbox, remote MCP and application-hosted tools as separate outbound routes.',
            '启用自动审查时仍需执行网络规则与凭据约束。分别审计沙箱、远端 MCP 与应用侧工具的出口。',
        ),
            ('https://developers.openai.com/api/docs/guides/agents-api/environments/security', 'Sandbox security'),
            ('https://developers.openai.com/api/docs/guides/agents-api/environments/openai-hosted', 'Hosted configuration'),
            ('https://openai.com/index/designing-agents-to-resist-prompt-injection/', 'ChatGPT Agent design'),
        ),
        product('Vercel Sandbox', (
            'Each sandbox uses a Firecracker microVM. The external firewall supports network policies and can inject HTTP headers on matching outbound HTTPS requests or forward traffic to your proxy.',
            '每个沙箱使用 Firecracker microVM。VM 外的防火墙支持网络策略，可向匹配的 HTTPS 请求注入头部，也可把请求转发到自有代理。',
        ), (
            'Set a policy explicitly because the documented default is allow-all. Use request-level checks for shared API hosts where domain-level authorization is too broad.',
            '文档给出的默认值是 allow-all，应显式设置策略。共享 API 主机上的操作权限过宽时，在代理层检查具体请求。',
        ),
            ('https://vercel.com/docs/sandbox', 'Vercel Sandbox'),
            ('https://vercel.com/changelog/advanced-egress-firewall-filtering-for-vercel-sandbox', 'SNI and CIDR firewall'),
            ('https://vercel.com/changelog/safely-inject-credentials-in-http-headers-with-vercel-sandbox', 'Header injection'),
            recipe="const sandbox = await Sandbox.create({\n  networkPolicy: 'deny-all',\n});",
            recipe_note=('Create with a closed network, then allow reviewed endpoints when the workload needs them.', '创建时关闭网络，工作负载确有需要时再开放通过审查的端点。'),
        ),
        product('Microsoft Foundry / Azure SRE Agent', (
            'Foundry documents Spotlighting in Prompt Shields for external documents. Azure SRE Agent documents a separate execution sandbox, structured calls to that sandbox and short-lived credentials delivered through its identity service.',
            'Foundry 的 Prompt Shields 为外部文档提供 Spotlighting。Azure SRE Agent 则记录了独立执行沙箱、结构化调用和通过身份服务发放的短时凭据。',
        ), (
            'Use the Foundry setting to test document screening and measure impact on task quality. Use the SRE Agent architecture to study where execution and identity are enforced on a different product surface.',
            '用 Foundry 设置测试文档检测效果并衡量对任务质量的影响。Azure SRE Agent 的架构则用于了解另一产品如何约束执行与身份。',
        ),
            ('https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/content-filter-prompt-shields', 'Prompt Shields'),
            ('https://learn.microsoft.com/en-us/azure/sre-agent/security-overview', 'SRE Agent security'),
        ),
        product('Docker Sandboxes', (
            'This developer-side example uses a microVM per sandbox and an external credential proxy. Shared folders and other exposed interfaces define what the agent can access.',
            '这个开发端实例为每个沙箱使用 microVM 和外部凭据代理。Agent 可访问的内容由共享目录与其他外露接口决定。',
        ), (
            'The Docker security model places local stdio MCP servers on the host. Treat their installation and execution permissions as a separate boundary from commands running in the VM.',
            'Docker 文档说明本地 stdio MCP 服务器运行在宿主上。它们的安装与执行权限需独立于 VM 内的命令进行审查。',
        ),
            ('https://docs.docker.com/ai/sandboxes/security/', 'Trust boundaries'),
            ('https://docs.docker.com/ai/sandboxes/configuration/credentials', 'Credential management'),
        ),
    ]) + '</div>' + recent)

    design = section(6, (
        'A support agent reads customer records, consults a public help center and can draft a response. Use separate paths for public browsing and access to customer data.',
        '以客服 Agent 为例：它需要读客户记录、查看公开帮助中心并拟写回复。公开浏览与客户数据访问走独立路径。',
    ), deployment_architecture(zh) + architecture_references(zh) + support_request(zh) + paragraph(
        'If privileged infrastructure is in scope, place the sensitive components in a confidential VM and bind key delivery to attestation. Check external model and tool endpoints separately.',
        '若威胁模型纳入具有特权的基础设施，可将敏感组件放入机密 VM，并把密钥交付绑定到远程证明。外部模型和工具端点需要分别核对。',
    ) + '<p><a href="#tee-attestation-diagram">' + t(
        'See the TEE attestation and key delivery flow', '查看 TEE 证明与密钥发放流程',
    ) + ' ↑</a></p>' + list_items([
        (('Provision.', '创建。'), ('Pin runtime images and tools. Allocate one isolated workspace to a tenant-bound job and mount only the required input. Gate cold startup and restore on the same policy. Set task TTL, quotas and recursion limits.', '固定运行镜像与工具版本。为绑定租户的任务分配隔离工作区，只挂载必要输入。新建与恢复都校验同一策略，并配置任务有效期、配额、递归上限。')),
        (('Constrain.', '约束。'), ('Keep raw credentials and customer record lookups outside the sandbox. Give the sandbox a narrow workspace and network path. Disallow public export of ticket-derived data. Require review before sending the exact message.', '原始凭据和客户记录读取留在沙箱外。沙箱只取得必要工作区与网络路径。禁止公开导出工单派生数据，发信前审批具体收件人和正文。')),
        (('Observe and revoke.', '审计与撤销。'), ('Log tenant, session, proposer, tool, normalized target, policy version and verdict. Minimize payload logging. Correlate sandbox, MCP and egress events. Expire tokens, discard temporary data, and retain approved artifacts under a tenant ACL.', '记录租户、会话、发起者、工具、规范化目标、策略版本和判断。尽量减少正文日志，关联沙箱、MCP 与网络出口事件。使令牌过期、清除临时数据，并按租户 ACL 保存获准产物。')),
        (('Verify failure paths.', '验证拒绝路径。'), ('Use canary strings in fake data. Probe private IPs, DNS and redirect bypass, an allowed host with an unauthorized upload, stale approval replay, sensitive tool output and wrong-tenant snapshot restore. Compare legitimate task completion and blocked malicious effects.', '在模拟敏感数据里放入标记值，测试私网地址、DNS 与重定向绕过、允许域名上的未授权上传、重放审批、敏感工具结果和跨租户恢复快照。分别衡量正常任务完成率与恶意副作用阻断率。')),
    ]) + refs(('https://github.com/ethz-spylab/agentdojo', 'AgentDojo benchmark')))

    cases = [
        ('search', ('Private data in a public search', '把私有数据发到公开搜索'), ('A webpage suggests putting a private order alias into a public query. The query goes to an allowed host.', '网页诱导 Agent 把私有订单代号写入公开查询，搜索网站本身在允许列表内。'), 'flow'),
        ('write', ('Write on an allowed host', '在允许主机上执行写操作'), ('Code proposes a POST to an allowed service. The job only has read authority.', '代码拟向允许列表内的服务发起 POST，但任务只有读取权限。'), 'tool'),
        ('route', ('Unexpected network destination', '访问未获准的网络目标'), ('A tool follows a redirect from an allowed web page to a disallowed host.', '工具从允许的网页跟随重定向，目标主机未经授权。'), 'egress'),
        ('mount', ('Read a credential from disk', '从磁盘读取凭据'), ('Generated code tries to read a credential file outside the mounted task directory.', '生成的代码尝试读取任务挂载目录以外的凭据文件。'), 'sandbox'),
    ]
    switches = [
        ('sandbox', 'Restrict filesystem', '约束文件系统'),
        ('egress', 'Check network destination', '核验网络目标'),
        ('tool', 'Check operation scope', '校验操作权限'),
        ('flow', 'Check data at outbound sinks', '检查出口数据'),
    ]
    options = ''.join(
        f'<option value="{ident}" data-control="{control}" data-description="{escape(t(*desc), quote=True)}">{t(*label)}</option>'
        for ident, label, desc, control in cases
    )
    checks = ''.join(f'<label><input type="checkbox" id="{ident}" checked> {t(en, cn)}</label>' for ident, en, cn in switches)
    lab = section(7, (
        'Choose a scenario and toggle its controls. This browser-only simulation highlights which check changes the outcome.',
        '选择情境并开关防护，观察哪一层检查会改变结果。实验只在当前浏览器中模拟决策。',
    ), f'''<div class="lab" id="policy-lab">
      <div><label for="scenario">{t('Scenario', '实验情境')}</label><select id="scenario">{options}</select>
      <p id="scenario-description">{t(*cases[0][2])}</p><fieldset><legend>{t('Enabled controls', '启用防护')}</legend>{checks}</fieldset></div>
      <div class="verdict" id="verdict" role="status" data-pass="{t("Blocked", "已拦截")}" data-fail="{t("Would pass", "会放行")}">
        <strong>{t('Blocked', '已拦截')}</strong><p>{t('Check data at outbound sinks', '检查出口数据')}</p>
      </div>
    </div>''')
    description = t('Cloud AI agent isolation, tool authorization, egress, obfuscation, and product practices.', '云端 AI Agent 安全隔离、工具授权、出口控制、混淆与业界实践。')
    return f'''<!doctype html>
<html lang="{t('en', 'zh-CN')}"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{description}"><meta name="theme-color" content="#101719">
<title>{title} · ShundaZhang</title>
<link rel="stylesheet" href="style.css"><link rel="stylesheet" href="figures.css"><script src="../language.js"></script><script defer src="lab.js"></script>
</head><body>
<a class="skip" href="#main">{t('Skip to content', '跳至正文')}</a>
<header class="top"><div class="shell top-inner">
<a href="{t('../#security', '../index.zh.html#security')}" class="home"><span aria-hidden="true">←</span> {t('Security', '安全')}</a>
<span class="brand">{title}</span>
<nav class="languages" aria-label="{t('Language', '语言')}">
<a href="index.html" data-atlas-lang="en"{t(' aria-current="page"', '')}>EN</a>
<a href="index.zh.html" data-atlas-lang="zh"{t('', ' aria-current="page"')}>中文</a>
</nav></div></header>
<main class="shell" id="main">
{hero}
<nav class="chapters" aria-label="{t('Chapters', '章节目录')}">{nav}</nav>
{threats}{isolation}{identity}{permissions}{data}{products}{design}{lab}
</main>
<footer class="shell"><a href="{t('../#security', '../index.zh.html#security')}">{t('Back to Security', '返回安全专题')} ↗</a><span>ShundaZhang</span></footer>
</body></html>
'''


if __name__ == '__main__':
    for chinese, filename in [(False, 'index.html'), (True, 'index.zh.html')]:
        (ROOT / filename).write_text(build(chinese), encoding='utf-8')
