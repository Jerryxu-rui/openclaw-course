# 第12课：自定义Skill开发

## 课程目标
- 理解Skill结构
- 掌握Skill开发流程
- 学会集成第三方API
- 发布Skill到社区

---

## 第一部分：Skill结构（20分钟）

### 1.1 Skill目录结构

```
my-skill/
├── SKILL.md          # Skill说明（Agent会读取）
├── package.json      # 依赖声明
├── scripts/          # 可执行脚本
│   ├── main.sh
│   └── helper.py
└── assets/           # 资源文件
    └── template.txt
```

### 1.2 SKILL.md规范

```markdown
# My Skill

### 1.3 Skills工作原理

Skills是OpenClaw的能力扩展单元。理解它的加载机制，才能真正用好这个系统。

#### 三层优先级
OpenClaw的Skill有三个来源，按优先级从高到低排列：

| 优先级 | 位置 | 说明 |
|--------|------|------|
| 最高 | `<workspace>/skills/` | 项目级Skills，只对当前工作区生效。适合针对特定项目定制的能力。 |
| 中 | `~/.openclaw/skills/` | 用户级Skills，全局生效。通过ClawHub安装或手动放置的Skills都在这里。 |
| 最低 | bundled skills | 内置的55个Skills，随OpenClaw版本发布。不需要安装，开箱即用。 |

**核心建议**：如果同名Skill存在于多个层级，高优先级会覆盖低优先级。这意味着你可以在workspace级别「重写」一个内置Skill的行为，而不影响其他项目。

#### Skill加载过程
当OpenClaw启动或收到消息时，Skills的加载遵循以下流程：

1. **读取Skill元数据**：扫描三层目录，读取每个Skill的`SKILL.md`文件，解析名称、描述、触发条件、所需环境变量等元信息。
2. **应用环境变量**：如果Skill声明了需要的API Key或环境变量（如`GITHUB_TOKEN`），系统会从`openclaw.json`的`env`字段中注入。缺少必要变量的Skill会被静默跳过。
3. **构建System Prompt**：将所有可用Skills的描述注入到system prompt中，告知模型当前可以调用哪些能力。这是模型「知道自己能做什么」的关键步骤。
4. **运行后恢复**：Skill执行完毕后，恢复原始环境变量和上下文状态，避免Skill之间互相干扰。

#### ClawHub注册表
ClawHub（clawhub.com）是OpenClaw的官方Skill注册表，类似npm之于Node.js。它提供：
- 公共Skills的发布和版本管理
- 基于向量搜索的Skill发现
- 下载量统计和社区评分
- VirusTotal合作的安全扫描（但覆盖率有限）

## 功能
这个Skill可以做什么

## 使用方法
如何使用这个Skill

## 示例
具体的使用示例

## 依赖
需要安装的依赖
```

---

## 第二部分：开发流程（40分钟）

### 2.1 创建Skill

```bash
# 创建目录
mkdir ~/.openclaw/skills/my-skill
cd ~/.openclaw/skills/my-skill

# 创建文件
touch SKILL.md package.json
mkdir scripts assets
```

### 2.2 编写脚本

```bash
# scripts/main.sh
#!/bin/bash
echo "Hello from my skill!"
```

### 2.3 测试Skill

```bash
# 重启Gateway加载Skill
openclaw gateway restart

# 测试
openclaw chat "使用my-skill"
```

---

## 第三部分：集成第三方API（40分钟）

### 3.1 API集成示例

```python
# scripts/api_call.py
import requests
import sys

def call_api(query):
    response = requests.get(
        "https://api.example.com/search",
        params={"q": query}
    )
    return response.json()

if __name__ == "__main__":
    query = sys.argv[1]
    result = call_api(query)
    print(result)
```

### 3.2 配置API密钥

```json
{
  "skills": {
    "entries": {
      "my-skill": {
        "apiKey": "${MY_SKILL_API_KEY}"
      }
    }
  }
}
```

---

## 第四部分：发布Skill（30分钟）

### 4.1 打包Skill

```bash
# 创建README
echo "# My Skill" > README.md

# 初始化git
git init
git add .
git commit -m "Initial commit"
```

### 4.2 发布到GitHub

```bash
# 创建仓库
gh repo create my-skill --public

# 推送代码
git push origin main
```

### 4.3 提交到ClaHub

访问 https://clawhub.com 提交你的Skill

---

## 作业与练习

### 作业1：开发简单Skill（必做）
开发一个Hello World Skill

### 作业2：API集成（必做）
集成一个第三方API

### 作业3：发布Skill（选做）
发布Skill到GitHub和ClaHub

---

## 课程总结

### 本节课你学到了：
✅ Skill结构和规范  
✅ Skill开发流程  
✅ API集成方法  
✅ Skill发布流程  

### 关键要点：
1. **SKILL.md是核心**
2. **脚本要可执行**
3. **API密钥要安全**
4. **测试要充分**

---

**下节课见！** 🚀
