"""AI workloads, heterogeneous processors and memory-system trade-offs."""

AI_SOURCES = {
    'cuda-simt': ('https://docs.nvidia.com/cuda/cuda-programming-guide/02-basics/writing-cuda-kernels.html', 'NVIDIA CUDA · SIMT and memory access', 'NVIDIA CUDA · SIMT 与内存访问'),
    'amx': ('https://www.intel.com/content/www/us/en/developer/articles/technical/tuning-guide-for-ai-on-the-4th-generation.html', 'Intel · AMX and CPU tuning', 'Intel · AMX 与 CPU 调优'),
    'rvv': ('https://docs.riscv.org/reference/isa/unpriv/v-st-ext', 'RISC-V V vector extension', 'RISC-V V 向量扩展'),
    'flash': ('https://arxiv.org/abs/2205.14135', 'FlashAttention paper', 'FlashAttention 论文'),
    'paged': ('https://arxiv.org/abs/2309.06180', 'PagedAttention paper', 'PagedAttention 论文'),
    'mi300a': ('https://instinct.docs.amd.com/projects/system-acceptance/en/latest/gpus/mi300a.html', 'AMD MI300A architecture', 'AMD MI300A 架构'),
    'mi355x': ('https://www.amd.com/en/products/accelerators/instinct/mi350/mi355x.html', 'AMD MI355X specifications', 'AMD MI355X 规格'),
    'rubin-spec': ('https://www.nvidia.com/en-gb/data-center/vera-rubin-nvl72/', 'NVIDIA Vera Rubin NVL72 specifications', 'NVIDIA Vera Rubin NVL72 规格'),
    'vera': ('https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Launches-Vera-CPU-Purpose-Built-for-Agentic-AI/default.aspx', 'NVIDIA Vera host CPU announcement', 'NVIDIA Vera 主机 CPU 公告'),
    'rubin': ('https://nvidianews.nvidia.com/news/vera-rubin-full-production-agentic-ai-factory', 'NVIDIA Vera Rubin production announcement', 'NVIDIA Vera Rubin 生产公告'),
    'cxl': ('https://computeexpresslink.org/cxl-specification/', 'CXL Consortium specifications', 'CXL 联盟规范'),
    'linux-cxl': ('https://docs.kernel.org/6.16/driver-api/cxl/devices/device-types.html', 'Linux · CXL devices and protocols', 'Linux · CXL 设备与协议'),
    'pim': ('https://news.samsung.com/us/samsung-develops-industrys-first-high-bandwidth-memory-with-ai-processing-power/', 'Samsung · HBM-PIM demonstration', '三星 · HBM-PIM 技术演示'),
}


