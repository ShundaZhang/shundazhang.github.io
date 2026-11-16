"""Responsive reference architecture and request diagrams."""

from html import escape


def figure(zh, ident, title, body, description, *, sources=()):
    label = title[zh]
    reference_links = ' · '.join(
        f'<a href="{escape(url, quote=True)}" target="_blank" rel="noopener noreferrer">{escape(name)} ↗</a>'
        for name, url in sources
    )
    references = f'<p class="drawing-refs">{reference_links}</p>' if sources else ''
    return (
        f'<figure class="drawing" id="{ident}" aria-labelledby="{ident}-title">'
        f'<figcaption id="{ident}-title">{escape(label)}</figcaption>'
        f'{body}<p class="drawing-note">{escape(description[zh])}</p>{references}</figure>'
    )


def nodes(zh, items):
    return '<ol class="drawing-nodes">' + ''.join(
        f'<li><strong>{escape(title[zh])}</strong><span>{escape(detail[zh])}</span></li>'
        for title, detail in items
    ) + '</ol>'


def exchange(zh, ident, title, steps, description, *, stop, sources=()):
    items = []
    for actor, action, detail in steps:
        items.append(
            f'<li><span class="exchange-actor">{escape(actor[zh])}</span>'
            f'<div><strong>{escape(action[zh])}</strong><p>{escape(detail[zh])}</p></div></li>'
        )
    stop_label = '停止条件' if zh else 'Stop condition'
    failure = f'<p class="drawing-stop"><strong>{stop_label}</strong> {escape(stop[zh])}</p>'
    return figure(
        zh, ident, title, '<ol class="exchange">' + ''.join(items) + '</ol>' + failure,
        description, sources=sources,
    )


OPENAI_SANDBOX = 'https://developers.openai.com/api/docs/guides/agents/sandboxes'
OPENAI_ARCHITECTURE = 'https://developers.openai.com/images/api/agents/harness_separate_from_compute.png'
AWS_GATEWAY = 'https://aws.amazon.com/blogs/machine-learning/secure-ai-agents-with-policy-and-lambda-interceptors-in-amazon-bedrock-agentcore-gateway/'
AWS_FLOW = 'https://d2908q01vomqb2.cloudfront.net/f1f836cb4ea6efb2a0b1b99f41ad8b103eff4b59/2026/05/29/ML-20712-5.png'
DOCKER_FLOW = 'https://docs.docker.com/ai/sandboxes/architecture#follow-an-authenticated-request'
GKE_ARCHITECTURE = 'https://docs.cloud.google.com/kubernetes-engine/docs/concepts/machine-learning/agent-workloads#actor-based-model-agent-substrate-on-gke-recommended'


