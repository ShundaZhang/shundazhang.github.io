"use strict";

const isChinese = document.documentElement.lang === "zh-CN";
const localize = (english, chinese) => isChinese ? chinese : english;

function readHex(input) {
  const value = input.value.trim();
  if (!/^(?:0x)?[\da-f]{1,16}$/i.test(value)) return null;
  return BigInt(value.startsWith("0x") || value.startsWith("0X") ? value : "0x" + value);
}

function showCache([addressInput, waysInput]) {
  const address = readHex(addressInput);
  const ways = waysInput.valueAsNumber;
  if (address === null || ![1, 2, 4, 8].includes(ways)) {
    return localize("Enter up to 16 hex digits and choose 1, 2, 4 or 8 ways.",
                    "请输入最多 16 位十六进制数字，并选择 1、2、4 或 8 路。");
  }

  const sets = 32768n / (64n * BigInt(ways));
  const line = address / 64n;
  const tag = (line / sets).toString(16);
  const set = line % sets;
  const offset = address % 64n;
  return localize(`Sets ${sets} · Set ${set} · Offset ${offset} B · Tag 0x${tag}`,
                  `组数 ${sets} · 组索引 ${set} · 偏移 ${offset} B · Tag 0x${tag}`);
}

function showSv39([addressInput]) {
  const address = readHex(addressInput);
  if (address === null) {
    return localize("Enter up to 16 hex digits.", "请输入最多 16 位十六进制数字。");
  }

  const sign = (address >> 38n) & 1n;
  const upper = address >> 39n;
  if (upper !== (sign ? (1n << 25n) - 1n : 0n)) {
    return localize("Noncanonical for Sv39. Bits 63–39 must copy bit 38.",
                    "这是 Sv39 非规范地址。位 63–39 必须全部等于位 38。");
  }

  const vpn = [30n, 21n, 12n].map(shift => "0x" + ((address >> shift) & 511n).toString(16));
  const offset = (address & 4095n).toString(16);
  return localize(`VPN[2:0] = (${vpn.join(", ")}) · Offset 0x${offset}`,
                  `VPN[2:0] = (${vpn.join(", ")}) · 页内偏移 0x${offset}`);
}

function showCpi(inputs) {
  if (!inputs.every(input => input.value !== "" && input.validity.valid)) {
    return localize("Enter whole percentages from 0 to 100 and a penalty from 0 to 1000.",
                    "请输入 0 到 100 的整数百分比，以及 0 到 1000 的周期代价。");
  }
  const [frequency, missRate, penalty] = inputs.map(input => input.valueAsNumber);
  const overhead = frequency * missRate * penalty / 10000;
  return localize(`Branch overhead ${overhead.toFixed(4)} cycles/instruction · Estimated CPI ${(1 + overhead).toFixed(4)}`,
                  `分支开销 ${overhead.toFixed(4)} 周期/指令 · 估计 CPI ${(1 + overhead).toFixed(4)}`);
}

for (const [outputId, ids, calculate] of [
  ["cache-result", ["cache-address", "cache-ways"], showCache],
  ["sv39-result", ["sv39-address"], showSv39],
  ["cpi-result", ["cpi-branch", "cpi-miss", "cpi-penalty"], showCpi],
]) {
  const output = document.getElementById(outputId);
  const inputs = ids.map(id => document.getElementById(id));
  const update = () => { output.textContent = calculate(inputs); };
  inputs.forEach(input => input.addEventListener("input", update));
  update();
}
