"""Bilingual chapter content and primary references."""

from ai import AI_SOURCES, ai_chapter
from commons import commons_figure, four_way_cache_figure
from diagrams import address_spaces, cache_schematics, sv39_fields

SOURCES = {
    **AI_SOURCES,
    'intel': ('https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html', 'Intel SDM', 'Intel SDM'),
    'intel-opt': ('https://www.intel.com/content/www/us/en/developer/articles/technical/intel64-and-ia32-architectures-optimization.html', 'Intel Optimization Reference Manual', 'Intel 优化参考手册'),
    'rv': ('https://riscv.org/specifications/ratified/', 'RISC-V ratified specifications', 'RISC-V 正式规范'),
    'rv64': ('https://docs.riscv.org/reference/isa/unpriv/rv64.html', 'RV64I base ISA', 'RV64I 基础指令集'),
    'rvpriv': ('https://docs.riscv.org/reference/isa/priv/supervisor.html', 'RISC-V supervisor architecture', 'RISC-V 监管级架构'),
    'rvwmo': ('https://docs.riscv.org/reference/isa/unpriv/rvwmo.html', 'RVWMO memory model', 'RVWMO 内存模型'),
    'rvabi': ('https://riscv-non-isa.github.io/riscv-elf-psabi-doc/', 'RISC-V ELF psABI', 'RISC-V ELF psABI'),
    'x86abi': ('https://gitlab.com/x86-psABIs/x86-64-ABI', 'System V AMD64 ABI', 'System V AMD64 ABI'),
    'boom': ('https://docs.boom-core.org/en/latest/sections/intro-overview/boom.html', 'BOOM core documentation', 'BOOM 核心文档'),
    'mit': ('https://computationstructures.org/', 'MIT Computation Structures', 'MIT Computation Structures 课程'),
    'cs61c': ('https://cs61c.org/', 'Berkeley CS61C', 'Berkeley CS61C 课程'),
    'linux-dma': ('https://docs.kernel.org/core-api/dma-api-howto.html', 'Linux DMA mapping guide', 'Linux DMA 映射指南'),
    'linux-mmio': ('https://docs.kernel.org/driver-api/device-io.html', 'Linux device I/O accessors', 'Linux 设备 I/O 访问接口'),
    'msi': ('https://docs.kernel.org/PCI/msi-howto.html', 'Linux PCI MSI guide', 'Linux PCI MSI 指南'),
    'aia': ('https://docs.riscv.org/reference/aia/index.html', 'RISC-V Advanced Interrupt Architecture', 'RISC-V 高级中断架构'),
    'iommu': ('https://docs.riscv.org/reference/iommu/', 'RISC-V IOMMU architecture', 'RISC-V IOMMU 架构'),
    'qemu': ('https://www.qemu.org/docs/master/system/riscv/virt.html', 'QEMU RISC-V virt platform', 'QEMU RISC-V virt 平台'),
    'perf': ('https://docs.kernel.org/admin-guide/perf-security.html', 'Linux perf events and access control', 'Linux perf 事件与访问控制'),
    'linux-pte': ('https://docs.kernel.org/mm/page_tables.html', 'Linux page tables', 'Linux 页表文档'),
    'linux-vma': ('https://docs.kernel.org/mm/process_addrs.html', 'Linux process addresses and VMAs', 'Linux 进程地址与 VMA'),
    'linux-tlb': ('https://docs.kernel.org/core-api/cachetlb.html', 'Linux cache and TLB invalidation', 'Linux 缓存与 TLB 失效'),
    'roofline': ('https://digicoll.lib.berkeley.edu/record/136692/files/EECS-2008-134.pdf', 'Williams et al. · Roofline', 'Williams 等 · Roofline 原论文'),
}