def deployment_architecture(zh):
    ingress = nodes(zh, [
        (('Application ingress', '应用接入层'),
         ('Authenticate user and tenant. Keep user intent separate from source-tagged web and tool data.',
          '认证用户与租户。区分用户意图和带来源标记的网页内容、工具结果。')),
        (('Harness · application control plane', 'Harness · 应用控制面'),
         ('Manage the session, minimize context and route proposed actions. Keep approvals and policy state here.',
          '管理会话、最小化上下文并分发拟执行的动作。审批和策略状态保留在控制面。')),
        (('Model endpoint', '模型端点'),
         ('Receive policy-filtered context and return a proposed action. Treat a remote provider as a separate trust boundary.',
          '接收按策略筛选的上下文，返回拟执行动作。远端模型服务属于独立信任边界。')),
    ])
    tool_path = nodes(zh, [
        (('Tools / MCP gateway', '工具 / MCP 网关'),
         ('Resolve tenant and resource server-side. Check operation, parameters and any approval receipt.',
          '在服务端解析租户与资源，核对操作、参数和所需审批。')),
        (('Credential broker', '凭据代理'),
         ('Retrieve credentials from a separate vault after approval. Attach a scoped credential to this request.',
          '授权满足后从独立凭据库取用凭据，只为本次请求附加限权凭据。')),
        (('Private API / MCP target', '私有 API / MCP 服务'),
         ('The upstream service enforces resource access. The gateway filters and labels returned data.',
          '上游服务执行资源级权限检查，网关过滤并标记返回的数据。')),
    ])
    code_path = nodes(zh, [
        (('Task execution sandbox', '任务执行沙箱'),
         ('Run generated code with a scoped workload identity, limited mounts and resource quotas.',
          '用受限的工作负载身份、挂载和资源配额运行生成的代码。')),
        (('Egress proxy outside sandbox', '沙箱外出口代理'),
         ('Authenticate the workload. Default to deny and check destination, method and payload according to policy.',
          '认证工作负载，默认拒绝，按策略校验目的地、请求方法和载荷。')),
        (('Approved public endpoint', '获准的公开端点'),
         ('Use approved read-only routes. Access to private tools is mediated by the structured gateway path.',
          '只走获准的只读路径，访问私有工具时走结构化工具网关。')),
    ])
    dispatch, tool_label, code_label, audit_label = (
        ('Harness 按动作类型分发', '私有工具与业务操作', '隔离执行与受控外联', '审计与会话状态') if zh
        else ('Harness dispatches by action type', 'Private tools and business actions', 'Isolated execution and controlled network access', 'Audit and session state')
    )
    audit = (
        '网关、凭据代理和出口代理关联同一任务 ID，记录策略决定。产物和快照按租户隔离，日志避免记录秘密和原始客户数据。'
        if zh else
        'The gateway, credential broker and egress proxy log decisions under a shared job ID. Artifacts and snapshots are tenant-scoped. Logs omit secrets and raw customer data.'
    )
    body = f'''<div class="architecture-ingress">{ingress}</div>
    <p class="drawing-dispatch">{dispatch}</p><div class="drawing-lanes">
      <div class="drawing-lane"><strong>{tool_label}</strong>{tool_path}</div>
      <div class="drawing-lane"><strong>{code_label}</strong>{code_path}</div>
    </div><p class="drawing-audit"><strong>{audit_label}</strong> {audit}</p>'''
    return figure(
        zh, 'agent-system-diagram',
        ('Reference architecture for a cloud support agent', '云端客服 Agent 安全参考架构'), body,
        ('This design combines published product patterns. Place authorization outside model reasoning and keep reusable credentials out of the code sandbox. The source notes below identify the official diagrams and the decisions made for this design.',
         '此方案组合了公开产品设计。权限由模型之外的组件执行，可复用凭据保留在代码沙箱外。下方注明所参考的官方原图及本方案的取舍。'),
    )


def architecture_references(zh):
    entries = [
        (
            'OpenAI Agents SDK',
            ('The official figure keeps the Harness and its trusted access to tools separate from sandbox compute. Here the application runs session and approval state in the control plane, and gives code only a task workspace.',
             '官方图把 Harness 及可信工具访问与沙箱计算分开。本方案在应用控制面管理会话和审批，代码只接触任务工作区。'),
            [(('Official diagram', '官方原图'), OPENAI_ARCHITECTURE), (('Sandbox documentation', '沙箱文档'), OPENAI_SANDBOX)],
        ),
        (
            'AWS Bedrock AgentCore Gateway',
            ('The official flow enriches a validated request before Cedar evaluation and filters the response afterward. This design uses the same enforcement point, with credential attachment after policy and required human approval.',
             '官方图在 Cedar 判断前补充已验证的请求上下文，返回时再过滤结果。本方案沿用网关这一权限执行点，并在策略与所需人工审批均通过后附加上游凭据。'),
            [(('Official request flow', '官方请求流程原图'), AWS_FLOW), (('Architecture article', '架构文章'), AWS_GATEWAY)],
        ),
        (
            'Docker Sandboxes',
            ('The official local-product walkthrough shows a placeholder crossing the microVM boundary and the host proxy adding the real credential. This design applies the same separation to a cloud credential broker.',
             '官方本地产品流程展示了占位符如何穿过 microVM 边界，再由宿主代理注入真实凭据。本方案借鉴这一划分，将凭据代理放在云端沙箱外。'),
            [(('Official interactive request flow', '官方交互式请求流程'), DOCKER_FLOW)],
        ),
        (
            'Google Cloud · Agent Substrate on GKE',
            ('GKE documents an identity per actor, mTLS tunnels and an Envoy egress gateway. This design authenticates each task at its egress proxy before checking the destination.',
             'GKE 文档介绍了每 Actor 独立身份、mTLS 隧道和 Envoy 出口网关。本方案同样让出口代理先认证任务身份，再判断是否放行目标。'),
            [(('Official GKE architecture', '官方 GKE 架构文档'), GKE_ARCHITECTURE)],
        ),
    ]
    cards = []
    for name, note, sources in entries:
        links = ' · '.join(
            f'<a href="{escape(url, quote=True)}" target="_blank" rel="noopener noreferrer">{escape(label[zh])} ↗</a>'
            for label, url in sources
        )
        cards.append(
            f'<div><dt>{escape(name)}</dt><dd>{escape(note[zh])}'
            f'<p class="drawing-refs">{links}</p></dd></div>'
        )
    heading = '图中设计来自哪里' if zh else 'Published designs behind the diagram'
    return f'<section class="architecture-sources" aria-labelledby="architecture-sources-title"><h3 id="architecture-sources-title">{heading}</h3><dl>{"".join(cards)}</dl></section>'


