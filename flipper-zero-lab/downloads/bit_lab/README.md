# Bit Lab

A small original Flipper Zero FAP game. Match the displayed hexadecimal byte with eight editable bits.

- Left / right move the cursor
- Up / down toggle the selected bit
- OK checks the byte; a correct match advances to a deterministic new target
- Back exits and releases resources

Build with the official uFBT SDK. From this folder run `ufbt`. Use `ufbt launch` only with your own Flipper connected. The app does not access radios, NFC, storage or networks.

中文：方向键左右移动、上下翻转位，OK 核对十六进制目标，Back 退出。运行 `ufbt` 编译，实际屏幕与按键行为需连接设备测试。
