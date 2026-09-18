# Contributing

欢迎继续把适合孩子学习的 Codex Skills 沉淀到这个仓库。

## 新增 Skill

1. 在 `skills/` 下创建一个小写英文短横线目录，例如 `mental-math-sheet`。
2. 每个 Skill 目录必须包含 `README.md` 和 `SKILL.md`。
3. 如果有稳定、重复的生成逻辑，优先放到 `scripts/`。
4. 如果有示例配置，放到 `examples/`。
5. 不提交孩子的隐私数据、真实作业照片或账号信息。
6. 新增后更新 `skills/README.md` 和根目录 `README.md` 的 Skill 列表。

## Skill README 建议结构

- 用途
- 适合触发的请求
- 依赖
- 示例命令
- 输出文件
- 扩展方向

## 验证建议

新增或修改 Skill 后，至少做一次真实样例测试。对于 Codex Skill，可以运行官方校验：

```powershell
python "$env:USERPROFILE\.codex\skills\.system\skill-creator\scripts\quick_validate.py" .\skills\<skill-name>
```