def support_request(zh):
    return exchange(
        zh, 'agent-request-diagram',
        ('End-to-end request: read an order, draft, send', '端到端流程：查订单、拟稿、发信'),
        [
            (('Support user → application', '客服人员 → 应用'), ('Open a tenant-bound session', '创建绑定租户的会话'),
             ('Authenticate the user. Bind the session to the operator and tenant before accepting the task.',
              '先认证客服人员，将会话绑定到操作者和租户，再接收任务。')),
            (('Harness → gateway → order API', 'Harness → 网关 → 订单 API'), ('Read one permitted order', '读取获准的订单'),
             ('Resolve the order in the authenticated tenant, authorize read access, then return only the necessary fields under an alias.',
              '在认证租户范围内解析订单，检查读权限，返回代号和所需的最少字段。')),
            (('Separate job → egress proxy', '独立检索任务 → 出口代理'), ('Read the public help center', '查阅公开帮助中心'),
             ('Pass a generic question into a separate job. Allow a read-only request to the reviewed help center. Tag the response as external content.',
              '将通用问题交给独立任务，只允许向经审查的帮助中心发出只读请求。将返回内容标为外部来源。')),
            (('Harness ↔ model', 'Harness ↔ 模型'), ('Draft for review', '生成待审批的草稿'),
             ('The model composes a draft from the minimized context. Store it as an artifact in the authorized tenant.',
              '模型用最小化上下文拟写回复，草稿保存在获准租户的产物存储中。')),
            (('Human → gateway → broker → mail API', '审批人 → 网关 → 凭据代理 → 邮件 API'), ('Send only the approved message', '发送经过审批的那一封邮件'),
             ('Bind approval to the normalized recipient and exact body. Recheck policy, attach a send-scoped credential and deduplicate the write. Record the outcome.',
              '将审批绑定到规范化收件人与具体正文，复核策略后附加发信限权凭据，并对写操作去重。记录执行结果。')),
        ],
        ('This example exercises both paths in the architecture. The ticket and send calls use the tool gateway. Public browsing uses the separate execution job and egress proxy.',
         '这个例子走通了架构里的两条路径。读订单和发信通过工具网关，公开检索走独立执行任务和出口代理。'),
        stop=('Reject an external page’s request to send order fields to an unapproved endpoint. If the recipient or message changes after approval, request a new approval before sending.',
              '若外部网页要求把订单字段发到未经授权的端点，出口应拦截。审批后收件人或正文有变更，发信前需重新审批。'),
    )


