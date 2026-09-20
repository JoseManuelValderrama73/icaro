---
description: Changes optimized for the cluster
---

When i ask you for any task regarding code or a specific file, you must optimice the code to work in any of the nodes of the ADA cluster, and tell me, if needed, what node is better for the specific job or what changes should i make depending of the used node, because not always i can use every node i want.
This is the specifiction of all the nodes there are:
ADA Cluster
Main node (1 node)
Platform: R281-3CO
Processor: 2x Intel (R) Xeon (R) Silver 4210 CPU @ 2.20GHz
RAM memory: 96 GB DDR4 @ 2933 Mhz
Storage size: 60TB (shared storage)

Storage node (1 node)
Platform: S451-3R1
Processor: 2x Intel(R) Xeon(R) Silver 4210R CPU @ 2.40GHz
RAM memory: 192 GB DDR4 @ 3200 Mhz
Storage size: 500 TB (shared storage BeeGFS)

TESLA Ampere compute node (1 node)
Plataform: G262-ZR0
Processor: 2x AMD EPYC 7282 CPU @ 2.80GHz
GPU: 4x NVIDIA Tesla A100 (40GB, Ampere)
RAM memory: 256 GB DDR4 @ 3200 Mhz
Storage size: 1.8 TB

TESLA Volta compute nodes (2 nodes)
Platform: G291-281
Processor: 2x Intel (R) Xeon (R) Silver 4208 CPU @ 2.10GHz
GPU: 2x NVIDIA Tesla V100 (32GB, Volta)
RAM memory: 192 GB DDR4 @ 2933 Mhz
Storage size: 1.8TB

RTX compute nodes (4 nodes)
Plataform: G291-281
Processor: 2x Intel(R) Xeon(R) Silver 4208 CPU @ 2.10GHz
GPU: 6x\* NVIDIA GeForce RTX 2080Ti (11GB, Turing)
RAM memory: 192 GB DDR4 @ 2933 Mhz
Store: 1.8 TB

- Of the four RTX compute nodes, two nodes have 6 GPUs and the other two have 7 GPUs. There is a total of 26 GPUs RTX.
