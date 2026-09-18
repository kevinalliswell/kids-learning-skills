# New Skill Checklist

新增学习类 Skill 时，用这份清单快速过一遍。

## 命名

- 使用英文小写短横线，例如 `make-handwriting-sheet`。
- 名字尽量动词开头，描述这个 Skill 做什么。

## 必备文件

- `README.md`：给人看的说明。
- `SKILL.md`：给 Codex 看的触发描述和工作流。

## 可选文件夹

- `scripts/`：稳定、可重复执行的脚本。
- `examples/`：示例配置、示例输入，不放隐私数据。
- `assets/`：模板、字体、图标等静态资源。
- `references/`：较长的参考说明，避免塞进 `SKILL.md`。

## README 内容

- 这个 Skill 解决什么学习问题。
- 适合什么年级或场景。
- 用户可以怎么说来触发它。
- 如何运行脚本或验证输出。
- 后续扩展方向。

## 发布前检查

- Skill 目录里没有孩子的个人信息。
- 脚本能在一个简单示例上跑通。
- `skills/README.md` 和根 `README.md` 已更新。
- 如是 Codex Skill，运行 `quick_validate.py`。