def tool_exchange(zh):
    return exchange(
        zh, 'tool-authorization-diagram',
        ('Tool authorization and credential delivery', '工具授权与凭据发放时序'),
        [
            (('Harness → gateway', 'Harness → 网关'), ('Propose a typed action', '提交结构化操作'),
             ('Include the tool, operation and arguments. Use the authenticated tenant and session from the server.',
              '提交工具、操作与参数。租户和会话身份由服务端认证取得。')),
            (('Gateway → policy', '网关 → 策略引擎'), ('Resolve and authorize the resource', '规范化资源并检查权限'),
             ('Check operation, tenant ownership and destination against current policy.',
              '按当前策略核对操作类型、租户归属与目的地。')),
            (('Gateway ↔ approver', '网关 ↔ 审批人'), ('Review a write, when required', '按策略审批写操作'),
             ('Show the exact recipient, operation and arguments. Bind the approval to those values and an expiry.',
              '展示具体的收件人、操作与参数，并把审批绑定到这些值和有效期。')),
            (('Broker → upstream API', '凭据代理 → 上游 API'), ('Execute once with a scoped token', '使用限权令牌执行操作'),
             ('Recheck the approved action, attach the credential at the broker and deduplicate writes using an idempotency key.',
              '复核当前请求与审批一致，由代理附加凭据，并通过幂等键避免重复写入。')),
            (('Gateway → harness', '网关 → Harness'), ('Return a filtered result', '返回过滤后的结果'),
             ('Record the policy decision, redact sensitive fields and mark the response as tool data.',
              '记录策略判断，移除敏感字段，并标记该内容来自工具。')),
        ],
        ('Example: a support agent can read an order and draft a reply. Sending the reply requires a new policy decision and, if configured, exact-action approval.',
         '例如，客服 Agent 可以读订单并拟稿。真正发信时需要重新做权限判断，并按配置审批该次具体操作。'),
        stop=('If authorization fails or approval is missing, altered or expired, stop before calling the upstream API.',
              '权限校验失败，或审批缺失、被修改、已过期时，在调用上游 API 前停止。'),
        sources=(('AWS AgentCore · official request flow', AWS_FLOW),
                 ('MCP Security Best Practices', 'https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices'),),
    )


def context_flow(zh):
    body = nodes(zh, [
        (('Private order record', '私有订单记录'),
         ('The application checks access and replaces the customer identifier with a task-scoped alias.',
          '应用先检查访问权限，再用任务级代号替换客户标识符。')),
        (('Tagged model context', '带标记的模型上下文'),
         ('Keep the alias and order-derived fields tagged private. Mark web text as untrusted input.',
          '订单代号及其派生字段保留私有标签，网页文字标记为不可信输入。')),
        (('Proposed public search', '拟发起公开搜索'),
         ('The model proposes a query based on a webpage instruction. The query contains the alias.',
          '模型根据网页里的指令提出搜索请求，查询中包含订单代号。')),
        (('Egress decision', '出口决策'),
         ('Deny the private payload. A separate research step can receive a generic public topic.',
          '拦截携带私有数据的请求。独立检索步骤只接收不含订单信息的公开主题。')),
    ])
    return figure(
        zh, 'context-flow-diagram',
        ('From data minimization to egress enforcement', '从最小化上下文到数据出口拦截'), body,
        ('Track sensitivity through transformations. An allowlisted search host can still receive private data if the gateway checks hostname alone.',
         '数据变换后也要保留敏感度。即使搜索网站在允许列表中，只检查主机名仍可能放行私有数据。'),
        sources=(('CaMeL research', 'https://arxiv.org/abs/2503.18813'),
                 ('URL-based exfiltration', 'https://cdn.openai.com/pdf/dd8e7875-e606-42b4-80a1-f824e4e11cf4/prevent-url-data-exfil.pdf')),
    )


