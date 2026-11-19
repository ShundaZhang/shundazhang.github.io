"""Build the bilingual, dependency-free virtualization learning site."""
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent


SOURCES = {
    'qemu': ('QEMU system introduction', 'https://www.qemu.org/docs/master/system/introduction.html'),
    'kvm': ('Linux KVM API', 'https://docs.kernel.org/virt/kvm/api.html'),
    'intel': ('Intel SDM · VMX and EPT', 'https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html'),
    'amd': ('AMD64 APM · System Programming', 'https://docs.amd.com/v/u/en-US/24593_3.44_APM_Vol2'),
    'riscv': ('RISC-V Hypervisor extension', 'https://docs.riscv.org/reference/isa/priv/hypervisor.html'),
    'mmu': ('KVM x86 MMU', 'https://docs.kernel.org/virt/kvm/x86/mmu.html'),
    'virtio': ('OASIS Virtio 1.2', 'https://docs.oasis-open.org/virtio/virtio/v1.2/virtio-v1.2.html'),
    'vhost': ('QEMU vhost-user protocol', 'https://www.qemu.org/docs/master/interop/vhost-user.html'),
    'vfio': ('Linux VFIO', 'https://docs.kernel.org/driver-api/vfio.html'),
    'sriov': ('Linux SR-IOV guide', 'https://docs.kernel.org/PCI/pci-iov-howto.html'),
    'images': ('QEMU disk images', 'https://www.qemu.org/docs/master/system/images.html'),
    'snapshot': ('libvirt snapshots', 'https://libvirt.org/formatsnapshot.html'),
    'network': ('libvirt virtual networks', 'https://libvirt.org/formatnetwork.html'),
    'vxlan': ('Linux VXLAN', 'https://docs.kernel.org/networking/vxlan.html'),
    'domain': ('libvirt domain configuration', 'https://libvirt.org/formatdomain.html'),
    'clock': ('KVM timekeeping', 'https://docs.kernel.org/virt/kvm/x86/timekeeping.html'),
    'ksm': ('Linux KSM', 'https://docs.kernel.org/admin-guide/mm/ksm.html'),
    'migration': ('QEMU migration framework', 'https://www.qemu.org/docs/master/devel/migration/main.html'),
    'nested': ('KVM nested guests', 'https://docs.kernel.org/virt/kvm/x86/running-nested-guests.html'),
    'security': ('QEMU security model', 'https://www.qemu.org/docs/master/system/security.html'),
    'firecracker': ('Firecracker design', 'https://github.com/firecracker-microvm/firecracker/blob/main/docs/design.md'),
    'kata': ('Kata Containers architecture', 'https://github.com/kata-containers/kata-containers/blob/main/docs/design/architecture/README.md'),
    'hyperv': ('Microsoft Hyper-V architecture', 'https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/architecture'),
    'invocation': ('QEMU invocation', 'https://www.qemu.org/docs/master/system/invocation.html'),
    'virsh': ('virsh manual', 'https://libvirt.org/manpages/virsh.html'),
}