def ai_chapter(t, p, code, rows, picture, exercise, refs):
    return [
        ('workload',t('Follow one inference request','跟踪一次推理请求'),
         picture(('Host and accelerator roles in an example server','推理服务中主机和加速器的分工'),[
             (('CPU and runtime','CPU 与运行时'),('Tokenize, queue requests, schedule batches, and submit work.','做分词、请求排队、批次调度，并提交任务。')),
             (('Prefill','预填充'),('Process the prompt in parallel and populate key/value state for attention.','并行处理输入 token，建立 attention 的 K/V 状态。')),
             (('Decode','逐 token 解码'),('Generate tokens in order. Reuse earlier K/V state and append the new token’s state.','依次生成 token，复用已有 K/V 状态，并追加新 token 的状态。')),
             (('Return','返回结果'),('The runtime streams output and frees or reuses resources when requests finish.','运行时流式返回输出，请求结束后释放或复用资源。')),
         ],('Prefill and decode place different demands on arithmetic, memory and scheduling. Exact bottlenecks vary with model, batch and context.',
             '预填充与解码对算力、内存和调度的要求不同。实际瓶颈随模型、批次与上下文变化。'))
         +p(t('Prefill often gives matrix units more parallel work per request. Small-batch decode can spend much of its time streaming model weights and accessing K/V state for each generated step. More batching can reuse weight reads across requests but consumes more K/V capacity and changes latency. Measure time to first token, time between tokens and aggregate tokens per second separately.',
              '预填充通常能给矩阵单元提供更多并行工作。小批次解码的每一步可能花大量时间读取模型权重和 K/V 状态。增加批次可在请求间复用权重读，却会占用更多 K/V 容量并改变延迟。首 token 延迟、token 间隔与总吞吐应分别测量。'))
         +refs(('flash','paged'))),
        ('cores',t('Why the CPU and GPU are designed differently','CPU 和 GPU 的设计为何不同'),
         rows([('Aspect','方面'),('CPU','CPU'),('GPU','GPU')],[
             [('Execution','执行'),('Large cores handle diverse control flow and try to make a few threads finish quickly.','大核心处理多样控制流，重点缩短少量线程的完成时间。'),('Many groups of lanes keep arithmetic units busy. NVIDIA CUDA groups threads into warps.','大量 lane 分组维持运算单元利用率，NVIDIA CUDA 把线程组织为 warp。')],
             [('Latency handling','隐藏延迟'),('Out-of-order scheduling, branch prediction and caches exploit work within a thread.','用乱序调度、分支预测和缓存挖掘线程内部的并行。'),('A scheduler can issue another ready warp while one waits. Diverging branches can lower lane utilization.','一组 warp 等待时可发射其他就绪 warp，分支分歧会降低 lane 利用率。')],
             [('Data reuse','数据复用'),('Hardware caches and vector or matrix instructions help reuse nearby data.','通过硬件缓存和向量、矩阵指令复用附近数据。'),('A kernel arranges nearby accesses, tiles data and can reuse it in registers or on-chip shared memory.','kernel 组织相邻访存并做分块，可在寄存器或片上共享内存中复用。')],
         ])
         +picture(('Why tiling helps matrix work','为什么矩阵运算要分块'),[
             (('Bring in a tile','载入分块'),('Load a block of operands from GPU memory.','从 GPU 内存载入一块操作数。')),
             (('Reuse on chip','片上复用'),('Hold it in shared memory or registers across many multiply-adds.','留在共享内存或寄存器，在多次乘加中复用。')),
             (('Accumulate','累加'),('Use suitable vector or matrix units and keep partial results local.','使用合适的向量或矩阵单元，尽量在片上保留部分结果。')),
             (('Write back','写回'),('Store the output tile. Fewer external bytes per operation improve arithmetic intensity.','写出结果块。每次运算需要的外部字节变少，算术强度提高。')),
         ],('FlashAttention applies the same I/O-aware idea to attention and avoids materializing the full score matrix in HBM.',
             'FlashAttention 将类似的 I/O 感知思想用于 attention，避免把完整分数矩阵写入 HBM。'))
         +p(t('Some x86 CPUs add tile matrix operations such as Intel AMX. RISC-V’s optional V extension exposes vector-length-aware instructions and can support CPU-side kernels. An SoC can also pair a RISC-V CPU with an accelerator through a device interface. This choice is distinct from implementing the GPU execution model in the CPU.',
              '部分 x86 CPU 增加了 Intel AMX 一类分块矩阵操作。RISC-V 可选的 V 扩展提供感知向量长度的指令，可用于 CPU 侧计算。SoC 也可以通过设备接口把 RISC-V CPU 与专用加速器搭配。加速器的执行模型由其自身设计决定。'))
         +refs(('cuda-simt','amx','rvv','flash'))),
        ('capacity',t('Size weights and KV state before choosing memory','先算权重和 KV 状态，再选内存'),
         picture(('Where the bytes may live','模型数据可能放在哪'),[
             (('On chip','片上'),('Registers, SRAM and cache hold active tiles and intermediates.','寄存器、SRAM 和缓存保留正在使用的分块及中间结果。')),
             (('GPU HBM','GPU HBM'),('High-bandwidth capacity for hot weights and active KV blocks.','用高带宽容量存放热点权重与活跃 KV 块。')),
             (('Host memory','主机内存'),('CPU-attached DRAM can stage data or hold offloaded state.','CPU 直连 DRAM 可暂存数据或保存卸载状态。')),
             (('Expansion and storage','扩容与存储'),('CXL memory or storage can add capacity when software manages placement and transport.','CXL 内存或存储可扩展容量，软件负责放置与传输。')),
         ],('Illustrative tiers. Links, placement policies and performance vary by system.',
             '这是示意层级，具体互连、放置策略与性能随系统而异。'))
         +code('KV bytes = 2 × layers × KV heads × head dimension\n             × bytes per element × cached tokens per sequence × sequences\n\n32 layers × 8 KV heads × 128 dimensions × 2 B × 2 (K and V)\n= 128 KiB per token and sequence\n32,768 tokens → 4 GiB per sequence → 32 GiB for 8 sequences')
         +p(t('This is the payload for conventional attention with equal-length requests and fixed-width K and V. For grouped-query attention, use the number of KV heads, which may be smaller than query heads. Weight storage is a separate budget. For example, 70 billion parameters at 2 bytes each take about 140 GB (130.4 GiB), before runtime buffers and allocator overhead. Quantization, sharing, sharding and sequence lengths can change these totals.',
              '这是传统 attention 在请求等长且 K、V 精度固定时的有效载荷。使用分组查询注意力时，公式取 KV 头数，它可以少于查询头数。权重另算，例如 700 亿参数、每参数 2 字节约占 140 GB（130.4 GiB），还要预留运行时缓冲与分配开销。量化、共享、分片和序列长度都会改变实际占用。'),
            t('PagedAttention manages KV state in blocks, so requests can grow without preallocating the maximum contiguous length and compatible prefixes can share blocks. These software blocks are an analogy to virtual memory. Their sizes and placement are managed by the serving runtime.',
              'PagedAttention 按块管理 KV 状态，请求可逐步增长，无需提前预分配最大长度的连续空间，兼容的前缀也可共享块。这与虚拟内存分页有相似之处，块的尺寸和放置由推理运行时管理。'))
         +exercise('labs',('Open the KV capacity lab →','打开 KV 容量实验 →'),
                   ('Double context length and compare it with doubling the number of active sequences. Both increase this payload linearly.',
                    '把上下文长度翻倍，再把并发序列数翻倍。两者分别会使这部分有效载荷线性增长。'),'#kv-capacity')
         +refs(('paged','cxl'))),
        ('platforms',t('Three ways platforms increase usable memory','平台如何扩大可用内存'),
         rows([('Design','方案'),('Example','实例'),('What it changes','改变什么')],[
             [('More GPU-local bandwidth and capacity','增加 GPU 本地带宽与容量'),('AMD MI355X specifies 288 GB HBM3E per accelerator. NVIDIA lists 288 GB HBM4 per Rubin GPU and announced platform production in 2026.','AMD MI355X 单加速器规格为 288 GB HBM3E。NVIDIA 公布 Rubin 单 GPU 配置为 288 GB HBM4，并在 2026 年发布了平台生产公告。'),('More hot state can stay near compute. Multi-GPU model sharding still depends on interconnect traffic.','更多热点状态可留在计算附近，多 GPU 模型分片仍受互连流量约束。')],
             [('Coherent CPU–GPU memory','CPU–GPU 一致性内存'),('AMD MI300A combines x86 Zen 4 cores and a CDNA 3 GPU with a coherent 128 GB HBM3 pool.','AMD MI300A 把 x86 Zen 4 核心与 CDNA 3 GPU 放入同一封装，共享一致的 128 GB HBM3。'),('Suitable buffers can be accessed from both sides with fewer explicit copies. Locality, cache coherence and synchronization still affect the cost.','合适的缓冲区可由双方访问，减少显式拷贝。局部性、一致性与同步仍影响成本。')],
             [('Host expansion or pooling','主机扩容或池化'),('CXL Type 3 memory devices expand host-addressable memory. Later CXL fabrics support forms of pooling with suitable switches and management.','CXL Type 3 内存设备扩展主机可寻址内存，后续 CXL 互连可配合交换机与管理软件实现一定形式的池化。'),('A larger or shareable capacity tier helps placement. Access latency and bandwidth depend on the link and topology.','更大或可共享的容量层便于做数据放置，但延迟与带宽取决于链路和拓扑。')],
         ])
         +p(t('A unified virtual address space, shared physical backing, hardware cache coherence and runtime-managed page migration are distinct properties. A platform can provide some of them without the rest. CXL 4.0 is a published specification. Actual feature support depends on the host, device, switch, firmware and OS.',
              '统一虚拟地址空间、共享物理内存、硬件缓存一致性和运行时页迁移是不同属性，平台可以只提供其中一部分。CXL 4.0 是已发布规范，实际支持范围由主机、设备、交换机、固件和 OS 共同决定。'))
         +p(t('The 2026 Vera host CPU is a concrete example of how this changes CPU design. NVIDIA pairs CPU-side LPDDR5X with GPU-side HBM4 and a coherent CPU–GPU link. The host runs runtimes, data movement and orchestration while the GPU handles tensor-heavy work. Those are architectural choices about where to place bandwidth, latency and coherence.',
              '2026 年的 Vera 主机 CPU 展示了这类负载怎样影响 CPU 设计。NVIDIA 将 CPU 侧 LPDDR5X、GPU 侧 HBM4 和 CPU–GPU 一致性互连放在同一平台。主机承担运行时、数据搬运与编排，GPU 执行张量密集计算。系统需要决定把带宽、低延迟访问和一致性放在哪一侧。'))
         +refs(('mi300a','mi355x','rubin','rubin-spec','vera','cxl','linux-cxl'))),
        ('pim',t('Move computation closer to the bytes','把计算移到更靠近数据的位置'),
         picture(('A bandwidth-bound vector operation in two layouts','访存受限向量运算的两种布局'),[
             (('Conventional path','常规路径'),('Read A and B over the memory interface, compute at the processor, then write C back.','经内存接口读 A、B，在处理器计算，再写回 C。')),
             (('Near-memory / PIM path','近存／存内路径'),('Dispatch a supported operation near the memory banks. Read and combine data locally, then return only what the host needs.','将受支持的运算派发到内存 bank 附近，就地读取和运算，只返回主机需要的结果。')),
         ],('Compare the bytes crossing the external link. If intermediate data must travel anyway, the benefit can shrink.',
             '比较穿过外部链路的字节数。如果中间数据仍需传出，收益就可能缩小。'))
         +p(t('Near-memory computing places logic close to memory, for example in a logic die or controller. Digital PIM can place arithmetic in or near DRAM banks. Some compute-in-memory research instead performs operations within a memory array, including analog approaches. The programming, precision, data layout and validation constraints differ across these designs.',
              '近存计算把逻辑放在内存附近，例如逻辑裸片或控制器。数字 PIM 可在 DRAM bank 内部或附近放置运算单元。另一些存内计算研究则在存储阵列内运算，包括模拟方案。不同设计对编程、精度、数据布局和验证的要求各不相同。'),
            t('Samsung HBM-PIM illustrates putting arithmetic close to DRAM data. For each candidate operation, check what runs there, how operands are laid out, what must cross banks, and how CPU or GPU access is synchronized. Dense math with high on-chip reuse, bandwidth-bound vector work, and capacity-bound inference can favor different designs.',
              '三星 HBM-PIM 演示了把运算靠近 DRAM 数据的做法。评估具体算子时，应核对支持的操作、操作数布局、跨 bank 的流量及与 CPU、GPU 的同步方式。高片上复用的密集运算、带宽受限的向量运算与容量受限的推理，可能适合不同设计。'))
         +refs(('pim','roofline'))),
    ]