def attestation_exchange(zh):
    return exchange(
        zh, 'tee-attestation-diagram',
        ('Attestation and key delivery to a confidential VM', '机密 VM 的远程证明与密钥发放'),
        [
            (('Verifier → guest', '验证者 → Guest'), ('Issue a fresh challenge', '发出新鲜挑战值'),
             ('The verifier requests evidence for this session with a nonce.',
              '验证者用 nonce 请求本次会话的证明证据。')),
            (('Guest → verifier', 'Guest → 验证者'), ('Submit evidence bound to a guest key', '提交绑定 Guest 密钥的证据'),
             ('The guest generates an ephemeral key. Hardware evidence binds the nonce and the guest public key to the measured environment.',
              'Guest 生成临时密钥，硬件证据把 nonce 和 Guest 公钥绑定到经度量的环境。')),
            (('Verifier → key broker', '验证者 → 密钥代理'), ('Appraise the platform and workload', '评估平台和工作负载'),
             ('Check endorsement, freshness, measurements and the TCB. Return an attestation result bound to the guest key.',
              '核对背书、新鲜度、度量和 TCB，返回绑定 Guest 公钥的证明结果。')),
            (('Key broker → guest', '密钥代理 → Guest'), ('Authorize and wrap the requested key', '授权并加密封装请求的密钥'),
             ('Apply resource policy and encrypt the secret to the verified guest key. The guest unwraps it inside the VM.',
              '执行资源策略，用验证过的 Guest 公钥加密秘密，Guest 在 VM 内解封。')),
        ],
        ('This example covers an Agent VM and its key delivery path. An external model or SaaS that receives plaintext is a separate trust boundary.',
         '此例覆盖 Agent VM 和它的密钥发放链路。接收明文的外部模型或 SaaS 有独立的信任边界。'),
        stop=('Reject missing, stale or mismatched evidence. A valid report still needs to pass resource authorization.',
              '拒绝缺失、过期或不匹配的证据。证据验证通过后仍需满足资源授权策略。'),
        sources=(('IETF RATS · RFC 9334', 'https://www.rfc-editor.org/rfc/rfc9334.html'),
                 ('Trustee architecture', 'https://confidentialcontainers.org/docs/attestation/architecture/')),
    )


def runtime_boundaries(zh):
    host_kernel = ('Host Linux kernel', '宿主 Linux 内核')[zh]
    guest_kernel = ('Guest Linux kernel', 'Guest Linux 内核')[zh]
    vm_boundary = ('VM boundary', 'VM 隔离边界')[zh]
    deployments = [
        (('Conventional Linux containers', '普通 Linux 容器'),
         ('Container runtime (e.g. runc)', '容器运行时（如 runc）'),
         ('Container A · Container B', '容器 A · 容器 B'), None),
        (('Direct microVM', '直接运行 microVM'),
         ('Sandbox service → Firecracker VMM', '沙箱服务 → Firecracker VMM'),
         ('Agent task process', 'Agent 任务进程'), ('microVM', 'microVM')),
        (('Kata Containers', 'Kata Containers'),
         ('kubelet → Kata shim → VMM', 'kubelet → Kata shim → VMM'),
         ('App container · Sidecar', '应用容器 · Sidecar'), ('Pod VM', 'Pod VM')),
    ]
    cards = []
    for title, launcher, workloads, guest in deployments:
        workload_layer = f'<p class="runtime-layer">{escape(workloads[zh])}</p>'
        kernel = host_kernel
        if guest:
            workload_layer = (
                f'<div class="runtime-guest"><strong>{guest[zh]} · {vm_boundary}</strong>'
                f'{workload_layer}<p class="runtime-kernel">{guest_kernel}</p></div>'
            )
            kernel += ' + KVM'
        cards.append(
            f'<div class="runtime-stack"><h4>{escape(title[zh])}</h4>'
            f'<p class="runtime-launch">{escape(launcher[zh])}</p>'
            f'{workload_layer}<p class="runtime-kernel">{kernel}</p></div>'
        )
    return figure(
        zh, 'runtime-boundaries-diagram',
        ('Which kernel does the workload use?', '工作负载使用哪个内核？'),
        '<div class="runtime-stacks">' + ''.join(cards) + '</div>',
        ('The dashed boxes show the VM boundary around the workload and the guest kernel it uses. The launcher and VMM run on the host side.',
         '虚线框标出 VM 隔离边界，工作负载及其使用的 Guest 内核在框内。启动组件和 VMM 在宿主侧运行。'),
        sources=(('Docker containers', 'https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-a-container/'),
                 ('Firecracker Design', 'https://github.com/firecracker-microvm/firecracker/blob/main/docs/design.md'),
                 ('Kata Architecture', 'https://github.com/kata-containers/kata-containers/blob/main/docs/design/architecture/README.md')),
    )