def build(zh):
    def t(en, cn):
        return cn if zh else en

    def p(en, cn):
        return '<p>' + t(en, cn) + '</p>'

    def refs(*keys):
        return '<ul class="sources" aria-label="' + t('Official references', '官方资料') + '">' + ''.join(
            f'<li><a href="{SOURCES[key][1]}" target="_blank" rel="noopener noreferrer">{escape(SOURCES[key][0])}</a></li>'
            for key in keys
        ) + '</ul>'

    def table(headings, rows):
        head = ''.join(f'<th scope="col">{t(*label)}</th>' for label in headings)
        body = ''.join('<tr>' + ''.join(
            f'<th scope="row">{t(*cell)}</th>' if index == 0 else f'<td>{t(*cell)}</td>'
            for index, cell in enumerate(row)
        ) + '</tr>' for row in rows)
        return '<div class="table-scroll" tabindex="0" role="region" aria-label="' + t('Scrollable comparison', '可滚动的对照表') + '"><table><thead><tr>' + head + '</tr></thead><tbody>' + body + '</tbody></table></div>'

    def bullets(items):
        return '<ul class="explain">' + ''.join(f'<li>{t(*item)}</li>' for item in items) + '</ul>'

    def block(label, detail='', kind=''):
        return f'<div class="block {kind}"><strong>{escape(t(*label))}</strong>' + (f'<span>{escape(t(*detail))}</span>' if detail else '') + '</div>'

    def flow(items):
        return '<div class="flow">' + ''.join(block(label, detail) for label, detail in items) + '</div>'

    def fig(ident, title, body, note):
        return f'<figure class="diagram" id="{ident}" aria-labelledby="{ident}-title"><figcaption id="{ident}-title">{escape(t(*title))}</figcaption>{body}<p class="diagram-note">{escape(t(*note))}</p></figure>'

    def code(value):
        return '<pre><code>' + escape(value) + '</code></pre>'

    chapters = [
        ('foundation', 'The VM stack', '虚拟机技术全景'),
        ('cpu', 'CPU virtualization', 'CPU 虚拟化'),
        ('memory', 'Memory virtualization', '内存虚拟化'),
        ('io', 'Devices and DMA', '设备与 DMA'),
        ('storage', 'Disks and snapshots', '磁盘与快照'),
        ('network', 'Virtual networks', '虚拟网络'),
        ('performance', 'Scheduling and performance', '调度与性能'),
        ('migration', 'Migration and nesting', '迁移与嵌套'),
        ('platforms', 'Platforms and microVMs', '平台与 microVM'),
        ('security', 'Isolation boundaries', '隔离边界'),
        ('labs', 'Practice', '动手实践'),
        ('reading', 'Reading path', '资料与学习路径'),
    ]

    def section(index, lead, body):
        ident, en, cn = chapters[index]
        return f'<section class="chapter" id="{ident}"><header><h2>{t(en, cn)}</h2><p>{t(*lead)}</p></header>{body}</section>'

    guest_a = block(('VM A', '虚拟机 A'), ('Applications + guest kernel', '应用 + Guest 内核'), 'guest')
    guest_b = block(('VM B', '虚拟机 B'), ('Applications + guest kernel', '应用 + Guest 内核'), 'guest')
    stack = '<div class="stack"><div class="columns">' + guest_a + guest_b + '</div>' + block(
        ('QEMU processes', 'QEMU 进程'), ('Machine model · virtual devices · guest RAM backing', '机器模型 · 虚拟设备 · Guest RAM 后备内存')) + block(
        ('Linux kernel + KVM', 'Linux 内核 + KVM'), ('Host scheduling · memory management · virtualization controls', '宿主调度 · 内存管理 · 虚拟化控制')) + block(
        ('Physical machine', '物理机器'), ('CPU virtualization extensions · DRAM · PCIe devices', 'CPU 虚拟化扩展 · DRAM · PCIe 设备'), 'hardware') + '</div>'
    foundation = section(0, (
        'A VM presents a machine interface to a guest operating system. Follow the execution, memory and I/O paths separately.',
        '虚拟机向 Guest 操作系统提供一套机器接口。分别沿执行、内存和 I/O 路径，理解它如何使用真实硬件。',
    ), fig('vm-stack', ('A Linux QEMU/KVM deployment', 'Linux 上的 QEMU/KVM 部署'), stack,
        ('This is a simplified placement diagram. Guest instructions can execute directly on the physical CPU under KVM control.', '此图简化展示组件位置。Guest 指令可在 KVM 控制下直接在物理 CPU 上执行。')) + table(
        [('Term', '概念'), ('Responsibility', '职责'), ('Concrete example', '具体例子')], [
            [('Hypervisor / VMM', 'Hypervisor / VMM'), ('Controls virtual CPU state, address spaces and device access. Implementations divide this work across kernel and userspace.', '控制虚拟 CPU 状态、地址空间和设备访问，具体实现可将工作分布在内核与用户态。'), ('KVM handles virtualization in the Linux kernel. QEMU supplies a machine model and device backends.', 'KVM 在 Linux 内核中提供虚拟化能力，QEMU 提供机器模型与设备后端。')],
            [('Hardware-assisted virtualization', '硬件辅助虚拟化'), ('Uses CPU virtualization extensions to run compatible guest instructions and intercept selected operations.', '通过 CPU 虚拟化扩展运行兼容的 Guest 指令，并拦截选定操作。'), ('Intel VMX, AMD SVM, RISC-V H', 'Intel VMX、AMD SVM、RISC-V H')],
            [('Emulation', '模拟执行'), ('Software implements the target CPU and machine, allowing an ISA different from the host.', '软件实现目标 CPU 和机器，可运行与宿主 ISA 不同的系统。'), ('QEMU TCG can run a RISC-V guest on an x86 host.', 'QEMU TCG 可在 x86 宿主模拟 RISC-V Guest。')],
            [('Paravirtualization', '半虚拟化'), ('The guest cooperates through a virtualization-aware interface.', 'Guest 通过感知虚拟化的接口与宿主协作。'), ('Virtio drivers and paravirtual clocks can coexist with hardware-assisted CPU execution.', 'Virtio 驱动、半虚拟化时钟可与硬件辅助 CPU 执行配合。')],
            [('VM management', '虚拟机管理层'), ('Creates domains, configures devices and coordinates lifecycle operations.', '创建虚拟机、配置设备并协调生命周期操作。'), ('libvirt / virsh / virt-manager', 'libvirt / virsh / virt-manager')],
        ]) + p(
        'Type 1 commonly describes a hypervisor at the hardware layer. Type 2 describes a VMM hosted by an operating system. For Linux/KVM, inspect the kernel virtualization and userspace device components to understand the actual boundary.',
        'Type 1 通常指直接位于硬件层的 Hypervisor，Type 2 指运行在宿主操作系统上的 VMM。理解 Linux/KVM 时，可以进一步拆开内核虚拟化与用户态设备组件，查看实际边界。') + '<h3>' + t('From configuration to guest boot', '从配置到 Guest 启动') + '</h3>' + bullets([
        ('<strong>Configure.</strong> The manager selects the CPU model, memory, firmware and device backends. A QEMU process allocates guest RAM backing.', '<strong>配置。</strong>管理层选定 CPU 模型、内存、固件与设备后端，QEMU 进程分配 Guest RAM 的后备内存。'),
        ('<strong>Create.</strong> KVM_CREATE_VM creates a VM handle. The VMM registers memory slots, creates vCPUs and initializes their state.', '<strong>创建。</strong>KVM_CREATE_VM 创建 VM 句柄，VMM 登记 memory slot、创建 vCPU 并初始化状态。'),
        ('<strong>Boot.</strong> Firmware or a direct kernel boot path starts the guest OS, which discovers its virtual hardware and loads drivers.', '<strong>启动。</strong>固件或直接内核启动路径拉起 Guest OS，Guest 枚举虚拟硬件并加载驱动。'),
    ]) + refs('qemu', 'kvm', 'domain'))

    cpu = section(1, (
        'A vCPU is saved architectural state plus a schedulable execution context. Ordinary guest computation can stay on the CPU.',
        'vCPU 由可保存的架构状态和可调度的执行上下文构成。普通 Guest 计算可直接在 CPU 上持续执行。',
    ), fig('vmexit', ('A userspace-handled device access', '一次由用户态处理的设备访问'), flow([
        (('Enter guest', '进入 Guest'), ('KVM_RUN starts or resumes a vCPU', 'KVM_RUN 启动或恢复 vCPU')),
        (('Guest executes', 'Guest 执行'), ('An intercepted MMIO access triggers an exit', '被拦截的 MMIO 访问触发退出')),
        (('KVM handles exit', 'KVM 处理退出'), ('Return KVM_EXIT_MMIO when userspace is needed', '需要用户态时返回 KVM_EXIT_MMIO')),
        (('QEMU backend', 'QEMU 后端'), ('Emulate the access and resume with KVM_RUN', '模拟设备访问，再调用 KVM_RUN 恢复')),
    ]), ('KVM handles some exits entirely in the kernel. The hypervisor configures which events trigger exits.', '部分退出由 KVM 在内核中直接处理。Hypervisor 配置哪些事件触发退出。')) + table(
        [('Architecture', '架构'), ('Execution controls', '执行控制'), ('Memory / interrupt support', '内存与中断支持')], [
            [('Intel x86 VMX', 'Intel x86 VMX'), ('VMX root hosts the VMM, non-root runs the guest. Both have privilege rings. VMCS holds guest/host state and controls, with VMLAUNCH / VMRESUME and VM exits.', 'VMM 使用 VMX root，Guest 使用 non-root，两者各自具有特权环。VMCS 保存 Guest/Host 状态及控制项，配合 VMLAUNCH / VMRESUME 和 VM exit。'), ('EPT translates GPA to HPA. APIC virtualization and posted interrupts reduce selected interrupt overhead.', 'EPT 完成 GPA 到 HPA 的转换。APIC 虚拟化和 posted interrupt 可减少部分中断开销。')],
            [('AMD x86 SVM', 'AMD x86 SVM'), ('VMCB records guest state and intercept controls. VMRUN enters the guest, with intercepted operations returning control to the VMM.', 'VMCB 记录 Guest 状态与拦截控制，VMRUN 进入 Guest，被拦截的操作使控制权返回 VMM。'), ('Nested Page Tables (NPT) provide second-stage address translation.', 'Nested Page Tables（NPT）提供第二阶段地址转换。')],
            [('RISC-V H extension', 'RISC-V H 扩展'), ('HS-mode manages guests running in VS/VU modes. Virtual supervisor CSRs and trap routing preserve a guest supervisor environment.', 'HS 模式管理运行在 VS/VU 模式的 Guest，通过虚拟 supervisor CSR 与陷入路由提供 Guest supervisor 环境。'), ('vsatp controls VS-stage translation, hgatp controls G-stage. Virtual interrupt injection is managed by hypervisor CSRs and applicable interrupt extensions.', 'vsatp 管理 VS-stage，hgatp 管理 G-stage。通过 Hypervisor CSR 和适用的中断扩展注入虚拟中断。')],
        ]) + p(
        'A guest syscall normally switches from guest user mode to its own kernel. An exit occurs when an event meets the configured virtualization controls. During a VM switch, registers, interrupt state and relevant control state must remain consistent.',
        'Guest syscall 通常从 Guest 用户态进入自己的内核。事件满足虚拟化控制项配置时才触发退出，切换时须保持寄存器、中断及相关控制状态一致。') + refs('intel', 'amd', 'riscv', 'kvm'))

    memory = section(2, (
        'The guest owns its process page tables. The hypervisor controls the mapping from guest physical memory to host physical pages.',
        'Guest 管理进程页表，Hypervisor 控制 Guest 物理内存到宿主物理页的映射。',
    ), fig('two-stage-translation', ('One load, two address translations', '一次访存，两阶段地址转换'), flow([
        (('GVA · process address', 'GVA · 进程虚拟地址'), ('0x0040_1234', '0x0040_1234')),
        (('Guest page tables', 'Guest 页表'), ('GVA → GPA 0x002A_1234', 'GVA → GPA 0x002A_1234')),
        (('EPT / NPT / G-stage', 'EPT / NPT / G-stage'), ('GPA → HPA 0x812A_1234', 'GPA → HPA 0x812A_1234')),
        (('Physical memory', '物理内存'), ('Read the byte at HPA', '读取 HPA 指向的字节')),
    ]), ('Illustrative 4 KiB mappings preserve the 0x234 page offset. The addresses show the final mapping, not a page-table entry format.', '示例采用 4 KiB 页，页内偏移 0x234 保持不变。地址展示映射结果，页表项格式另由架构定义。')) + bullets([
        ('<strong>Nested page walks.</strong> Guest page-table entries live at GPAs, so reading them also requires second-stage translation. A combined translation cached by the TLB can avoid repeated walks.', '<strong>嵌套页表遍历。</strong>Guest 页表项位于 GPA，读取这些页表项也需要第二阶段转换。TLB 缓存组合后的转换结果，可减少重复遍历。'),
        ('<strong>Two kinds of faults.</strong> A guest page fault is handled by its OS for an invalid first-stage mapping. An EPT violation or guest-page fault can transfer control to the hypervisor for a second-stage mapping or permission issue.', '<strong>两类缺页。</strong>第一阶段映射无效时，由 Guest OS 处理 Guest page fault。第二阶段映射或权限有问题时，可触发 EPT violation 或 RISC-V guest-page fault，交由 Hypervisor 处理。'),
        ('<strong>Shadow paging.</strong> The VMM can maintain a composed mapping from GVA to HPA and track guest page-table changes. Hardware-assisted two-stage paging moves the nested translation machinery into the CPU.', '<strong>影子页表。</strong>VMM 维护 GVA 到 HPA 的组合映射，跟踪 Guest 页表更新。硬件辅助两阶段分页则由 CPU 完成嵌套转换。'),
        ('<strong>Mappings need invalidation.</strong> Reassigning a host page requires invalidating affected cached translations. Architecture mechanisms include INVEPT / INVVPID and RISC-V HFENCE operations.', '<strong>修改映射需失效缓存。</strong>重新分配宿主页时，需要清除受影响的缓存转换。架构提供 INVEPT / INVVPID、RISC-V HFENCE 等机制。'),
    ]) + p(
        'In a conventional userspace VMM, a host virtual address (HVA) locates the memory backing a GPA. KVM memory slots associate guest ranges with that backing. HVA belongs to the host process view, while the CPU’s second-stage translation ultimately selects a host physical page.',
        '在常规用户态 VMM 中，宿主虚拟地址 HVA 定位 GPA 对应的后备内存，KVM memory slot 将 Guest 地址范围关联到该内存。HVA 属于宿主进程视图，CPU 第二阶段转换最终选中的是宿主物理页。') + refs('mmu', 'riscv', 'kvm'))

    io = section(3, (
        'A virtual device needs a programming interface, a data path and a way to notify completion. Device assignment adds DMA isolation requirements.',
        '虚拟设备需要编程接口、数据路径和完成通知。设备直通还需要约束 DMA 能访问哪些内存。',
    ), table([('Model', '方式'), ('Data path', '数据路径'), ('Engineering trade-off', '工程取舍')], [
        [('Emulated device', '设备模拟'), ('Guest driver accesses a model of hardware registers, such as a virtual e1000 NIC.', 'Guest 驱动访问模拟硬件寄存器，例如虚拟 e1000 网卡。'), ('Works with existing device drivers, with register emulation and exit overhead.', '可复用已有设备驱动，开销包括寄存器模拟和退出。')],
        [('Virtio', 'Virtio'), ('Guest frontend and host backend exchange buffers through shared virtqueues.', 'Guest 前端与宿主后端通过共享 virtqueue 交换缓冲区。'), ('Requires a compatible guest driver. Batching and notification suppression reduce overhead.', '需要兼容的 Guest 驱动，批处理与通知抑制可降低开销。')],
        [('VFIO passthrough', 'VFIO 直通'), ('The guest uses an assigned physical device or PCIe function.', 'Guest 使用被分配的物理设备或 PCIe function。'), ('Needs IOMMU isolation, device reset and suitable host grouping. Device state affects migration support.', '需检查 IOMMU 隔离、设备复位与宿主分组，设备状态也影响迁移支持。')],
        [('SR-IOV', 'SR-IOV'), ('A Physical Function (PF) exposes Virtual Functions (VFs), which can be assigned to guests.', '物理功能 PF 创建多个虚拟功能 VF，可分别分配给 Guest。'), ('Guests share physical hardware resources. Firmware, per-VF features and isolation depend on the device.', 'Guest 共享物理硬件资源，固件、单 VF 能力和隔离行为取决于设备。')],
    ]) + fig('virtqueue-flow', ('Virtio split virtqueue request flow', 'Virtio split virtqueue 请求流程'), flow([
        (('Guest driver', 'Guest 驱动'), ('Fill descriptors with buffer addresses and lengths', '填写含缓冲区地址与长度的描述符')),
        (('Available ring', 'Available ring'), ('Publish descriptor chain head, then notify if needed', '发布描述符链首索引，按需通知')),
        (('Device backend', '设备后端'), ('Validate descriptors and process buffers', '验证描述符并处理缓冲区')),
        (('Used ring', 'Used ring'), ('Publish completion; driver recycles buffers', '发布完成项，驱动回收缓冲区')),
    ]), ('Memory ordering and ownership rules govern when each side may read or reuse a buffer. Packed virtqueues use a different ring layout.', '内存顺序和所有权规则决定双方何时可以读取或复用缓冲区。Packed virtqueue 使用另一种环布局。')) + p(
        'vhost moves supported Virtio backend processing into the kernel. vhost-user uses a separate userspace backend process, with a control channel to configure shared memory and queues. These optimize where I/O work runs.',
        'vhost 可将支持的 Virtio 后端处理移到内核；vhost-user 使用独立用户态后端进程，通过控制通道配置共享内存与队列。它们优化的是 I/O 处理的位置。') + fig('iommu-path', ('The device has its own address translation path', '设备有自己的地址转换路径'), flow([
        (('Assigned PCIe function', '已分配的 PCIe function'), ('DMA request + requester identity', 'DMA 请求 + 请求方标识')),
        (('IOMMU', 'IOMMU'), ('Translate permitted IOVA mappings', '转换允许的 IOVA 映射')),
        (('Assigned host pages', '分配给 Guest 的宿主页'), ('DMA reaches only mapped pages', 'DMA 访问映射允许的页')),
    ]), ('CPU EPT/NPT and device IOMMU tables serve different requesters. VFIO configures device access through the IOMMU domain.', 'CPU 的 EPT/NPT 与设备 IOMMU 页表服务于不同请求方，VFIO 通过 IOMMU domain 配置设备访问。')) + refs('virtio', 'vhost', 'vfio', 'sriov'))

    storage = section(4, (
        'The guest sees logical sectors. The host maps them to a file, a block device or a network storage backend.',
        'Guest 看到逻辑扇区，宿主将其映射到文件、块设备或网络存储后端。',
    ), p(
        'Raw images map virtual disk offsets with little format metadata. qcow2 adds cluster allocation, reference counts and copy-on-write. A sparse image allocates host storage as data is written. Deleting a guest file releases host space only when discard and the full storage path support reclamation.',
        'Raw 镜像的格式元数据较少；qcow2 增加 cluster 分配、引用计数与写时复制。稀疏镜像随写入分配宿主空间，删除 Guest 文件后能否回收宿主空间，取决于 discard 及整个存储路径的支持。') + fig('cow-disk', ('An external copy-on-write overlay', '外部写时复制增量盘'), '<div class="columns">' + block(
        ('Read unchanged sector', '读取未修改的扇区'), ('Guest → overlay lookup → backing image', 'Guest → 查询增量盘 → 读取基础镜像')) + block(
        ('Write a sector', '写入一个扇区'), ('Guest → allocate overlay cluster → keep backing image intact', 'Guest → 在增量盘分配 cluster → 保留基础镜像内容')) + '</div>',
        ('The overlay depends on its backing chain. Moving or deleting a backing image changes what the overlay can read.', '增量盘依赖完整的 backing chain，移动或删除基础镜像会影响增量盘读取。')) + table(
        [('Captured state', '捕获状态'), ('What it gives you', '能够恢复什么'), ('Consistency', '一致性')], [
            [('Disk snapshot', '磁盘快照'), ('Disk contents at a point in time', '某一时刻的磁盘内容'), ('A running guest may produce crash-consistent state. Guest filesystem freeze and application coordination improve consistency.', '运行中的 Guest 可能仅达到崩溃一致性，文件系统冻结与应用协调可提高一致性。')],
            [('Memory + device state', '内存与设备状态'), ('CPU registers, RAM and supported virtual devices', 'CPU 寄存器、RAM 和支持的虚拟设备状态'), ('Restore against matching disk state and a compatible virtual machine configuration.', '恢复时须配套匹配的磁盘状态与兼容虚拟机配置。')],
            [('Backup', '备份'), ('A retained copy with a defined recovery process', '按恢复方案保留的独立副本'), ('Test restore, retention and dependency integrity. External services keep their own state.', '验证恢复、保留策略及依赖完整性，外部服务另有自己的状态。')],
        ]) + p(
        'Durability also depends on guest flush requests, host caching and the storage backend. A snapshot restores local state, while a previously sent network message or committed external transaction keeps its effect.',
        '持久性还取决于 Guest flush 请求、宿主缓存与存储后端。快照恢复本地状态，先前已发出的网络消息或已提交的外部事务仍有其效果。') + refs('images', 'snapshot'))

    network = section(5, (
        'Separate the virtual NIC from the virtual switch and the uplink policy. They solve different parts of packet delivery.',
        '将虚拟网卡、虚拟交换机和上联策略分开理解，它们各自处理数据包转发的一部分。',
    ), fig('packet-path', ('A bridged Virtio network path', 'Virtio 桥接网络路径'), flow([
        (('Guest', 'Guest'), ('Socket → guest TCP/IP → virtio-net', 'Socket → Guest TCP/IP → virtio-net')),
        (('Host backend', '宿主后端'), ('QEMU or vhost-net → TAP interface', 'QEMU 或 vhost-net → TAP 接口')),
        (('Virtual switch', '虚拟交换机'), ('Linux bridge or Open vSwitch', 'Linux bridge 或 Open vSwitch')),
        (('Uplink', '物理上联'), ('Host physical NIC → network', '宿主物理网卡 → 外部网络')),
    ]), ('NAT adds routing and address translation to the forwarding path. A passed-through VF uses a different data path.', 'NAT 会在转发路径上加入路由与地址转换，直通 VF 使用另一条数据路径。')) + table(
        [('Mode', '模式'), ('Packet handling', '包如何转发'), ('Where to inspect', '查看位置')], [
            [('NAT', 'NAT'), ('Guests use a private subnet and the host translates permitted outbound traffic.', 'Guest 使用私有子网，宿主对允许的出站流量做地址转换。'), ('Host routes, NAT rules and explicit inbound mappings', '宿主路由、NAT 规则与显式入站映射')],
            [('Bridge / routed', '桥接 / 路由'), ('A bridge forwards Layer 2 frames. Routed networks forward between IP subnets.', '桥接转发二层帧，路由网络在 IP 子网间转发。'), ('Switch ports, VLANs, routes and access policy', '交换端口、VLAN、路由及访问策略')],
            [('Isolated virtual network', '隔离虚拟网络'), ('Guests can share a host-side virtual network with no configured external forwarding.', 'Guest 可共享宿主虚拟网络，由配置限制外部转发。'), ('Guest-to-guest policy and access to services on the host', 'Guest 互访策略与宿主服务访问')],
        ]) + p(
        'In a cloud, an overlay such as VXLAN can connect tenant networks across hosts using encapsulation. Network identity and policy bind virtual ports to tenants. Place enforcement on the actual packet path, including offloaded or directly assigned devices.',
        '云环境还可用 VXLAN 等封装连接跨宿主的租户网络，将虚拟端口与租户身份、策略绑定。策略执行点须覆盖实际包路径，包括被卸载或直通的设备。') + refs('network', 'vxlan'))

    performance = section(6, (
        'Measure contention, memory locality and I/O queues alongside CPU utilization. Every VM still consumes physical resources.',
        '结合 CPU 利用率、资源竞争、内存局部性和 I/O 队列分析性能，每台 VM 都需要实际物理资源。',
    ), table([('Mechanism', '机制'), ('Principle', '原理'), ('What to observe', '观察指标')], [
        [('vCPU scheduling', 'vCPU 调度'), ('In a typical QEMU/KVM setup, vCPUs run in host threads. Several runnable vCPUs may compete for physical CPU time.', '典型 QEMU/KVM 中，vCPU 在宿主线程中运行，多个可运行 vCPU 可能竞争物理 CPU 时间。'), ('Guest steal time where supported, host scheduling delay, CPU pinning and SMT contention', '支持时查看 Guest steal time，并观察宿主调度延迟、绑核与 SMT 竞争')],
        [('NUMA placement', 'NUMA 放置'), ('Keep guest memory near the CPUs executing it, with a guest topology consistent with host placement.', '将 Guest 内存靠近执行它的 CPU 放置，Guest 拓扑与宿主分配相匹配。'), ('Remote memory access, bandwidth and cross-node placement', '远端内存访问、带宽及跨节点放置')],
        [('Huge pages', '大页'), ('Larger mappings can reduce TLB pressure at the guest or host stage, subject to alignment and backing support.', '满足对齐及后备内存条件时，Guest 或 Host 阶段的大页映射可降低 TLB 压力。'), ('TLB misses, fragmentation and available huge-page pools', 'TLB miss、内存碎片及大页池余量')],
        [('Ballooning and overcommit', '气球与超分'), ('A guest balloon driver releases usable guest pages to the host when instructed. Host demand can exceed currently available RAM.', 'Guest balloon 驱动按指示交还可用 Guest 页，宿主承诺的内存可能超过当前实际余量。'), ('Guest memory pressure, swap latency and host OOM risk', 'Guest 内存压力、swap 延迟和宿主 OOM 风险')],
        [('KSM', 'KSM'), ('Registered identical pages can share a write-protected host page, copied when written.', '已登记的相同页可合并为一个写保护宿主页，写入时再复制。'), ('ksmd CPU work, page sharing and cross-tenant deduplication policy', 'ksmd CPU 开销、共享页数量与跨租户去重策略')],
        [('Queue and thread tuning', '队列与线程调优'), ('Virtio multiqueue and I/O threads can distribute work across cores.', 'Virtio 多队列与 I/O 线程可将处理分布到多个核心。'), ('Queue depth, interrupt rate, p95/p99 latency and backend saturation', '队列深度、中断率、p95/p99 延迟和后端饱和情况')],
    ]) + p(
        'Virtual time needs special care when a vCPU is descheduled or moved to another host. KVM clock interfaces and TSC virtualization help guests read a consistent clock. Timer delivery latency can still affect time-sensitive applications.',
        'vCPU 被暂停调度或迁往其他宿主时，虚拟时钟需要保持连续。KVM clock 接口与 TSC 虚拟化帮助 Guest 获取一致的时钟，定时器递送延迟仍会影响时延敏感应用。') + refs('domain', 'ksm', 'clock'))

    migration = section(7, (
        'Migration transfers a running machine’s state between hosts. Nesting runs a hypervisor inside a guest.',
        '迁移将一台机器的运行状态转移到其他宿主，嵌套虚拟化则在 Guest 内运行另一个 Hypervisor。',
    ), fig('precopy', ('Live migration with pre-copy', 'Pre-copy 热迁移'), flow([
        (('Prepare destination', '准备目标端'), ('Compatible CPU model, machine and devices', '兼容 CPU 模型、机器及设备')),
        (('Copy RAM', '复制 RAM'), ('Source runs and tracks dirtied pages', '源端继续运行并跟踪脏页')),
        (('Repeat dirty pages', '重复复制脏页'), ('Transfer pages changed since the last round', '传送上一轮以来修改的页')),
        (('Stop and switch', '暂停并切换'), ('Transfer final state, resume destination', '传送最终状态，在目标端恢复')),
    ]), ('Storage must be shared or transferred in a coordinated way. Device state and in-flight I/O need migration support.', '存储须共享或协调传输，设备状态及在途 I/O 需要相应迁移支持。')) + p(
        'If dirtying approaches the effective transfer rate, pre-copy may struggle to converge. Post-copy resumes the destination earlier and fetches missing pages on demand, creating a period of dependence on the source. CPU features, device backends and external network identity must be compatible across the move.',
        '脏页产生速率接近有效传输速率时，pre-copy 可能难以收敛。Post-copy 更早恢复目标端，按需拉取缺失页，因此存在依赖源端的阶段。迁移还须兼顾 CPU 特性、设备后端兼容及外部网络身份。') + fig(
        'nested-vm', ('Nested virtualization layers', '嵌套虚拟化层次'), '<div class="stack">' + block(
            ('L2 · nested guest', 'L2 · 嵌套 Guest'), ('Application and guest OS', '应用与 Guest OS'), 'guest') + block(
            ('L1 · guest hypervisor', 'L1 · Guest Hypervisor'), ('Runs a VMM inside an L0 guest', '在 L0 的 Guest 内运行 VMM')) + block(
            ('L0 · physical host hypervisor', 'L0 · 物理宿主 Hypervisor'), ('Owns the physical virtualization hardware', '管理物理虚拟化硬件'), 'hardware') + '</div>',
        ('L0 exposes a virtual virtualization interface to L1 and handles the combined execution and memory controls needed for L2.', 'L0 向 L1 暴露虚拟化接口，并处理 L2 所需的组合执行与内存控制。')) + refs('migration', 'nested'))

    platforms = section(8, (
        'Choose a stack by its supported guest, devices and management interface. Each product packages the underlying mechanisms differently.',
        '根据 Guest、设备与管理接口选择技术栈，各平台对底层机制有不同的组合方式。',
    ), table([('Stack', '技术栈'), ('Components and use', '组件与用途'), ('Read first', '先读什么')], [
        [('QEMU / KVM / libvirt', 'QEMU / KVM / libvirt'), ('Linux virtualization, with hardware execution, flexible device models and managed VM lifecycle.', 'Linux 虚拟化，结合硬件执行、灵活设备模型与 VM 生命周期管理。'), ('Start with KVM vCPU execution and the QEMU machine/device model.', '先理解 KVM 的 vCPU 执行和 QEMU 的机器 / 设备模型。')],
        [('Microsoft Hyper-V', 'Microsoft Hyper-V'), ('The hypervisor isolates partitions. The root partition manages devices, with VMBus connecting virtualization-aware I/O components.', 'Hypervisor 隔离各 partition，root partition 管理设备，VMBus 连接感知虚拟化的 I/O 组件。'), ('Root/child partitions, VSP/VSC and VMBus', 'Root / child partition、VSP/VSC 与 VMBus')],
        [('Firecracker microVM', 'Firecracker microVM'), ('A minimal KVM VMM with a reduced device model for lightweight guest workloads.', '基于 KVM 的精简 VMM，通过缩减设备模型运行轻量 Guest 工作负载。'), ('vCPU threads, Virtio devices, API and snapshot state', 'vCPU 线程、Virtio 设备、API 与快照状态')],
        [('Kata Containers', 'Kata Containers'), ('A container runtime places Pod containers inside a VM with a guest kernel and kata-agent.', '容器运行时将 Pod 容器放进 VM，VM 内包含 Guest 内核与 kata-agent。'), ('Host shim, VMM backend and guest-agent lifecycle RPCs', '宿主 shim、VMM 后端与 Guest agent 生命周期 RPC')],
    ]) + p(
        'A microVM still has vCPUs, guest memory and its own kernel. Reducing devices and boot dependencies helps build a smaller runtime. Kata integrates a VM with container workflows. It can use different supported VMM backends.',
        'microVM 仍包含 vCPU、Guest 内存和独立内核，精简设备和启动依赖可缩小运行时。Kata 将 VM 接入容器工作流，并可选用不同受支持的 VMM 后端。') + refs('qemu', 'hyperv', 'firecracker', 'kata'))

    security = section(9, (
        'Trace which component handles guest-controlled input and which identity can administer the VM.',
        '追踪哪些组件处理 Guest 可控输入，以及哪些身份可以管理虚拟机。',
    ), bullets([
        ('<strong>Guest-to-host interfaces.</strong> Device descriptors, emulated registers, shared folders, guest agents and management APIs each expose parsing or authorization logic. Limit the enabled devices and backend privileges to the workload.', '<strong>Guest 到宿主接口。</strong>设备描述符、模拟寄存器、共享目录、Guest agent 和管理 API 都包含解析或授权逻辑。按工作负载收紧启用设备与后端权限。'),
        ('<strong>Management and saved state.</strong> Protect QMP/libvirt endpoints, VM images, snapshots and migration channels. Stored RAM can contain live credentials and customer data.', '<strong>管理面与保存状态。</strong>保护 QMP / libvirt 端点、镜像、快照与迁移通道，保存的 RAM 可能包含有效凭据和客户数据。'),
        ('<strong>Shared microarchitecture.</strong> Guests can contend for caches, predictors and memory bandwidth. Scheduling, CPU mitigations and tenant placement need to match the chosen isolation requirements.', '<strong>共享微架构。</strong>Guest 可能竞争缓存、预测器与内存带宽，需要按隔离要求配置调度、CPU 缓解措施和租户放置。'),
        ('<strong>Confidential VMs.</strong> TDX and SEV-SNP add protection for private guest state against a privileged host within their threat models. Their attestation and device-sharing rules extend the virtualization design.', '<strong>机密虚拟机。</strong>TDX、SEV-SNP 在各自威胁模型下保护 Guest 私有状态，抵御特权宿主。远程证明及设备共享规则进一步扩展了虚拟化设计。'),
    ]) + p(
        'For dedicated treatments, continue with <a href="/tee-tdx-sgx/">TEE</a>, <a href="/side-channel-atlas/">CPU side channels</a> or <a href="/agent-security-atlas/">Agent isolation</a>.',
        '专题详解可继续阅读 <a href="/tee-tdx-sgx/index.zh.html">TEE</a>、<a href="/side-channel-atlas/index.html">CPU 侧信道</a>或 <a href="/agent-security-atlas/index.zh.html">Agent 隔离</a>。') + refs('security'))

    labs = section(10, (
        'Use an x86-64 Linux host with QEMU/KVM for these exercises. Keep the virtual machine configuration with your measurements.',
        '以下练习使用装有 QEMU/KVM 的 x86-64 Linux 宿主，将虚拟机配置与测量结果一起记录。',
    ), '<h3>' + t('Inspect the host and an existing VM', '观察宿主与已有虚拟机') + '</h3>' + code(
        'lscpu\nls -l /dev/kvm\nqemu-system-x86_64 -accel help\nvirsh -c qemu:///system list --all\nvirsh -c qemu:///system dominfo lab-vm\nvirsh -c qemu:///system dumpxml lab-vm\nvirsh -c qemu:///system domstats lab-vm') + p(
        'Install QEMU and libvirt using your Linux distribution packages. Replace lab-vm with an existing domain and use an account authorized for that libvirt connection. Record the CPU model, vCPU count, memory backing, NIC model and storage format.',
        '通过 Linux 发行版软件包安装 QEMU 与 libvirt，将 lab-vm 换为已有虚拟机名，并使用有权访问对应 libvirt 连接的账号。记录 CPU 模型、vCPU 数、内存后备、网卡模型与存储格式。') + '<h3>' + t(
        'Boot a disposable overlay', '用独立增量盘启动练习 VM') + '</h3>' + p(
        'Prepare an existing, powered-off x86-64 Linux qcow2 boot image as base.qcow2. Use an image configured for a serial console and an appropriate boot mode. The example uses the default x86 firmware. The commands below create a new overlay in the current directory.',
        '准备已关机的 x86-64 Linux qcow2 启动镜像 base.qcow2，镜像须配置串口控制台并采用适当启动模式。示例使用默认 x86 固件，以下命令在当前目录创建新的增量盘。') + code(
        'qemu-img info base.qcow2\nqemu-img create -f qcow2 -F qcow2 -b base.qcow2 work.qcow2\nqemu-system-x86_64 \\\n  -accel kvm -cpu host -smp 2 -m 2048 \\\n  -drive file=work.qcow2,format=qcow2,if=virtio \\\n  -nic user,model=virtio-net-pci \\\n  -nographic') + p(
        'The overlay references base.qcow2 relative to its own location. It must retain that backing image. This example uses QEMU user-mode networking, which provides a different host-side path from the bridge diagram above. UEFI-only images need a matching firmware configuration. In the default serial multiplexing setup, Ctrl-a x exits QEMU.',
        '增量盘中的 base.qcow2 相对路径基于增量盘所在目录解析，需保留该基础镜像。示例使用 QEMU 用户态网络，其宿主路径与上方桥接图不同。仅支持 UEFI 的镜像需另配匹配固件。默认串口复用配置下，可用 Ctrl-a x 退出 QEMU。') + '<h3>' + t('Explain an observation', '用观察结果检验理解') + '</h3>' + bullets([
        ('Locate the QEMU vCPU threads on the host. Explain what changes when the guest starts a CPU-bound workload.', '在宿主找到 QEMU vCPU 线程，解释 Guest 启动 CPU 密集任务后发生的变化。'),
        ('Inspect guest block and network drivers. Identify Virtio devices and correlate them with the host configuration.', '检查 Guest 块设备和网络驱动，找出 Virtio 设备并与宿主配置对应。'),
        ('Shut down the guest, then inspect work.qcow2 with qemu-img info --backing-chain. Explain how its virtual size differs from allocated host space.', '关闭 Guest 后，用 qemu-img info --backing-chain work.qcow2 查看依赖链，解释虚拟容量与宿主实际占用的区别。'),
    ]) + refs('invocation', 'images', 'virsh'))

    reading = section(11, (
        'Read in four passes and check each pass by explaining one complete path.',
        '分四轮推进，每轮用一条完整路径检查自己是否理解。',
    ), '<ol class="route">' + ''.join('<li><strong>' + t(*title) + '</strong><p>' + t(*detail) + '</p></li>' for title, detail in [
        (('Build the machine model', '建立机器模型'), ('Read the VM stack and CPU chapters, then describe QEMU, KVM and a vCPU in one boot sequence.', '先读技术全景与 CPU 章节，沿启动流程说明 QEMU、KVM、vCPU 各自做什么。')),
        (('Follow one byte', '追踪一个字节'), ('Trace a guest load through two-stage paging, then follow a disk request through Virtio and a qcow2 backing chain.', '跟随一次 Guest load 完成两阶段转换，再沿 Virtio 和 qcow2 依赖链追踪一次磁盘请求。')),
        (('Run and measure', '运行与测量'), ('Use the exercises to identify drivers, scheduling and memory allocation. Change one resource setting at a time.', '通过练习观察驱动、调度和内存分配，每次只改变一项资源配置。')),
        (('Preserve state across hosts', '跨宿主保存状态'), ('Explain pre-copy convergence, device migration constraints, nested guests and isolation boundaries.', '说明 pre-copy 收敛条件、设备迁移限制、嵌套 Guest 与隔离边界。')),
    ]) + '</ol><div class="reading-grid">' + ''.join(
        '<a href="' + SOURCES[key][1] + '" target="_blank" rel="noopener noreferrer"><strong>' + SOURCES[key][0] + '</strong><span>' + t(*detail) + '</span></a>' for key, detail in [
            ('intel', ('VMX controls, exits and EPT', 'VMX 控制、退出与 EPT')),
            ('riscv', ('HS/VS modes and two-stage translation', 'HS/VS 模式与两阶段转换')),
            ('kvm', ('Build a VM and vCPU through ioctls', '通过 ioctl 创建 VM 与 vCPU')),
            ('virtio', ('Feature negotiation and virtqueue layout', '特性协商与 virtqueue 布局')),
            ('vfio', ('Device assignment and IOMMU groups', '设备分配与 IOMMU 分组')),
            ('migration', ('RAM, device state and migration protocol', 'RAM、设备状态与迁移协议')),
        ]) + '</div>')

    nav = ''.join(f'<a href="#{ident}">{t(en, cn)}</a>' for ident, en, cn in chapters)
    lang = 'zh-CN' if zh else 'en'
    title = t('Virtualization', '虚拟化')
    home = '../index.zh.html#computer-systems' if zh else '../index.html#computer-systems'
    description = t('Learn virtual machines through CPU execution, two-stage paging, Virtio, IOMMU, storage, networking, migration and QEMU/KVM labs.', '沿 CPU 执行、两阶段页表、Virtio、IOMMU、存储、网络与迁移学习虚拟机技术，配合 QEMU/KVM 实践。')
    return f'''<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{description}"><meta name="theme-color" content="#102631"><title>{title} · ShundaZhang</title>
<link rel="icon" href="../favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="style.css"><script src="../language.js"></script></head>
<body><a class="skip" href="#main">{t('Skip to content', '跳至正文')}</a>
<header class="top"><div class="wrap top-inner"><a class="home" href="{home}">{t('Computer systems', '计算机系统')}</a><span>ShundaZhang</span>
<nav class="language" aria-label="{t('Language', '语言')}"><a href="index.html" data-atlas-lang="en"{'' if zh else ' aria-current="page"'}>EN</a><a href="index.zh.html" data-atlas-lang="zh"{' aria-current="page"' if zh else ''}>中文</a></nav></div></header>
<main id="main"><section class="hero"><div class="wrap hero-inner"><div><p class="eyebrow">SYSTEMS / VIRTUAL MACHINES</p><h1>{title}</h1><p class="lead">{t('One physical machine<br>Many independent guest systems', '一台物理机器<br>多个独立 Guest 系统')}</p><p>{description}</p><a class="button" href="#foundation">{t('Explore the VM stack', '从虚拟机架构开始')}</a></div>
<div class="hero-map" aria-label="{t('The three virtualization paths', '虚拟化的三条路径')}">{block(('Execute', '执行'), ('vCPU → hypervisor → physical CPU', 'vCPU → Hypervisor → 物理 CPU'))}{block(('Translate', '地址转换'), ('GVA → GPA → host physical page', 'GVA → GPA → 宿主物理页'))}{block(('Transfer', '数据传输'), ('Guest driver → device backend → hardware', 'Guest 驱动 → 设备后端 → 硬件'))}</div></div></section>
<div class="wrap layout"><nav class="chapters" aria-label="{t('Chapters', '章节')}">{nav}</nav><div class="content">
{foundation}{cpu}{memory}{io}{storage}{network}{performance}{migration}{platforms}{security}{labs}{reading}
</div></div></main><footer><div class="wrap"><a href="{home}">{t('Back to personal home', '返回个人主页')}</a><span>{t('Official references checked', '官方资料核对')} <time datetime="2026-11-19">2026-11-19</time></span></div></footer></body></html>'''


if __name__ == '__main__':
    for chinese, filename in [(False, 'index.html'), (True, 'index.zh.html')]:
        (ROOT / filename).write_text(build(chinese), encoding='utf-8')
