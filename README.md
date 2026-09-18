# Kids Learning Skills

给家里孩子学习用的 Codex Skills 开源仓库。

这个仓库用来长期沉淀可复用的学习类 Skill，例如语文练字帖、阅读理解、口算练习、错题整理、听写单生成等。每个 Skill 都单独放在 `skills/<skill-name>/` 目录中，方便复制、安装、维护和继续扩展。

## 当前 Skills

| Skill | 用途 |
| --- | --- |
| [`make-handwriting-sheet`](skills/make-handwriting-sheet/README.md) | 生成 A4 小学中文楷书练字帖，支持作文格、横线格、一行示范一行空白 |

## 仓库结构

```text
kids-learning-skills/
  README.md
  LICENSE
  CONTRIBUTING.md
  requirements.txt
  docs/
    new-skill-checklist.md
  skills/
    README.md
    make-handwriting-sheet/
      README.md
      SKILL.md
      agents/
      scripts/
      examples/
```

## 使用方式

把某个 Skill 文件夹复制到本机 Codex Skill 目录：

```powershell
Copy-Item -Recurse .\skills\make-handwriting-sheet "$env:USERPROFILE\.codex\skills\make-handwriting-sheet" -Force
```

之后在 Codex 里可以这样触发：

```text
用 $make-handwriting-sheet 根据这张图片做一页练字帖。
```

## 新增 Skill 的约定

每个 Skill 必须至少包含：

- `README.md`：给人看的说明，包括用途、触发方式、依赖和示例。
- `SKILL.md`：给 Codex 看的 Skill 指令。
- `scripts/`、`examples/`、`assets/` 等按需添加。

新增前参考 [`docs/new-skill-checklist.md`](docs/new-skill-checklist.md)。

## 隐私原则

这个仓库是开源仓库，不提交孩子的姓名、照片、学校、班级、作业原图或其他个人隐私材料。示例文件只放脱敏文本或公开课文片段。

## License

MIT License. See [`LICENSE`](LICENSE).