def chapters(t, p, code, table, flow, link, refs):
    def rows(headers, entries):
        return table([t(*header) for header in headers],
                     [[t(*cell) if isinstance(cell, tuple) else cell for cell in entry] for entry in entries],
                     t('Architecture comparison','体系结构对照'))

    def picture(label, entries, caption):
        return flow(t(*label), [(t(*a), t(*b)) for a,b in entries], t(*caption))

    def exercise(chapter, label, text, anchor=''):
        return '<aside class="exercise"><strong>'+t('Try it','动手练习')+'</strong>'+p(t(*text))+link(chapter,t(*label),anchor)+'</aside>'

    isa = [
        ('bits',t('Read bytes, integers and addresses','从字节、整数和地址开始'),
         p(t('A register value is a bit pattern. Instructions and software give the pattern meaning. In an 8-bit teaching ALU, 0xff + 1 wraps to 0x00 with an unsigned carry. In two’s complement, 0xff means −1, so this same addition has no signed overflow. Conversely 0x7f + 1 overflows the signed range while producing 0x80.',
             '寄存器中的值是一串比特，由指令和软件赋予含义。在 8 位教学 ALU 中，0xff + 1 回绕到 0x00，产生无符号进位。补码里 0xff 表示 −1，这次加法没有有符号溢出。反过来，0x7f + 1 得到 0x80，却超出了有符号表示范围。'),
           t('Byte order tells you how a multibyte value is laid out. In a little-endian setup, storing 0x12345678 places 78 56 34 12 at consecutive addresses, lowest address first. The examples here assume the common little-endian x86-64 and RV64 Linux environments.',
             '字节序决定多字节值在内存中的布局。小端环境存入 0x12345678 后，从低地址到高地址依次是 78 56 34 12。本站示例使用常见的小端 x86-64 与 RV64 Linux 环境。'))
         +refs(('mit','cs61c'))),
        ('contract',t('ISA, ABI and platform','ISA、ABI 与平台'),
         p(t('An ISA specifies instructions, architectural registers, exceptions and ordering guarantees. The ABI adds conventions for calls, stack layout and binary interfaces. A platform defines components and discovery rules such as interrupt controllers, firmware tables and buses. Microarchitecture is how a specific core implements the ISA.',
             'ISA 规定指令、架构寄存器、异常和顺序保证。ABI 补充函数调用、栈布局和二进制接口约定。平台规定中断控制器、固件表和总线等组件及发现方式。微架构则描述某个具体核心如何实现 ISA。'))
         +rows([('Aspect','方面'),('x86-64','x86-64'),('RISC-V RV64','RISC-V RV64')],[
             [('Encoding','编码'),('Variable length, up to 15 bytes per instruction.','变长编码，单条最长 15 字节。'),('Base instructions are 32 bits. C adds 16-bit compressed encodings.','基础指令 32 位，C 扩展加入 16 位压缩编码。')],
             [('Registers and operands','寄存器与操作数'),('16 general-purpose registers in baseline 64-bit mode. Many instructions allow a memory operand.','基线 64 位模式有 16 个通用寄存器，许多指令允许内存操作数。'),('RV64I has 32 integer registers including hardwired zero x0. Loads and stores access data memory.','RV64I 有 32 个整数寄存器，含恒为零的 x0。数据访存由 load/store 指令完成。')],
             [('Privilege','特权'),('Rings 0–3, with ring 0 and ring 3 typically used by Linux.','Ring 0–3，Linux 通常使用 ring 0 和 ring 3。'),('M-mode is mandatory. General-purpose systems typically also implement S-mode and U-mode.','M 模式必选，通用系统通常也实现 S、U 模式。')],
             [('Feature discovery','发现功能'),('CPUID reports hardware features. Some features also require OS enablement.','CPUID 报告硬件功能，部分功能还需 OS 启用。'),('An implementation chooses extensions. On Linux use the OS capability interface for application feature detection.','实现选择扩展组合。Linux 应用通过 OS 提供的能力接口检测功能。')],
         ])+refs(('intel','rv64','rv'))),
        ('trace',t('Trace the same C function','跟踪同一个 C 函数'),
         p(t('The following examples use the System V AMD64 and RISC-V psABIs. The pointer arrives in rdi or a0, and the result returns in rax or a0. The routines read one 64-bit value and add one modulo 2⁶⁴.',
             '以下示例采用 System V AMD64 与 RISC-V psABI。指针分别从 rdi 或 a0 传入，结果从 rax 或 a0 返回。两个例程都读取一个 64 位数，并按模 2⁶⁴ 加一。'))
         +code('uint64_t next(const uint64_t *p) { return *p + 1; }\n\nx86-64 (AT&T)                 RV64I\nmovq (%rdi), %rax             ld a0, 0(a0)\naddq $1, %rax                 addi a0, a0, 1\nret                           ret  # jalr x0, 0(ra)')
         +p(t('The x86 CALL places the return address on the stack. A typical RV64 call writes the link register ra, which a non-leaf function may save. The loads can fault and both cores may satisfy them from cache. Use retired instructions and measured time when comparing different binaries.',
              'x86 CALL 将返回地址压栈。RV64 的常见调用写链接寄存器 ra，非叶函数可能需要保存它。两边的加载都可能触发异常，也都可能由缓存满足。比较不同二进制时，记录提交指令数和实测时间。'))
         +refs(('x86abi','rvabi'))),
    ]

    cpu = [
        ('datapath',t('Build a datapath for one load','搭出一条加载指令的数据通路'),
         p(t('Start with a register file, PC, ALU, multiplexers and memory interface. Control logic uses the decoded opcode to select data sources and enable writes. For RV64 ld rd, imm(rs1), read rs1, sign-extend the immediate, add them, request eight bytes, and route the returned value to rd when the instruction completes successfully.',
             '从寄存器堆、PC、ALU、多路选择器和内存接口开始。控制逻辑根据译码后的操作码选择数据源并开启写入。以 RV64 的 ld rd, imm(rs1) 为例，读取 rs1，将立即数符号扩展后相加，请求八字节，并在指令成功完成时将返回值写入 rd。'))
         +picture(('A simple five-stage teaching pipeline','五级教学流水线'),[
             (('IF','IF 取指'),('Use PC to fetch the instruction.','用 PC 取指。')),
             (('ID','ID 译码'),('Decode and read register operands.','译码并读取源寄存器。')),
             (('EX','EX 执行'),('Compute an address or ALU result.','计算地址或 ALU 结果。')),
             (('MEM','MEM 访存'),('Access data memory for loads and stores.','为加载与存储访问数据存储器。')),
             (('WB','WB 写回'),('Write a register when required.','按需写寄存器。')),
         ],('Stages can overlap across instructions. Real cores split and schedule them differently.',
             '不同指令的阶段可以重叠。实际核心会按自己的设计拆分和调度。'))
         +p(t('A dependent add after a load may need a stall in this pipeline because data becomes available late. Bypassing forwards a result directly to a dependent stage when timing allows. Port conflicts cause structural hazards, unresolved branches cause control hazards, and a branch misprediction squashes younger instructions.',
              '加载后的依赖 add 可能需要停顿，因为数据到得较晚。时序允许时，旁路可直接将结果转发给依赖阶段。端口冲突是结构冒险，尚未确定方向的分支带来控制冒险，预测错误会撤销其后的年轻指令。'))
         +refs(('mit','cs61c'))),
        ('ooo',t('From in-order pipelines to out-of-order cores','从顺序流水线到乱序核心'),
         picture(('A representative out-of-order core','典型乱序核心的数据流'),[
             (('Front end','前端'),('Predict the next PC and fetch/decode operations.','预测后续 PC，完成取指和译码。')),
             (('Rename','重命名'),('Allocate physical registers and reorder-buffer entries.','分配物理寄存器及 ROB 项。')),
             (('Schedule','调度'),('Issue ready operations to execution ports.','向执行端口发射就绪操作。')),
             (('Execute','执行'),('Run ALU, vector and load/store operations.','运行 ALU、向量与访存操作。')),
             (('Retire','提交'),('Commit in program order or take a precise exception.','按程序顺序提交或处理精确异常。')),
         ],('Cache misses can overlap with independent work. Dependent work waits for its operands.',
             '缓存未命中可以与独立指令重叠，依赖指令仍须等待操作数。'))
         +p(t('Renaming removes false WAR and WAW name dependencies. A true RAW dependency remains. The reorder buffer tracks completion and supports in-order retirement. Load/store queues track addresses and ordering, and a load can receive data from an older matching store. A retired store may still wait in a buffer before it becomes visible to other cores.',
              '重命名消除 WAR 和 WAW 的假依赖，真正的 RAW 数据依赖仍在。重排序缓冲区跟踪完成状态并支持顺序提交。访存队列跟踪地址和顺序，加载可以从更早且地址匹配的存储获得转发数据。已提交的存储还可能暂留在缓冲区，之后才对其他核心可见。'),
            t('Many modern x86 cores decode instructions into micro-operations. RISC-V is implemented by small in-order cores and by out-of-order cores such as BOOM. Predictors, queue sizes and issue width are implementation choices. A misprediction restores the architectural path and may leave microarchitectural traces in caches or predictors.',
              '许多现代 x86 核心把指令译成微操作。RISC-V 既有小型顺序核心，也有 BOOM 这样的乱序核心。预测器、队列容量和发射宽度都由实现决定。预测失败后处理器恢复架构路径，缓存和预测器仍可能留下微架构痕迹。'))
         +refs(('intel-opt','boom'))),
    ]

    cache = [
        ('mapping',t('Map an address to a cache line','把地址映射到缓存行'),
         p(t('Temporal locality comes from reusing data. Spatial locality comes from accessing nearby bytes. The cache transfers a line at a time. A simple set-associative cache splits an address into tag, set index and byte offset, then compares tags of all valid ways in that set.',
             '重复使用数据体现时间局部性，访问相邻字节体现空间局部性。缓存按行传输。简单组相联缓存把地址拆成 tag、组索引和行内偏移，再与该组各个有效路位的 tag 比较。'))
         +picture(('Example with a 32 KiB, four-way cache','32 KiB、四路缓存算例'),[
             (('64 B / line','每行 64 B'),('Offset uses six low bits.','低六位是行内偏移。')),
             (('128 sets','128 组'),('32 KiB ÷ (64 B × 4) gives 128 sets. Index uses seven bits.','32 KiB ÷ (64 B × 4) 得到 128 组，索引占七位。')),
             (('4 ways / set','每组四路'),('At most four valid lines with distinct tags fit in the selected set.','所选组最多容纳四条 tag 不同的有效行。')),
         ],('In this model 0x1234 maps to set 72, offset 52, tag 0. Actual LLCs may hash physical bits into slices and sets.',
             '在此模型中，0x1234 映射到第 72 组，偏移 52，tag 为 0。真实 LLC 可能用物理地址的哈希选 slice 和组。'))
         +p(t('Cold misses happen on first touch, capacity misses occur when the working set exceeds available capacity, and conflict misses occur when too many active lines map to one set. In multicore systems, invalidation can cause additional coherence misses. Increasing ways can reduce conflicts while changing lookup cost.',
              '冷未命中来自首次访问，容量未命中来自工作集超出容量，冲突未命中来自过多活跃行落到同一组。多核系统还可能因一致性失效而重新取数。增加路数可减轻冲突，同时也会改变查找成本。'))
         +cache_schematics(t)
         +'<div class="wiki-pair">'
         +commons_figure(t,'cache-direct',
             ('Direct mapping, one way per set','直接映射，每组只有一路'),
             ('Address fields select one cache entry. A comparator checks its tag and valid bit.','地址字段选择一个条目，比较器检查 tag 和有效位。'),
             ('Follow Index to a row, then compare Tag. This is the one-way version of the preceding four-way example.',
              '沿原图的 Index 选中一行，再检查 Tag。这相当于上面四路算例的单路版本。'))
         +four_way_cache_figure(t,
             ('Four-way lookup in hardware','四路组相联的硬件查找'),
             ('Four comparators and valid bits on the left determine which way can drive the data output from the multiplexers on the right.',
              '左侧的四个比较器和有效位决定哪一路能把右侧多路选择器选出的数据送到输出端。'),
             ('Start at Index: the two decoders select the same set in the tag and data arrays. On the left, four comparators check tags in parallel, and each result is gated by that way’s valid bit. On the right, the offset feeds the word multiplexers (MUX); only the matching valid way drives the output.',
              '从 Index（组索引）开始：两个译码器在标签阵列和数据阵列中选中同一组。左侧四个 Comparator（比较器）并行比较 Tag，再分别检查对应路的 Valid Bit（有效位）。右侧的 MUX（多路选择器）按偏移选出行内的字，只有有效且匹配的那一路驱动输出。'))
         +'</div>'
         +exercise('labs',('Try the cache mapper →','打开缓存映射实验 →'),('Enter 0x3234 and change ways from 4 to 1. Explain why the same address now uses a different set and tag.','输入 0x3234，再把路数从 4 改到 1，解释为何同一地址会选中不同的组索引与 tag。'),'#cache-mapping')),
        ('policies',t('Follow a miss and a dirty eviction','跟踪未命中与脏行逐出'),
         picture(('A read miss in a write-back cache','写回缓存中的一次读未命中'),[
             (('Check ways','检查路位'),('No valid tag matches in the selected set.','所选组内没有有效 tag 匹配。')),
             (('Select a slot','选择路位'),('Use a free way or choose a victim.','使用空闲路位或选择牺牲行。')),
             (('Preserve dirty data','保存脏数据'),('Write back a modified victim if needed.','必要时回写已修改的牺牲行。')),
             (('Fill and resume','填入并继续'),('Install the incoming line and satisfy the waiting load.','填入新行，满足等待中的加载。')),
         ],('A core may overlap the writeback and the new request. The boxes show the logical responsibilities.',
             '核心可以重叠回写与新请求，图示区分各步骤承担的工作。'))
         +p(t('On a read miss, an implementation can allocate an entry to track the outstanding request, fetch the line from a lower level and resume dependent loads once data arrives. A replacement policy selects a victim line. With write-back, a dirty victim needs writeback. Write-through forwards writes to the lower level, usually through buffering. On a store miss, write-allocate fills the line, while no-write-allocate can send the store onward.',
             '读未命中时，处理器可分配一个在途请求项，从下一级取回缓存行，并在数据返回时继续依赖的加载。替换策略决定逐出哪一行。写回缓存逐出脏行前要回写，写直达通常经缓冲把写入传给下一级。写未命中时，写分配会先填入缓存行，非写分配可把写入转交下一级。'),
           t('AMAT = hit time + miss rate × miss penalty for a single cache level. With 1 ns hit time, 5% miss rate and 40 ns extra penalty, AMAT is 3 ns. For multiple levels use the lower level’s conditional miss rate when following an upper-level miss. Prefetching and overlapped requests change observed throughput.',
             '单级缓存的 AMAT = 命中时间 + 未命中率 × 额外代价。若命中 1 ns、未命中率 5%、额外代价 40 ns，则 AMAT 为 3 ns。多级缓存递推时，用上一级未命中后下一级的条件未命中率。预取和请求重叠会改变实测吞吐。'),
           t('L1I and L1D often separate instruction and data paths. The size, associativity, sharing and inclusion of L2 and LLC depend on the processor. x86 software can consult CPUID cache parameters where supported. RISC-V cache geometry depends on the core and platform, and optional cache-block extensions expose particular maintenance operations.',
             'L1I 和 L1D 常分离指令与数据路径。L2 和 LLC 的大小、相联度、共享范围与包容性取决于处理器。支持时可用 x86 CPUID 查询缓存参数。RISC-V 的缓存组织由核心和平台决定，可选的缓存块扩展提供特定维护操作。'))
         +refs(('intel','rv','cs61c'))),
    ]

    memory = [
        ('mappings',t('A process address map and its physical backing','进程地址空间与物理页的关系'),
         picture(('Common regions in a process address space','进程虚拟地址空间中的常见区域'),[
             (('Program image','程序映像'),('Executable code, read-only constants and writable data from the loaded image.','加载后的代码、只读常量和可写数据。')),
             (('Heap and anonymous mappings','堆与匿名映射'),('Allocator arenas and other anonymous virtual regions.','分配器使用的堆区和其他匿名虚拟区域。')),
             (('File mappings','文件映射'),('Shared libraries or file-backed regions created by mmap.','共享库或 mmap 创建的文件后备区域。')),
             (('Stacks and gaps','栈与空洞'),('Thread stacks, guard regions and unmapped addresses.','线程栈、保护区域和未映射地址。')),
         ],('These are categories, not a fixed address order. ASLR, the loader and the OS decide actual placement.',
             '这些是区域类型，具体地址布局由 ASLR、加载器和操作系统决定。'))
         +p(t('On Linux, a VMA describes a contiguous virtual range and its policy, including permissions and backing. A page-table entry describes one active hardware mapping or the state used to resolve it. One VMA can contain many pages, some not yet resident. Contiguous virtual pages can map to noncontiguous physical frames. Two address spaces can also map the same frame at different virtual addresses.',
             'Linux 的 VMA 描述一段连续虚拟地址及其策略，包括权限和后备对象。页表项描述单个硬件映射，或保留供后续解析的状态。一段 VMA 可含许多页，其中一部分尚未驻留。连续虚拟页可以映射到离散物理页，两个地址空间也能用不同虚拟地址映射同一物理页。'))
         +commons_figure(t,'virtual-physical',
             ('Virtual pages and physical frames','虚拟页与物理页框'),
             ('Arrows map text, data and stack pages in one process to scattered frames in physical memory.','箭头将进程的代码、数据和栈页映射到分散的物理页框。'),
             ('Read from left to right. Each arrow connects one virtual page to its backing frame. The addresses illustrate an example layout.',
              '从左向右看，每条箭头把一个虚拟页连到它的后备页框。图中的地址只代表一种示例布局。'))
         +refs(('linux-vma','linux-pte'))),
        ('translation',t('From virtual address to physical address','从虚拟地址到物理地址'),
         picture(('Load address translation','一次加载的地址翻译'),[
             (('Virtual address','虚拟地址'),('The core computes the effective address.','核心计算有效地址。')),
             (('TLB','TLB'),('A matching translation also supplies permission information.','命中的翻译项也提供权限信息。')),
             (('Page walk on miss','未命中时遍历页表'),('Read PTEs and validate permissions and format.','读取 PTE 并检查权限与格式。')),
             (('Physical access','物理访问'),('Combine the page number with the offset and access the hierarchy.','拼接物理页号和页内偏移，再访问存储层次。')),
         ],('A TLB miss may be resolved by a walk. Invalid or unauthorized translations can cause a page fault.',
             'TLB 未命中可通过页表遍历解决。无效翻译或权限不符可能引起页故障。'))
         +rows([('Aspect','方面'),('x86-64','x86-64'),('RV64 Sv39','RV64 Sv39')],[
             [('4 KiB pages','4 KiB 页'),('Four levels with 48-bit linear addresses, or five levels with LA57 on supported systems. Nine index bits per level.','四级分页采用 48 位线性地址，支持 LA57 的系统可用五级。每级九位索引。'),('Three levels with 39-bit virtual addresses and nine index bits per level.','三级页表，39 位虚拟地址，每级九位索引。')],
             [('Root and context','根与上下文'),('CR3 selects the root and can carry a PCID when enabled.','CR3 选择页表根，启用 PCID 时可携带上下文标识。'),('satp holds MODE, ASID and the root physical page number.','satp 含 MODE、ASID 与根物理页号。')],
             [('Large leaves','大页叶项'),('2 MiB and, where supported, 1 GiB.','支持 2 MiB，以及硬件允许时的 1 GiB。'),('An aligned leaf at an upper level can map 2 MiB or 1 GiB.','上层对齐的叶项可映射 2 MiB 或 1 GiB。')],
             [('Maintenance','翻译维护'),('INVLPG or other architecture-defined invalidation as appropriate.','按上下文使用 INVLPG 等架构规定的失效手段。'),('SFENCE.VMA orders page-table updates with implicit translation reads and affects local translation caching as specified.','SFENCE.VMA 对页表更新和隐式翻译读排序，并按规定影响本 hart 的翻译缓存。')],
         ])
         +p(t('For 0x40123456, Sv39 extracts VPN[2:0] = (1, 0, 0x123) and offset 0x456. A successful 4 KiB leaf with physical page number 0x81234 gives physical address 0x81234456. A valid page-table entry can still deny the requested read, write or execute. After changing a shared mapping, the OS coordinates invalidation on the other cores or harts that may retain it.',
              '以 0x40123456 为例，Sv39 取出 VPN[2:0] = (1, 0, 0x123)，偏移为 0x456。若允许访问的 4 KiB 叶项给出物理页号 0x81234，得到物理地址 0x81234456。有效的页表项仍可拒绝读、写或执行。共享映射修改后，OS 还需协调可能保留旧翻译的其他核心或 hart 执行失效。'))
         +exercise('labs',('Open the Sv39 decoder →','打开 Sv39 地址实验 →'),('Check which field changes if you add 4 KiB to the virtual address.','虚拟地址加 4 KiB 后，检查哪个字段发生变化。'),'#sv39')
         +refs(('intel','rvpriv'))),
        ('walk',t('Walk Sv39 with real indices','用具体索引逐级走一遍 Sv39'),
         sv39_fields(t)
         +picture(('Example page walk after a TLB miss','TLB 未命中后的一次页表遍历'),[
             (('Root table','根页表'),('satp.PPN = 0x80000. Read root[1] at 0x80000008. It points to 0x80001000.','satp.PPN = 0x80000。读 0x80000008 的 root[1]，指向 0x80001000。')),
             (('Middle table','中间页表'),('Read middle[0] at 0x80001000. It points to 0x80002000.','读 0x80001000 的 middle[0]，指向 0x80002000。')),
             (('Leaf table','末级页表'),('Read leaf[0x123] at 0x80002918. The valid leaf supplies PPN 0x81234.','读 0x80002918 的 leaf[0x123]，有效叶项给出 PPN 0x81234。')),
             (('Physical byte','物理字节'),('Combine PPN and offset. PA = 0x81234000 + 0x456 = 0x81234456.','拼接页号与偏移。PA = 0x81234000 + 0x456 = 0x81234456。')),
         ],('Example assumes a permitted 4 KiB leaf. Each Sv39 table holds 512 eight-byte entries. The PTE address is table base + index × 8.',
             '假设命中允许访问的 4 KiB 叶项。每张 Sv39 页表有 512 个八字节条目。页表项地址等于表基址加索引 × 8。'))
         +rows([('Entry information','页表项信息'),('x86-64','x86-64'),('RISC-V Sv39','RISC-V Sv39')],[
             [('Validity and access','有效性与权限'),('P, R/W, U/S and XD/NX where enabled. Permissions can constrain access at multiple levels.','P、R/W、U/S，以及启用时的 XD/NX。多个层级的权限均可能约束访问。'),('V, R, W, X and U, with further checks such as SUM and MXR.','V、R、W、X 与 U，还要检查 SUM、MXR 等条件。')],
             [('Leaf or pointer','叶项或下一级指针'),('PT entries map 4 KiB pages. The PS bit at supported levels selects a larger leaf.','末级表项映射 4 KiB 页，支持大页的层级可用 PS 位选择大页叶项。'),('A valid PTE with R=W=X=0 points to the next table. A valid readable or executable entry can be a leaf.','有效项的 R=W=X=0 时指向下一级。合法的可读或可执行项可作为叶项。')],
             [('Usage tracking','访问状态'),('Accessed and Dirty bits record usage as specified.','Accessed 和 Dirty 位按架构规则记录使用状态。'),('A and D bits track accesses and writes. Update or fault behavior depends on the implemented mode.','A、D 记录访问与写入，更新或触发故障取决于实现模式。')],
         ])
         +commons_figure(t,'page-tables-five-levels',
             ('Compare with x86-64 five-level paging','对照 x86-64 五级分页'),
             ('CR3 selects the top table. Address indices lead through five levels to a physical page, then the low bits select a byte.','CR3 选出顶级表，地址索引穿过五级到达物理页，最后由低位选中字节。'),
             ('This LA57 illustration follows a 4 KiB leaf. Each table has 512 entries and each index consumes nine bits. Compare five table indices here with the three in Sv39 above. The high field marked Reserved represents bits 63–57 here. A canonical LA57 address copies bit 56 into all seven of those bits.',
              '这张 LA57 图沿着 4 KiB 叶项翻译。每张表有 512 个条目，每级消耗 9 位索引。和上面的 Sv39 对照，五级分页用五段索引。图中标为 Reserved 的是第 63–57 位，规范的 LA57 地址要求这七位都等于第 56 位。'))
         +refs(('intel','rvpriv','linux-pte'))),
        ('management',t('What the OS does when a mapping changes','映射变化时操作系统做什么'),
         picture(('Demand paging after a new anonymous mapping','建立匿名映射后的按需分配'),[
             (('mmap','mmap'),('Record an allowed virtual range in a VMA. The backing frames can be allocated later.','在 VMA 记录允许访问的虚拟范围，物理页可以稍后分配。')),
             (('First write','首次写入'),('An absent translation faults. The handler checks the address and write permission against the VMA.','尚无翻译时触发缺页。处理程序按 VMA 检查地址与写权限。')),
             (('Populate','填充'),('Allocate and zero the backing frame as needed, then install a valid PTE.','按需分配并清零后备页，再安装有效 PTE。')),
             (('Retry','重试'),('The faulting instruction can retry. An invalid access may instead be reported to the process.','重新执行故障指令。非法访问则可能作为错误通知进程。')),
         ],('This example follows a valid first write. File-backed faults may instead obtain a page through the page cache.',
             '此图以合法的首次写入为例。文件映射的缺页也可能通过页缓存取得后备页。'))
         +address_spaces(t)
         +p(t('After fork, private writable mappings can share backing with writes blocked in their page-table entries. If B writes while the page is still shared, the OS handles the fault, copies the page and updates B’s mapping. A permission fault is therefore sometimes part of normal memory management.',
              'fork 后，私有可写映射可先共享后备页，并在双方页表项禁止写入。若 B 在页面仍共享时写入，OS 处理故障、复制页面并更新 B 的映射。权限故障因此也可能是正常内存管理的一环。'))
         +picture(('Unmap a page that may be cached on another core','取消映射时，另一核心可能还缓存着旧翻译'),[
             (('Update PTE','更新页表项'),('Remove the mapping or lower its permissions.','移除映射或收紧权限。')),
             (('Invalidate','使旧翻译失效'),('Invalidate locally and coordinate relevant remote cores or harts.','在本地失效，并协调相关远端核心或 hart。')),
             (('Complete','确认完成'),('Once stale access is ruled out and references are gone, the old frame can be reused.','确保旧访问路径失效且引用释放后，旧页框才可复用。')),
         ],('PCID and ASID label translation contexts. A changed mapping can still require a TLB shootdown on other CPUs.',
             'PCID 和 ASID 给翻译上下文加标签。修改映射时，仍可能需要在其他 CPU 上执行 TLB shootdown。'))
         +refs(('linux-vma','linux-tlb','rvpriv'))),
        ('dram',t('DRAM, bandwidth and NUMA','DRAM、带宽与 NUMA'),
         p(t('A DRAM controller maps addresses across channels, ranks, banks and rows. Activating a row loads it into a row buffer, so accesses to an open row can cost less than switching rows. Banks and channels enable overlap. Refresh, controller queues and read/write turnarounds affect latency under load.',
             'DRAM 控制器把地址分到通道、rank、bank 与行。激活行会把它读入行缓冲，访问已打开的行通常比换行成本低。多个 bank 和通道可重叠工作。刷新、控制器队列以及读写方向切换都会影响负载下的延迟。'),
           t('Latency is the time for one request. Bandwidth measures sustained data transfer and benefits from parallel requests. On a NUMA machine, placement determines which memory controller serves a page, and a remote node adds fabric traffic. Measure placement and access pattern along with throughput.',
             '延迟是一次请求花费的时间，带宽是持续的数据传输能力，可受益于多个并行请求。NUMA 机器的页放置决定由哪个内存控制器服务，访问远端节点会增加互连流量。测吞吐时也要记录放置位置与访存模式。'))
         +commons_figure(t,'numa',
             ('Local memory and remote memory in NUMA','NUMA 的本地内存和远端内存'),
             ('Each node has processors and local memory. A fabric connects nodes to one another.','每个节点都有处理器和本地内存，互连把各节点连接起来。'),
             ('Compare a CPU accessing the Memory box on its own node with an access that crosses the network to another node. A larger system can have more capacity without uniform access costs.',
              '比较 CPU 访问同节点的 Memory 方框，与跨互连访问另一节点内存的路径。系统容量增加时，各位置的访问代价仍可能不同。'))
         +refs(('intel-opt','cs61c'))),
    ]

    io = [
        ('registers',t('Discover a device and access its registers','发现设备并访问寄存器'),
         p(t('PCIe devices expose configuration space. During enumeration the system discovers devices, sizes and assigns address windows described by BARs, and binds drivers. The driver maps a BAR and uses MMIO accessors such as readl/writel for register access. Register reads can have side effects, and posted writes may complete at the device after the CPU has continued. Follow the device and bus ordering rules.',
             'PCIe 设备暴露配置空间。枚举时系统发现设备，确定 BAR 所描述的地址窗口大小、分配地址并绑定驱动。驱动映射 BAR，再通过 readl/writel 等 MMIO 接口访问寄存器。读寄存器可能有副作用，posted write 也可能在 CPU 继续执行后才到达设备。排序遵循设备与总线规则。'),
           t('x86 platforms can expose MMIO and a separate port-I/O space accessed by IN/OUT. RISC-V platforms commonly use MMIO for device registers. A driver also needs platform discovery, for example PCI configuration, ACPI tables or a device tree. QEMU virt is one documented RISC-V platform.',
             'x86 平台可以同时提供 MMIO 和独立的端口 I/O 空间，后者使用 IN/OUT。RISC-V 平台通常以 MMIO 暴露设备寄存器。驱动还需要发现平台设备，例如通过 PCI 配置、ACPI 表或设备树。QEMU virt 是一个有文档的 RISC-V 平台实例。'))
         +refs(('linux-mmio','intel','qemu'))),
        ('dma',t('Walk through a DMA completion','跟踪一次 DMA 完成'),
         picture(('A queue-based device transfer','基于队列的设备传输'),[
             (('Prepare','准备'),('The driver maps a buffer for DMA and fills a descriptor with its device-visible address.','驱动映射 DMA 缓冲区，把设备可见地址写入描述符。')),
             (('Publish','发布'),('Order descriptor writes, transfer ownership and ring the MMIO doorbell.','保证描述符写入顺序，交出所有权，再写 MMIO 门铃。')),
             (('Transfer','传输'),('The device reads or writes memory through DMA. An IOMMU can translate and restrict requests.','设备通过 DMA 读写内存，IOMMU 可翻译并约束请求。')),
             (('Complete','完成'),('The driver sees completion by interrupt or polling, then synchronizes or unmaps as required.','驱动通过中断或轮询发现完成，再按要求同步或解除映射。')),
         ],('The CPU virtual address, CPU physical address and device DMA address describe different views.',
             'CPU 虚拟地址、CPU 物理地址与设备 DMA 地址分别属于不同视图。'))
         +p(t('A coherent DMA allocation keeps shared descriptor data coherent but still needs ordering before setting ownership bits. Streaming DMA mappings have a direction and ownership lifecycle. For a reused streaming mapping, perform the required synchronization when handing the buffer between CPU and device. Unmap only after the device has stopped using it.',
              '一致性 DMA 分配可维持共享描述符数据的一致性，但设置所有权位之前仍需保证顺序。流式 DMA 映射有方向与所有权生命周期。复用流式映射时，CPU 与设备交接缓冲区要执行相应同步。设备停止使用后才能解除映射。'),
            t('On x86, common PCIe systems deliver interrupts via APIC infrastructure, with MSI/MSI-X represented as device writes. RISC-V boards may route interrupts through a PLIC or through AIA components such as APLIC and IMSIC. The OS manages masks, priorities and affinity. Polling trades CPU time for lower notification overhead at high completion rates.',
              '在常见 x86 PCIe 系统中，中断经 APIC 基础设施投递，MSI/MSI-X 由设备发起写事务。RISC-V 板卡可能采用 PLIC，也可能使用 AIA 的 APLIC、IMSIC 等组件。OS 管理屏蔽、优先级和亲和性。高完成率下，轮询用 CPU 时间换取较低的通知开销。'))
         +refs(('linux-dma','msi','aia','iommu','qemu'))),
    ]

    parallel = [
        ('coherence',t('Coherence tracks ownership of one line','一致性跟踪一条缓存行的所有权'),
         picture(('Two cores increment independent counters in one line','两个核心修改同一行内的不同计数器'),[
             (('Core A writes','核心 A 写入'),('Acquire write ownership of the line containing both counters.','获得包含两个计数器的缓存行写权限。')),
             (('Core B writes','核心 B 写入'),('Request ownership and invalidate or transfer A’s copy.','请求写权限，使 A 的副本失效或发生转移。')),
             (('Repeat','继续写入'),('The line moves again. Padding or separating hot counters can help.','缓存行再次转移。填充或分开放置热点计数器可以缓解。')),
         ],('This is false sharing. Independent variables can still compete at cache-line granularity.',
             '这是伪共享。不同变量仍会在缓存行粒度上竞争。'))
         +p(t('A protocol such as MESI tracks states such as Modified, Exclusive, Shared and Invalid. Snooping and directories are ways to coordinate which agents have copies. Exact states and interconnects depend on the implementation. SIMD works across lanes within an instruction, SMT shares core resources between hardware threads, and multiple cores execute instruction streams with separate or shared caches.',
              'MESI 一类协议跟踪 Modified、Exclusive、Shared、Invalid 等状态。监听与目录是协调哪些节点持有副本的方式。具体状态和互连取决于实现。SIMD 在一条指令内处理多个 lane，SMT 让硬件线程共享核心资源，多核则使用各自或共享的缓存执行多条指令流。'))
         +refs(('intel-opt','cs61c'))),
        ('ordering',t('Ordering connects observations at different addresses','内存顺序约束跨地址的观察结果'),
         p(t('Coherence concerns one location. A memory consistency model constrains how reads and writes to different locations may be observed. In this hardware litmus test, x and y are initially zero and occupy distinct normal memory locations.',
             '一致性处理单一位置，内存一致性模型约束多个位置的读写可怎样被观察。下面的硬件 litmus test 中，x 和 y 初始为零，位于不同的普通内存位置。'))
         +code('Core 0             Core 1\nx = 1              y = 1\nr0 = y             r1 = x\n\nCan (r0, r1) = (0, 0)?')
         +p(t('Yes under the usual x86 ordering rules for normal write-back memory, and under RVWMO without additional ordering. On x86 a store can wait in the local store buffer while a later load reads another address. An appropriate full store-to-load barrier on both cores rules out this outcome. RISC-V also provides FENCE and acquire/release semantics for supported atomic instructions, with RVWMO as the base model and Ztso as an optional extension.',
              '在 x86 普通写回内存的顺序规则下可以出现，在没有额外排序的 RVWMO 下也可以。x86 存储可在本地存储缓冲区等待，后续加载可以读取其他地址。两边都插入适当的完整 store-to-load 屏障可排除此结果。RISC-V 还提供 FENCE 及受支持原子指令的 acquire/release 语义，默认模型为 RVWMO，Ztso 为可选扩展。'),
            t('For shared state in C or C++, use language atomics and synchronization. A release store and an acquire load that reads from it can publish prior data. Compiler ordering, ISA ordering and the rules for device memory each need their own treatment.',
              'C 或 C++ 中的共享状态应通过语言原子操作及同步机制处理。release 存储与读取该值的 acquire 加载可以发布先前写入的数据。编译器顺序、ISA 顺序和设备内存规则分别处理。'))
         +refs(('intel','rvwmo','rv'))),
    ]

    performance = [
        ('metrics',t('Start with an explicit performance model','先写出性能模型'),
         p(t('For one thread over a measured region, CPU time is retired instructions × average CPI ÷ average cycle rate, using consistent definitions for counters and time. At 2 billion instructions, CPI 1.2 and 3 GHz, that is 0.8 s of CPU time. Elapsed time can also include scheduling, I/O and waiting. Compare latency, sustained throughput and CPU time separately.',
             '对单线程的测量区间，CPU 时间 = 提交指令数 × 平均 CPI ÷ 平均周期频率，计数器与时间口径须一致。若提交 20 亿条指令，CPI 1.2，频率 3 GHz，CPU 时间为 0.8 秒。墙钟时间还可能包括调度、I/O 与等待。分别比较延迟、持续吞吐和 CPU 时间。'),
           t('Amdahl’s law gives total speedup 1/((1−p)+p/s) when fraction p of baseline time improves by factor s. If 80% improves 4×, the total speedup is 2.5×. Roofline limits throughput by min(peak compute, bandwidth × arithmetic intensity). At 50 GB/s and 2 FLOP/byte, the bandwidth ceiling is 100 GFLOP/s at the stated memory boundary.',
             '若基线耗时中比例 p 的部分加速 s 倍，Amdahl 定律给出总加速比 1/((1−p)+p/s)。80% 的耗时加速 4 倍，总体仅加速 2.5 倍。Roofline 用 min(峰值算力, 带宽 × 算术强度) 限定吞吐。在指定内存边界，50 GB/s 与 2 FLOP/字节对应 100 GFLOP/s 的带宽上限。'))
         +exercise('labs',('Open the CPI calculator →','打开 CPI 计算实验 →'),('Compute the branch overhead at 20% branches, 5% mispredictions and 15 cycles per miss.','用 20% 分支、5% 误预测率和 15 周期代价计算分支开销。'),'#cpi')
         +refs(('roofline','cs61c'))),
        ('measurement',t('Use counters to test a hypothesis','用计数器检验一个假设'),
         picture(('A repeatable measurement loop','可复核的测量过程'),[
             (('Hypothesis','假设'),('Changing the loop order improves locality.','改变循环顺序能提高局部性。')),
             (('Compare','对照'),('Keep the data, compiler options and placement fixed.','保持数据、编译选项与运行位置一致。')),
             (('Measure','测量'),('Repeat with several working-set sizes and inspect relevant events.','用多个工作集规模重复测量，并检查相关事件。')),
             (('Explain','解释'),('Compare time and counters, then check the generated instructions.','对照耗时与计数结果，再检查生成的指令。')),
         ],('One counter rarely identifies a bottleneck. A controlled change makes the diagnosis easier to verify.',
             '单个计数器往往无法定位瓶颈。控制变量后改变一个条件，更容易验证诊断。'))
         +code('perf stat -r 5 -e cycles,instructions,branches,branch-misses -- ./program')
         +p(t('Availability and semantics depend on the PMU and kernel. Check perf list, CPU affinity, frequency policy, and counter multiplexing. Event names and retired instruction counts are not necessarily comparable across an x86 and a RISC-V system. Record workload, compiler, CPU, counters and run-to-run variation alongside the result.',
              '事件可用性和语义取决于 PMU 与内核。核对 perf list、CPU 亲和性、频率策略和计数器复用。x86 与 RISC-V 系统的事件名和提交指令数不一定可直接比较。记录工作负载、编译器、CPU、计数事件和重复测量波动。'))
         +refs(('perf','intel-opt','rv'))),
    ]

    return [
        ('isa',('ISA / ABI',t('Read the contract','读懂指令集契约'),
                t('Compare instructions, registers, privileges and calling conventions through one C example.','用同一段 C 代码对照指令、寄存器、特权与调用约定。')),isa),
        ('cpu',('DATAPATH / CORE',t('Inside the CPU','CPU 内部如何工作'),
                t('Build a datapath and trace pipelining, hazards, speculation and retirement.','从数据通路开始，理解流水线、冒险、推测执行和提交。')),cpu),
        ('cache',('LOCALITY / CACHE',t('Where the bytes wait','数据在缓存里怎样存放'),
                  t('Work through address mapping, locality, replacement, write policies and miss cost.','跟算地址映射，再理解局部性、替换、写策略和未命中代价。')),cache),
        ('memory',('TRANSLATION / DRAM',t('Translate an address','从虚拟地址走到 DRAM'),
                   t('Walk x86-64 paging and RISC-V Sv39, then follow the request to DRAM and NUMA.','对照 x86-64 分页与 RISC-V Sv39，继续追踪 DRAM 和 NUMA 路径。')),memory),
        ('io',('DEVICE / BUS',t('How devices move data','设备如何传输数据'),
               t('Follow MMIO, PCIe, interrupts, DMA and IOMMU through a device queue.','沿一条设备队列理解 MMIO、PCIe、中断、DMA 和 IOMMU。')),io),
        ('parallel',('COHERENCE / ORDERING',t('When cores share memory','多个核心怎样共享内存'),
                     t('Separate cache coherence, false sharing and cross-address memory ordering.','理解缓存一致性、伪共享以及跨地址的内存顺序。')),parallel),
        ('performance',('CPI / MEASUREMENT',t('Measure what costs time','测出时间花在哪里'),
                        t('Use CPI, Amdahl, Roofline and hardware counters to test a performance hypothesis.','用 CPI、Amdahl、Roofline 和硬件计数器检验性能假设。')),performance),
        ('ai',('GPU / MEMORY SYSTEMS',t('How AI changes the system','AI 怎样改变体系结构'),
               t('Follow inference through CPUs, GPUs, HBM, CXL and processing near memory.',
                 '沿推理的数据路径理解 CPU、GPU、HBM、CXL 和近存／存内计算。')),
         ai_chapter(t, p, code, rows, picture, exercise, refs)),
    ]
