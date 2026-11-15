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


def deployment_architecture(zh):
    ingress = nodes(zh, [
        (('Request and external data', '请求与外部数据'),
         ('Authenticated user intent, plus web, files and tool results marked by source.',
          '记录经过认证的用户意图，并标明网页、文件和工具结果的来源。')),
        (('Harness ↔ model', 'Harness ↔ 模型'),
         ('Build a minimal context. The model returns a proposed action.',
          '构建最小上下文，由模型返回拟执行动作。')),
    ])
    tool_path = nodes(zh, [
        (('Tool authorization gateway', '工具授权网关'),
         ('Check tenant, operation, resource and approval. Deny out-of-scope requests.',
          '检查租户、操作、资源和审批，拦截越权请求。')),
        (('Credential broker → tool API', '凭据代理 → 工具 API'),
         ('Attach a short-lived scoped credential to the permitted request.',
          '只为获准的请求附加短时限权凭据。')),
    ])
    code_path = nodes(zh, [
        (('Per-job sandbox', '任务级沙箱'),
         ('Run generated code with limited mounts, identity and resource budgets.',
          '限制挂载、身份和资源配额，在其中运行生成的代码。')),
        (('Egress proxy → permitted destination', '出口代理 → 允许的目标'),
         ('Check destination and data policy. Route privileged calls through the tool gateway.',
          '检查目的地和数据策略。调用高权限工具时转交授权网关。')),
    ])
    dispatch, tool_label, code_label, audit_label = (
        ('按动作类型分发', '结构化工具调用', '运行生成的代码', '审计与会话状态') if zh
        else ('Dispatch by action type', 'Structured tool call', 'Generated code', 'Audit and session state')
    )
    audit = (
        '网关与出口代理记录策略判断，运行日志和产物按租户隔离。工具结果返回 Harness 时继续保留来源和敏感度标记。'
        if zh else
        'The gateway and proxy record policy decisions. Logs and artifacts stay tenant-scoped. Tool results return to the harness with provenance and sensitivity labels.'
    )
    body = f'''{ingress}<p class="drawing-dispatch">{dispatch}</p><div class="drawing-lanes">
      <div class="drawing-lane"><strong>{tool_label}</strong>{tool_path}</div>
      <div class="drawing-lane"><strong>{code_label}</strong>{code_path}</div>
    </div><p class="drawing-audit"><strong>{audit_label}</strong> {audit}</p>'''
    return figure(
        zh, 'agent-system-diagram',
        ('Reference architecture for a cloud agent', '云端 Agent 安全参考架构'), body,
        ('The model proposes an action. The gateway and proxy enforce policy at the points where tools execute and data leaves.',
         '模型提出动作。授权网关在工具执行前校验权限，出口代理在数据离开前校验流向。'),
        sources=(('OWASP AI Agent Security', 'https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html'),),
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
        sources=(('MCP Security Best Practices', 'https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices'),),
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