def kata_stack(zh):
    body = nodes(zh, [
        (('Host · Kubernetes and Kata shim', '宿主 · Kubernetes 与 Kata shim'),
         ('Kubelet requests a Pod sandbox through the CRI. With containerd, the configured Kata shim starts the VM.',
          'kubelet 通过 CRI 请求创建 Pod 沙箱。在 containerd 部署中，由配置好的 Kata shim 启动 VM。')),
        (('Host · VMM and KVM', '宿主 · VMM 与 KVM'),
         ('The VMM configures vCPUs, guest memory and virtual devices. KVM provides Linux’s hardware virtualization interface.',
          'VMM 配置 vCPU、Guest 内存与虚拟设备。KVM 提供 Linux 的硬件虚拟化接口。')),
        (('Inside PodVM · Linux and kata-agent', 'PodVM 内 · Linux 与 kata-agent'),
         ('The guest boots its own kernel. The host shim sends lifecycle requests to kata-agent, commonly through ttRPC over vsock.',
          'Guest 启动自己的内核。宿主 shim 通常经 vsock 上的 ttRPC 向 kata-agent 发送生命周期请求。')),
        (('Inside PodVM · Pod containers', 'PodVM 内 · Pod 容器'),
         ('The Guest starts the application and sidecar containers as isolated processes sharing its kernel.',
          'Guest 把应用容器和 sidecar 启动为相互隔离的进程，它们共享 Guest 内核。')),
    ])
    return figure(
        zh, 'kata-stack-diagram', ('From a Kubernetes Pod to containers inside a VM', '从 Kubernetes Pod 到 VM 内的容器'),
        body,
        ('Read this as the layers involved in startup. Once the VM is running, lifecycle RPCs go from the host Kata shim to kata-agent over the host–guest channel.',
         '图中列出启动时涉及的层次。虚拟机启动后，容器生命周期 RPC 由宿主侧 Kata shim 经宿主与 Guest 的通信通道发给 kata-agent。'),
        sources=(('Kata Architecture', 'https://github.com/kata-containers/kata-containers/blob/main/docs/design/architecture/README.md'),
                 ('Virtualization in Kata', 'https://github.com/kata-containers/kata-containers/blob/main/docs/design/virtualization.md')),
    )


def sandbox_lifecycle(zh):
    body = nodes(zh, [
        (('Allocate', '分配'),
         ('Bind the job to its tenant and policy. Start a clean sandbox or authorize a tenant-scoped restore.',
          '绑定任务、租户和策略。启动干净沙箱，或授权恢复该租户的快照。')),
        (('Run', '运行'),
         ('Mount minimal data, assign a temporary workspace and enforce limits and egress.',
          '挂载必要数据，分配临时工作区，限制资源用量和网络出口。')),
        (('Export or pause', '导出或暂停'),
         ('Approve permitted artifacts. Store any snapshot under the same tenant’s access policy.',
          '审批允许导出的产物。保存快照时应用原租户的访问策略。')),
        (('Revoke and destroy', '撤销与销毁'),
         ('Revoke job access and delete temporary state. Apply retention limits to saved artifacts and snapshots.',
          '撤销任务访问权限，删除临时状态。已保存的产物与快照按保留期限清理。')),
    ])
    return figure(
        zh, 'sandbox-lifecycle-diagram',
        ('Sandbox lifecycle and tenant state', '沙箱生命周期与租户状态'), body,
        ('Recheck tenant, policy version and snapshot integrity before resuming a job. Revalidate credentials for the resumed session.',
         '恢复任务前重新核对租户、策略版本和快照完整性，并重新校验恢复会话的凭据。'),
    )
